document.addEventListener('DOMContentLoaded', () => {
  const productsContainer = document.querySelector('#productsContainer');
  if (!productsContainer || typeof PRODUCTS === 'undefined') return;

  productsContainer.innerHTML = PRODUCTS.map((product, index) => `
    <article class="card">
      <div class="pic">
        ${index === 0 ? '<span class="new">جديد</span>' : ''}
        <img src="${product.cover}" alt="${product.name}" loading="lazy">
      </div>
      <div class="body">
        <h3>${product.name}</h3>
        <p>${product.description}</p>
        <a href="product.html?id=${product.id}">عرض التفاصيل</a>
      </div>
    </article>
  `).join('');

  document.querySelectorAll('[data-whatsapp]').forEach(link => {
    link.href = whatsappLink();
  });
});
