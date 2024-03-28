let button = document.querySelector("button");
button.addEventListener("click", () => {
  let form = document.querySelector("form");
  form.reset();
});

// 顯示出事件 e 的內容
// let button2 = document.querySelectorAll("button")[2];
// button2.addEventListener("click", (e) => {
//   console.log(e);
// });

// 偵測使用者鍵盤按下哪個按鍵
// window.addEventListener("keydown", (e) => {
//   console.log(e);
// });

// event.target 會顯示觸發事件的對象是哪個 element
let button2 = document.querySelectorAll("button")[2];
button2.addEventListener("click", (e) => {
  console.log(e.target);
});

// preventDefault() 可以阻止事件被傳遞, 下面的程式碼可以阻止表單內容被提交出去
let form = document.querySelector("form");
form.addEventListener("submit", (e) => {
  e.preventDefault();
});
