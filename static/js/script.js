// Floating balloons & confetti
const canvas = document.getElementById('partyCanvas');
const balloons = ['🎈','🎊','🎉','⭐','✨','🌟','💫'];
const colors = ['#FF6B9D','#FF8C42','#FFD166','#06D6A0','#118AB2','#845EC2','#EF476F'];

for(let i=0;i<12;i++){
  const b = document.createElement('div');
  b.className='balloon';
  b.textContent = balloons[Math.floor(Math.random()*balloons.length)];
  b.style.left = Math.random()*100+'vw';
  b.style.animationDuration = (10+Math.random()*15)+'s';
  b.style.animationDelay = (Math.random()*10)+'s';
  b.style.fontSize = (1.5+Math.random()*2)+'rem';
  canvas.appendChild(b);
}
for(let i=0;i<25;i++){
  const c = document.createElement('div');
  c.className='confetti-piece';
  c.style.left = Math.random()*100+'vw';
  c.style.background = colors[Math.floor(Math.random()*colors.length)];
  c.style.animationDuration = (5+Math.random()*8)+'s';
  c.style.animationDelay = (Math.random()*8)+'s';
  c.style.width = (6+Math.random()*8)+'px';
  c.style.height = (6+Math.random()*8)+'px';
  c.style.borderRadius = Math.random()>.5?'50%':'2px';
  canvas.appendChild(c);
}

// Nav scroll
window.addEventListener('scroll',()=>{
  document.getElementById('nav').classList.toggle('scrolled',window.scrollY>60);
});

// Mobile menu
function toggleMenu(){document.getElementById('mobMenu').classList.toggle('open')}

// Services tabs
const tabColors = ['t0','t1','t2','t3','t4'];
function switchSvc(idx, btn){
  document.querySelectorAll('.svc-panel').forEach(p=>p.classList.remove('show'));
  document.querySelectorAll('.svc-tab').forEach((b,i)=>{
    b.classList.remove('on');
    tabColors.forEach(t=>b.classList.remove(t));
  });
  document.getElementById('sp'+idx).classList.add('show');
  btn.classList.add('on','t'+idx);
}

// Scroll reveal
const obs = new IntersectionObserver(entries=>{
  entries.forEach(e=>{if(e.isIntersecting)e.target.classList.add('in')});
},{threshold:.1});
document.querySelectorAll('.reveal').forEach(el=>obs.observe(el));

// Form submit
function submitForm(){
  const s=document.getElementById('fSuccess');
  s.style.display='block';
  // Launch confetti burst!
  for(let i=0;i<15;i++){
    const c=document.createElement('div');
    c.className='confetti-piece';
    c.style.cssText=`position:fixed;top:50%;left:${20+Math.random()*60}vw;background:${colors[Math.floor(Math.random()*colors.length)]};animation:confettiFall .8s ${Math.random()*.5}s ease forwards;width:${8+Math.random()*10}px;height:${8+Math.random()*10}px;border-radius:${Math.random()>.5?'50%':'2px'};z-index:9999`;
    document.body.appendChild(c);
    setTimeout(()=>c.remove(),2000);
  }
  setTimeout(()=>s.style.display='none',6000);
}

function closeBookingModal() {
    document.getElementById('bookingModalOverlay').classList.remove('show');
    const url = new URL(window.location);
    url.searchParams.delete('booked');
    window.history.replaceState({}, '', url);
  }

  document.addEventListener('DOMContentLoaded', function () {
    const params = new URLSearchParams(window.location.search);
    if (params.get('booked') === '1') {
      document.getElementById('bookingModalOverlay').classList.add('show');
    }

    document.getElementById('bookingModalOverlay').addEventListener('click', function (e) {
      if (e.target === this) closeBookingModal();
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeBookingModal();
    });
  });