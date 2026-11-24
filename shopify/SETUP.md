# Vigilante on Shopify — setup steps

Files in this folder:
- `vigilante-theme.zip` — the Vigilante mascot design as a Shopify theme
- `vigilante-products.csv` — all 8 products with sizes, prices and photos

## 1. Create the store
Sign up at shopify.com and pick the **Basic** plan when you're ready to launch.

## 2. Import the products
Admin → **Products** → **Import** → choose `vigilante-products.csv` → **Import products**.

This adds:
- Dreams Don't Die Tee and Vigi University Tee — $55, sizes S–3XL
- Vigilante Sweatsuit (Blackout, Heather Grey) — Full Set $125 / Hoodie Only $65 / Pants Only $50, sizes S–3XL
- Distressed Beanie (Black, Red, Pink, Charcoal) — $40, one size

Photos are pulled from the current Render site, so keep that site running until the import finishes.
Stock is **not tracked** yet (items never sell out). To track stock: open a product → each variant → check "Track quantity" and enter how many you have.
Shipping weights are estimates (tee 230 g, beanie 120 g, full set 900 g). Update them if your real weights differ — they affect shipping rates.

## 3. Create collections (used by the menu and homepage)
Admin → **Products** → **Collections** → **Create collection** → choose **Automated** → condition "Product tag is equal to …":

| Collection title | Tag |
|---|---|
| Tees | tees |
| Sets | sets |
| Headwear | headwear |
| New | new |
| Best Sellers | best-seller |

The page addresses must be `tees`, `sets`, `headwear`, `new` and `best-sellers` (Shopify creates these from the titles automatically).

## 4. Upload the theme
Admin → **Online Store** → **Themes** → **Add theme** → **Upload zip file** → choose `vigilante-theme.zip` → **Publish**.
Use **Customize** to change the homepage text, buttons, colors, or the free-shipping amount shown in the cart.

## 5. Menu
Admin → **Online Store** → **Navigation** → **Main menu**: add Shop All (/collections/all), Tees, Sets, Headwear.
If the menu is empty, the theme shows those four links anyway.

## 6. Free shipping over $60
Admin → **Settings** → **Shipping and delivery** → your shipping profile → **Add rate** → name "Free shipping", price $0 → **Add conditions** → based on order price, minimum $60.
Keep a normal paid rate for orders under $60.

## 7. Payments and launch
Admin → **Settings** → **Payments** → activate **Shopify Payments** (cards, Apple Pay, Shop Pay).
When ready, remove the store password: **Online Store** → **Preferences** → uncheck password protection.

## 8. Your domain
If you own a domain, connect it in **Settings** → **Domains**. After launch you can shut down the Render site.
