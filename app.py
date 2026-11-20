from flask import Flask, render_template, abort

app = Flask(__name__)

# Product catalog. Replace "price" placeholders with real prices (numbers, in dollars).
PRODUCTS = [
    {
        "slug": "dreams-dont-die-tee",
        "name": "Dreams Don't Die Tee",
        "color": "Vintage Cream",
        "category": "tees",
        "price": None,
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
        "price": None,
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
        "price": None,
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
        "price": None,
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
        "price": None,
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
        "price": None,
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
        "price": None,
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
        "price": None,
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
    return f"${value:,.2f}" if value is not None else "$[XX]"


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


if __name__ == "__main__":
    app.run(debug=True)
