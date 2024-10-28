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
params.append("soundType", soundTypes.length > 0 ? soundTypes[0] : "Noise");
if (dateFrom) params.append("dateFrom", dateFrom);
if (dateTo) params.append("dateTo", dateTo);

// Redirect to the filtered sound data view
window.location.href = `/?${params.toString()}`;
}

function resetFilters() {
  window.location.href = `/`;
}

window.toggleFilters = toggleFilters;
window.applyFilters = applyFilters;
window.resetFilters = resetFilters;
