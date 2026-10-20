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

// Reveal on the displayed image's load event: no preloaded animation consuming frames.
function createNightsPlayback(art,motion){
  var still=art.getAttribute('src'), objectURL=null, generation=0;
  function release(){if(objectURL){URL.revokeObjectURL(objectURL);objectURL=null;}}
  function showStill(fade){
    var run=++generation;
    art.onload=null;
    art.classList.remove('is-fallback');
    function reveal(){
      if(run!==generation) return;
      if(fade && !motion.matches) art.classList.add('is-fallback');
      art.classList.add('is-ready');
      art.onload=null;
    }
    art.onload=reveal;art.src=still;release();
    if(motion.matches || (art.complete && art.naturalWidth)) reveal();
  }
  function play(){
    if(motion.matches){showStill(false);return;}
    var run=++generation;
    art.onload=null;art.classList.remove('is-ready','is-fallback');
    loadNightsAnimation(art.dataset.animation).then(function(blob){
      if(run!==generation || motion.matches) return;
      release();objectURL=URL.createObjectURL(blob);
      art.onload=function(){
        if(run!==generation || motion.matches) return;
        art.classList.add('is-ready');art.onload=null;
      };
      art.src=objectURL;
    }).catch(function(){if(run===generation) showStill(true);});
  }
  art.addEventListener('error',function(){if(art.getAttribute('src')!==still) showStill(true);});
  return {play:play,showStill:showStill};
}

// Original handwriting, with the existing arrival and scroll-back replay thresholds.
(function(){
  var art=document.querySelector('.hero .nights-script');
  if(!art) return;
  var motion=window.matchMedia('(prefers-reduced-motion: reduce)'), playback=createNightsPlayback(art,motion);
  var away=false, lastY=window.scrollY;
  function onScroll(){
    var y=window.scrollY, rect=art.parentElement.getBoundingClientRect();
    if(rect.bottom<=0) away=true;
    if(away && y<lastY && rect.bottom>rect.height*.35 && rect.top<window.innerHeight){
      away=false;playback.play();
    }
    lastY=y;
  }
  window.addEventListener('scroll',onScroll,{passive:true});
  motion.addEventListener('change',function(){if(motion.matches) playback.showStill(false);else playback.play();});
  window.addEventListener('pageshow',function(e){if(e.persisted) playback.play();});
  if(motion.matches) playback.showStill(false);
  else if(art.parentElement.getBoundingClientRect().bottom>0) playback.play();else away=true;
})();

// Reveal the decorative background only after YouTube confirms playback.
// Unavailable/blocked video leaves the original black hero behind the logo.
(function(){
  var frame=document.getElementById('hero-background');
  if(!frame) return;
  function disableCaptions(player){
    try{player.unloadModule('captions');}catch(error){}
    try{player.setOption('captions','track',{});}catch(error){}
  }
  function createPlayer(){
    new YT.Player(frame,{events:{
      onReady:function(e){disableCaptions(e.target);e.target.mute();e.target.playVideo();},
      onApiChange:function(e){if(e.target.getOptions().indexOf('captions')!==-1) disableCaptions(e.target);},
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

// Draw the existing footer lockup on the same viewport-entry threshold as before.
(function(){
  var art=document.querySelector('.closing-script');
  if(!art) return;
  var motion=window.matchMedia('(prefers-reduced-motion: reduce)'), playback=createNightsPlayback(art,motion), inView=false;
  if(!('IntersectionObserver' in window)){playback.showStill(false);return;}
  if(motion.matches) playback.showStill(false);
  var observer=new IntersectionObserver(function(entries){
    entries.forEach(function(entry){
      if(entry.isIntersecting && !inView) playback.play();
      inView=entry.isIntersecting;
    });
  },{threshold:.25});
  observer.observe(art);
  motion.addEventListener('change',function(){if(motion.matches) playback.showStill(false);else if(inView) playback.play();});
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
  var media=section.querySelector('.media'), image=media && media.querySelector('img'), frame=0, progress=null, imageHeight=0;
  if(!image) return;
  function measure(){
    if(!image.naturalWidth) return;
    var rect=section.getBoundingClientRect();
    imageHeight=Math.max(rect.height,rect.width*image.naturalHeight/image.naturalWidth);
    media.style.setProperty('--parallax-height',imageHeight+'px');
    media.style.setProperty('--parallax-width',(imageHeight*image.naturalWidth/image.naturalHeight)+'px');
    schedule();
  }
  function update(){
    frame=0;
    if(motion.matches || !imageHeight) return;
    var rect=section.getBoundingClientRect(), height=window.innerHeight;
    if(rect.bottom<0 || rect.top>height || !image.naturalWidth) return;
    // Match Squarespace's 30% intensity / 90-degree background effect.
    // Normalize to the available scroll range, including the nearby page end.
    var top=rect.top+window.scrollY, after=document.documentElement.scrollHeight-top-rect.height;
    var before=Math.min(top,height), end=Math.min(after,height);
    var range=before+rect.height+end-height;
    var target=Math.max(0,Math.min(1,range>0?(before-rect.top)/range:.5));
    var delta=progress===null?0:target-progress;
    progress=progress===null || Math.abs(delta)<.01?target:progress+delta*.1;
    var offset=(.5-progress)*imageHeight*.15/.85;
    media.style.setProperty('--parallax-y',offset.toFixed(2)+'px');
    if(Math.abs(target-progress)>=.01) frame=requestAnimationFrame(update);
  }
  function schedule(){if(!motion.matches && !frame) frame=requestAnimationFrame(update);}
  function configure(){
    section.classList.toggle('has-parallax',!motion.matches);
    if(motion.matches){cancelAnimationFrame(frame);frame=0;progress=null;media.style.removeProperty('--parallax-y');}
    else schedule();
  }
  window.addEventListener('scroll',schedule,{passive:true});
  window.addEventListener('resize',measure,{passive:true});
  window.addEventListener('pageshow',measure);
  image.addEventListener('load',measure);
  if('ResizeObserver' in window) new ResizeObserver(measure).observe(section);
  motion.addEventListener('change',configure);
  measure();configure();
})();
