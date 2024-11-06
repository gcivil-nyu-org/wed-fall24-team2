const MIN_ZOOM_LEVEL = 13;

/* MARKERS */

function addUserSound(map) {
  USER_SOUND_DATA.forEach((sound) => {
    const el = document.createElement('div');
    el.className = 'sound-marker';

    const popup = new mapboxgl.Popup({ offset: 25 }).setHTML(`
    <div style="font-family: Arial, sans-serif; width: 250px; color: #333;">
    <div id="popup-content">
      <h3 style="margin: 0 0 10px; font-size: 18px;">Sound</h3>
      <div style="margin-bottom: 10px;">
        <button id="popup-upload-sound-btn" style="background-color: #007BFF; color: white; border: none; padding: 5px 10px; cursor: pointer; margin-left: 5px;">Upload</button>
      </div>
      <h4 style="font-size: 16px; margin: 10px 0;">Uploaded Sounds:</h4>
      <ul id="sounds-list" style="list-style-type: none; padding-left: 0; margin: 0;"></ul>
    </div>
    <div id="upload-sound-form" style="display: none; margin-top: 10px; padding: 10px; border: 1px solid #ccc; border-radius: 5px; background-color: #f9f9f9;">
      <form id="sound-upload-form">
        <input type="file" id="sound-file" accept="audio/*" required style="margin-bottom: 1px;"/>
        <span id="file-size-error" style="display: block; color: red; font-size: 9px; margin-top: 0px; margin-bottom: 5px">Max file size is 3 MB</span>
        <label for="sound-descriptor" style="margin-bottom: 5px; display: block;">Sound Descriptor:</label>
        <select id="sound-descriptor" required style="width: 100%; padding: 5px; margin-bottom: 10px;">
          <option value="">Select a descriptor</option>
          ${SOUND_DESCRIPTORS.map(descriptor => 
            `<option value="${descriptor.descriptor}">${descriptor.descriptor}</option>`
          ).join('')}
        </select>
        <input type="hidden" id="latitude" value="${sound.latitude}"/>
        <input type="hidden" id="longitude" value="${sound.longitude}"/>
        <button type="submit" style="background-color: #007BFF; color: white; border: none; padding: 5px 10px; cursor: pointer;">Submit</button>
        <button type="button" id="close-upload-form-btn" style="background-color: #FF4C4C; color: white; border: none; padding: 5px 10px; cursor: pointer; margin-left: 5px;">Close</button>
      </form>
    </div>
  </div>
`);
    existingMarkers.push({
      lng: sound.longitude,
      lat: sound.latitude,
    });
    new mapboxgl.Marker(el)
      .setLngLat([sound.longitude, sound.latitude])
      .setPopup(popup)
      .addTo(map);
    popup.on('open', () => {
      fetchAndDisplaySounds(sound.latitude, sound.longitude);

      // document
      //   .getElementById('popup-hear-sound-btn')
      //   .addEventListener('click', function () {
      //     alert('Playing sound at this location!');
      //   });

      document.getElementById('popup-upload-sound-btn').addEventListener('click', function () {
        document.getElementById('popup-content').style.display = 'none';
        document.getElementById('upload-sound-form').style.display = 'block';
      });
    

      document.getElementById('close-upload-form-btn').addEventListener('click', function () {
        document.getElementById('upload-sound-form').style.display = 'none';
        document.getElementById('popup-content').style.display = 'block';
      });

      document
        .getElementById('sound-upload-form')
        .addEventListener('submit', function (event) {
          event.preventDefault();
          const soundFile = document.getElementById('sound-file').files[0];
          if (soundFile.size > 3 *1024 * 1024) {  // 3 MB limit
            alert('Please limit the sound file size to 3 MB');
            return;
          }

          const latitude = document.getElementById('latitude').value;
          const longitude = document.getElementById('longitude').value;
          const soundDescriptor =
            document.getElementById('sound-descriptor').value;

          // Handle the file upload and form data submission
          const formData = new FormData();
          formData.append('username', username);
          formData.append('sound_file', soundFile);
          formData.append('latitude', latitude);
          formData.append('longitude', longitude);
          formData.append('sound_descriptor', soundDescriptor);

          fetch('/soundscape_user/upload/', {
            method: 'POST',
            headers: {
              'X-CSRFToken': csrfToken,
            },
            body: formData,
          })
            .then((response) => response.json())
            .then((data) => {

              if (data.error)
              {
                alert(data.error)
              }else{
                alert('Sound uploaded successfully!');
                document.getElementById('upload-sound-form').style.display = 'none';
                document.getElementById('popup-content').style.display = 'block';

                document.getElementById('sound-upload-form').reset();

                fetchAndDisplaySounds(sound.latitude, sound.longitude);
              }
            })
            .catch((error) => {
              alert('Error uploading sound');
              console.error('Error:', error);
            });
        });
    });
  });
}

