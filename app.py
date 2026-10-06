import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Rắn săn mồi",
    page_icon="🐍",
    layout="centered"
)

st.title("🐍 Rắn săn mồi")
st.caption("Dùng phím mũi tên hoặc WASD để điều khiển")

game = """
<!DOCTYPE html>
<html>
<head>

<style>

body {
    margin: 0;
    background: #111827;
    font-family: Arial;
    text-align: center;
    color: white;
}

#game {
    background: #18251b;
    border: 4px solid #22c55e;
    border-radius: 10px;
    max-width: 100%;
}

#score {
    font-size: 24px;
    font-weight: bold;
    margin: 10px;
    color: #4ade80;
}

button {
    background: #22c55e;
    color: white;
    border: none;
    padding: 10px 25px;
    border-radius: 8px;
    font-size: 18px;
    font-weight: bold;
    cursor: pointer;
}

button:hover {
    background: #16a34a;
}

#help {
    color: #aaa;
    margin: 10px;
}

</style>

</head>

<body>

<div id="score">
    Điểm: <span id="scoreValue">0</span>
</div>

<canvas id="game" width="500" height="500"></canvas>

<p id="help">
    ⬆️⬇️⬅️➡️ hoặc W A S D
</p>

<button onclick="restartGame()">
    🔄 Chơi lại
</button>

<script>

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

const grid = 25;
const tile = canvas.width / grid;

let snake;
let food;
let direction;
let nextDirection;
let score;
let gameOver;

let speed = 110;

function startGame() {

    snake = [
        {x: 12, y: 12},
        {x: 11, y: 12},
        {x: 10, y: 12}
    ];

    direction = {
        x: 1,
        y: 0
    };

    nextDirection = {
        x: 1,
        y: 0
    };

    score = 0;

    gameOver = false;

    document.getElementById(
        "scoreValue"
    ).innerText = score;

    createFood();

    draw();

    setTimeout(gameLoop, speed);
}


function createFood() {

    let valid = false;

    while (!valid) {

        food = {
            x: Math.floor(Math.random() * grid),
            y: Math.floor(Math.random() * grid)
        };

        valid = true;

        for (let part of snake) {

            if (
                part.x === food.x &&
                part.y === food.y
            ) {

                valid = false;
                break;
            }
        }
    }
}


function changeDirection(x, y) {

    // Không cho quay đầu 180 độ

    if (
        direction.x + x === 0 &&
        direction.y + y === 0
    ) {
        return;
    }

    nextDirection = {
        x: x,
        y: y
    };
}


document.addEventListener(
    "keydown",
    function(event) {

        const key = event.key.toLowerCase();

        if (
            key === "arrowup" ||
            key === "w"
        ) {
            event.preventDefault();
            changeDirection(0, -1);
        }

        if (
            key === "arrowdown" ||
            key === "s"
        ) {
            event.preventDefault();
            changeDirection(0, 1);
        }

        if (
            key === "arrowleft" ||
            key === "a"
        ) {
            event.preventDefault();
            changeDirection(-1, 0);
        }

        if (
            key === "arrowright" ||
            key === "d"
        ) {
            event.preventDefault();
            changeDirection(1, 0);
        }

        if (
            key === " " &&
            gameOver
        ) {
            restartGame();
        }

    }
);


function update() {

    if (gameOver) {
        return;
    }

    direction = nextDirection;

    const head = {
        x: snake[0].x + direction.x,
        y: snake[0].y + direction.y
    };


    // Đụng tường

    if (
        head.x < 0 ||
        head.x >= grid ||
        head.y < 0 ||
        head.y >= grid
    ) {

        endGame();

        return;
    }


    // Đụng thân

    for (let i = 0; i < snake.length; i++) {

        if (
            head.x === snake[i].x &&
            head.y === snake[i].y
        ) {

            endGame();

            return;
        }
    }


    snake.unshift(head);


    // Ăn mồi

    if (
        head.x === food.x &&
        head.y === food.y
    ) {

        score++;

        document.getElementById(
            "scoreValue"
        ).innerText = score;

        createFood();

    } else {

        snake.pop();

    }

}


function drawGrid() {

    ctx.strokeStyle = "#1f3524";
    ctx.lineWidth = 1;

    for (let i = 0; i <= grid; i++) {

        ctx.beginPath();

        ctx.moveTo(i * tile, 0);
        ctx.lineTo(i * tile, canvas.height);

        ctx.stroke();


        ctx.beginPath();

        ctx.moveTo(0, i * tile);
        ctx.lineTo(canvas.width, i * tile);

        ctx.stroke();
    }
}


function drawFood() {

    ctx.fillStyle = "#ef4444";

    ctx.beginPath();

    ctx.arc(
        food.x * tile + tile / 2,
        food.y * tile + tile / 2,
        tile * 0.35,
        0,
        Math.PI * 2
    );

    ctx.fill();

    // Cuống

    ctx.fillStyle = "#22c55e";

    ctx.fillRect(
        food.x * tile + tile / 2,
        food.y * tile + 3,
        3,
        6
    );
}


function drawSnake() {

    for (
        let i = 0;
        i < snake.length;
        i++
    ) {

        const part = snake[i];

        if (i === 0) {

            // Đầu rắn

            ctx.fillStyle = "#4ade80";

        } else {

            ctx.fillStyle = "#22c55e";

        }

        ctx.fillRect(
            part.x * tile + 2,
            part.y * tile + 2,
            tile - 4,
            tile - 4
        );


        // Mắt

        if (i === 0) {

            ctx.fillStyle = "white";

            let eyeX1;
            let eyeY1;
            let eyeX2;
            let eyeY2;


            if (direction.x !== 0) {

                eyeX1 =
                    part.x * tile +
                    tile / 2 +
                    direction.x * 6;

                eyeY1 =
                    part.y * tile +
                    tile / 2 -
                    5;

                eyeX2 =
                    part.x * tile +
                    tile / 2 +
                    direction.x * 6;

                eyeY2 =
                    part.y * tile +
                    tile / 2 +
                    5;

            } else {

                eyeX1 =
                    part.x * tile +
                    tile / 2 -
                    5;

                eyeY1 =
                    part.y * tile +
                    tile / 2 +
                    direction.y * 6;

                eyeX2 =
                    part.x * tile +
                    tile / 2 +
                    5;

                eyeY2 =
                    part.y * tile +
                    tile / 2 +
                    direction.y * 6;
            }


            ctx.beginPath();

            ctx.arc(
                eyeX1,
                eyeY1,
                3,
                0,
                Math.PI * 2
            );

            ctx.fill();


            ctx.beginPath();

            ctx.arc(
                eyeX2,
                eyeY2,
                3,
                0,
                Math.PI * 2
            );

            ctx.fill();
        }
    }
}


function draw() {

    // Nền

    ctx.fillStyle = "#18251b";

    ctx.fillRect(
        0,
        0,
        canvas.width,
        canvas.height
    );


    drawGrid();

    drawFood();

    drawSnake();


    // Game over

    if (gameOver) {

        ctx.fillStyle =
            "rgba(0, 0, 0, 0.65)";

        ctx.fillRect(
            0,
            0,
            canvas.width,
            canvas.height
        );


        ctx.fillStyle = "white";

        ctx.textAlign = "center";

        ctx.font =
            "bold 42px Arial";

        ctx.fillText(
            "GAME OVER",
            canvas.width / 2,
            220
        );


        ctx.font =
            "24px Arial";

        ctx.fillText(
            "Điểm: " + score,
            canvas.width / 2,
            270
        );


        ctx.font =
            "18px Arial";

        ctx.fillText(
            "Nhấn SPACE hoặc Chơi lại",
            canvas.width / 2,
            320
        );
    }

}


function endGame() {

    gameOver = true;

    draw();
}


function gameLoop() {

    update();

    draw();

    if (!gameOver) {

        // Càng nhiều điểm càng nhanh

        let newSpeed =
            Math.max(
                55,
                110 - score * 2
            );

        setTimeout(
            gameLoop,
            newSpeed
        );
    }
}


function restartGame() {

    startGame();
}


startGame();

</script>

</body>
</html>
"""

components.html(
    game,
    height=650,
    scrolling=False
)
