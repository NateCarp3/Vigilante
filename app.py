import os

import stripe
from flask import Flask, render_template, abort, request, jsonify, url_for
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)  # Render sits in front of the app

# --- Stripe checkout settings (set these in Render → Environment) ---
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")        # sk_test_... or sk_live_...
FREE_SHIPPING_MIN = 60                                        # free shipping on orders of $60+
STANDARD_SHIPPING = os.environ.get("STANDARD_SHIPPING")       # shipping charge in dollars for orders under $60, e.g. "8"

# Price list (dollars). Use these when adding new products.
PRICES = {
    "tee": 55,          # every shirt is $55
    "sweatsuit": 125,   # full set; top $65, bottom $50 if bought separately
    "sweatsuit_top": 65,
    "sweatsuit_bottom": 50,
    "beanie": 40,
    "hat": 40,
    "zip_hoodie": 80,
    "pullover": 70,
}

SWEATSUIT_OPTIONS = [
    {"label": "Full Set", "price": PRICES["sweatsuit"]},
    {"label": "Hoodie Only", "price": PRICES["sweatsuit_top"]},
    {"label": "Pants Only", "price": PRICES["sweatsuit_bottom"]},
]

# Product catalog
PRODUCTS = [
    {
        "slug": "dreams-dont-die-tee",
        "name": "Dreams Don't Die Tee",
        "color": "Vintage Cream",
        "category": "tees",
        "price": PRICES["tee"],
        "image": "tee-dreams-dont-die.jpg",
        "alt": "Dreams Don't Die graphic tee in vintage cream",
        "badge": "Best Seller",
        "sizes": ["S", "M", "L", "XL", "2XL", "3XL"],
        "description": "Hand-drawn Vigilante graphic — skyline, stars and stripes, and the V signal — "
                       "across a washed, distressed cream tee. Raw edges and worn-in holes, finished "
                       "with Dreams Don't Die at the hem. [ADD FABRIC + WEIGHT]",
    },
    {
        "slug": "vigi-university-tee",
        "name": "Vigi University Tee",
        "color": "Washed White",
        "category": "tees",
        "price": PRICES["tee"],
        "image": "tee-vigi-university.jpg",
        "alt": "Vigi University distressed tee in washed white",
        "badge": "Best Seller",
        "sizes": ["S", "M", "L", "XL", "2XL", "3XL"],
        "description": "Washed, distressed tee with the Vigi University graduate print. [ADD FABRIC + WEIGHT]",
    },
    {
        "slug": "vigilante-set-blackout",
        "name": "Vigilante Set",
        "color": "Blackout",
        "category": "sets",
        "price": PRICES["sweatsuit"],
        "options": SWEATSUIT_OPTIONS,
        "image": "set-blackout.jpg",
        "alt": "Black Vigilante hoodie and sweatpant set",
        "badge": "Best Seller",
        "sizes": ["S", "M", "L", "XL", "2XL", "3XL"],
        "description": "Heavyweight hoodie and sweatpant set with the Vigilante V logo. [ADD FABRIC + FIT]",
    },
    {
        "slug": "vigilante-set-heather-grey",
        "name": "Vigilante Set",
        "color": "Heather Grey",
        "category": "sets",
        "price": PRICES["sweatsuit"],
        "options": SWEATSUIT_OPTIONS,
        "image": "set-heather-grey.jpg",
        "alt": "Heather grey Vigilante hoodie and sweatpant set",
        "badge": "New",
        "sizes": ["S", "M", "L", "XL", "2XL", "3XL"],
        "description": "Heavyweight hoodie and sweatpant set with the Vigilante V logo. [ADD FABRIC + FIT]",
    },
    {
        "slug": "distressed-beanie-black",
        "name": "Distressed Beanie",
        "color": "Black",
        "category": "headwear",
        "price": PRICES["beanie"],
        "image": "beanie-black.jpg",
        "alt": "Black distressed knit beanie with Vigilante patch",
        "badge": "Best Seller",
        "sizes": ["One Size"],
        "description": "Oversized rib-knit beanie with distressed edges and the Vigilante star patch.",
    },
    {
        "slug": "distressed-beanie-red",
        "name": "Distressed Beanie",
        "color": "Red",
        "category": "headwear",
        "price": PRICES["beanie"],
        "image": "beanie-red.jpg",
        "alt": "Red distressed knit beanie with Vigilante patch",
        "badge": "New",
        "sizes": ["One Size"],
        "description": "Oversized rib-knit beanie with distressed edges and the Vigilante star patch.",
    },
    {
        "slug": "distressed-beanie-pink",
        "name": "Distressed Beanie",
        "color": "Pink",
        "category": "headwear",
        "price": PRICES["beanie"],
        "image": "beanie-pink.jpg",
        "alt": "Pink distressed knit beanie with Vigilante patch",
        "badge": "New",
        "sizes": ["One Size"],
        "description": "Oversized rib-knit beanie with distressed edges and the Vigilante star patch.",
    },
    {
        "slug": "distressed-beanie-charcoal",
        "name": "Distressed Beanie",
        "color": "Charcoal",
        "category": "headwear",
        "price": PRICES["beanie"],
        "image": "beanie-grey.jpg",
        "alt": "Charcoal distressed knit beanie with Vigilante patch",
        "badge": "New",
        "sizes": ["One Size"],
        "description": "Oversized rib-knit beanie with distressed edges and the Vigilante star patch.",
    },
]

