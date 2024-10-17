const MIN_ZOOM_LEVEL = 13;
const NYC_NEIGHBORHOODS = [
  { name: 'Manhattan', lat: 40.7831, lng: -73.9712, nearbyStreet: 'Broadway' },
  {
    name: 'Brooklyn',
    lat: 40.6782,
    lng: -73.9442,
    nearbyStreet: 'Flatbush Avenue',
  },
  {
    name: 'Queens',
    lat: 40.7282,
    lng: -73.7949,
    nearbyStreet: 'Queens Boulevard',
  },
  {
    name: 'The Bronx',
    lat: 40.837,
    lng: -73.8654,
    nearbyStreet: 'Fordham Road',
  },
  {
    name: 'Staten Island',
    lat: 40.5795,
    lng: -74.1502,
    nearbyStreet: 'Richmond Avenue',
  },
  {
    name: 'Upper East Side',
    lat: 40.7736,
    lng: -73.9566,
    nearbyStreet: 'Park Avenue',
  },
  {
    name: 'Upper West Side',
    lat: 40.787,
    lng: -73.9734,
    nearbyStreet: 'Columbus Avenue',
  },
  { name: 'Harlem', lat: 40.8116, lng: -73.9453, nearbyStreet: '125th Street' },
  {
    name: 'Greenwich Village',
    lat: 40.7336,
    lng: -73.9962,
    nearbyStreet: 'Bleecker Street',
  },
  {
    name: 'East Village',
    lat: 40.7274,
    lng: -73.9817,
    nearbyStreet: 'St. Marks Place',
  },
  {
    name: 'West Village',
    lat: 40.7331,
    lng: -74.0028,
    nearbyStreet: 'Hudson Street',
  },
  { name: 'SoHo', lat: 40.7242, lng: -74.0036, nearbyStreet: 'Spring Street' },
  {
    name: 'Tribeca',
    lat: 40.719,
    lng: -74.0113,
    nearbyStreet: 'Warren Street',
  },
  { name: 'Chelsea', lat: 40.7442, lng: -74.0022, nearbyStreet: '23rd Street' },
  {
    name: "Hell's Kitchen",
    lat: 40.7645,
    lng: -73.9936,
    nearbyStreet: '9th Avenue',
  },
  {
    name: 'Financial District',
    lat: 40.7074,
    lng: -74.0113,
    nearbyStreet: 'Wall Street',
  },
  {
    name: 'Lower East Side',
    lat: 40.7132,
    lng: -73.9866,
    nearbyStreet: 'Orchard Street',
  },
  {
    name: 'Williamsburg',
    lat: 40.7081,
    lng: -73.9571,
    nearbyStreet: 'Bedford Avenue',
  },
  {
    name: 'Bushwick',
    lat: 40.6928,
    lng: -73.911,
    nearbyStreet: 'Knickerbocker Avenue',
  },
  {
    name: 'Crown Heights',
    lat: 40.6618,
    lng: -73.9352,
    nearbyStreet: 'Eastern Parkway',
  },
  {
    name: 'Prospect Lefferts Gardens',
    lat: 40.6533,
    lng: -73.9515,
    nearbyStreet: 'Flatbush Avenue',
  },
  {
    name: 'Astoria',
    lat: 40.7694,
    lng: -73.9257,
    nearbyStreet: 'Steinway Street',
  },
  {
    name: 'Flushing',
    lat: 40.7676,
    lng: -73.8272,
    nearbyStreet: 'Main Street',
  },
  {
    name: 'Jackson Heights',
    lat: 40.7464,
    lng: -73.892,
    nearbyStreet: 'Roosevelt Avenue',
  },
  {
    name: 'Long Island City',
    lat: 40.7435,
    lng: -73.9512,
    nearbyStreet: 'Jackson Avenue',
  },
  {
    name: 'Sunnyside',
    lat: 40.7431,
    lng: -73.924,
    nearbyStreet: 'Queens Boulevard',
  },
  {
    name: 'Forest Hills',
    lat: 40.713,
    lng: -73.8443,
    nearbyStreet: 'Austin Street',
  },
  {
    name: 'Bayside',
    lat: 40.7658,
    lng: -73.7691,
    nearbyStreet: 'Bell Boulevard',
  },
  {
    name: 'Riverdale',
    lat: 40.8952,
    lng: -73.9144,
    nearbyStreet: 'Riverdale Avenue',
  },
  { name: 'DUMBO', lat: 40.7033, lng: -73.9879, nearbyStreet: 'Water Street' },
  {
    name: 'City Island',
    lat: 40.8356,
    lng: -73.7755,
    nearbyStreet: 'City Island Avenue',
  },
  {
    name: 'Marine Park',
    lat: 40.6083,
    lng: -73.9174,
    nearbyStreet: 'Flatbush Avenue',
  },
  {
    name: 'Park Slope',
    lat: 40.6683,
    lng: -73.9804,
    nearbyStreet: '7th Avenue',
  },
  {
    name: 'Carroll Gardens',
    lat: 40.6834,
    lng: -73.9955,
    nearbyStreet: 'Court Street',
  },
  {
    name: 'Greenpoint',
    lat: 40.728,
    lng: -73.9515,
    nearbyStreet: 'Manhattan Avenue',
  },
  {
    name: 'Sheepshead Bay',
    lat: 40.5964,
    lng: -73.9412,
    nearbyStreet: 'Emmons Avenue',
  },
];
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
      marker: true
    }
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
    existingMarkers.push({ lng: neighborhood.lng, lat: neighborhood.lat });
    new mapboxgl.Marker(el)
      .setLngLat([neighborhood.lng, neighborhood.lat])
      .setPopup(popup)
      .addTo(map);
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
      if (isDuplicateMarker(coordinates.lng, coordinates.lat, existingMarkers)) {
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
