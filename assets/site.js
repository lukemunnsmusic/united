// UNITED Nights site behaviour, matching the Squarespace site:
// fixed transparent header that hides on scroll down and returns solid on scroll up,
// full-screen mobile menu, and forms.

// Header "scroll back"
(function(){
  var h=document.querySelector('.site-head'); if(!h) return;
  var last=window.scrollY;
  function onScroll(){
    var y=window.scrollY;
    if(y<=10){h.classList.remove('hidden','solid');}
    else if(y>last && y>h.offsetHeight){h.classList.add('hidden');h.classList.add('solid');}
    else if(y<last){h.classList.remove('hidden');h.classList.add('solid');}
    last=y;
  }
  window.addEventListener('scroll',onScroll,{passive:true}); onScroll();
})();

// Mobile menu
(function(){
  var b=document.querySelector('.burger'); if(!b) return;
  b.addEventListener('click',function(){
    var open=document.body.classList.toggle('menu-open');
    b.setAttribute('aria-expanded',open?'true':'false');
    document.documentElement.style.overflow=open?'hidden':'';
  });
})();

// Forms post to the Hub (lmm-hub /api/united/website-form): each submission becomes a UNITED
// contact in the Hub, mirrors to the UNITED Google Sheet and emails hello@unitednights.com.
// FORM_ENDPOINT stays empty until lmm-hub PR #106 is merged and live; until then forms
// validate, show a preview notice and send nothing. Then set it to:
// https://hub.lukemunnsmusic.com/api/united/website-form
var FORM_ENDPOINT='';
document.querySelectorAll('form.sq').forEach(function(f){
  f.addEventListener('submit',function(ev){
    ev.preventDefault();
    var note=f.querySelector('.form-note');
    if(f.querySelector('.hp input').value) return; // spam trap
    if(!f.checkValidity()){f.reportValidity();return;}
    var data=Object.fromEntries(new FormData(f).entries());
    delete data.website;
    data.form=f.dataset.form; data.page=location.pathname; data.sent_at=new Date().toISOString();
    if(!FORM_ENDPOINT){note.textContent='Preview only: this form is not connected yet, so nothing was sent.';return;}
    var btn=f.querySelector('button'); btn.disabled=true;
    fetch(FORM_ENDPOINT,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)})
      .then(function(r){return r.json().catch(function(){return {};}).then(function(j){if(!r.ok){var e=new Error(j.error||'');e.server=true;throw e;}});})
      .then(function(){f.reset(); f.hidden=true; var done=f.nextElementSibling; if(done) done.hidden=false;})
      .catch(function(err){note.textContent=(err&&err.server&&err.message)||'Something went wrong. Please email hello@unitednights.com.';})
      .finally(function(){btn.disabled=false;});
  });
});
