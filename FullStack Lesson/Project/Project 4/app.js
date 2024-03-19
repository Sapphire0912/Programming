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

// 點選新增按鈕就會新增一個 form
let addButton = document.querySelector(".plus-btn");
addButton.addEventListener("click", () => {
  let newForm = document.createElement("form");
  let newDiv = document.createElement("div");
  newDiv.classList.add("grader");

  // 製作表單元素
  let newInput1 = document.createElement("input");
  newInput1.setAttribute("type", "text");
  newInput1.setAttribute("list", "opt");
  newInput1.classList.add("class-type");

  let newInput2 = document.createElement("input");
  newInput2.setAttribute("type", "text");
  newInput2.classList.add("class-number");

  let newInput3 = document.createElement("input");
  newInput3.setAttribute("type", "number");
  newInput3.setAttribute("min", "0");
  newInput3.setAttribute("max", "6");
  newInput3.classList.add("class-credit");
  newInput3.addEventListener("change", () => {
    setGPA();
  });

  let newSelect = document.createElement("select");
  newSelect.innerHTML =
    '<select><option value=""></option><option value="A">A</option><option value="A-">A-</option><option value="B+">B+</option><option value="B">B</option><option value="B-">B-</option><option value="C+">C+</option><option value="C">C</option><option value="C-">C-</option><option value="D+">D+</option><option value="D">D</option><option value="D-">D-</option><option value="F">F</option></select>';
  newSelect.classList.add("select");
  newSelect.addEventListener("change", (e) => {
    setGPA();
    changeColor(e.target);
  });

  let newButton = document.createElement("button");
  newButton.classList.add("trash-button");
  let newItag = document.createElement("i");
  newItag.classList.add("fas");
  newItag.classList.add("fa-trash");
  newButton.appendChild(newItag);
  // 這是清除表單的動畫, 第2種呈現方式; 利用 animationend 效果
  newButton.addEventListener("click", (e) => {
    e.preventDefault(); // 避免送出表單內容
    e.target.parentElement.parentElement.style.animation =
      "scaleDown 0.5s ease forwards";
    e.target.parentElement.parentElement.addEventListener(
      "animationend",
      (e) => {
        e.target.remove();
        setGPA();
      }
    );
  });

  // 將表單新增至 HTML 頁面, 並在各自對應的父元素上
  newDiv.appendChild(newInput1);
  newDiv.appendChild(newInput2);
  newDiv.appendChild(newInput3);
  newDiv.appendChild(newSelect);
  newDiv.appendChild(newButton);
  newForm.appendChild(newDiv);
  document.querySelector(".all-inputs").appendChild(newForm);
  newForm.style.animation = "scaleUp 0.5s ease forwards";
});

// 製作垃圾桶功能
let allTrash = document.querySelectorAll(".trash-button");
allTrash.forEach((trash) => {
  // 讓整個 form 消失
  trash.addEventListener("click", (e) => {
    // 找到該垃圾桶上層的 form Element 並移除
    // console.log(e.target.parentElement.parentElement);

    // 若直接移除就沒有動畫效果, 所以改用 CSS 的方式讓 form 漸漸消失
    // e.target.parentElement.parentElement.remove();

    /* 註: CSS的消失動畫不是真的讓 form 完全從 HTML 移除, 會留一大個空白在 HTML 上.
           因此, 要實現動畫執行結束後刪除 form 的效果, 要在外部寫一個 function
     */
    e.target.parentElement.parentElement.classList.add("remove");
  });
});

allTrash.forEach((trash) => {
  let form = trash.parentElement.parentElement;
  // 當動畫執行結束後, 才會刪除 form; transitionend: 代表動畫結束才會執行的 function
  form.addEventListener("transitionend", (e) => {
    e.target.remove();
    setGPA();
  });
});