function fetchAndDisplaySounds(lat, lng) {
  fetch(`/soundscape_user/soundfiles_at_location/${lat}/${lng}/`)
    .then((response) => response.json())
    .then((data) => {

      if (data.sounds && data.sounds.length > 0) {
        // Check if there are sounds
        const soundsListPromises = data.sounds.map((sound) => {
          // Create the initial loading list item
          const listItem = `
            <li id="${sound.sound_name}"> <!-- Assign a unique ID based on sound data -->
              ${sound.user_name} - ${sound.sound_descriptor}
              <span class="loading"></span>
            </li>
          `;

          // Create a promise to download the sound file
          const soundPromise = fetch(sound.listen_link)
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

              const deleteBtn = isLoggedInUser(sound.user_name)? 
              `<button class="delete-icon" id="delete-sound-${sound.sound_name}"></button>` : ``;

              // Replace the loading message with the audio element
              document.getElementById(
                sound.sound_name
              ).innerHTML = `${sound.user_name} - ${sound.sound_descriptor} ${deleteBtn} ${audioElement}`;

              
              if (isLoggedInUser(sound.user_name)) {
                document.getElementById("delete-sound-" + sound.sound_name).addEventListener('click', () => {
                  if (window.confirm("Are you sure you want to delete this sound file?")) {
                    fetch('/soundscape_user/delete/', {
                      method: 'POST',
                      headers: {
                        'X-CSRFToken': csrfToken,
                      },
                      body: JSON.stringify(sound),
                    })
                    .then((response) => response.json())
                    .then((data) => {
                      
                      if (data.error) {
                        alert(data.error)
                      } else {
                        alert('You have deleted a sound file!');
                      }
                      
                      fetchAndDisplaySounds(lat, lng);
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
                sound.sound_name
              ).innerHTML = `${sound.user_name} - ${sound.sound_descriptor} (Error loading sound)`;
            });

          return Promise.resolve(listItem); // Resolve the initial loading item
        });

        // Wait for all sounds to be processed and display them
        Promise.all(soundsListPromises).then((soundsList) => {
          // Set the innerHTML for the list
          document.getElementById('sounds-list').innerHTML =
            soundsList.join('');
        });
      } else {
        document.getElementById('sounds-list').innerHTML =
          '<p>No sounds yet.</p>';
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

function addMarker(lng, lat, map) {
  const currentZoom = map.getZoom();
  const currentCenter = map.getCenter();

  const distanceFromUser = getDistance(
    lat,
    lng,
    currentCenter.lat,
    currentCenter.lng
  );

  if (currentZoom < MIN_ZOOM_LEVEL || distanceFromUser > 1000) {
    return;
  }

  const popup = new mapboxgl.Popup({ offset: 25 }).setHTML(`
  <div style="font-family: Arial, sans-serif; width: 250px; color: #333;">
    <div id="popup-content">
      <h3 style="margin: 0 0 10px; font-size: 18px;">Sound</h3>
      <div style="margin-bottom: 10px;">
        <button id="popup-upload-sound-btn" style="background-color: #007BFF; color: white; border: none; padding: 5px 10px; cursor: pointer; margin-left: 5px;">Upload</button>
      </div>
      <h4 style="font-size: 16px; margin: 10px 0;">Uploaded Sounds:</h4>
      <ul id="sounds-list" style="list-style-type: none; padding-left: 0; margin: 0;"></ul>
    </div>
    <div id="upload-sound-form" style="display: none; margin-top: 10px; padding: 10px; border: 1px solid #ccc; border-radius: 5px; background-color: #f9f9f9;">
      <form id="sound-upload-form">
        <input type="file" id="sound-file" accept="audio/*" required style="margin-bottom: 1px;"/>
        <span id="file-size-error" style="display: block; color: red; font-size: 9px; margin-top: 0px; margin-bottom: 5px">Max file size is 3 MB</span>
        <label for="sound-descriptor" style="margin-bottom: 5px; display: block;">Sound Descriptor:</label>
        <select id="sound-descriptor" required style="width: 100%; padding: 5px; margin-bottom: 10px;">
          <option value="">Select a descriptor</option>
          ${SOUND_DESCRIPTORS.map(descriptor => 
            `<option value="${descriptor.descriptor}">${descriptor.descriptor}</option>`
          ).join('')}
        </select>
        <input type="hidden" id="latitude" value="${lat}"/>
        <input type="hidden" id="longitude" value="${lng}"/>
        <button type="submit" style="background-color: #007BFF; color: white; border: none; padding: 5px 10px; cursor: pointer;">Submit</button>
        <button type="button" id="close-upload-form-btn" style="background-color: #FF4C4C; color: white; border: none; padding: 5px 10px; cursor: pointer; margin-left: 5px;">Close</button>
      </form>
    </div>
  </div>
`);

  const el = document.createElement('div');
  el.className = 'sound-marker';

  const marker = new mapboxgl.Marker(el)
    .setLngLat([lng, lat])
    .setPopup(popup)
    .addTo(map);

  popup.on('open', () => {
    fetchAndDisplaySounds(lat, lng);

    // document
    //   .getElementById('popup-hear-sound-btn')
    //   .addEventListener('click', function () {
    //     alert('Playing sound at this location!');
    //   });

    document.getElementById('popup-upload-sound-btn').addEventListener('click', function () {
      document.getElementById('popup-content').style.display = 'none';
      document.getElementById('upload-sound-form').style.display = 'block';
    });
  

    document.getElementById('close-upload-form-btn').addEventListener('click', function () {
      document.getElementById('upload-sound-form').style.display = 'none';
      document.getElementById('popup-content').style.display = 'block';
    });
  


    document
      .getElementById('sound-upload-form')
      .addEventListener('submit', function (event) {
        event.preventDefault();
        const soundFile = document.getElementById('sound-file').files[0];
        if (soundFile.size > 3 *1024 * 1024) {  // 3 MB limit
          alert('Please limit the sound file size to 3 MB');
          return;
        }

        const latitude = document.getElementById('latitude').value;
        const longitude = document.getElementById('longitude').value;
        const soundDescriptor =
          document.getElementById('sound-descriptor').value;

        // Handle the file upload and form data submission
        const formData = new FormData();
        formData.append('username', username);
        formData.append('sound_file', soundFile);
        formData.append('latitude', latitude);
        formData.append('longitude', longitude);
        formData.append('sound_descriptor', soundDescriptor);

        fetch('/soundscape_user/upload/', {
          method: 'POST',
          headers: {
            'X-CSRFToken': csrfToken,
          },
          body: formData,
        })
          .then((response) => response.json())
          .then((data) => {

            if (data.error)
            {
              alert(data.error)
            }else{
              alert('Sound uploaded successfully!');
              document.getElementById('upload-sound-form').style.display = 'none';
              document.getElementById('popup-content').style.display = 'block';

              document.getElementById('sound-upload-form').reset();

              fetchAndDisplaySounds(lat, lng);
            }
          })
          .catch((error) => {
            alert('Error uploading sound');
            console.error('Error:', error);
          });
      });
  });
}

function isDuplicateMarker(lng, lat, existingMarkers) {
  const threshold = 0.0005;
  return existingMarkers.some((marker) => {
    return (
      Math.abs(marker.lng - lng) < threshold &&
      Math.abs(marker.lat - lat) < threshold
    );
  });
}

function saveMarker(lng, lat, existingMarkers) {
  existingMarkers.push({ lng, lat });
  localStorage.setItem('markers', JSON.stringify(existingMarkers));
}

function addControls(map) {
  // Add geolocate control to the map.
  if (map) {
    /* SEARCH BOX */
    const search = new MapboxSearchBox();
    search.accessToken = mapboxgl.accessToken;
    search.options = {
      types: 'address,poi',
      proximity: map.getCenter().toArray(),
      marker: true,
    };
    map.addControl(search);

    /* GEOLOCATION */
    // map.addControl(
    //   new mapboxgl.GeolocateControl({
    //     positionOptions: {
    //       enableHighAccuracy: true,
    //     },
    //     // When active the map will receive updates to the device's location as it changes.
    //     trackUserLocation: true,
    //     // Draw an arrow next to the location dot to indicate which direction the device is heading.
    //     showUserHeading: true,
    //   })
    // );

    /* NAVIGATION CONTROL */
    map.addControl(new mapboxgl.NavigationControl());
  }
}

function isLoggedIn() {
  return username != 'Anonymous';
}

function isLoggedInUser(provided_username) {
  return username == provided_username
}

function addChatroomMarkers(map) {
  NYC_NEIGHBORHOODS.forEach((neighborhood) => {
    const el = document.createElement('div');
    el.className = 'chatroom-marker';

    const popup = new mapboxgl.Popup({
      offset: 25,
    }).setHTML(isLoggedIn() ? getChatroomComponent(neighborhood): getChatroomPublicComponent(neighborhood));
    existingMarkers.push({
      lng: neighborhood.longitude,
      lat: neighborhood.latitude,
    });
    const marker = new mapboxgl.Marker(el)
      .setLngLat([neighborhood.longitude, neighborhood.latitude])
      .setPopup(popup)
      .addTo(map);

    let chatInitialized = false;

    marker.getElement().addEventListener('click', () => {
      if (!chatInitialized && isLoggedIn()) {
        console.log('initializing chat for:', neighborhood);
        initializeChat(neighborhood);
        chatInitialized = true;
      }
    });
  });
}

function addHeatmapLayer(map) {
  map.on('load', () => {
    map.addSource('heatmap-data', {
      type: 'geojson',
      data: SOUND_GEOJSON_DATA,
    });

    map.addLayer({
      id: 'heatmap',
      type: 'heatmap',
      source: 'heatmap-data',
      paint: {
        // Set the heatmap weight based on the 'weight' property
        'heatmap-weight': [
          'coalesce', // Use 'coalesce' to provide a default value
          ['get', 'weight'], // Get the 'weight' property
          0, // Default weight if 'weight' is not present
        ],
        'heatmap-intensity': {
          stops: [
            [0, 0],
            [6, 2],
          ],
        },
        'heatmap-color': [
          'interpolate',
          ['linear'],
          ['heatmap-density'],
          0,
          'rgba(0,0,0,0)',
          0.2,
          'rgba(255,237,160,0.5)',
          0.4,
          'rgba(255,217,105,0.7)',
          0.6,
          'rgba(255,182,72,0.8)',
          0.8,
          'rgba(255,120,50,1)',
          1,
          'rgba(255,50,0,1)',
        ],
        'heatmap-radius': {
          stops: [
            [10, 30],
            [20, 50],
          ],
        },
        'heatmap-opacity': 0.8,
      },
    });

    const popup = new mapboxgl.Popup({
      closeButton: false,
      closeOnClick: false
    });

    map.on('mouseenter', 'heatmap', (e) => {
      // Change the cursor style as a UI indicator.
      map.getCanvas().style.cursor = 'pointer';

      const coordinates = e.features[0].geometry.coordinates;
      const complaint_type = e.features[0].properties.complaint_type.split(/[ - ]+/).pop();
      const descriptor = e.features[0].properties.descriptor;
      const status = e.features[0].properties.status;
      const created_date = e.features[0].properties.created_date;
      const closed_date = e.features[0].properties.closed_date;

      popup.setLngLat(coordinates).setHTML(`
        <div class="sound-information">
          <span>Type: ${complaint_type}</span>
          <span>Descriptor: ${descriptor}</span>
          <span>Reported at: ${new Intl.DateTimeFormat('en-US').format(
            new Date(created_date)
          )}</span>
          ${closed_date?
            `<span>Closed at: ${new Intl.DateTimeFormat('en-US').format(
              new Date(closed_date)
            )}</span>` : ``
          }

          ${status == "Open"?
            `<span class="open-badge">${status}</span>` :
            (status == "In Progress"?
            `<span class="in-progress-badge">${status}</span>` :
            `<span class="closed-badge">${status}</span>`)}
        </div>
      `).addTo(map);
    });

    map.on('mouseleave', 'heatmap', () => {
      map.getCanvas().style.cursor = '';
      popup.remove();
    });
  });
}

/* MAP */
function initializeMap(centerCoordinates, map, existingMarkers) {
  if (!map) {
    console.log('initializing map');
    map = new mapboxgl.Map({
      container: 'map',
      style: 'mapbox://styles/mapbox/streets-v11',
      center: centerCoordinates,
      zoom: 12,
    });
    // Register onClick function on map
    map.on('click', function (e) {
      const coordinates = e.lngLat;
      if (
        isDuplicateMarker(coordinates.lng, coordinates.lat, existingMarkers)
      ) {
        return;
      }
      addMarker(coordinates.lng, coordinates.lat, map);
      saveMarker(coordinates.lng, coordinates.lat, existingMarkers);
    });
  }

  addHeatmapLayer(map);
  addChatroomMarkers(map);
  if (isLoggedIn()) {
    addUserSound(map);
  }

  addControls(map);
}

function successLocation(position, map, existingMarkers) {
  const { latitude, longitude } = position.coords;
  initializeMap([longitude, latitude], map, existingMarkers);
}

function errorLocation(error, map, existingMarkers) {
  // alert(
  //   'Unable to retrieve your location. Initializing map at default location. ' +
  //     error
  // );
  // Optional: Set a default location (e.g., NYC) if geolocation fails
  initializeMap([-74.006, 40.7128], map, existingMarkers); // Default center (New York City)
}
