document.addEventListener('DOMContentLoaded', function() {
    var categoryField = document.querySelector('#id_category');
    var subcategoryField = document.querySelector('.field-ensino_subcategory');

    function toggleSubcategoryField() {
        if (categoryField.value === 'ensino') {
            subcategoryField.style.display = 'block';
        } else {
            subcategoryField.style.display = 'none';
        }
    }

    categoryField.addEventListener('change', toggleSubcategoryField);
    toggleSubcategoryField(); // Inicializa a lógica ao carregar a página
});
