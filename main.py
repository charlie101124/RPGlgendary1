import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(
    page_title="심야의 학교 탈출",
    page_icon="👻",
    layout="centered"
)

# 다크 모드 강제 스타일 적용
st.markdown("""
    <style>
    .stApp {
        background-color: #0a0a0c;
        color: #e0e0e0;
    }
    h1 {
        color: #ff3b3b;
        text-align: center;
        font-family: 'Courier New', Courier, monospace;
        text-shadow: 0 0 10px #ff0000;
    }
    .info-box {
        background-color: #16161a;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #333;
        margin-bottom: 15px;
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("👻 심야의 학교 탈출")

st.markdown("""
<div class="info-box">
    <b>[게임 방법]</b><br>
    • <b>이동:</b> 방향키 (↑, ↓, ←, →) 또는 W, A, S, D<br>
    • <b>목표:</b> 어두운 학교 복도를 탐색해 <b>열쇠 3개(🔑)</b>를 모두 찾은 뒤, <b>출구(🚪)</b>로 탈출하세요.<br>
    • <b>주의:</b> 붉은 눈의 귀신(👻)이 순찰 중입니다. 가까이 다가가면 심장 소리가 빨라지며 추격해 옵니다!
</div>
""", unsafe_allow_html=True)

# HTML5 Canvas + JavaScript 기반 실시간 게임 엔진
game_html = """
<!DOCTYPE html>
<html>
<head>
<style>
    body {
        margin: 0;
        padding: 0;
        background-color: #0a0a0c;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-family: sans-serif;
        color: white;
        user-select: none;
    }
    #hud {
        width: 600px;
        display: flex;
        justify-content: space-between;
        padding: 10px 15px;
        background: #141418;
        border: 1px solid #2a2a30;
        border-bottom: none;
        box-sizing: border-box;
        font-size: 16px;
        font-weight: bold;
    }
    canvas {
        border: 2px solid #333;
        background-color: #050505;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.9);
    }
    #controls {
        margin-top: 15px;
        display: grid;
        grid-template-columns: repeat(3, 55px);
        grid-template-rows: repeat(2, 55px);
        gap: 8px;
    }
    .btn {
        background: #1f1f24;
        color: #ddd;
        border: 1px solid #444;
        border-radius: 8px;
        font-size: 20px;
        cursor: pointer;
    }
    .btn:active {
        background: #ff3b3b;
        color: white;
    }
    #restart-btn {
        margin-top: 15px;
        padding: 10px 24px;
        font-size: 16px;
        background: #8b0000;
        color: white;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        display: none;
    }
    #restart-btn:hover {
        background: #b30000;
    }
</style>
</head>
<body>

<div id="hud">
    <div>🔑 열쇠: <span id="key-count">0</span> / 3</div>
    <div id="status-msg" style="color: #aaa;">열쇠를 찾아 교실을 뒤지세요...</div>
</div>

<canvas id="gameCanvas" width="600" height="450"></canvas>

<button id="restart-btn" onclick="initGame()">다시 도전하기</button>

<!-- 모바일/마우스 지원용 가상 패드 -->
<div id="controls">
    <div></div>
    <button class="btn" onmousedown="setKey('ArrowUp', true)" onmouseup="setKey('ArrowUp', false)" ontouchstart="setKey('ArrowUp', true)" ontouchend="setKey('ArrowUp', false)">▲</button>
    <div></div>
    <button class="btn" onmousedown="setKey('ArrowLeft', true)" onmouseup="setKey('ArrowLeft', false)" ontouchstart="setKey('ArrowLeft', true)" ontouchend="setKey('ArrowLeft', false)">◀</button>
    <button class="btn" onmousedown="setKey('ArrowDown', true)" onmouseup="setKey('ArrowDown', false)" ontouchstart="setKey('ArrowDown', true)" ontouchend="setKey('ArrowDown', false)">▼</button>
    <button class="btn" onmousedown="setKey('ArrowRight', true)" onmouseup="setKey('ArrowRight', false)" ontouchstart="setKey('ArrowRight', true)" ontouchend="setKey('ArrowRight', false)">▶</button>
</div>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
const TILE = 30;
const ROWS = 15;
const COLS = 20;

// 1: 학교 벽(교실/복도), 0: 이동 가능 복도, 2: 출구
const initialMap = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
    [1,0,1,0,1,0,1,1,1,0,1,0,1,1,1,1,1,1,0,1],
    [1,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,1],
    [1,0,1,1,1,1,1,0,1,1,1,0,1,0,1,1,0,1,0,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,1],
    [1,1,1,0,1,0,1,1,1,0,1,1,1,0,1,0,1,1,1,1],
    [1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,2],
    [1,0,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,0,1],
    [1,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,1],
    [1,0,1,0,1,1,1,0,1,0,1,0,1,0,1,1,0,1,0,1],
    [1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1],
    [1,0,1,1,1,0,1,1,1,1,1,1,1,0,1,0,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
];

