const canvas = document.getElementById("myCanvas");
const canvasHeight = canvas.height;
const canvasWidth = canvas.width;
const ctx = canvas.getContext("2d");

let circle_x = 160;
let circle_y = 60;
let radius = 20;
let xSpeed = 20;
let ySpeed = 20;

let ground_x = 100;
let ground_y = 500;
let ground_h = 5;
let brickArray = [];
let count = 0;

class Brick {
  constructor(x, y) {
    this.x = x;
    this.y = y;
    this.width = 50;
    this.height = 50;
    this.visible = true;
    brickArray.push(this);
  }

  drawBrick() {
    ctx.fillStyle = "lightgreen";
    ctx.fillRect(this.x, this.y, this.width, this.height);
  }

  touchingBall(ballX, ballY) {
    return (
      ballX >= this.x - radius &&
      ballX <= this.x + this.width + radius &&
      ballY <= this.y + this.height + radius &&
      ballY >= this.y - radius
    );
  }
}

// 製作 bricks
function getRandomArbitrary(min, max) {
  return min + Math.floor(Math.random() * (max - min));
}

for (let i = 0; i < 20; i++) {
  new Brick(getRandomArbitrary(0, 950), getRandomArbitrary(0, 450));
}

canvas.addEventListener("mousemove", (e) => {
  //   console.log(e.clientX); 滑鼠游標移動的 x 座標
  ground_x = e.clientX >= 800 ? 800 : e.clientX;
});

function drawCircle() {
  // 確認球是否有打到磚塊
  brickArray.forEach((brick, index) => {
    if (brick.visible && brick.touchingBall(circle_x, circle_y)) {
      // 優化系統效能
      count++;
      brick.visible = false;

      // 改變 x, y 方向速度, 並且將 brick 從 brickArray 移除
      if (circle_y >= brick.y + brick.height || circle_y <= brick.y) {
        // 球從上下方向撞到磚塊
        ySpeed *= -1;
      } else if (circle_x <= brick.x || circle_x >= brick.x + brick.width) {
        xSpeed *= -1;
      }
      //   brickArray.splice(index, 1); // O(n)
      if (count == 20) {
        alert("遊戲結束");
        clearInterval(game);
      }
    }
  });
  // 確認球有沒有碰到板子
  if (
    circle_x + radius >= ground_x &&
    circle_x + radius <= ground_x + 200 &&
    circle_y + radius >= ground_y &&
    circle_y - radius <= ground_y
  ) {
    if (ySpeed > 0) {
      circle_y -= 40;
    } else {
      circle_y += 40;
    }
    ySpeed *= -1;
  }

  // 碰到牆壁要讓球彈回
  if (circle_x + radius >= canvasWidth) {
    // 碰到右側牆壁
    xSpeed *= -1;
  }
  if (circle_x - radius <= 0) {
    // 碰到左側牆壁
    xSpeed *= -1;
  }
  if (circle_y - radius <= 0) {
    // 碰到上面牆壁
    ySpeed *= -1;
  }
  if (circle_y + radius >= canvasHeight) {
    ySpeed *= -1;
  }

  // 更新圓的座標
  circle_x += xSpeed;
  circle_y += ySpeed;

  // 清除畫布
  ctx.fillStyle = "black";
  ctx.fillRect(0, 0, canvasWidth, canvasHeight);

  // 繪製地板
  ctx.fillStyle = "orange";
  ctx.fillRect(ground_x, ground_y, 200, ground_h);

  // 繪製圓球
  ctx.beginPath();
  ctx.arc(circle_x, circle_y, radius, 0, 2 * Math.PI);
  ctx.stroke();
  ctx.fillStyle = "yellow";
  ctx.fill();

  // 繪製磚塊
  brickArray.forEach((brick) => {
    if (brick.visible) {
      brick.drawBrick();
    }
  });
}

let game = setInterval(drawCircle, 25);
