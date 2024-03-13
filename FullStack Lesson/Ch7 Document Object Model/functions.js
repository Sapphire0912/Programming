// console.log(f(10, 5));
let f = function (a, b) {
  return a + b;
};

// console.log(f(10, 5));

let Eric = {
  name: "Eric",
  greet() {
    console.log(this.name + " say hello");
  },
  walk: function () {
    console.log(this.name + " is walking.");
  },
};

// Eric.greet();
// Eric.walk();

// higher order function: 函數本身的參數又有一個函數
// callback function: 被作為參數傳遞的函數
function react() {
  alert("Clicked!!!");
}

// window.addEventListener("click", react);
window.addEventListener("click", function () {
  alert("Clicked!!!");
});

/* 
匿名函數優點：
   1. 若程式碼有許多 callback function 都採用 function declaration,
      命名變數時, 都要避開 function declaration.
   2. callback function 名稱其實沒有意義
   3. 程式碼會變乾淨
*/

// IIFE 的宣告方式
(function (a, b) {
  console.log(a + b);
})(10, 5);
