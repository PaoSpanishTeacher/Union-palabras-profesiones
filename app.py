import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Rompecabezas Profesiones", layout="wide")

st.markdown("""
    <style>
    .block-container { padding: 0rem; }
    iframe { border: none; }
    </style>
    """, unsafe_allow_html=True)

html_profesiones_premium = r"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600&family=Quicksand:wght@500;700&family=Dancing+Script:wght@700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #4cc9f0;
            --secondary: #4895ef;
            --accent: #f72585;
            --success: #4caf50;
            --error: #f44336;
            --bg-school: #fdf0d5;
            --text-main: #3a0ca3;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }

        body {
            font-family: 'Quicksand', sans-serif;
            min-height: 100vh;
            background-color: var(--bg-school);
            background-image: radial-gradient(#00b4d822 2px, transparent 2px), linear-gradient(180deg, #caf0f8 0%, #fdf0d5 100%);
            display: flex; flex-direction: column; align-items: center;
            padding-top: 50px;
        }

        header { text-align: center; padding-bottom: 20px; width: 100%; }
        h1 { font-family: 'Fredoka', sans-serif; font-size: 2.8rem; color: var(--text-main); text-shadow: 2px 2px 0px white; }
        .brand-name { font-family: 'Dancing Script', cursive; font-size: 1.6rem; color: var(--accent); }

        .main-layout {
            display: grid;
            grid-template-columns: 280px 1fr;
            gap: 30px;
            width: 95%;
            max-width: 1200px;
            margin-top: 20px;
        }

        /* LISTA DE GUÍA */
        .reference-sidebar {
            background: white;
            padding: 25px;
            border-radius: 25px;
            border: 4px solid var(--primary);
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
            height: fit-content;
        }
        .reference-sidebar h3 { font-family: 'Fredoka', sans-serif; color: var(--secondary); margin-bottom: 20px; text-align: center; }
        .ref-item {
            padding: 12px 18px;
            margin-bottom: 12px;
            background: #f8f9ff;
            border-radius: 15px;
            font-weight: 700;
            color: var(--text-main);
            display: flex; justify-content: space-between; align-items: center;
            border: 2px solid transparent;
            transition: all 0.3s;
        }
        .ref-item.done {
            background: #e8f5e9;
            color: #2e7d32;
            border-color: #c8e6c9;
            text-decoration: line-through;
            opacity: 0.7;
        }

        /* ÁREA DE JUEGO */
        .game-zone { display: flex; flex-direction: column; gap: 25px; }

        .progress-bar-wrap {
            width: 100%; background: white; height: 25px;
            border-radius: 20px; border: 3px solid var(--secondary);
            overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }
        #progress-fill {
            height: 100%; width: 0%; background: linear-gradient(90deg, #4cc9f0, #f72585);
            transition: width 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }

        .drop-area {
            background: white; border: 4px dashed var(--text-main);
            border-radius: 25px; padding: 40px; min-height: 160px;
            display: flex; justify-content: center; align-items: center;
            gap: 15px; position: relative;
            box-shadow: inset 0 5px 15px rgba(0,0,0,0.05);
        }
        .drop-area::before { content: "¡Sueltas las sílabas aquí!"; color: #bbb; font-style: italic; font-size: 1.2rem; }
        .drop-area.has-content::before { display: none; }

        .pool-area {
            background: rgba(255, 255, 255, 0.4); border: 3px solid var(--secondary);
            border-radius: 25px; padding: 25px; display: flex; flex-wrap: wrap;
            justify-content: center; gap: 15px; min-height: 250px;
            backdrop-filter: blur(5px);
        }

        .syllable {
            background: white; border: 3px solid var(--secondary);
            border-radius: 15px; padding: 15px 25px;
            font-family: 'Fredoka', sans-serif; font-size: 1.4rem;
            color: var(--text-main); cursor: grab;
            box-shadow: 0 6px 0px var(--secondary);
            text-transform: uppercase;
        }
        .syllable:active { cursor: grabbing; transform: translateY(3px); box-shadow: 0 2px 0px var(--secondary); }
        .syllable.dragging { opacity: 0.3; }
        .syllable.is-correct { background: var(--success); color: white; border-color: #2e7d32; box-shadow: 0 4px 0px #2e7d32; }

        /* ALERTAS Y EFECTOS */
        #alert-box {
            position: fixed; top: 15%; left: 50%; transform: translateX(-50%) scale(0);
            padding: 15px 40px; border-radius: 50px; color: white; font-weight: bold;
            font-size: 1.5rem; z-index: 200; transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        #alert-box.show { transform: translateX(-50%) scale(1); }
        .bg-win { background: var(--success); }
        .bg-fail { background: var(--error); }

        .balloon { position: absolute; bottom: -100px; animation: floatUp 6s linear forwards; font-size: 3rem; z-index: 1001; }
        @keyframes floatUp { to { transform: translateY(-120vh) rotate(20deg); } }

        #win-modal {
            position: fixed; inset: 0; background: rgba(255, 255, 255, 0.98);
            display: none; flex-direction: column; justify-content: center;
            align-items: center; z-index: 1000; text-align: center;
        }
        #win-modal.active { display: flex; }

        .btn-play {
            background: var(--accent); color: white; border: none;
            padding: 20px 50px; font-size: 1.8rem; border-radius: 60px;
            cursor: pointer; margin-top: 30px; box-shadow: 0 8px 0px #a3165b;
            font-family: 'Fredoka', sans-serif; transition: 0.1s;
        }
        .btn-play:active { transform: translateY(4px); box-shadow: 0 4px 0px #a3165b; }
    </style>
</head>
<body>

    <header>
        <h1>Rompecabezas - Profesiones</h1>
        <div class="brand-name">PaoSpanishTeacher</div>
    </header>

    <div class="main-layout">
        <div class="reference-sidebar">
            <h3>Lista de Guía</h3>
            <div id="guide-container"></div>
        </div>

        <div class="game-zone">
            <div class="progress-bar-wrap">
                <div id="progress-fill"></div>
            </div>

            <div class="drop-area" id="drop-zone"></div>
            <div class="pool-area" id="pieces-pool"></div>
        </div>
    </div>

    <div id="alert-box"></div>

    <div id="win-modal">
        <span style="font-size: 8rem;">👨‍🏫</span>
        <h1>¡Increíble! ¡Eres un experto!</h1>
        <p style="font-size: 1.5rem; color: var(--secondary);">Has completado todas las profesiones.</p>
        <button class="btn-play" onclick="resetGame()">Jugar de nuevo</button>
    </div>

    <script>
        const PROFESSIONS = [
            { id: "doctor", parts: ["DOC", "TOR"] },
            { id: "profesora", parts: ["PRO", "FE", "SORA"] },
            { id: "ingeniero", parts: ["IN", "GE", "NIE", "RO"] },
            { id: "policía", parts: ["PO", "LI", "CÍ", "A"] },
            { id: "bombero", parts: ["BOM", "BE", "RO"] },
            { id: "enfermera", parts: ["EN", "FER", "ME", "RA"] },
            { id: "abogado", parts: ["ABO", "GA", "DO"] },
            { id: "piloto", parts: ["PI", "LO", "TO"] },
            { id: "músico", parts: ["MÚ", "SI", "CO"] },
            { id: "arquitecta", parts: ["AR", "QUI", "TEC", "TA"] }
        ];

        let score = 0;
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

        function playSound(f, d) {
            const osc = audioCtx.createOscillator();
            const g = audioCtx.createGain();
            osc.frequency.value = f;
            g.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + d);
            osc.connect(g); g.connect(audioCtx.destination);
            osc.start(); osc.stop(audioCtx.currentTime + d);
        }

        function spawnBalloons() {
            for(let i=0; i<10; i++){
                setTimeout(() => {
                    const b = document.createElement('div');
                    b.className = 'balloon';
                    b.innerHTML = ['🎈', '✨', '🏆', '🎓'][Math.floor(Math.random()*4)];
                    b.style.left = Math.random() * 90 + 'vw';
                    document.body.appendChild(b);
                    setTimeout(() => b.remove(), 6000);
                }, i * 300);
            }
        }

        function resetGame() {
            score = 0;
            document.getElementById('win-modal').classList.remove('active');
            document.getElementById('progress-fill').style.width = '0%';
            document.getElementById('drop-zone').innerHTML = '';
            document.getElementById('drop-zone').classList.remove('has-content');
            initGame();
        }

        function initGame() {
            const pool = document.getElementById('pieces-pool');
            const guide = document.getElementById('guide-container');
            pool.innerHTML = '';
            guide.innerHTML = '';

            // 1. Cargar Guía
            PROFESSIONS.forEach(p => {
                guide.innerHTML += `<div class="ref-item" id="ref-${p.id}">${p.id} <span>❓</span></div>`;
            });

            // 2. Mezclar TODAS las piezas (Cambian de lugar cada vez)
            let allSyllables = [];
            PROFESSIONS.forEach(p => {
                p.parts.forEach(s => allSyllables.push({ text: s, parent: p.id }));
            });
            allSyllables.sort(() => Math.random() - 0.5);

            allSyllables.forEach(data => {
                const div = document.createElement('div');
                div.className = 'syllable';
                div.textContent = data.text;
                div.dataset.parent = data.parent;
                div.draggable = true;
                div.ondragstart = (e) => div.classList.add('dragging');
                div.ondragend = () => div.classList.remove('dragging');
                pool.appendChild(div);
            });
        }

        const dz = document.getElementById('drop-zone');
        dz.ondragover = (e) => e.preventDefault();
        dz.ondrop = (e) => {
            const dragging = document.querySelector('.dragging');
            if(dragging) {
                dz.appendChild(dragging);
                dz.classList.add('has-content');
                checkWord();
            }
        };

        const pl = document.getElementById('pieces-pool');
        pl.ondragover = (e) => e.preventDefault();
        pl.ondrop = (e) => {
            const dragging = document.querySelector('.dragging');
            if(dragging) {
                pl.appendChild(dragging);
                if(dz.children.length === 0) dz.classList.remove('has-content');
            }
        };

        function checkWord() {
            const currentItems = Array.from(dz.children);
            if (currentItems.length < 2) return;

            const parentId = currentItems[0].dataset.parent;
            const target = PROFESSIONS.find(p => p.id === parentId);
            const currentStr = currentItems.map(i => i.textContent).join('');

            if (currentStr === target.parts.join('')) {
                // ¡CORRECTO!
                currentItems.forEach(i => i.classList.add('is-correct'));
                playSound(523, 0.5); setTimeout(() => playSound(659, 0.5), 100);
                
                // Confeti individual por palabra
                confetti({ particleCount: 50, spread: 60, origin: { y: 0.7 } });
                
                triggerAlert("¡Excelente!", "bg-win");

                setTimeout(() => {
                    dz.innerHTML = '';
                    dz.classList.remove('has-content');
                    const ref = document.getElementById(`ref-${parentId}`);
                    ref.classList.add('done');
                    ref.querySelector('span').textContent = '✅';
                    
                    score++;
                    document.getElementById('progress-fill').style.width = (score / PROFESSIONS.length) * 100 + '%';
                    
                    if(score === PROFESSIONS.length) finalize();
                }, 1000);
            } else if (currentItems.length >= target.parts.length) {
                playSound(150, 0.4);
                triggerAlert("Intenta otra vez", "bg-fail");
            }
        }

        function triggerAlert(txt, cls) {
            const a = document.getElementById('alert-box');
            a.textContent = txt; a.className = cls + ' show';
            setTimeout(() => a.classList.remove('show'), 1500);
        }

        function finalize() {
            playSound(523, 0.3); playSound(659, 0.3); playSound(783, 0.5);
            confetti({ particleCount: 200, spread: 90, origin: { y: 0.6 } });
            spawnBalloons();
            setTimeout(() => {
                document.getElementById('win-modal').classList.add('active');
                if ('speechSynthesis' in window) {
                    const u = new SpeechSynthesisUtterance("Te felicito, sigue avanzando en tu español.");
                    u.lang = 'es-ES'; window.speechSynthesis.speak(u);
                }
            }, 1000);
        }

        initGame();
    </script>
</body>
</html>
"""

components.html(html_profesiones_premium, height=950, scrolling=False)
