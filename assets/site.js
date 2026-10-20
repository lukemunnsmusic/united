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
// If FORM_ENDPOINT is ever emptied, forms validate, show a preview notice and send nothing.
var FORM_ENDPOINT='https://hub.lukemunnsmusic.com/api/united/website-form';
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


// Share one animation download between the opening and closing marks.
var nightsAnimationRequest=null;
function loadNightsAnimation(url){
  if(!nightsAnimationRequest) nightsAnimationRequest=fetch(url).then(function(r){
    if(!r.ok) throw new Error('Animation unavailable');
    return r.blob();
  }).catch(function(error){nightsAnimationRequest=null;throw error;});
  return nightsAnimationRequest;
}

// Original transparent handwriting frames, encoded once as WebP (no traced paths).
// One image means one NIGHTS layer, including reduced motion and failed loads.
(function(){
  var art=document.querySelector('.hero .nights-script');
  if(!art) return;
  var still=art.getAttribute('src'), motion=window.matchMedia('(prefers-reduced-motion: reduce)');
  var blob=null, pending=null, objectURL=null, away=false, lastY=window.scrollY, generation=0;
  function release(){
    if(objectURL){URL.revokeObjectURL(objectURL);objectURL=null;}
  }
  function showStill(){
    generation++;
    art.src=still;
    release();
  }
  function replay(){
    if(motion.matches) return;
    var run=++generation;
    // Cache bytes, but use a fresh URL to restart the single-play image reliably.
    if(!pending) pending=loadNightsAnimation(art.dataset.animation)
      .then(function(value){blob=value;return value;}).catch(function(){pending=null;return null;});
    pending.then(function(value){
      if(!value || run!==generation || motion.matches) return;
      release();
      objectURL=URL.createObjectURL(blob);
      art.src=objectURL;
    });
  }
  art.addEventListener('error',function(){if(art.getAttribute('src')!==still) showStill();});
  function onScroll(){
    var y=window.scrollY, rect=art.parentElement.getBoundingClientRect();
    if(rect.bottom<=0) away=true;
    if(away && y<lastY && rect.bottom>rect.height*.35 && rect.top<window.innerHeight){
      away=false;
      replay();
    }
    lastY=y;
  }
  window.addEventListener('scroll',onScroll,{passive:true});
  motion.addEventListener('change',function(){if(motion.matches) showStill();else replay();});
  window.addEventListener('pageshow',function(e){if(e.persisted) replay();});
  if(art.parentElement.getBoundingClientRect().bottom>0) replay();else away=true;
})();

// Reveal the decorative background only after YouTube confirms playback.
// Unavailable/blocked video leaves the original black hero behind the logo.
(function(){
  var frame=document.getElementById('hero-background');
  if(!frame) return;
  function createPlayer(){
    new YT.Player(frame,{events:{
      onReady:function(e){e.target.mute();e.target.playVideo();},
      onStateChange:function(e){frame.classList.toggle('is-playing',e.data===1);},
      onError:function(){frame.classList.remove('is-playing');}
    }});
  }
  if(window.YT && window.YT.Player) createPlayer();
  else{
    window.onYouTubeIframeAPIReady=createPlayer;
    var script=document.createElement('script');
    script.src='https://www.youtube.com/iframe_api';
    script.async=true;
    document.head.appendChild(script);
  }
})();

