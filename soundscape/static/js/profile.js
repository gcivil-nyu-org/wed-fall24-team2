function formatDateTimeUser(dateString) {
  const date = new Date(dateString);
  const options = {
    weekday: 'short',
    year: 'numeric',
    month: 'numeric',
    day: 'numeric',
  };
  const formattedDate = date.toLocaleDateString('en-US', options);

  let hours = date.getHours();
  let minutes = date.getMinutes();
  const ampm = hours >= 12 ? 'PM' : 'AM';
  hours = hours % 12;
  hours = hours ? hours : 12;
  minutes = minutes < 10 ? '0' + minutes : minutes;

  return `${formattedDate} ${hours}:${minutes} ${ampm}`;
}

// Ensure `toggleProfile` is defined and accessible
function toggleProfile() {
  const panel = document.getElementById('profilePanel');
  panel.classList.toggle('open');
}

window.toggleProfile = toggleProfile;

currentAudio = null; // Global variable to track the currently playing audio

function fetchSoundUser(user_name, map) {
  fetch(`/soundscape_user/soundfiles_for_user/${user_name}/`)
    .then((response) => response.json())
    .then((datauser) => {
      if (datauser.sounds && datauser.sounds.length > 0) {
        // Check if there are sounds
        const soundsListPromisesUser = datauser.sounds.map((sounduser) => {
          // Create the initial loading list item
          const formattedDateUser = formatDateTimeUser(sounduser.created_at);
          const listItemUser = `
            <div id="${sounduser.sound_name}-user"> <!-- Assign a unique ID based on sound data -->
              ${sounduser.user_name} - ${sounduser.sound_descriptor}
              <div class="sound-date">${formattedDateUser}</div>
              <span class="loading"></span>
            </div>

          `;

          // Create a promise to download the sound file
          const soundPromiseUser = fetch(sounduser.listen_link)
            .then((response) => {
              if (!response.ok) {
                throw new Error('Network response was not ok');
              }
              return response.blob(); // Convert to Blob
            })
            .then((blob) => {
              const audioUrl = URL.createObjectURL(blob);

              // Create an audio element with controls
              const audioElement = document.createElement('audio');
              audioElement.controls = true;
              audioElement.style.width = '100%';

              const sourceElement = document.createElement('source');
              sourceElement.src = audioUrl;
              sourceElement.type = 'audio/mpeg';
              audioElement.appendChild(sourceElement);

              // Manage single audio playback
              audioElement.addEventListener('play', () => {
                if (currentAudio && currentAudio !== audioElement) {
                  currentAudio.pause(); // Pause any currently playing audio
                }
                currentAudio = audioElement; // Set the current audio to this one
              });

              const deleteBtn = isLoggedInUser(sounduser.user_name)
                ? `<button class="delete-icon" id="delete-sound-${sounduser.sound_name}-user"></button>`
                : '';

              document.getElementById(
                `${sounduser.sound_name}-user`
              ).innerHTML = `
                <div class="sound-listen-panel" id=${sounduser.sound_name}-user-sound-item>
                  <div class="sound-top-panel">
                    <div class="sound-name-stuff">
                      <div>${sounduser.user_name} - ${sounduser.sound_descriptor}</div>
                      <div class="sound-date">${formattedDateUser}</div>
                    </div>
                    ${deleteBtn}
                  </div>
                </div>
              `;

              // Append the audio element to the DOM
              document
                .getElementById(`${sounduser.sound_name}-user-sound-item`)
                .appendChild(audioElement);
              document
                .getElementById(`${sounduser.sound_name}-user-sound-item`)
                .addEventListener('click', () => {
                  const userSoundData = USER_SOUND_DATA?.find((soundData) => {
                    return (
                      soundData['s3_file_name'] === sounduser['sound_name']
                    );
                  });

                  if (userSoundData) {
                    map.flyTo({
                      center: [userSoundData.longitude, userSoundData.latitude],
                      zoom: 18,
                      speed: 1.2,
                    });
                  }
                });

              if (isLoggedInUser(sounduser.user_name)) {
                document
                  .getElementById(
                    'delete-sound-' + sounduser.sound_name + '-user'
                  )
                  .addEventListener('click', () => {
                    if (
                      window.confirm(
                        'Are you sure you want to delete this sound file?'
                      )
                    ) {
                      fetch('/soundscape_user/delete/', {
                        method: 'POST',
                        headers: {
                          'X-CSRFToken': csrfToken,
                        },
                        body: JSON.stringify(sounduser),
                      })
                        .then((response) => response.json())
                        .then((data) => {
                          if (data.error) {
                            alert(data.error);
                          } else {
                            alert('You have deleted a sound file!');
                          }
                          fetchSoundUser(sounduser.user_name);
                        })
                        .catch((error) => {
                          console.log('Error deleting sound file:', error);
                        });
                    }
                  });
              }
            })
            .catch((error) => {
              console.error('Error fetching sound file:', error);
              document.getElementById(
                `${sounduser.sound_name}-user`
              ).innerHTML = `
                ${sounduser.user_name} - ${sounduser.sound_descriptor} (Error loading sound)
              `;
            });

          return Promise.resolve(listItemUser);
        });

        Promise.all(soundsListPromisesUser).then((soundsListUser) => {
          document.getElementById('user-sounds-list').innerHTML =
            soundsListUser.join('');
        });
      } else {
        document.getElementById('user-sounds-list').innerHTML =
          '<p>No sounds yet.</p>';
      }
    })
    .catch((error) => console.error('Error loading sounds:', error));
}
