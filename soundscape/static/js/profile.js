function toggleProfile() {
  const panel = document.getElementById('profilePanel');
  panel.classList.toggle('open');
}

document.addEventListener('click', function (event) {
  const panel = document.getElementById('profilePanel');
  const toggle = document.querySelector('.profile-toggle');

  if (panel && toggle && !panel.contains(event.target) && !toggle.contains(event.target)) {
    panel.classList.remove('open');
  }
});

window.toggleProfile = toggleProfile;