// Draw the NIGHTS part of the existing footer lockup when it enters view.
(function(){
  var art=document.querySelector('.closing-script');
  if(!art || !('IntersectionObserver' in window)) return;
  var still=art.getAttribute('src'), motion=window.matchMedia('(prefers-reduced-motion: reduce)');
  var objectURL=null, generation=0, inView=false;
  function release(){if(objectURL){URL.revokeObjectURL(objectURL);objectURL=null;}}
  function showStill(){generation++;art.src=still;art.classList.remove('is-waiting');release();}
  function play(){
    if(motion.matches) return;
    var run=++generation;
    loadNightsAnimation(art.dataset.animation).then(function(blob){
      if(run!==generation || motion.matches) return;
      release();objectURL=URL.createObjectURL(blob);art.src=objectURL;
      art.classList.remove('is-waiting');
    }).catch(function(){if(run===generation) showStill();});
  }
  art.addEventListener('error',function(){if(art.getAttribute('src')!==still) showStill();});
  if(!motion.matches) art.classList.add('is-waiting');
  var observer=new IntersectionObserver(function(entries){
    entries.forEach(function(entry){
      if(entry.isIntersecting && !inView) play();
      inView=entry.isIntersecting;
    });
  },{threshold:.25});
  observer.observe(art);
  motion.addEventListener('change',function(){if(motion.matches) showStill();else if(inView) play();});
})();

// Progressive enhancement: content remains visible with no JS or reduced motion.
(function(){
  var motion=window.matchMedia('(prefers-reduced-motion: reduce)');
  if(motion.matches || !('IntersectionObserver' in window)) return;
  var targets=document.querySelectorAll('.intro h2,.intro p,.join .c-wide>p,.post h1,.post h2,.post h3,.post h4,.post p,.story h1,.story p,.legal h4,.legal p');
  var observer=new IntersectionObserver(function(entries){
    entries.forEach(function(entry){
      if(!entry.isIntersecting) return;
      entry.target.classList.remove('is-pending','divider-pending');
      observer.unobserve(entry.target);
    });
  },{threshold:.1,rootMargin:'0px 0px -20px 0px'});
  targets.forEach(function(el){
    // Leave content already in view alone; reveal only incoming text.
    if(el.getBoundingClientRect().top<window.innerHeight) return;
    el.classList.add('scroll-reveal','is-pending');observer.observe(el);
  });
  document.querySelectorAll('.fine-divider').forEach(function(el){
    if(el.getBoundingClientRect().top<window.innerHeight) return;
    el.classList.add('divider-pending');observer.observe(el);
  });
  motion.addEventListener('change',function(){
    if(!motion.matches) return;
    observer.disconnect();
    document.querySelectorAll('.is-pending,.divider-pending').forEach(function(el){el.classList.remove('is-pending','divider-pending');});
  });
})();

// The opening cue retires as soon as the visitor starts scrolling.
(function(){
  var cue=document.querySelector('.scroll-cue');
  if(!cue) return;
  function retire(){
    if(window.scrollY<=8) return;
    cue.classList.add('is-gone');cue.setAttribute('aria-hidden','true');cue.tabIndex=-1;
    window.removeEventListener('scroll',retire);
  }
  window.addEventListener('scroll',retire,{passive:true});retire();
})();

// Lightweight background-only parallax, with static no-JS/reduced-motion fallbacks.
(function(){
  var section=document.querySelector('.join'), motion=window.matchMedia('(prefers-reduced-motion: reduce)');
  if(!section) return;
  var media=section.querySelector('.media'), frame=0;
  if(!media) return;
  function update(){
    frame=0;
    if(motion.matches) return;
    var rect=section.getBoundingClientRect(), height=window.innerHeight;
    if(rect.bottom<0 || rect.top>height) return;
    var space=parseFloat(getComputedStyle(section).getPropertyValue('--parallax-space'))||0;
    var offset=Math.max(-space,Math.min(space,(height/2-rect.top-rect.height/2)*.12));
    media.style.setProperty('--parallax-y',offset.toFixed(2)+'px');
  }
  function schedule(){if(!motion.matches && !frame) frame=requestAnimationFrame(update);}
  function configure(){
    section.classList.toggle('has-parallax',!motion.matches);
    if(motion.matches){cancelAnimationFrame(frame);frame=0;media.style.removeProperty('--parallax-y');}
    else schedule();
  }
  window.addEventListener('scroll',schedule,{passive:true});
  window.addEventListener('resize',schedule,{passive:true});
  window.addEventListener('pageshow',schedule);
  motion.addEventListener('change',configure);
  configure();
})();
