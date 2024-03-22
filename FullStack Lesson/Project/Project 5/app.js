const canvas = document.getElementById("myCanvas");
const ctx = canvas.getContext("2d");

const unit = 20; // 設定 單位長度
const row = canvas.height / unit; // 320 / 20 = 16
const column = canvas.width / unit; // 320 / 20 = 16

let snake = []; // array 中的每個元素都是一個物件(儲存身體的 x, y 座標)
function createSnake() {
  snake[0] = {
    x: 80,
    y: 0,
  };
  snake[1] = {
    x: 60,
    y: 0,
  };
  snake[2] = {
    x: 40,
    y: 0,
  };
  snake[3] = {
    x: 20,
    y: 0,
  };
}
// 蛇的初始位置設定
createSnake();

// 利用電腦鍵盤的上下左右按鍵控制蛇的方向
window.addEventListener("keydown", changeDirection);
/* 
蛇轉動的限制條件:
1. 蛇沒辦法 180 度迴轉 (ex. 正在向右走, 不能立刻就向左走)
2. 蛇往同個方向走時, 是不會有任何動作
*/

// 設定果實的位置
class Fruit {
  constructor() {
    this.x = Math.floor(Math.random() * column) * unit;
    this.y = Math.floor(Math.random() * row) * unit;
  }

  drawFrult() {
    ctx.fillStyle = "yellow";
    ctx.fillRect(this.x, this.y, unit, unit);
  }

  pickLocation() {
    // 選定的位置不可以和蛇的當前位置重疊
    let overlapping = false;
    let new_x;
    let new_y;

    function checkOverLap(new_x, new_y) {
      for (let i = 0; i < snake.length; i++) {
        if (new_x == snake[i].x && new_y == snake[i].y) {
          overlapping = true;
          return;
        } else {
          overlapping = false;
        }
      }
    }
    do {
      new_x = Math.floor(Math.random() * column) * unit;
      new_y = Math.floor(Math.random() * row) * unit;
      checkOverLap(new_x, new_y);
    } while (overlapping);
    this.x = new_x;
    this.y = new_y;
  }
}
let myFrult = new Fruit();

// 設定遊戲分數
let score = 0;
let bestScore;
loadHighestScore();
document.getElementById("bestScore").innerHTML = "最高分數: " + bestScore;
document.getElementById("myScore").innerHTML = "遊戲分數: " + score;

// canvas 繪製
let d = "Right"; // 設定蛇走的方向
function changeDirection(event) {
  // 讀取鍵盤的上下左右按鍵, 並判斷限制條件 1.
  if (event.key == "ArrowLeft" && d != "Right") {
    d = "Left";
  } else if (event.key == "ArrowRight" && d != "Left") {
    d = "Right";
  } else if (event.key == "ArrowUp" && d != "Down") {
    d = "Up";
  } else if (event.key == "ArrowDown" && d != "Up") {
    d = "Down";
  }
  /* 
    問題: 若按鍵盤的速度太快(在下一次更新 draw function 時間裡), 
    讓原本 d = "Left" -> d = "Up" -> d = "Right"; 則會相當於,
    d = "Left" -> d = "Right"; 因此蛇會在原地自殺
  */
  // 處理該問題: 要在每按下按鍵之後, 在下一幀更新之前任何按鍵都無效
  window.removeEventListener("keydown", changeDirection); // 按下按鍵之後, 就移除監聽事件
}

function draw() {
  // 判斷蛇是否撞到自己的身體(在繪製新畫布之前)
  for (let i = 1; i < snake.length; i++) {
    if (snake[i].x == snake[0].x && snake[i].y == snake[0].y) {
      window.clearInterval(myGame);
      alert("遊戲結束");
      return;
    }
  }

  // 更新畫布內容(先設定背景色, 再重新填滿背景)
  ctx.fillStyle = "black";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // 繪製果實位置
  myFrult.drawFrult();

  // 繪製蛇的身體
  for (let i = 0; i < snake.length; i++) {
    ctx.fillStyle = i != 0 ? "lightblue" : "lightseagreen";
    ctx.strokeStyle = "white";

    if (snake[i].x >= canvas.width) {
      snake[i].x = 0;
    }
    if (snake[i].x < 0) {
      snake[i].x = canvas.width - unit;
    }
    if (snake[i].y < 0) {
      snake[i].y = canvas.height - unit;
    }
    if (snake[i].y >= canvas.height) {
      snake[i].y = 0;
    }

    ctx.fillRect(snake[i].x, snake[i].y, unit, unit);
    ctx.strokeRect(snake[i].x, snake[i].y, unit, unit);
  }

  // 根據 d 的方向來決定 蛇往哪邊走
  // 當蛇撞到牆壁時, 蛇的頭可以從牆壁的另一端出現
  let snakeX = snake[0].x;
  let snakeY = snake[0].y;
  if (d == "Left") {
    snakeX -= unit;
  } else if (d == "Right") {
    snakeX += unit;
  } else if (d == "Up") {
    snakeY -= unit;
  } else if (d == "Down") {
    snakeY += unit;
  }

  // 更新蛇的位置
  let newHead = {
    x: snakeX,
    y: snakeY,
  };

  // 判斷是否吃到果實
  if (snake[0].x == myFrult.x && snake[0].y == myFrult.y) {
    // 重新選擇新的隨機果實位置
    myFrult.pickLocation();
    // 更新分數, 並判斷是否需要更新最新紀錄
    score++;
    setBestScore(score);
    document.getElementById("myScore").innerHTML = "遊戲分數: " + score;
    document.getElementById("bestScore").innerHTML = "最高分數: " + bestScore;
  } else {
    snake.pop();
  }
  snake.unshift(newHead);

  // 蛇已經更新位置了, 重新開啟鍵盤監聽事件
  window.addEventListener("keydown", changeDirection);
}

let myGame = window.setInterval(draw, 100); // 每 0.1s 執行 draw function

function loadHighestScore() {
  // 是否已經有最高分的紀錄
  if (localStorage.getItem("bestScore") == null) {
    bestScore = 0;
  } else {
    bestScore = Number(localStorage.getItem("bestScore"));
  }
}

function setBestScore(score) {
  if (score > bestScore) {
    localStorage.setItem("bestScore", score);
    bestScore = score;
  }
}
