// Simple client-side cart stored in localStorage.
// Swap this for a real checkout (e.g. Stripe or Shopify) when you're ready to sell.
(function () {
  const KEY = 'vigilante_cart';
  const FREE_SHIPPING = 60; // free shipping on orders of this amount or more
  const load = () => { try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch (e) { return []; } };
  const save = (c) => { try { localStorage.setItem(KEY, JSON.stringify(c)); } catch (e) {} };
  let cart = load();

  const drawer = document.querySelector('[data-cart]');
  const linesEl = document.querySelector('[data-cart-lines]');
  const subtotalEl = document.querySelector('[data-cart-subtotal]');

  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const money = (n) => '$' + (Number.isInteger(n) ? n : n.toFixed(2));

  function render() {
    const count = cart.reduce((n, l) => n + l.qty, 0);
    document.querySelectorAll('[data-cart-count]').forEach((el) => { el.textContent = count; });
    if (!cart.length) {
      linesEl.innerHTML = '<div class="cart-empty"><p>It\'s quiet in here.</p><button class="btn btn-outline" data-close-cart>KEEP SHOPPING</button></div>';
    } else {
      linesEl.innerHTML = cart.map((l, i) => `
        <div class="cart-line">
          <img src="${esc(l.img)}" alt="">
          <div class="cart-line-info">
            <strong>${esc(l.name)}</strong>
            <span class="muted">Size: ${esc(l.size)} · Qty: ${l.qty}</span>
            <span class="muted">${l.price ? money(l.price * l.qty) : '$[XX]'}</span>
          </div>
          <button class="link-btn" data-remove="${i}">Remove</button>
        </div>`).join('');
    }
    const allPriced = cart.length && cart.every((l) => l.price);
    const total = cart.reduce((s, l) => s + (l.price || 0) * l.qty, 0);
    subtotalEl.textContent = allPriced ? money(total) : '$[XX]';
    const shipEl = document.querySelector('[data-ship-msg]');
    if (shipEl) {
      shipEl.hidden = !cart.length;
      shipEl.textContent = total >= FREE_SHIPPING ? 'You\'ve got free shipping!' : 'You\'re ' + money(FREE_SHIPPING - total) + ' away from free shipping.';
    }
  }

  function add(item) {
    const existing = cart.find((l) => l.id === item.id && l.size === item.size && l.name === item.name);
    if (existing) existing.qty += item.qty; else cart.push(item);
    save(cart); render(); open();
  }
  function open() { drawer.hidden = false; document.body.style.overflow = 'hidden'; }
  function close() { drawer.hidden = true; document.body.style.overflow = ''; }

  document.addEventListener('click', (e) => {
    const t = e.target.closest('[data-open-cart],[data-close-cart],[data-remove],[data-add-to-cart]');
    if (!t) return;
    if (t.matches('[data-open-cart]')) open();
    else if (t.matches('[data-close-cart]')) close();
    else if (t.matches('[data-remove]')) { cart.splice(Number(t.dataset.remove), 1); save(cart); render(); }
    else if (t.matches('[data-add-to-cart]')) {
      if (t.dataset.href) { window.location = t.dataset.href; return; } // needs a size: go to product page
      add({ id: t.dataset.id, name: t.dataset.name, price: parseFloat(t.dataset.price) || null, size: t.dataset.size, img: t.dataset.img, qty: 1 });
    }
  });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && !drawer.hidden) close(); });

  // Product page: size, quantity, add to cart
  const pdp = document.querySelector('[data-pdp]');
  if (pdp) {
    let size = null, qty = 1;
    const sizeBtns = pdp.querySelectorAll('.size-btn:not(.option-btn)');
    const addBtn = pdp.querySelector('[data-pdp-add]');
    const sizeLabel = pdp.querySelector('[data-size-label]');
    const qtyVal = pdp.querySelector('[data-qty-val]');
    if (sizeBtns.length === 1) size = sizeBtns[0].dataset.size;
    // Piece options (e.g. sweatsuit: full set / hoodie only / pants only)
    const optBtns = pdp.querySelectorAll('.option-btn');
    const priceEl = pdp.querySelector('[data-pdp-price]');
    const optLabel = pdp.querySelector('[data-option-label]');
    let option = optBtns.length ? optBtns[0].dataset.option : null;
    let price = optBtns.length ? parseFloat(optBtns[0].dataset.optionPrice) : (parseFloat(pdp.dataset.price) || null);
    optBtns.forEach((b) => b.addEventListener('click', () => {
      option = b.dataset.option; price = parseFloat(b.dataset.optionPrice);
      optBtns.forEach((x) => { const on = x === b; x.classList.toggle('on', on); x.setAttribute('aria-pressed', on); });
      optLabel.textContent = option.toUpperCase(); priceEl.textContent = '$' + price;
    }));
    sizeBtns.forEach((b) => b.addEventListener('click', () => {
      size = b.dataset.size;
      sizeBtns.forEach((x) => { const on = x === b; x.classList.toggle('on', on); x.setAttribute('aria-pressed', on); });
      sizeLabel.textContent = size; addBtn.textContent = 'ADD TO CART';
    }));
    pdp.querySelectorAll('[data-qty]').forEach((b) => b.addEventListener('click', () => {
      qty = Math.min(10, Math.max(1, qty + Number(b.dataset.qty))); qtyVal.textContent = qty;
    }));
    addBtn.addEventListener('click', () => {
      if (!size) { sizeLabel.textContent = 'Please select a size'; return; }
      add({ id: pdp.dataset.id, name: pdp.dataset.name + (option ? ' — ' + option.toUpperCase() : ''), price, size, img: pdp.dataset.img, qty });
    });
  }

  // Newsletter (front-end only for now)
  const nl = document.querySelector('[data-newsletter]');
  if (nl) nl.addEventListener('submit', (e) => {
    e.preventDefault();
    nl.outerHTML = '<p class="newsletter-done">You\'re on the list.</p>';
  });

  render();
})();