BY_SLUG = {p["slug"]: p for p in PRODUCTS}


@app.template_filter("money")
def money(value):
    if value is None:
        return "$[XX]"
    return f"${value:,.0f}" if float(value).is_integer() else f"${value:,.2f}"


@app.route("/")
def index():
    best = [BY_SLUG[s] for s in ("dreams-dont-die-tee", "vigilante-set-blackout",
                                 "distressed-beanie-black", "vigi-university-tee")]
    new = [p for p in PRODUCTS if p["badge"] == "New"]
    return render_template("index.html", best=best, new=new, total=len(PRODUCTS))


@app.route("/shop")
@app.route("/shop/<category>")
def shop(category=None):
    items = [p for p in PRODUCTS if category is None or p["category"] == category]
    if category and not items:
        abort(404)
    title = category.title() if category else "All Products"
    return render_template("shop.html", products=items, title=title)


@app.route("/product/<slug>")
def product(slug):
    p = BY_SLUG.get(slug)
    if not p:
        abort(404)
    related = [x for x in PRODUCTS if x["slug"] != slug][:4]
    return render_template("product.html", p=p, related=related)


def unit_price(p, option):
    """Price in dollars for a product (and sweatsuit piece), taken from the catalog — never from the browser."""
    if p.get("options"):
        return next((o["price"] for o in p["options"] if o["label"] == option), None)
    return p["price"]


@app.post("/create-checkout-session")
def create_checkout_session():
    if not stripe.api_key:
        return jsonify(error="Checkout isn't switched on yet."), 503
    items = (request.get_json(silent=True) or {}).get("items") or []
    line_items, subtotal = [], 0
    for it in items[:50]:
        p = BY_SLUG.get(str(it.get("id")))
        size = it.get("size")
        option = it.get("option") or None
        price = unit_price(p, option) if p else None
        if not p or size not in p["sizes"] or price is None:
            return jsonify(error="Something in your cart is no longer available. Please remove it and try again."), 400
        try:
            qty = max(1, min(10, int(it.get("qty", 1))))
        except (TypeError, ValueError):
            qty = 1
        name = f"{p['name']} \u201c{p['color']}\u201d" + (f" \u2014 {option}" if option else "")
        line_items.append({
            "price_data": {
                "currency": "usd",
                "unit_amount": int(round(price * 100)),
                "product_data": {
                    "name": name,
                    "description": f"Size: {size}",
                    "images": [url_for("static", filename="images/" + p["image"], _external=True)],
                    "metadata": {"slug": p["slug"], "size": size, "option": option or ""},
                },
            },
            "quantity": qty,
        })
        subtotal += price * qty
    if not line_items:
        return jsonify(error="Your cart is empty."), 400

    if subtotal >= FREE_SHIPPING_MIN:
        shipping = {"display_name": "Free shipping", "amount": 0}
    elif STANDARD_SHIPPING:
        shipping = {"display_name": "Standard shipping", "amount": int(round(float(STANDARD_SHIPPING) * 100))}
    else:
        return jsonify(error="Shipping isn't set up yet."), 503

    try:
        session = stripe.checkout.Session.create(
            mode="payment",
            line_items=line_items,
            shipping_address_collection={"allowed_countries": ["US"]},
            shipping_options=[{"shipping_rate_data": {
                "type": "fixed_amount",
                "display_name": shipping["display_name"],
                "fixed_amount": {"amount": shipping["amount"], "currency": "usd"},
            }}],
            phone_number_collection={"enabled": True},
            success_url=url_for("order_success", _external=True) + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=url_for("index", _external=True),
        )
    except stripe.StripeError as e:
        app.logger.error("Stripe error: %s", e)
        return jsonify(error="Checkout is having trouble right now. Please try again."), 502
    return jsonify(url=session.url)


@app.route("/order/success")
def order_success():
    session = None
    sid = request.args.get("session_id", "")
    if stripe.api_key and sid.startswith("cs_"):
        try:
            session = stripe.checkout.Session.retrieve(sid)
        except stripe.StripeError:
            session = None
    return render_template("success.html", session=session)


if __name__ == "__main__":
    app.run(debug=True)
