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
// window.addEventListener("click", function () {
//   alert("Clicked!!!");
// });

/* 
匿名函數優點：
   1. 若程式碼有許多 callback function 都採用 function declaration,
      命名變數時, 都要避開 function declaration.
   2. callback function 名稱其實沒有意義
   3. 程式碼會變乾淨
*/

// IIFE 的宣告方式
// (function (a, b) {
//   console.log(a + b);
// })(10, 5);

// Arrow Function Expression
let hello = () => {
  console.log("Hello world");
};

// hello();

let addition = (a, b) => {
  return a + b;
};

// 可以不加 () 宣告
let power_2 = (n) => {
  return 2 ** n;
};

// 不加 {} 會直接 return arrow function 後面的 expression
let multi = (i, j) => i * j;
// console.log(multi(3, 8));

let Sapphire = {
  name: "Sapphire",
  walk: () => {
    // arrow function express 沒有 this keyword 綁定
    console.log("Sapphire is walking.");
    // console.log(this.name + " is walking.");  // undefined is walking
  },
};
// Sapphire.walk();

// forEach() Method
let myLuckyNumbers = [1, 2, 3, 4, 5, 6, 7];
// 若每項都要 +3, 以往的做法要用 for loop 迭代
// for (let i = 0; i < myLuckyNumbers.length; i++) {
//   myLuckyNumbers[i] += 3;
// }

// 利用 forEach 方法, 可以讓每個函數都去執行 plus3 的函數
function plus3(n) {
  console.log(n + 3);
}
// myLuckyNumbers.forEach(plus3);
// myLuckyNumbers.forEach((n) => {
//   console.log(n + 3);
// });

// forEach() 第二個參數 index
// myLuckyNumbers.forEach((n, index) => {
//   console.log(n + " is at index " + index);
// });

// NodeList
let nodeList = document.querySelectorAll(".hello");
nodeList.forEach((hello) => {
  console.log(hello);
});

// HTMLCollection
let HTMLCollection = document.getElementsByClassName("hello");
HTMLAllCollection.forEach((hello) => {
  console.log(hello);
});
// TypeError: HTMLAllCollection.forEach is not a function
