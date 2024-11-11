<<<<<<< HEAD
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

=======
// function toggleProfile() {
//   const panel = document.getElementById('profilePanel');
//   panel.classList.toggle('open');
// }

// document.addEventListener('click', function (event) {
//   const panel = document.getElementById('profilePanel');
//   const toggle = document.querySelector('.profile-toggle');

//   if (panel && toggle && !panel.contains(event.target) && !toggle.contains(event.target)) {
//     panel.classList.remove('open');
//   }
// });

// window.toggleProfile = toggleProfile;

document.addEventListener("DOMContentLoaded", () => {

  // console.log(USER_SOUND_DATA);
  // console.log(USERNAME);

  if (typeof USER_SOUND_DATA === 'undefined') return;
  
  fetchSoundUser(USERNAME);

});

function fetchSoundUser(user_name) {
  fetch(`/soundscape_user/soundfiles_for_user/${user_name}/`)
    .then((response) => response.json())
    .then((datauser) => {
      // console.log("Why here")
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
              const audioUrl = URL.createObjectURL(blob); // Create a Blob URL
              // Update the list item to include the audio element
              const audioElement = `
                <audio controls style="width: 100%;">
                  <source src="${audioUrl}" type="audio/mpeg">
                  Your browser does not support the audio element.
                </audio>
              `;

              const deleteBtn = isLoggedInUser(sounduser.user_name)? 
              `<button class="delete-icon" id="delete-sound-${sounduser.sound_name}-user"></button>` : ``;

              // Replace the loading message with the audio element
              document.getElementById(
                `${sounduser.sound_name}-user`
              ).innerHTML = `
              <div class="sound-listen-panel">
                <div class="sound-top-panel">
                  <div class="sound-name-stuff">
                    <div>${sounduser.user_name} - ${sounduser.sound_descriptor}</div>
                    <div class="sound-date">${formattedDateUser}</div>
                  </div>
                  ${deleteBtn}
                </div>
                ${audioElement}
              </div>
              `;

              
              if (isLoggedInUser(sounduser.user_name)) {
                document.getElementById("delete-sound-" + sounduser.sound_name + "-user").addEventListener('click', () => {
                  if (window.confirm("Are you sure you want to delete this sound file?")) {
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
                        alert(data.error)
                      } else {
                        alert('You have deleted a sound file!');
                      }
                      
                      fetchSoundUser(sounduser.user_name);
                    })
                    .catch((error) => {
                      console.log('Error deleting sound file:', error);
                    })
                  }
                });
              }

            })
            .catch((error) => {
              console.error('Error fetching sound file:', error);
              // Handle error gracefully by showing a message
              document.getElementById(
                sounduser.sound_name
              ).innerHTML = `${sounduser.user_name} - ${sounduser.sound_descriptor} (Error loading sound)`;
            });

          return Promise.resolve(listItemUser); // Resolve the initial loading item
        });

        // Wait for all sounds to be processed and display them
        Promise.all(soundsListPromisesUser).then((soundsListUser) => {
          // Set the innerHTML for the list
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

function formatDateTimeUser(dateString) {
  // console.log(dateString)
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

function toggleProfile() {
  const panel = document.getElementById('profilePanel');
  panel.classList.toggle('open');
  console.log("Toggled profile panel for user:", USERNAME);
}

>>>>>>> develop
window.toggleProfile = toggleProfile;