let player, ghost, keys, gameState, collectedKeys;
const inputKeys = {};

// 사운드 효과 (Web Audio API - 별도 파일 불필요)
const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
function playTone(freq, type, duration, vol=0.1) {
    if (audioCtx.state === 'suspended') audioCtx.resume();
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.type = type;
    osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
    gain.gain.setValueAtTime(vol, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duration);
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start();
    osc.stop(audioCtx.currentTime + duration);
}

function initGame() {
    player = { x: 1.5 * TILE, y: 1.5 * TILE, radius: 9, speed: 2.3 };
    ghost = { x: 17.5 * TILE, y: 12.5 * TILE, radius: 11, speed: 1.45, dirX: -1, dirY: 0 };
    keys = [
        { x: 1.5 * TILE, y: 13.5 * TILE, collected: false },
        { x: 17.5 * TILE, y: 1.5 * TILE, collected: false },
        { x: 9.5 * TILE, y: 9.5 * TILE, collected: false }
    ];
    collectedKeys = 0;
    gameState = "PLAYING";
    document.getElementById("key-count").innerText = "0";
    document.getElementById("status-msg").innerText = "열쇠를 찾아 교실을 뒤지세요...";
    document.getElementById("status-msg").style.color = "#aaa";
    document.getElementById("restart-btn").style.display = "none";
}

function setKey(code, state) {
    inputKeys[code] = state;
}

window.addEventListener("keydown", (e) => {
    inputKeys[e.code] = true;
    if(["ArrowUp","ArrowDown","ArrowLeft","ArrowRight"].indexOf(e.code) > -1) {
        e.preventDefault();
    }
});
window.addEventListener("keyup", (e) => {
    inputKeys[e.code] = false;
});

function canMove(nx, ny, radius) {
    const points = [
        { x: nx - radius, y: ny - radius },
        { x: nx + radius, y: ny - radius },
        { x: nx - radius, y: ny + radius },
        { x: nx + radius, y: ny + radius }
    ];
    for (let p of points) {
        let c = Math.floor(p.x / TILE);
        let r = Math.floor(p.y / TILE);
        if (r < 0 || r >= ROWS || c < 0 || c >= COLS) return false;
        let tile = initialMap[r][c];
        if (tile === 1) return false;
        if (tile === 2 && collectedKeys < 3) return false; // 열쇠 3개 미만이면 출구 잠김
    }
    return true;
}

let heartbeatTimer = 0;

