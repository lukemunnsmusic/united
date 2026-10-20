// UNITED Nights site behaviour: mobile menu, reveal on scroll, forms.
document.documentElement.classList.add('js');

// Mobile menu
(function(){
  var b=document.querySelector('.burger'), m=document.querySelector('.menu');
  if(!b||!m) return;
  b.addEventListener('click',function(){
    var open=m.classList.toggle('open');
    b.setAttribute('aria-expanded',open?'true':'false');
  });
})();

// Reveal on scroll
(function(){
  var els=document.querySelectorAll('.rv');
  if(!('IntersectionObserver' in window)){els.forEach(function(e){e.classList.add('in')});return;}
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}})},{rootMargin:'0px 0px -8% 0px'});
  els.forEach(function(e){io.observe(e)});
})();

// Forms. FORM_ENDPOINT is empty until Luke decides where submissions go
// (Hub leads or email). Until then the form is validated and shows a notice,
// and nothing is sent anywhere.
var FORM_ENDPOINT = '';
document.querySelectorAll('form.lead').forEach(function(f){
  f.addEventListener('submit',function(ev){
    ev.preventDefault();
    var note=f.querySelector('.form-note');
    if(f.querySelector('.hp input').value){return;} // spam trap
    if(!f.checkValidity()){f.reportValidity();return;}
    var data=Object.fromEntries(new FormData(f).entries());
    delete data.website;
    data.form=f.dataset.form; data.page=location.pathname; data.sent_at=new Date().toISOString();
    if(!FORM_ENDPOINT){
      note.className='form-note';
      note.textContent='Preview only: this form is not connected yet, so nothing was sent.';
      return;
    }
    var btn=f.querySelector('button'); btn.disabled=true;
    fetch(FORM_ENDPOINT,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)})
      .then(function(r){if(!r.ok) throw new Error(r.status);
        f.reset(); note.className='form-note ok'; note.textContent=f.dataset.thanks;})
      .catch(function(){note.className='form-note'; note.textContent='Something went wrong. Please email hello@unitednights.com.';})
      .finally(function(){btn.disabled=false;});
  });
});
