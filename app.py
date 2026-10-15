import streamlit as st
import streamlit.components.v1 as components

# Configure the Streamlit page
st.set_page_config(
    page_title="The Meow Button",
    page_icon="🐱",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Hide Streamlit's default top header, footer, and extra padding for a clean full-screen look
st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
            max-width: 100%;
        }
        body, .stApp {
            background-color: #FFFBF7;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# Self-contained HTML/CSS/JS with Web Audio API Cat Synthesizer
meow_app_html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@600;700&family=Plus+Jakarta+Sans:wght@600;700&display=swap" rel="stylesheet">
<style>
  * {
    box-sizing: border-box;
    user-select: none;
    -webkit-user-select: none;
    margin: 0;
    padding: 0;
  }
  body {
    background: radial-gradient(circle at 50% 45%, #FFFDFB 0%, #F7EFE6 100%);
    font-family: 'Plus Jakarta Sans', sans-serif;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    height: 92vh;
    overflow: hidden;
    padding: 20px;
    border-radius: 24px;
  }

  /* Counter Pill */
  .counter-pill {
    background: #FFFFFF;
    padding: 10px 22px;
    border-radius: 999px;
    box-shadow: 0 8px 24px -4px rgba(74, 53, 49, 0.08);
    border: 2px solid #F3E5D8;
    font-weight: 700;
    color: #4A3531;
    font-size: 1rem;
    display: flex;
    align-items: center;
    gap: 8px;
    z-index: 10;
    transition: transform 0.15s cubic-bezier(0.34, 1.56, 0.64, 1);
  }
  .counter-pill.bump {
    transform: scale(1.12);
  }
  .counter-num {
    font-family: 'Fredoka', sans-serif;
    color: #FF7E67;
    font-size: 1.25rem;
    font-variant-numeric: tabular-nums;
  }

  /* Main Button Stage */
  .stage {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    flex: 1;
    width: 100%;
  }

  .meow-btn {
    position: relative;
    width: 240px;
    height: 240px;
    border-radius: 50%;
    background: linear-gradient(180deg, #FF947E 0%, #FF7E67 100%);
    border: 6px solid #FFFFFF;
    box-shadow: 
      0 14px 0 #D95943,
      0 24px 40px rgba(74, 53, 49, 0.18),
      inset 0 4px 8px rgba(255, 255, 255, 0.5);
    cursor: pointer;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    transition: transform 0.12s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.12s ease;
    outline: none;
    z-index: 5;
    -webkit-tap-highlight-color: transparent;
  }

  .meow-btn:hover {
    transform: translateY(-4px) scale(1.02);
    box-shadow: 
      0 18px 0 #D95943,
      0 28px 45px rgba(74, 53, 49, 0.22),
      inset 0 4px 8px rgba(255, 255, 255, 0.6);
  }

  .meow-btn:active, .meow-btn.pressed {
    transform: translateY(10px) scale(0.96);
    box-shadow: 
      0 4px 0 #D95943,
      0 10px 20px rgba(74, 53, 49, 0.15),
      inset 0 2px 4px rgba(255, 255, 255, 0.4);
  }

  .cat-svg {
    width: 135px;
    height: 120px;
    overflow: visible;
  }

  .btn-label {
    font-family: 'Fredoka', sans-serif;
    font-size: 1.7rem;
    font-weight: 700;
    color: #FFFFFF;
    letter-spacing: 0.04em;
    margin-top: 6px;
    text-shadow: 0 2px 0 #D95943;
  }

  /* Cat Face States */
  .eyes-closed, .mouth-open { display: none; }
  .meow-btn:active .eyes-open, .meow-btn.pressed .eyes-open { display: none; }
  .meow-btn:active .eyes-closed, .meow-btn.pressed .eyes-closed { display: block; }
  .meow-btn:active .mouth-closed, .meow-btn.pressed .mouth-closed { display: none; }
  .meow-btn:active .mouth-open, .meow-btn.pressed .mouth-open { display: block; }

  /* Floating Particles & Shockwave */
  .particle {
    position: absolute;
    font-family: 'Fredoka', sans-serif;
    font-weight: 700;
    font-size: 1.4rem;
    color: #FF7E67;
    pointer-events: none;
    text-shadow: 0 2px 8px rgba(255, 255, 255, 0.9);
    animation: floatUp 0.85s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    z-index: 20;
  }

  @keyframes floatUp {
    0% { opacity: 1; transform: translate(0, 0) scale(0.6) rotate(0deg); }
    100% { opacity: 0; transform: translate(var(--dx), var(--dy)) scale(1.25) rotate(var(--rot)); }
  }

  .ripple {
    position: absolute;
    width: 240px;
    height: 240px;
    border-radius: 50%;
    border: 4px solid #FFB085;
    pointer-events: none;
    animation: expandRipple 0.6s ease-out forwards;
    z-index: 1;
  }

  @keyframes expandRipple {
    0% { transform: scale(1); opacity: 0.7; }
    100% { transform: scale(1.65); opacity: 0; }
  }

  /* Mood Selector Dock */
  .mood-dock {
    background: #FFFFFF;
    padding: 6px;
    border-radius: 999px;
    display: flex;
    gap: 6px;
    box-shadow: 0 8px 24px -4px rgba(74, 53, 49, 0.08);
    border: 2px solid #F3E5D8;
    z-index: 10;
  }

  .mood-btn {
    border: none;
    background: transparent;
    padding: 8px 14px;
    border-radius: 999px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 700;
    font-size: 0.85rem;
    color: #9C827A;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .mood-btn.active {
    background: #FFF0EB;
    color: #FF7E67;
  }
</style>
</head>
<body>

  <!-- Top Counter -->
  <div class="counter-pill" id="counterPill">
    <span>🐾 Meows:</span>
    <span class="counter-num" id="meowCount">0</span>
  </div>

  <!-- Center Button Stage -->
  <div class="stage" id="stage">
    <button class="meow-btn" id="meowBtn" aria-label="Meow Button">
      <svg class="cat-svg" viewBox="0 0 140 120">
        <!-- Left & Right Ears -->
        <path d="M22 65 L12 16 C11 10 17 7 22 11 L55 38 Z" fill="#FFFDFB" stroke="#4A3531" stroke-width="5" stroke-linejoin="round"/>
        <path d="M24 52 L19 23 L43 41 Z" fill="#FFB5A7"/>
        <path d="M118 65 L128 16 C129 10 123 7 118 11 L85 38 Z" fill="#FFFDFB" stroke="#4A3531" stroke-width="5" stroke-linejoin="round"/>
        <path d="M116 52 L121 23 L97 41 Z" fill="#FFB5A7"/>

        <!-- Head Base -->
        <ellipse cx="70" cy="68" rx="54" ry="44" fill="#FFFDFB" stroke="#4A3531" stroke-width="5"/>

        <!-- Cheeks -->
        <ellipse cx="34" cy="76" rx="9" ry="5.5" fill="#FFB5A7" opacity="0.8"/>
        <ellipse cx="106" cy="76" rx="9" ry="5.5" fill="#FFB5A7" opacity="0.8"/>

        <!-- Eyes Open -->
        <g class="eyes-open">
          <circle cx="46" cy="63" r="6.5" fill="#4A3531"/>
          <circle cx="44" cy="60.5" r="2.2" fill="#FFFFFF"/>
          <circle cx="94" cy="63" r="6.5" fill="#4A3531"/>
          <circle cx="92" cy="60.5" r="2.2" fill="#FFFFFF"/>
        </g>

        <!-- Eyes Squinting (> <) -->
        <g class="eyes-closed" stroke="#4A3531" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round" fill="none">
          <path d="M39 58 L49 64 L39 70"/>
          <path d="M101 58 L91 64 L101 70"/>
        </g>

        <!-- Pink Nose -->
        <polygon points="65,69 75,69 70,75" fill="#FF7E67" stroke="#4A3531" stroke-width="3" stroke-linejoin="round"/>

        <!-- Mouth Closed (:3) -->
        <g class="mouth-closed" stroke="#4A3531" stroke-width="4" stroke-linecap="round" fill="none">
          <path d="M70 75 C70 83, 57 83, 57 77"/>
          <path d="M70 75 C70 83, 83 83, 83 77"/>
        </g>

        <!-- Mouth Open (Meowing) -->
        <g class="mouth-open">
          <path d="M58 76 C58 96, 82 96, 82 76 Z" fill="#D95943" stroke="#4A3531" stroke-width="4" stroke-linejoin="round"/>
          <path d="M63 85 C63 92, 77 92, 77 85 Z" fill="#FF9E9E"/>
        </g>

        <!-- Whiskers -->
        <g stroke="#4A3531" stroke-width="3.5" stroke-linecap="round">
          <line x1="18" y1="68" x2="6" y2="65"/>
          <line x1="18" y1="76" x2="5" y2="78"/>
          <line x1="122" y1="68" x2="134" y2="65"/>
          <line x1="122" y1="76" x2="135" y2="78"/>
        </g>
      </svg>
      <span class="btn-label">MEOW</span>
    </button>
  </div>

  <!-- Bottom Mood Selector -->
  <div class="mood-dock">
    <button class="mood-btn active" data-mood="random">🎲 Surprise</button>
    <button class="mood-btn" data-mood="kitten">🍼 Kitten</button>
    <button class="mood-btn" data-mood="classic">🐱 Classic</button>
    <button class="mood-btn" data-mood="chonker">🍔 Chonker</button>
  </div>

<script>
  let audioCtx = null;
  let count = 0;
  let currentMood = 'random';

  const meowBtn = document.getElementById('meowBtn');
  const stage = document.getElementById('stage');
  const meowCountEl = document.getElementById('meowCount');
  const counterPill = document.getElementById('counterPill');
  const moodBtns = document.querySelectorAll('.mood-btn');

  // Mood Switcher
  moodBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      moodBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentMood = btn.dataset.mood;
    });
  });

  // Web Audio API Cat Meow Synthesizer
  function playMeowSound(mood) {
    if (!audioCtx) {
      audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
    if (audioCtx.state === 'suspended') {
      audioCtx.resume();
    }

    const now = audioCtx.currentTime;
    const chosenMood = mood === 'random' 
      ? ['kitten', 'classic', 'chonker'][Math.floor(Math.random() * 3)] 
      : mood;

    let baseFreq, peakFreq, endFreq, duration;
    const jitter = 0.94 + Math.random() * 0.12;

    if (chosenMood === 'kitten') {
      baseFreq = 580 * jitter;
      peakFreq = 860 * jitter;
      endFreq  = 460 * jitter;
      duration = 0.42;
    } else if (chosenMood === 'chonker') {
      baseFreq = 240 * jitter;
      peakFreq = 350 * jitter;
      endFreq  = 175 * jitter;
      duration = 0.72;
    } else {
      baseFreq = 380 * jitter;
      peakFreq = 570 * jitter;
      endFreq  = 290 * jitter;
      duration = 0.55;
    }

    // Primary vocal cord oscillator
    const osc = audioCtx.createOscillator();
    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(baseFreq, now);
    osc.frequency.exponentialRampToValueAtTime(peakFreq, now + duration * 0.28);
    osc.frequency.exponentialRampToValueAtTime(endFreq, now + duration);

    // Subtle throat vibrato
    const vibrato = audioCtx.createOscillator();
    const vibratoGain = audioCtx.createGain();
    vibrato.frequency.value = 6.5;
    vibratoGain.gain.value = 8;
    vibrato.connect(vibratoGain);
    vibratoGain.connect(osc.frequency);

    // Vowel Formant Filter ("M-E-O-W" mouth opening & closing)
    const filter = audioCtx.createBiquadFilter();
    filter.type = 'bandpass';
    filter.Q.value = 3.2;
    filter.frequency.setValueAtTime(baseFreq * 1.5, now);
    filter.frequency.exponentialRampToValueAtTime(peakFreq * 2.6, now + duration * 0.32);
    filter.frequency.exponentialRampToValueAtTime(endFreq * 1.4, now + duration);

    // Volume Envelope
    const gain = audioCtx.createGain();
    gain.gain.setValueAtTime(0.001, now);
    gain.gain.linearRampToValueAtTime(0.45, now + 0.05);
    gain.gain.exponentialRampToValueAtTime(0.001, now + duration);

    osc.connect(filter);
    filter.connect(gain);
    gain.connect(audioCtx.destination);

    osc.start(now);
    vibrato.start(now);
    osc.stop(now + duration);
    vibrato.stop(now + duration);
  }

  function spawnEffects() {
    // Ripple ring
    const ripple = document.createElement('div');
    ripple.className = 'ripple';
    stage.appendChild(ripple);
    setTimeout(() => ripple.remove(), 600);

    // Floating Meow Text
    const words = ['Meow!', 'Mrrp~', 'Purr!', 'Nya~', 'Mew!', 'Meowww!'];
    const particle = document.createElement('div');
    particle.className = 'particle';
    particle.textContent = words[Math.floor(Math.random() * words.length)];

    const angle = (Math.random() * 120 - 60) * (Math.PI / 180);
    const distance = 135 + Math.random() * 50;
    const dx = Math.sin(angle) * distance + 'px';
    const dy = -Math.cos(angle) * distance - 40 + 'px';
    const rot = (Math.random() * 36 - 18) + 'deg';

    particle.style.setProperty('--dx', dx);
    particle.style.setProperty('--dy', dy);
    particle.style.setProperty('--rot', rot);

    stage.appendChild(particle);
    setTimeout(() => particle.remove(), 850);
  }

  function triggerMeow() {
    playMeowSound(currentMood);
    spawnEffects();

    count++;
    meowCountEl.textContent = count;
    counterPill.classList.remove('bump');
    void counterPill.offsetWidth; // trigger reflow
    counterPill.classList.add('bump');
  }

  meowBtn.addEventListener('pointerdown', () => {
    meowBtn.classList.add('pressed');
    triggerMeow();
  });

  window.addEventListener('pointerup', () => {
    meowBtn.classList.remove('pressed');
  });

  // Spacebar / Enter support
  window.addEventListener('keydown', (e) => {
    if ((e.code === 'Space' || e.code === 'Enter') && !e.repeat) {
      e.preventDefault();
      meowBtn.classList.add('pressed');
      triggerMeow();
    }
  });
  window.addEventListener('keyup', (e) => {
    if (e.code === 'Space' || e.code === 'Enter') {
      meowBtn.classList.remove('pressed');
    }
  });
</script>
</body>
</html>
"""

# Render the component inside Streamlit
components.html(meow_app_html, height=680, scrolling=False)
