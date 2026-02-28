import streamlit as st
import streamlit.components.v1 as components

# Configuración de página
st.set_page_config(page_title="Rompecabezas Profesiones", layout="wide")

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
        }

        header { text-align: center; padding: 15px; }
        h1 { font-family: 'Fredoka', sans-serif; font-size: 2.5rem; color: var(--text-main); text-shadow: 2px 2px 0px white; }
        .brand-name { font-family: 'Dancing Script', cursive; font-size: 1.4rem; color: var(--accent); }

        /* DISEÑO DE COLUMNAS */
        .main-content {
            display: grid;
            grid-template-columns: 250px 1fr;
            gap: 20px;
            width: 95%;
            max-width: 1100px;
            margin-top: 10px;
        }

        /* LISTA LATERAL DE GUÍA */
        .reference-list {
            background: white;
            padding: 20px;
            border-radius: 20px;
            border: 3px solid var(--primary);
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            height: fit-content;
        }
        .reference-list h3 { 
            font-family: 'Fredoka', sans-serif; 
            color: var(--secondary); 
            margin-bottom: 15px; 
            text-align: center;
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
        }
        .ref-item {
            padding: 8px 12px;
            margin-bottom: 8px;
            background: #f8f9fa;
            border-radius: 8px;
            font-weight: bold;
            color: var(--text-main);
            text-transform: capitalize;
            display: flex;
            justify-content: space-between;
        }
        .ref-item.done {
            background: #e8f5e9;
            color: #2e7d32;
            text-decoration: line-through;
            opacity: 0.7;
        }

        .game-area { display: flex; flex-direction: column; gap: 20px; }

        .progress-container {
            width: 100%; background: white; height: 20px;
            border-radius: 20px; border: 3px solid var(--secondary);
            overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }
        #progress-bar {
            height: 100%; width: 0%; background: linear-gradient(90deg, #4cc9f0, #4361ee);
            transition: width 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }

        .drop-zone {
            background: white; border: 4px dashed var(--text-main);
            border-radius: 20px; padding: 25px; min-height: 120px;
            display: flex; justify-content: center; align-items: center;
            gap: 10px; position: relative;
        }
        .drop-zone::before {
            content: "Arrastra las sílabas aquí"; color: #aaa; font-style: italic;
        }
        .drop-zone.has-items::before { display: none; }

        .pieces-pool {
            background: rgba(255, 255, 255, 0.5); border: 2px solid var(--secondary);
            border-radius: 20px; padding: 15px; display: flex; flex-wrap: wrap;
            justify-content: center; gap: 10px; min-height: 180px;
        }

        .piece {
            background: white; border: 3px solid var(--secondary);
            border-radius: 10px; padding: 12px 20px;
            font-family: 'Fredoka', sans-serif; font-size: 1.2rem;
            color: var(--text-main); cursor: grab;
            box-shadow: 0 4px 0px var(--secondary);
            text-transform: uppercase;
        }
        .piece.dragging { opacity: 0.5; }
        .piece.correct { background: var(--success); color: white; border-color: #2e7d32; box-shadow: 0 4px 0px #2e7d32; }

        #final-screen {
            position: fixed; inset: 0; background: rgba(255, 255, 255, 0.98);
            display: none; flex-direction: column; justify-content: center;
            align-items: center; z-index: 1000; text-align: center;
        }
        #final-screen.active { display: flex; }

        .btn-restart {
            background: var(--accent); color: white; border: none;
            padding: 15px 40px; font-size: 1.5rem; border-radius: 50px;
            cursor: pointer; margin-top: 20px; box-shadow: 0 5px 0px #a3165b;
        }

        #msg-alert {
            position: fixed; top: 15%; left: 50%; transform: translateX(-50%) scale(0);
            padding: 10px 30px; border-radius: 50px; color: white; font-weight: bold;
            z-index: 100; transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        #msg-alert.show { transform: translateX(-50%) scale(1); }
        .msg-correct { background: var(--success); }
        .msg-error { background: var(--error); }
    </style>
</head>
<body>

    <header>
        <h1>Rompecabezas - Profesiones</h1>
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

    <div id="final-screen">
        <span style="font-size: 6rem;">👨‍🏫</span>
        <h1>¡Excelente trabajo!</h1>
        <p>Has completado todas las profesiones.</p>
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
            // Cargar guía
            guide.innerHTML = PROFESSIONS.map(p => `<div class="ref-item" id="ref-${p.full}">${p.full} <span>❓</span></div>`).join('');
            
            // Mezclar piezas
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
            dropZone.appendChild(el);
            dropZone.classList.add('has-items');
            check();
        };

        pool.ondragover = (e) => e.preventDefault();
        pool.ondrop = (e) => {
            const el = document.querySelector('.dragging');
            pool.appendChild(el);
            if(dropZone.children.length === 0) dropZone.classList.remove('has-items');
        };

        function check() {
            const items = Array.from(dropZone.children);
            if (items.length < 2) return;

            const parent = items[0].dataset.parent;
            const target = PROFESSIONS.find(p => p.full === parent);
            const currentString = items.map(i => i.textContent).join('');
            
            if (currentString === target.parts.join('')) {
                items.forEach(i => i.classList.add('correct'));
                showAlert("¡Correcto!", "msg-correct");
                setTimeout(() => {
                    dropZone.innerHTML = '';
                    dropZone.classList.remove('has-items');
                    document.getElementById(`ref-${parent}`).classList.add('done');
                    document.getElementById(`ref-${parent}`).querySelector('span').textContent = '✅';
                    completedCount++;
                    document.getElementById('progress-bar').style.width = (completedCount/10)*100 + '%';
                    if(completedCount === 10) win();
                }, 800);
            } else if (items.length >= target.parts.length) {
                showAlert("Sigue intentando", "msg-error");
            }
        }

        function showAlert(txt, cls) {
            const a = document.getElementById('msg-alert');
            a.textContent = txt; a.className = cls + ' show';
            setTimeout(() => a.classList.remove('show'), 1500);
        }

        function win() {
            confetti({ particleCount: 150, spread: 70, origin: { y: 0.6 } });
            document.getElementById('final-screen').classList.add('active');
            if ('speechSynthesis' in window) {
                window.speechSynthesis.speak(new SpeechSynthesisUtterance("Excelente trabajo"));
            }
        }

        init();
    </script>
</body>
</html>
"""

components.html(html_profesiones, height=850, scrolling=False)
