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

// 排序演算法 merge sort
let btn1 = document.querySelector(".sort-descending");
let btn2 = document.querySelector(".sort-ascending");
btn1.addEventListener("click", () => {
  handleSorting("descending");
});

btn2.addEventListener("click", () => {
  handleSorting("ascending");
});

function handleSorting(direction) {
  let graders = document.querySelectorAll("div.grader");
  let objectArray = [];

  for (let i = 0; i < graders.length; i++) {
    let children = graders[i].children;
    let class_name = children[0].value;
    let class_number = children[1].value;
    let class_credit = children[2].value;
    let class_grade = children[3].value;
    // 直接利用變數名稱當成 key, 屬於 js 的特別用法
    if (
      !(
        class_name == "" &&
        class_number == "" &&
        class_credit == "" &&
        class_grade == ""
      )
    ) {
      let class_object = {
        class_name,
        class_number,
        class_credit,
        class_grade,
      };
      objectArray.push(class_object);
    }
  }
  // 取得 object array 後, 將 grade 轉成 Number; 將 objectArray 新增 class_grade_number 屬性
  for (let i = 0; i < objectArray.length; i++) {
    objectArray[i].class_grade_number = convertor(objectArray[i].class_grade);
  }
  // objectArray = mergeSort2(objectArray);
  objectArray = mergeSort(objectArray); // self mergesort
  if (direction == "descending") {
    objectArray = objectArray.reverse();
  }

  // 根據 object array 內容來更新網頁內容
  let allInputs = document.querySelector(".all-inputs");
  allInputs.innerHTML = ""; // 清空 allInputs 裡面的內容
  for (let i = 0; i < objectArray.length; i++) {
    let formContent = `<form>
    <div class="grader">
      <input
        type="text"
        placeholder="class category"
        class="class-type"
        list="opt"
        value=${objectArray[i].class_name}
      /><!--
      --><input
        type="text"
        placeholder="class number"
        class="class-number"
        value=${objectArray[i].class_number}
      /><!--
      --><input
        type="number"
        placeholder="credits"
        min="0"
        max="6"
        class="class-credit"
        value=${objectArray[i].class_credit}
      /><!--
      --><select name="select" class="select">
        <option value=""></option>
        <option value="A">A</option>
        <option value="A-">A-</option>
        <option value="B+">B+</option>
        <option value="B">B</option>
        <option value="B-">B-</option>
        <option value="C+">C+</option>
        <option value="C">C</option>
        <option value="C-">C-</option>
        <option value="D+">D+</option>
        <option value="D">D</option>
        <option value="D-">D-</option>
        <option value="F">F</option></select
      ><!--
      --><button class="trash-button">
        <i class="fas fa-trash"></i>
      </button>
    </div>
    </form>`;
    allInputs.innerHTML += formContent;
  }

  // select 沒辦法直接用 string 更改, 因此直接用 js 更改
  graders = document.querySelectorAll("div.grader");
  for (let i = 0; i < graders.length; i++) {
    graders[i].children[3].value = objectArray[i].class_grade;
  }

  // 將新的 form 內容新增事件監聽(select)
  let allSelects = document.querySelectorAll("select");
  allSelects.forEach((select) => {
    changeColor(select);
    select.addEventListener("change", (e) => {
      setGPA();
      changeColor(e.target);
    });
  });

  // credits 事件監聽
  let allCredits = document.querySelectorAll(".class-credit");
  allCredits.forEach((credits) => {
    credits.addEventListener("change", (e) => {
      setGPA();
    });
  });

  // 垃圾桶 事件監聽
  let allTrash = document.querySelectorAll(".trash-button");
  allTrash.forEach((trash) => {
    trash.addEventListener("click", (e) => {
      e.preventDefault();
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
  });
}

function merge2(a1, a2) {
  let result = [];
  let i = 0;
  let j = 0;

  while (i < a1.length && j < a2.length) {
    if (a1[i].class_grade_number > a2[j].class_grade_number) {
      result.push(a2[j]);
      j++;
    } else {
      result.push(a1[i]);
      i++;
    }
  }

  while (i < a1.length) {
    result.push(a1[i]);
    i++;
  }

  while (j < a2.length) {
    result.push(a2[j]);
    j++;
  }

  return result;
}

function mergeSort2(arr) {
  if (arr.length == 0) return;
  if (arr.length == 1) return arr;

  let middle = Math.floor(arr.length / 2);
  let left = arr.slice(0, middle);
  let right = arr.slice(middle);

  return merge2(mergeSort2(left), mergeSort2(right));
}

function merge(left, right) {
  let result = [];
  while (left.length > 0 && right.length > 0) {
    if (left[0].class_grade_number < right[0].class_grade_number) {
      result.push(left.shift());
    } else {
      result.push(right.shift());
    }
  }
  return result.concat(left, right);
}

function mergeSort(array) {
  // 和 0 做位元運算符 OR 運算, 可以去除小數點的部分; 目前有 C, js 可以這麼做(較低階的語言)
  // JavaScript 中，使用位元 OR 運算符 | 對數字進行運算時，會將其轉換為 32 位元有符號整數，然後執行按位 OR 運算。
  // 在這個過程中，小數部分將被移除，因為這些運算只影響整數部分。
  if (array.length <= 1) return array;
  let middle = (array.length / 2) | 0;
  let left = array.slice(0, middle);
  let right = array.slice(middle);

  return merge(mergeSort(left), mergeSort(right));
}
