function toggleFilters() {
  const panel = document.getElementById('filterPanel');
  panel.classList.toggle('open');
}

document.addEventListener('click', function (event) {
  const panel = document.getElementById('filterPanel');
  const toggle = document.querySelector('.filter-toggle');

  if (panel && toggle && !panel.contains(event.target) && !toggle.contains(event.target)) {
    panel.classList.remove('open');
  }
});


function applyFilters(map) {
  const soundTypes = Array.from(document.querySelectorAll("input[name='soundType']:checked")).map(
    checkbox => checkbox.value
  );
  const dateFrom = document.getElementById("dateFrom").value;
  const dateTo = document.getElementById("dateTo").value;

  const params = new URLSearchParams();
  soundTypes.forEach(soundType => params.append("soundType", soundType));
  if (dateFrom) params.append("dateFrom", dateFrom);
  if (dateTo) params.append("dateTo", dateTo);

  console.log(params);

  // Redirect to the filtered sound data view
  window.location.href = `/?${params.toString()}`;
}


function resetFilters() {
  window.location.href = `/`;
}

window.toggleFilters = toggleFilters;
window.applyFilters = applyFilters;
window.resetFilters = resetFilters;


  // Function to initialize filters based on URL parameters
  function initializeFiltersFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    const filters = document.querySelectorAll('.filter-checkbox input[type="checkbox"]');

    filters.forEach((checkbox) => {
      const filterName = checkbox.name;
      const filterValue = checkbox.value;
      console.log(urlParams);

      // Check if the URL has the specific filter parameter and matches the checkbox value
      if (urlParams.has(filterName) && urlParams.getAll(filterName).includes(filterValue)) {
        checkbox.checked = true;
      } else {
        checkbox.checked = false;
      }
    });

    // Set date inputs if present in URL
    if (urlParams.has('dateFrom')) {
      document.getElementById('dateFrom').value = urlParams.get('dateFrom');
    }
    if (urlParams.has('dateTo')) {
      document.getElementById('dateTo').value = urlParams.get('dateTo');
    }
  }

  // Call the function when the page loads
  window.addEventListener('DOMContentLoaded', initializeFiltersFromURL);
