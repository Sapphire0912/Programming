let a = document.querySelector(".a");
let b = document.querySelector(".b");

a.addEventListener("click", () => {
  alert("紅色框的事件監聽器正在被執行");
});

b.addEventListener("click", (e) => {
  e.stopPropagation(); // 避免事件一直不斷往上層元素傳遞
  alert("藍色框的事件監聽器正在被執行");
});

// event bubbling 發生時, event object 的 target 屬性
// 在 child element & parent element 的 event handler 內會是一樣的
let outer = document.querySelector(".outer");
let middle = document.querySelector(".middle");
let inner = document.querySelector(".inner");

outer.addEventListener("click", (e) => {
  console.log("Outer Event Listener.");
  console.log("Event Target: ", e.target);
  console.log("Current Target: ", e.currentTarget);
});

middle.addEventListener("click", (e) => {
  console.log("Middle Event Listener.");
  console.log("Event Target: ", e.target);
  console.log("Current Target: ", e.currentTarget);
});

inner.addEventListener("click", (e) => {
  console.log("Inner Event Listener.");
  console.log("Event Target: ", e.target);
  console.log("Current Target: ", e.currentTarget);
});

// 上面的程式執行後, 會看見 Even target 都是 inner
// 要利用 currentTarget 來得知是哪個 child element 觸發事件
