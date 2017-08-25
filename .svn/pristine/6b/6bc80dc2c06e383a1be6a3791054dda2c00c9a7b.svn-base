var placeSearch, autocomplete, map, lastRedMarker;
var geocoder = new google.maps.Geocoder();
var componentForm = {
  street_number: 'short_name',
  route: 'long_name',
  locality: 'long_name',
  administrative_area_level_1: 'long_name',
  country: 'long_name',
  postal_code: 'short_name'
};

var componentToId = {
  street_number: 'address',
  route: 'address',
  locality: 'city',
  administrative_area_level_1: 'province',
  country: 'country',
  name: 'name',
  units: 'units',
  price: 'price',
  description: 'description'
}

function initializeMap(showOnly) {
  var mapOptions = {
    center: {lat: 43.6610854, lng: -79.3950972},
    zoom: 14
  };
  map = new google.maps.Map(document.getElementById('mapCanvas'), mapOptions);

  if (!showOnly) {
    autocomplete = new google.maps.places.Autocomplete(document.getElementById('address'),
      { types: ['geocode'] }
    );
    google.maps.event.addListener(autocomplete, 'place_changed', fillInAddress);

    google.maps.event.addListener(map, 'click', function(event) {
      var marker;
      var address = "";
      try {
        geocoder.geocode({
          latLng: event.latLng
        }, function(responses) {
          if (responses && responses.length > 0) {
            var find = ['street_number', 'route', 'locality', 'country'];
            var parts = ["", "", "", ""];

            for (var i = 0; i < responses[0].address_components.length; i++) {
              for (var j = 0; j < find.length; j++) {
                if ($.inArray(find[j], responses[0].address_components[i].types) > -1) {
                  parts[j] = responses[0].address_components[i].short_name;
                }
              }
            }

            address = parts.join(" ");
            address = (address.length < 4) ? "" : address.replace("  ", " ");
          }
          marker = addMarker(event.latLng, true, address);
        });
      } catch (e) {
        marker = addMarker(event.latLng, true, address);
      }
    });
  }
}
function fillInAddress() {
  var place = autocomplete.getPlace();

  clearEntry(true);

  var find = ['street_number', 'route', 'locality', 'country'];
  var parts = ["", "", "", ""];

  for (var i = 0; i < place.address_components.length; i++) {
    var addressType = place.address_components[i].types[0];
    if (componentToId[addressType]) {
      var val = place.address_components[i][componentForm[addressType]];
      if (addressType == 'street_number' && document.getElementById("address").value) {
        document.getElementById("address").value = val + " " + document.getElementById("address").value;
      } else if (addressType == 'route' && document.getElementById("address").value) {
        document.getElementById("address").value += " " + val;
      } else {
        document.getElementById(componentToId[addressType]).value = val;
      }
    }

    for (var j = 0; j < find.length; j++) {
      if ($.inArray(find[j], place.address_components[i].types) > -1) {
        parts[j] = place.address_components[i].short_name;
      }
    }
  }

  var address = parts.join(" ");
  address = (address.length < 4) ? "" : address.replace("  ", " ");
  
  var pos = new google.maps.LatLng(place.geometry.location.lat(),place.geometry.location.lng());
  addMarker(pos, false, address);
}

function addMarker(pos, asking_marker, address) {
  if (lastRedMarker) {
    lastRedMarker.setMap(null);
    lastRedMarker = null;
  }

  var marker = new google.maps.Marker({
    position: pos,
    map: map,
    title: address
  });

  var markerContent = '<div id="content">' + 
      (address.length ? address + '<br/><br/>' : '') +
      (asking_marker ? '<a href="javascript:void(0)" onclick="addMarker({' +
        'lat: ' + pos.lat() +
        ',lng: ' + pos.lng() +
      '}, false, \'' + address.replace("'", "\\'") + '\')">Set to This Location?</a>' : '') +
    '</div>';

  if (asking_marker) {
    lastRedMarker = marker;
  } else {
    map.setCenter(pos);
    try {
      document.getElementById('lat').value = marker.position.lat();
      document.getElementById('lon').value = marker.position.lng();  
    } catch (e) {}
  }

  var infoWindow = new google.maps.InfoWindow({
      content: markerContent
  });
  infoWindow.open(map, marker);

  google.maps.event.addListener(marker, 'click', function() {
      infoWindow.open(map, marker);
  });

  return marker;
}

function clearEntry(skip_some) {
  skip_some = skip_some || false;
  var keys = Object.keys(componentToId);

  for (var i = 0; i < keys.length; i++) {
    if (!skip_some || (keys[i] != 'name' && keys[i] != 'description' && keys[i] != 'units' && keys[i] != 'price')){
      document.getElementById(componentToId[keys[i]]).value = '';
    }
  }
}

function findOnMap() {
  var input = [];
  var loc_id = ['address', 'city', 'province', 'country'];

  for (var i = 0; i < loc_id.length; i++) {
    var val = document.getElementById(loc_id[i]).value.trim();
    if (val) {
      input.push(val);
    }
  }
  input = input.join(" ");

  console.log(input);
  if (input.length > 3) {
    geocoder.geocode({
      address: input
    }, function(responses) {
      if (responses && responses.length > 0) {
        var find = ['street_number', 'route', 'locality', 'country'];
        var parts = ["", "", "", ""];

        for (var i = 0; i < responses[0].address_components.length; i++) {
          for (var j = 0; j < find.length; j++) {
            if ($.inArray(find[j], responses[0].address_components[i].types) > -1) {
              parts[j] = responses[0].address_components[i].short_name;
            }
          }
        }

        var address = parts.join(" ");
        address = (address.length < 4) ? "" : address.replace("  ", " ");
      }

      var pos = new google.maps.LatLng(responses[0].geometry.location.lat(),responses[0].geometry.location.lng());
      addMarker(pos, true, address);
    });   
  } else {
    alert("Could not find on map. Please place a marker on the map and confirm.");
  }
}