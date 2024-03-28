let myButton = document.querySelector("#my-btn");
// myButton.addEventListener("click", () => {
//   alert("點擊了 button");
// });

let body = document.querySelector("body");
let myH4 = document.createElement("h4");
let myH3 = document.createElement("h3");
myH4.innerText =
  'H4: <a href="#">這是用來測試 appendChild 的方法, 以及用 innerText 屬性</a>';
myH3.innerHTML =
  'H3: <a href="#">這是用來測試 appendChild 的方法, 以及用 innerHTML 屬性</a>';
body.appendChild(myH4);
body.appendChild(myH3);

// classList 屬性: 可以取得當前 element 的 classList (列表)
let p_tag = document.querySelector(".hello");
// console.log(p_tag.classList);
p_tag.classList.add("evening");
// console.log(p_tag.classList);
p_tag.classList.remove("morning");
// console.log(p_tag.classList);

// 每觸發一次事件, 就會讓 p_tag 的 class, 新增 -> 刪除 red class -> 新增 -> 刪除 ...
// 類似開燈關燈的功能, 數位邏輯的雙穩態電路
p_tag.addEventListener("click", () => {
  p_tag.classList.toggle("red");
});

// 檢查 p_tag 是否包含 red 的 class
// console.log(p_tag.classList.contains("red"));

// let a = document.querySelector("a");
// console.log(a.getAttribute("href"));

let button = document.querySelector("button");
button.style.backgroundColor = "green";
button.style.color = "white";
// button.style = "font-size: 1.05rem"; 或是把想要的東西全部寫在 style 屬性裡

button.addEventListener("click", () => {
  let a = document.querySelector("a");
  a.remove();
});
