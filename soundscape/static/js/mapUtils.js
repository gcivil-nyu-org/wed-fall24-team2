function toRadians(deg) {
  return deg * (Math.PI / 180);
}

// Haversine formula to calculate the distance between two points (in meters)
function getDistance(lat1, lng1, lat2, lng2) {
  const R = 6371000; // Earth's radius in meters
  const dLat = toRadians(lat2 - lat1);
  const dLng = toRadians(lng2 - lng1);
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(toRadians(lat1)) *
      Math.cos(toRadians(lat2)) *
      Math.sin(dLng / 2) *
      Math.sin(dLng / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c; // Distance in meters
}

function convertToGeoJSON(data) {
  return {
    type: 'FeatureCollection',
    features: data.map((item) => ({
      type: 'Feature',
      geometry: {
        type: 'Point',
        coordinates: [item.longitude, item.latitude],
      },
      properties:{
        weight: 1,
        complaint_type: item.complaint_type,
        descriptor: item.descriptor,
        status: item.status,
        created_date: item.created_date,
        closed_date: item.closed_date
      }
    })),
  };
}
