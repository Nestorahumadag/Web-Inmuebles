document.getElementById('id_region').addEventListener('change', function() {
    var regionId = this.value;
    var comunaSelect = document.getElementById('id_comuna');
    comunaSelect.innerHTML = '<option value="">---------</option>';  // Clear previous options

    if (regionId) {
        fetch('/comunas/' + regionId + '/')
        .then(response => response.json())
        .then(data => {
            for (var key in data) {
                var option = document.createElement('option');
                option.value = key;
                option.textContent = data[key];
                comunaSelect.appendChild(option);
            }
        });
    }
});