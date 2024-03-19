let hero = document.querySelector(".hero"); // 圖片動畫
let slider = document.querySelector(".slider"); // 顯示漸層動畫
let animation = document.querySelector("section.animation-wrapper"); // 最下層的背景(容器)

const time_line = new TimelineMax();

/* 
parameter1: 要控制的對象, 
parameter2: duration, 設定 1 代表 1 秒
parameter3: 控制對象的原始狀態 
parameter4: 控制對象的動畫結束後的狀態
parameter5: 設定控制對象的動畫的起始時間, 設定 "-=1.2", 代表提早 1.2 秒就執行動畫
*/
time_line
  .fromTo(hero, 1, { height: "0%" }, { height: "100%", ease: Power2.easeInOut })
  .fromTo(
    hero,
    1.2,
    { width: "80%" },
    { width: "100%", ease: Power2.easeInOut }
  )
  .fromTo(
    slider,
    1,
    { x: "-100%" },
    { x: "0%", ease: Power2.easeInOut },
    "-=1.2"
  )
  .fromTo(animation, 0.3, { opacity: 1 }, { opacity: 0 });

// .fromTo(animation, 0.3, { opacity: 1 }, { opacity: 0 }); 動畫結束之後讓整個容器(和內容)都隱藏起來

window.setTimeout(() => {
  animation.style.pointerEvents = "none";
}, 2500);

// 避免使用者按 Enter 將表單的內容全部送出
window.addEventListener("keypress", (e) => {
  // 按下 Enter 鍵: keypress { target: body, key: "Enter", charCode: 0, keyCode: 13 }
  // console.log(e);
  if (e.key == "Enter") {
    e.preventDefault();
  }
});

// 防止點選垃圾桶的 button 將整個表單內容送出
let allButtons = document.querySelectorAll("button");
allButtons.forEach((button) => {
  button.addEventListener("click", (e) => {
    e.preventDefault();
  });
});

// 改變 <select> 裡面的 <option> color
let allSelects = document.querySelectorAll("select");
allSelects.forEach((select) => {
  select.addEventListener("change", (e) => {
    // 讀取是哪個 option 被選取
    // console.log(e.target.value);

    // 每調整一次成績, 就會動態調整 GPA 內容. selectedIndex 讀取哪個 option 被選取
    setGPA();
    changeColor(e.target); // e.target 就是 select 標籤
  });
});

// 改變 credit 之後, GPA 也要更新
let credits = document.querySelectorAll(".class-credit");
credits.forEach((credit) => {
  credit.addEventListener("change", () => {
    setGPA();
  });
});

function changeColor(target) {
  if (target.value == "A" || target.value == "A-") {
    target.style.backgroundColor = "lightgreen";
    target.style.color = "black";
  } else if (
    target.value == "B+" ||
    target.value == "B" ||
    target.value == "B-"
  ) {
    target.style.backgroundColor = "yellow";
    target.style.color = "black";
  } else if (
    target.value == "C+" ||
    target.value == "C" ||
    target.value == "C-"
  ) {
    target.style.backgroundColor = "orange";
    target.style.color = "black";
  } else if (
    target.value == "D+" ||
    target.value == "D" ||
    target.value == "D-"
  ) {
    target.style.backgroundColor = "red";
    target.style.color = "black";
  } else {
    target.style.backgroundColor = "gray";
    target.style.color = "white";
  }
}

function convertor(grade) {
  switch (grade) {
    case "A":
      return 4.0;
    case "A-":
      return 3.7;
    case "B+":
      return 3.4;
    case "B":
      return 3.0;
    case "B-":
      return 2.7;
    case "C+":
      return 2.4;
    case "C":
      return 2.0;
    case "C-":
      return 1.7;
    case "D+":
      return 1.4;
    case "D":
      return 1.0;
    case "D-":
      return 0.7;
    case "F":
      return 0.0;
    default:
      return 0;
  }
}

function setGPA() {
  let formLength = document.querySelectorAll("form").length;
  let credits = document.querySelectorAll(".class-credit");
  let selects = document.querySelectorAll(".select");
  let sum = 0;
  let creditSum = 0;

  for (let i = 0; i < credits.length; i++) {
    // credits[i].value 回傳的是 string
    if (!isNaN(credits[i].valueAsNumber)) creditSum += credits[i].valueAsNumber;
  }

  for (let i = 0; i < formLength; i++) {
    if (!isNaN(credits[i].valueAsNumber)) {
      sum += credits[i].valueAsNumber * convertor(selects[i].value);
    }
  }

  let GPA;
  if (creditSum == 0) {
    GPA = 0.0;
  } else {
    GPA = (sum / creditSum).toFixed(2);
  }
  document.getElementById("result-gpa").innerText = GPA;
}

// 每次重新整理視窗就將 form 的內容清除
window.onload = function () {
  let form = document.querySelectorAll("form");
  form.forEach((f) => {
    f.reset();
  });
};
