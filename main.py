import streamlit as st

# Streamlit 페이지 설정
st.set_page_config(
    page_title="길 건너 새 친구들",
    page_icon="🐥",
    layout="centered"
)

st.title("🐥 길 건너 새 친구들 (Streamlit 버전)")
st.write("아래 게임 화면을 클릭하여 포커스를 맞춘 뒤, **W, A, S, D** 키로 새를 조작해 차를 피하세요!")

# HTML/JS 게임 코드를 포함한 컴포넌트 임베дий
game_html = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>길 건너 새 친구들</title>
    <style>
        body {
            margin: 0;
            background-color: #222;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            color: white;
            font-family: Arial, sans-serif;
            flex-direction: column;
            overflow: hidden;
        }
        canvas {
            border: 4px solid #fff;
            background-color: #7dcea0;
            outline: none;
        }
        #scoreBoard {
            font-size: 20px;
            margin-bottom: 5px;
            font-weight: bold;
        }
    </style>
</head>
<body>

    <div id="scoreBoard">점수: <span id="score">0</span></div>
    <canvas id="gameCanvas" width="400" height="550" tabindex="1"></canvas>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

// 시작하자마자 캔버스에 포커스 주어 키보드 입력 받기
canvas.focus();

let score = 0;
let isGameOver = false;

let bird = {
    x: 180,
    y: 500,
    size: 20,
    speed: 20
};

let cars = [
    { x: 0, y: 420, speed: 3, dir: 1, color: '#e74c3c' },
    { x: 400, y: 360, speed: 4, dir: -1, color: '#f1c40f' },
    { x: 0, y: 260, speed: 5, dir: 1, color: '#3498db' },
    { x: 400, y: 200, speed: 3.5, dir: -1, color: '#9b59b6' },
    { x: 0, y: 100, speed: 6, dir: 1, color: '#e67e22' }
];

window.addEventListener("keydown", function(e) {
    // 게임 화면 스크롤 방지
    if(["Space","ArrowUp","ArrowDown","ArrowLeft","ArrowRight", "KeyW", "KeyA", "KeyS", "KeyD"].indexOf(e.code) > -1) {
        e.preventDefault();
    }

    if (isGameOver) {
        if (e.key === "Enter" || e.key === "enter") {
            resetGame();
        }
        return;
    }

    const key = e.key.toLowerCase();

    if (key === "w" || e.key === "ArrowUp") {
        bird.y -= bird.speed;
        score += 10;
        updateScore();
    } else if ((key === "s" || e.key === "ArrowDown") && bird.y < canvas.height - 40) {
        bird.y += bird.speed;
    } else if ((key === "a" || e.key === "ArrowLeft") && bird.x > 20) {
        bird.x -= bird.speed;
    } else if ((key === "d" || e.key === "ArrowRight") && bird.x < canvas.width - 40) {
        bird.x += bird.speed;
    }
});

function updateScore() {
    document.getElementById("score").innerText = score;
}

function resetGame() {
    bird.x = 180;
    bird.y = 500;
    score = 0;
    updateScore();
    isGameOver = false;
    canvas.focus();
    loop();
}

function checkCollision() {
    for (let i = 0; i < cars.length; i++) {
        let car = cars[i];
        if (
            bird.x < car.x + 60 &&
            bird.x + bird.size > car.x &&
            bird.y < car.y + 30 &&
            bird.y + bird.size > car.y
        ) {
            isGameOver = true;
        }
    }

    if (bird.y <= 40) {
        score += 100;
        updateScore();
        bird.y = 500;
    }
}

function update() {
    if (isGameOver) return;

    for (let i = 0; i < cars.length; i++) {
        let car = cars[i];
        car.x += car.speed * car.dir;

        if (car.dir === 1 && car.x > canvas.width) {
            car.x = -60;
        } else if (car.dir === -1 && car.x < -60) {
            car.x = canvas.width;
        }
    }

    checkCollision();
}

function draw() {
    ctx.fillStyle = '#7dcea0';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = '#566573';
    ctx.fillRect(0, 80, canvas.width, 80);
    ctx.fillRect(0, 180, canvas.width, 100);
    ctx.fillRect(0, 340, canvas.width, 100);

    ctx.strokeStyle = '#fff';
    ctx.setLineDash([5, 5]);
    ctx.beginPath();
    ctx.moveTo(0, 120); ctx.lineTo(canvas.width, 120);
    ctx.moveTo(0, 230); ctx.lineTo(canvas.width, 230);
    ctx.moveTo(0, 390); ctx.lineTo(canvas.width, 390);
    ctx.stroke();
    ctx.setLineDash([]);

    for (let i = 0; i < cars.length; i++) {
        let car = cars[i];
        ctx.fillStyle = car.color;
        ctx.fillRect(car.x, car.y, 60, 30);
        ctx.fillStyle = '#fff';
        ctx.fillRect(car.x + (car.dir === 1 ? 40 : 10), car.y + 5, 15, 20);
    }

    ctx.fillStyle = '#f1c40f';
    ctx.beginPath();
    ctx.arc(bird.x + 10, bird.y + 10, 12, 0, Math.PI * 2);
    ctx.fill();
    
    ctx.fillStyle = '#e67e22';
    ctx.fillRect(bird.x + 15, bird.y + 8, 8, 5);

    if (isGameOver) {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = 'white';
        ctx.font = '26px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('GAME OVER', canvas.width / 2, canvas.height / 2 - 20);

        ctx.font = '14px Arial';
        ctx.fillText('다시 하려면 [Enter]를 누르세요', canvas.width / 2, canvas.height / 2 + 20);
    }
}

function loop() {
    update();
    draw();
    if (!isGameOver) {
        requestAnimationFrame(loop);
    }
}

loop();
</script>

</body>
</html>
"""

# Streamlit에 HTML 컴포넌트 렌더링 (높이 설정)
st.components.v1.html(game_html, height=620)