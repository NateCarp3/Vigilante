# Vigilante storefront (Flask)

## Run it

```
cd C:\Users\cyntc\flask\Vigilante
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

## Pages

- `/` — homepage (hero, best sellers, Vigi University, just landed, categories, newsletter)
- `/shop`, `/shop/tees`, `/shop/sets`, `/shop/headwear` — product grids
- `/product/<slug>` — product page (size, quantity, add to cart)

## Where things live

- `app.py` — the product catalog (`PRODUCTS`). Set each `price` to a number (e.g. `45`) to replace the `$[XX]` placeholders.
- `templates/` — page HTML (Jinja). `base.html` holds the header, footer and cart drawer.
- `static/css/style.css` — all styling. Change `--accent` to recolor the site.
- `static/js/cart.js` — cart (saved in the browser for now; checkout isn't connected yet).
- `static/images/` — product photos.

## Still to fill in

Anything in `[BRACKETS]`: prices, free-shipping threshold, offer strip, fabric/fit details,
shipping & return policy, payment methods, BNPL provider, and extra product photos.
