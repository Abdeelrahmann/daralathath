document.addEventListener('DOMContentLoaded', () => {
  const params = new URLSearchParams(window.location.search);
  const id = params.get('id');
  const product = typeof getProduct === 'function' ? getProduct(id) : null;

  const mainImage = document.getElementById('mainProductImage');
  const thumbnails = document.getElementById('thumbnails');
  const name = document.getElementById('productName');
  const description = document.getElementById('productDescription');
  const whatsappButton = document.getElementById('whatsappButton');

  if (!product) {
    name.textContent = 'المنتج غير موجود';
    description.textContent = 'عذراً، لم يتم العثور على هذا المنتج.';
    return;
  }

  document.title = `${product.name} | دار الأثاث لغرف النوم`;
  name.textContent = product.name;
  description.textContent = product.description;
  whatsappButton.href = whatsappLink();

  function selectImage(src, thumbnail) {
    mainImage.src = src;
    mainImage.alt = product.name;
    document.querySelectorAll('.thumbnail').forEach(item => item.classList.remove('selected'));
    thumbnail.classList.add('selected');
  }

  product.images.forEach((src, index) => {
    const thumbnail = document.createElement('button');
    thumbnail.type = 'button';
    thumbnail.className = `thumbnail${index === 0 ? ' selected' : ''}`;
    thumbnail.innerHTML = `<img src="${src}" alt="${product.name} - صورة ${index + 1}" loading="lazy">`;
    thumbnail.addEventListener('click', () => selectImage(src, thumbnail));
    thumbnails.appendChild(thumbnail);
  });

  if (product.images.length) {
    mainImage.src = product.images[0];
    mainImage.alt = product.name;
  }
});
