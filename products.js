const PRODUCTS = Array.from({ length: 20 }, (_, index) => {
  const number = String(index + 1).padStart(2, '0');
  return {
    id: `room_${number}`,
    name: `غرفة نوم ${number}`,
    description: 'تصميم أنيق لغرفة نوم يجمع بين الجمال والراحة.',
    cover: `assets/rooms/room_${number}/ai-cover.jpg`,
    images: [
      `assets/rooms/room_${number}/original.jpg`
    ]
  };
});

function getProduct(id) {
  return PRODUCTS.find(product => product.id === id);
}

const WHATSAPP_NUMBER = '966576979199';
const WHATSAPP_MESSAGE = 'السلام عليكم، أريد الاستفسار عن هذا المنتج.';

function whatsappLink() {
  return `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(WHATSAPP_MESSAGE)}`;
}
