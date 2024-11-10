// function toggleProfile() {
//   const panel = document.getElementById('profilePanel');
//   panel.classList.toggle('open');
//   console.log("Hello");
//   console.log(USERNAME);
// }

// document.addEventListener('click', function (event) {
//   const panel = document.getElementById('profilePanel');
//   const toggle = document.querySelector('.profile-toggle');
//   console.log("Hello there");

//   if (panel && toggle && !panel.contains(event.target) && !toggle.contains(event.target)) {
//     panel.classList.remove('open');
//   }
// });

// window.toggleProfile = toggleProfile;

document.addEventListener("DOMContentLoaded", () => {

  console.log(USER_SOUND_DATA);
  console.log(USERNAME);

  if (typeof USER_SOUND_DATA === 'undefined') return;
  
  fetchSoundUser(USERNAME);

});

function fetchSoundUser(user_name) {
  fetch(`/soundscape_user/soundfiles_for_user/${user_name}/`)
    .then((response) => response.json())
    .then((data) => {

      if (data.sounds && data.sounds.length > 0) {
        const soundsListPromises = data.sounds.map((sound) => {
          const formattedDate = formatDateTime(sound.created_at);

          const listItem = `
            <li id="${sound.sound_name}" class="sound-item">
              <div class="sound-info">
                <div class="sound-header">
                  <div class="sound-name-header>
                  <span class="sound-user">${sound.user_name}</span>
                  <span class="sound-descriptor">${sound.sound_descriptor}</span>
                  </div>
                  ${isLoggedInUser(sound.user_name) ? 
                    `<button class="delete-icon" id="delete-sound-${sound.sound_name}"></button>` : ''}
                </div>
              </div>
              <div class="sound-date">${formattedDate}</div>
              <div class="sound-controls">
                <audio controls class="audio-player">
                  <source src="${sound.listen_link}" type="audio/mpeg">
                  Your browser does not support the audio element.
                </audio>
              </div>
            </li>
          `;

          const soundPromise = fetch(sound.listen_link)
            .then((response) => {
              if (!response.ok) {
                throw new Error('Network response was not ok');
              }
              return response.blob();
            })
            .then((blob) => {
              const audioUrl = URL.createObjectURL(blob);
              document.getElementById(sound.sound_name).querySelector(".audio-player source").src = audioUrl;
            })
            .catch((error) => {
              console.error('Error fetching sound file:', error);
              document.getElementById(sound.sound_name).querySelector(".sound-info").innerHTML +=
                '<span class="error">Error loading sound</span>';
            });

          return Promise.resolve(listItem);
        });

        Promise.all(soundsListPromises).then((soundsList) => {
          document.getElementById('user-sounds-list').innerHTML = soundsList.join('');
        });
      } else {
        document.getElementById('user-sounds-list').innerHTML = '<p>No sounds yet.</p>';
      }
    })
    .catch((error) => console.error('Error loading sounds:', error));
}

function playSound(url) {
  fetch(url)
    .then((response) => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.blob();
    })
    .then((blob) => {
      const audioUrl = URL.createObjectURL(blob);
      const audio = new Audio(audioUrl);
      audio.play();
    })
    .catch((error) => console.error('Error fetching sound file:', error));
}

function formatDateTime(dateString) {
  console.log(dateString)
  const date = new Date(dateString);

  const options = { weekday: 'short', year: 'numeric', month: 'numeric', day: 'numeric' };
  const formattedDate = date.toLocaleDateString('en-US', options);

  let hours = date.getHours();
  let minutes = date.getMinutes();
  const ampm = hours >= 12 ? 'PM' : 'AM';
  hours = hours % 12;
  hours = hours ? hours : 12;
  minutes = minutes < 10 ? '0' + minutes : minutes;
  
  const formattedTime = `${hours}:${minutes} ${ampm}`;

  return `${formattedDate} ${formattedTime}`;
}

// function deleteSound(soundId) {
//   fetch(`/soundscape_user/delete_sound/${soundId}/`, { method: 'DELETE' })
//     .then(response => response.ok ? console.log('Sound deleted') : console.log('Failed to delete sound'))
//     .catch(error => console.error('Error:', error));
// }

function toggleProfile() {
  const panel = document.getElementById('profilePanel');
  panel.classList.toggle('open');
  console.log("Toggled profile panel for user:", USERNAME);
}

// document.addEventListener('click', function (event) {
//   const panel = document.getElementById('profilePanel');
//   const toggle = document.querySelector('.profile-toggle');
//   console.log("Hello there");

//   if (panel && toggle && !panel.contains(event.target) && !toggle.contains(event.target)) {
//     panel.classList.remove('open');
//   }
// });

window.toggleProfile = toggleProfile;


