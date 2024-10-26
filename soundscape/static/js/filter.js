function toggleFilters() {
  const panel = document.getElementById('filterPanel');
  panel.classList.toggle('open');
}

document.addEventListener('click', function (event) {
  const panel = document.getElementById('filterPanel');
  const toggle = document.querySelector('.filter-toggle');

  if (!panel.contains(event.target) && !toggle.contains(event.target)) {
    panel.classList.remove('open');
  }
});
