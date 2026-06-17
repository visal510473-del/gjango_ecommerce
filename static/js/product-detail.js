const variants = JSON.parse(document.getElementById('variants-data').textContent);
const colorSelect = document.getElementById('color-select');
const storageSelect = document.getElementById('storage-select');
const variantInput = document.getElementById('variant-id-input');
const productImage = document.getElementById('product-image');

// Get unique colors
const colors = [...new Set(variants.map(v => v.color))];
colors.forEach(color => {
    const opt = document.createElement('option');
    opt.value = color;
    opt.textContent = color;
    colorSelect.appendChild(opt);
});

function updateStorage() {
    const selectedColor = colorSelect.value;
    const filtered = variants.filter(v => v.color === selectedColor);

    storageSelect.innerHTML = '';
    filtered.forEach(v => {
        const opt = document.createElement('option');
        opt.value = v.storage;
        opt.textContent = v.storage;
        storageSelect.appendChild(opt);
    });

    updateVariant();
}

function updateVariant() {
    const selectedColor = colorSelect.value;
    const selectedStorage = storageSelect.value;
    const match = variants.find(v => v.color === selectedColor && v.storage === selectedStorage);

    if (match && productImage) {
        variantInput.value = match.id;

        // Smooth slide + fade transition
        productImage.style.transition = 'opacity 0.2s ease, transform 0.2s ease';
        productImage.style.opacity = '0';
        productImage.style.transform = 'scale(0.95) translateY(10px)';

        setTimeout(() => {
            productImage.src = match.image;
            productImage.onload = () => {
                productImage.style.opacity = '1';
                productImage.style.transform = 'scale(1) translateY(0)';
            };
            // Fallback in case onload doesn't fire
            setTimeout(() => {
                productImage.style.opacity = '1';
                productImage.style.transform = 'scale(1) translateY(0)';
            }, 300);
        }, 200);
    }
}

colorSelect.addEventListener('change', updateStorage);
storageSelect.addEventListener('change', updateVariant);

updateStorage();