function update() {
    if (gameState !== "PLAYING") return;

    // 1. 플레이어 이동
    let dx = 0, dy = 0;
    if (inputKeys["ArrowUp"] || inputKeys["KeyW"]) dy -= player.speed;
    if (inputKeys["ArrowDown"] || inputKeys["KeyS"]) dy += player.speed;
    if (inputKeys["ArrowLeft"] || inputKeys["KeyA"]) dx -= player.speed;
    if (inputKeys["ArrowRight"] || inputKeys["KeyD"]) dx += player.speed;

    if (canMove(player.x + dx, player.y, player.radius)) player.x += dx;
    if (canMove(player.x, player.y + dy, player.radius)) player.y += dy;

    // 2. 열쇠 획득 체크
    for (let k of keys) {
        if (!k.collected) {
            let dist = Math.hypot(player.x - k.x, player.y - k.y);
            if (dist < player.radius + 10) {
                k.collected = true;
                collectedKeys++;
                document.getElementById("key-count").innerText = collectedKeys;
                playTone(880, 'sine', 0.25, 0.15);
                if (collectedKeys === 3) {
                    document.getElementById("status-msg").innerText = "모든 열쇠를 찾았다! 오른쪽 출구(🚪)로 달려가세요!";
                    document.getElementById("status-msg").style.color = "#4ade80";
                }
            }
        }
    }

    // 3. 출구 탈출 체크
    let pc = Math.floor(player.x / TILE);
    let pr = Math.floor(player.y / TILE);
    if (initialMap[pr][pc] === 2 && collectedKeys === 3) {
        gameState = "WIN";
        playTone(523.25, 'triangle', 0.5, 0.2);
        document.getElementById("restart-btn").style.display = "inline-block";
    }

    // 4. 귀신 AI (거리 가까우면 추적, 멀면 배회)
    let distToPlayer = Math.hypot(player.x - ghost.x, player.y - ghost.y);
    
    // 심장박동 효과음
    if (distToPlayer < 160) {
        heartbeatTimer++;
        let interval = Math.max(15, Math.floor(distToPlayer / 3));
        if (heartbeatTimer >= interval) {
            playTone(65, 'sine', 0.12, 0.25);
            heartbeatTimer = 0;
        }
    }

    if (distToPlayer < 180) {
        // 플레이어 추적
        let angle = Math.atan2(player.y - ghost.y, player.x - ghost.x);
        let vx = Math.cos(angle) * (ghost.speed * 1.15);
        let vy = Math.sin(angle) * (ghost.speed * 1.15);
        if (canMove(ghost.x + vx, ghost.y, ghost.radius)) ghost.x += vx;
        if (canMove(ghost.x, ghost.y + vy, ghost.radius)) ghost.y += vy;
    } else {
        // 복도 순찰
        let nx = ghost.x + ghost.dirX * ghost.speed;
        let ny = ghost.y + ghost.dirY * ghost.speed;
        if (canMove(nx, ny, ghost.radius) && Math.random() > 0.02) {
            ghost.x = nx;
            ghost.y = ny;
        } else {
            const dirs = [[1,0], [-1,0], [0,1], [0,-1]];
            let pick = dirs[Math.floor(Math.random() * dirs.length)];
            ghost.dirX = pick[0];
            ghost.dirY = pick[1];
        }
    }

    // 5. 귀신 충돌 체크 (게임 오버)
    if (distToPlayer < player.radius + ghost.radius - 2) {
        gameState = "LOSE";
        playTone(110, 'sawtooth', 0.8, 0.3);
        document.getElementById("restart-btn").style.display = "inline-block";
    }
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 1. 맵 그리기 (교실 벽 & 복도 바닥)
    for (let r = 0; r < ROWS; r++) {
        for (let c = 0; c < COLS; c++) {
            let x = c * TILE;
            let y = r * TILE;
            if (initialMap[r][c] === 1) {
                ctx.fillStyle = "#1e2028";
                ctx.fillRect(x, y, TILE, TILE);
                ctx.strokeStyle = "#111";
                ctx.strokeRect(x, y, TILE, TILE);
            } else if (initialMap[r][c] === 2) {
                ctx.fillStyle = collectedKeys === 3 ? "#15803d" : "#7f1d1d";
                ctx.fillRect(x, y, TILE, TILE);
                ctx.fillStyle = "white";
                ctx.font = "16px sans-serif";
                ctx.fillText("🚪", x + 5, y + 21);
            } else {
                ctx.fillStyle = "#0e0e12";
                ctx.fillRect(x, y, TILE, TILE);
            }
        }
    }

    // 2. 열쇠 그리기
    ctx.font = "16px sans-serif";
    for (let k of keys) {
        if (!k.collected) {
            ctx.fillText("🔑", k.x - 9, k.y + 6);
        }
    }

    // 3. 플레이어 그리기
    ctx.beginPath();
    ctx.arc(player.x, player.y, player.radius, 0, Math.PI * 2);
    ctx.fillStyle = "#38bdf8";
    ctx.fill();

    // 4. 귀신 그리기
    ctx.font = "20px sans-serif";
    ctx.fillText("👻", ghost.x - 11, ghost.y + 7);

    // 5. 손전등 어둠 효과 (플레이어 주변만 밝게)
    let grad = ctx.createRadialGradient(player.x, player.y, 25, player.x, player.y, 125);
    grad.addColorStop(0, "rgba(0, 0, 0, 0)");
    grad.addColorStop(0.7, "rgba(0, 0, 0, 0.88)");
    grad.addColorStop(1, "rgba(0, 0, 0, 0.98)");

    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // 귀신의 붉은 눈은 어둠 속에서도 희미하게 보임
    let dist = Math.hypot(player.x - ghost.x, player.y - ghost.y);
    if (dist < 220) {
        ctx.fillStyle = "rgba(255, 0, 0, 0.85)";
        ctx.beginPath();
        ctx.arc(ghost.x - 4, ghost.y - 2, 2.2, 0, Math.PI * 2);
        ctx.arc(ghost.x + 4, ghost.y - 2, 2.2, 0, Math.PI * 2);
        ctx.fill();
    }

    // 6. 게임 종료 오버레이
    if (gameState === "LOSE") {
        ctx.fillStyle = "rgba(120, 0, 0, 0.8)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "#ff4d4d";
        ctx.font = "bold 36px sans-serif";
        ctx.textAlign = "center";
        ctx.fillText("귀신에게 잡혔습니다...", canvas.width / 2, canvas.height / 2);
        ctx.textAlign = "start";
    } else if (gameState === "WIN") {
        ctx.fillStyle = "rgba(0, 40, 20, 0.85)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "#4ade80";
        ctx.font = "bold 32px sans-serif";
        ctx.textAlign = "center";
        ctx.fillText("무사히 학교를 탈출했습니다!", canvas.width / 2, canvas.height / 2);
        ctx.textAlign = "start";
    }
}

function loop() {
    update();
    draw();
    requestAnimationFrame(loop);
}

initGame();
loop();
</script>

</body>
</html>
"""

# 스트림릿에 게임 렌더링
components.html(game_html, height=620)