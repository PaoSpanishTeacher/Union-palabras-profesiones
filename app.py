import streamlit as st
import streamlit.components.v1 as components

# Configuración de página
st.set_page_config(page_title="Formar palabras de Profesiones", layout="wide")

st.markdown("""
    <style>
    .block-container { padding: 0rem; }
    iframe { border: none; }
    </style>
    """, unsafe_allow_html=True)

html_profesiones = r"""
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
            background-size: 30px 30px, 100% 100%;
            display: flex; flex-direction: column; align-items: center;
            padding-top: 40px; /* ESPACIO PARA QUE NO SE CORTE EL TITULO */
        }

        header { 
            text-align: center; 
            padding: 10px 20px 20px 20px; 
            width: 100%;
        }

        h1 { 
            font-family: 'Fredoka', sans-serif; 
            font-size: clamp(1.8rem, 4vw, 2.8rem); /* Tamaño adaptativo */
            color: var(--text-main); 
            text-shadow: 2px 2px 0px white;
            line-height: 1.2;
        }

        .brand-name { 
            font-family: 'Dancing Script', cursive; 
            font-size: 1.5rem; 
            color: var(--accent);
            margin-top: 5px;
        }

        .main-content {
            display: grid;
            grid-template-columns: 260px 1fr;
            gap: 25px;
            width: 95%;
            max-width: 1150px;
            margin-top: 20px;
            padding-bottom: 50px;
        }

        /* LISTA LATERAL */
        .reference-list {
            background: white;
            padding: 20px;
            border-radius: 20px;
            border: 3px solid var(--primary);
            box-shadow: 0 6px 15px rgba(0,0,0,0.1);
            height: fit-content;
            position: sticky;
            top: 20px;
        }
        .reference-list h3 { 
            font-family: 'Fredoka', sans-serif; 
            color: var(--secondary); 
            margin-bottom: 15px; 
            text-align: center;
            font-size: 1.4rem;
        }
        .ref-item {
            padding: 10px 15px;
            margin-bottom: 10px;
            background: #fdfbff;
            border: 1px solid #eee;
            border-radius: 12px;
            font-weight: 700;
            color: var(--text-main);
            text-transform: capitalize;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.3s ease;
        }
        .ref-item.done {
            background: #e8f5e9;
            color: #2e7d32;
            border-color: #c8e6c9;
            opacity: 0.8;
        }

        /* ÁREA JUEGO */
        .game-area { display: flex; flex-direction: column; gap: 25px; }

        .progress-container {
            width: 100%; background: white; height: 24px;
            border-radius: 20px; border: 3px solid var(--secondary);
            overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }
        #progress-bar {
            height: 100%; width: 0%; background: linear-gradient(90deg, #4cc9f0, #4361ee);
            transition: width 0.6s ease-in-out;
        }

        .drop-zone {
            background: white; border: 4px dashed var(--text-main);
            border-radius: 20px; padding: 30px; min-height: 140px;
            display: flex; justify-content: center; align-items: center;
            gap: 12px; position: relative;
            box-shadow: inset 0 4px 10px rgba(0,0,0,0.05);
        }
        .drop-zone::before {
            content: "Arrastra las sílabas aquí"; color: #aaa; font-style: italic; font-size: 1.1rem;
        }
        .drop-zone.has-items::before { display: none; }

        .pieces-pool {
            background: rgba(255, 255, 255, 0.4); border: 2px solid var(--secondary);
            border-radius: 20px; padding: 20px; display: flex; flex-wrap: wrap;
            justify-content: center; gap: 12px; min-height: 220px;
            backdrop-filter: blur(5px);
        }

        .piece {
            background: white; border: 3px solid var(--secondary);
            border-radius: 12px; padding: 14px 22px;
            font-family: 'Fredoka', sans-serif; font-size: 1.3rem;
            color: var(--text-main); cursor: grab;
            box-shadow: 0 5px 0px var(--secondary);
            text-transform: uppercase;
            transition: transform 0.2s;
        }
        .piece:hover { transform: translateY(-3px); }
        .piece.dragging { opacity: 0.4; transform: scale(1.1); }
        .piece.correct { background: var(--success); color: white; border-color: #2e7d32; box-shadow: 0 4px 0px #2e7d32; }

        /* ALERTAS */
        #msg-alert {
            position: fixed; top: 15%; left: 50%; transform: translateX(-50%) scale(0);
            padding: 12px 35px; border-radius: 50px; color: white; font-weight: bold;
            font-size: 1.3rem; z-index: 100; transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        #msg-alert.show { transform: translateX(-50%) scale(1); }
        .msg-correct { background: var(--success); box-shadow: 0 4px 15px rgba(76, 175, 80, 0.4); }
        .msg-error { background: var(--error); box-shadow: 0 4px 15px rgba(244, 67, 54, 0.4); }

        #final-screen {
            position: fixed; inset: 0; background: rgba(255, 255, 255, 0.98);
            display: none; flex-direction: column; justify-content: center;
            align-items: center; z-index: 1000; text-align: center;
        }
        #final-screen.active { display: flex; }

        .btn-restart {
            background: var(--accent); color: white; border: none;
            padding: 18px 45px; font-size: 1.6rem; border-radius: 50px;
            cursor: pointer; margin-top: 25px; box-shadow: 0 6px 0px #a3165b;
            font-family: 'Fredoka', sans-serif;
        }

        .watermark {
            position: fixed; bottom: 15px; right: 20px;
            font-size: 0.9rem; color: rgba(58, 12, 163, 0.2);
            font-family: 'Dancing Script', cursive; font-weight: bold;
        }

        @media (max-width: 800px) {
            .main-content { grid-template-columns: 1fr; }
            .reference-list { position: relative; top: 0; order: 2; }
            .game-area { order: 1; }
        }
    </style>
</head>
<body>

    <header>
        <h1>Unión de palabras - Profesiones</h1>
        <div class="brand-name">PaoSpanishTeacher</div>
    </header>

    <div class="main-content">
        <div class="reference-list">
            <h3>Lista de Guía</h3>
            <div id="guide-items"></div>
        </div>

        <div class="game-area">
            <div class="progress-container">
                <div id="progress-bar"></div>
            </div>

            <div class="drop-zone" id="drop-zone"></div>
            <div class="pieces-pool" id="pieces-pool"></div>
        </div>
    </div>

    <div id="msg-alert"></div>
    <div class="watermark">PaoSpanishTeacher</div>

    <div id="final-screen">
        <span style="font-size: 7rem;">👨‍🏫</span>
        <h1 style="margin-bottom: 10px;">¡Excelente trabajo!</h1>
        <p style="font-size: 1.3rem;">Has completado todas las profesiones.</p>
        <p style="font-weight: bold; color: var(--accent); margin-top: 10px;">Juego creado por PaoSpanishTeacher</p>
        <button class="btn-restart" onclick="location.reload()">Jugar otra vez</button>
    </div>

    <script>
        const PROFESSIONS = [
            { full: "doctor", parts: ["DOC", "TOR"] },
            { full: "profesora", parts: ["PRO", "FE", "SORA"] },
            { full: "ingeniero", parts: ["IN", "GE", "NIE", "RO"] },
            { full: "policía", parts: ["PO", "LI", "CÍ", "A"] },
            { full: "bombero", parts: ["BOM", "BE", "RO"] },
            { full: "enfermera", parts: ["EN", "FER", "ME", "RA"] },
            { full: "abogado", parts: ["ABO", "GA", "DO"] },
            { full: "piloto", parts: ["PI", "LO", "TO"] },
            { full: "músico", parts: ["MÚ", "SI", "CO"] },
            { full: "arquitecta", parts: ["AR", "QUI", "TEC", "TA"] }
        ];

        let completedCount = 0;
        const pool = document.getElementById('pieces-pool');
        const dropZone = document.getElementById('drop-zone');
        const guide = document.getElementById('guide-items');

        function init() {
            guide.innerHTML = PROFESSIONS.map(p => `<div class="ref-item" id="ref-${p.full}">${p.full} <span>❓</span></div>`).join('');
            
            let allParts = [];
            PROFESSIONS.forEach(p => p.parts.forEach(part => allParts.push({t: part, p: p.full})));
            allParts.sort(() => Math.random() - 0.5);

            allParts.forEach(data => {
                const div = document.createElement('div');
                div.className = 'piece';
                div.textContent = data.t;
                div.dataset.parent = data.p;
                div.draggable = true;
                div.ondragstart = (e) => { div.classList.add('dragging'); };
                div.ondragend = () => { div.classList.remove('dragging'); };
                pool.appendChild(div);
            });
        }

        dropZone.ondragover = (e) => e.preventDefault();
        dropZone.ondrop = (e) => {
            const el = document.querySelector('.dragging');
            if(el) {
                dropZone.appendChild(el);
                dropZone.classList.add('has-items');
                check();
            }
        };

        pool.ondragover = (e) => e.preventDefault();
        pool.ondrop = (e) => {
            const el = document.querySelector('.dragging');
            if(el) {
                pool.appendChild(el);
                if(dropZone.children.length === 0) dropZone.classList.remove('has-items');
            }
        };

        function check() {
            const items = Array.from(dropZone.children);
            if (items.length < 2) return;

            const parent = items[0].dataset.parent;
            const target = PROFESSIONS.find(p => p.full === parent);
            const currentString = items.map(i => i.textContent).join('');
            
            if (currentString === target.parts.join('')) {
                items.forEach(i => i.classList.add('correct'));
                showAlert("¡Muy bien!", "msg-correct");
                setTimeout(() => {
                    dropZone.innerHTML = '';
                    dropZone.classList.remove('has-items');
                    const refItem = document.getElementById(`ref-${parent}`);
                    refItem.classList.add('done');
                    refItem.querySelector('span').textContent = '✅';
                    completedCount++;
                    document.getElementById('progress-bar').style.width = (completedCount/PROFESSIONS.length)*100 + '%';
                    if(completedCount === PROFESSIONS.length) win();
                }, 800);
            } else if (items.length >= target.parts.length) {
                // Pequeño retardo para dejar que el usuario vea la palabra formada antes del error
                setTimeout(() => {
                    if(Array.from(dropZone.children).length >= target.parts.length) {
                         showAlert("Sigue intentando", "msg-error");
                    }
                }, 300);
            }
        }

        function showAlert(txt, cls) {
            const a = document.getElementById('msg-alert');
            a.textContent = txt; a.className = cls + ' show';
            setTimeout(() => a.classList.remove('show'), 1500);
        }

        function win() {
            confetti({ particleCount: 180, spread: 80, origin: { y: 0.6 } });
            document.getElementById('final-screen').classList.add('active');
            if ('speechSynthesis' in window) {
                const u = new SpeechSynthesisUtterance("Te felicito, sigue avanzando en tu español.");
                u.lang = 'es-ES';
                window.speechSynthesis.speak(u);
            }
        }

        init();
    </script>
</body>
</html>
"""

components.html(html_profesiones, height=950, scrolling=False)
