const MIN_ZOOM_LEVEL = 13;

/* MARKERS */
function loadMarkers(existingMarkers, map) {
  const markers = JSON.parse(localStorage.getItem('markers')) || [];
  markers.forEach(({ lng, lat }) => {
    addMarker(lng, lat, map);
  });
  existingMarkers = markers;
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
          <div>
            <h3>Sound</h3>
            <button id="popup-hear-sound-btn">Listen</button>
            <button id="popup-upload-sound-btn">Upload</button>
          </div>
        `);
  const marker = new mapboxgl.Marker()
    .setLngLat([lng, lat])
    .setPopup(popup)
    .addTo(map);

  popup.on('open', () => {
    document
      .getElementById('popup-hear-sound-btn')
      .addEventListener('click', function () {
        alert('Button inside popup clicked!');
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
function addChatroomMarkers(map) {
  NYC_NEIGHBORHOODS.forEach((neighborhood) => {
    const el = document.createElement('div');
    el.className = 'chatroom-marker';

    const popup = new mapboxgl.Popup({
      offset: 25,
    }).setHTML(getChatroomComponent(neighborhood));
    existingMarkers.push({
      lng: neighborhood.longitude,
      lat: neighborhood.latitude,
    });
    new mapboxgl.Marker(el)
      .setLngLat([neighborhood.longitude, neighborhood.latitude])
      .setPopup(popup)
      .addTo(map);
  });
}

// removing soundmarkers for heatmap
// function addSoundMarkers(map) {
//   SOUND_DATA.forEach((sound) => {
//     if (sound.longitude && sound.latitude) {
//       const el = document.createElement('div');
//       el.className = 'sound-marker';
//       const popup = new mapboxgl.Popup({
//         offset: 25,
//       }).setHTML(`
//           <div class="sound-information">
//              <span>Description: ${sound.descriptor}</span>
//              <span>Status: ${sound.status}</span>
//              <span>Date Reported: ${new Intl.DateTimeFormat('en-US').format(
//                new Date(sound.created_date)
//              )}</span>
//           </div>
//         `);
//       existingMarkers.push({
//         lng: sound.longitude,
//         lat: sound.latitude,
//       });
//       new mapboxgl.Marker(el)
//         .setLngLat([sound.longitude, sound.latitude])
//         .setPopup(popup)
//         .addTo(map);
//     }
//   });
// }

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

  // Load markers and add chatroom markers, then add search box
  loadMarkers(existingMarkers, map);
  addChatroomMarkers(map);
  addControls(map);
  addHeatmapLayer(map);
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
