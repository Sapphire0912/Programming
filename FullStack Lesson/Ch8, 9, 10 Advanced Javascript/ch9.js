// let a = 3;
// function area(s) {
//   /*
//     1. 執行 function 時, 會進入 creation phase
//     1.1 創建 argument object
//     => s = 3
//     1.2 創建 scope
//     1.3 創建 this
//     1.4 將 variables, class, function 分到記憶體
//     => (這裡沒有就不用進行此步驟)
//   */
//   return s * s;
// }

// let result = area(a);
// console.log(result);

// /*
// 1. (JS 在建立全域執行環境, 第一階段做的事情)creation phase:
// 1.1 global object 製作完成
// 1.2 建立 scope
// 1.3 建立 this keyword (指瀏覽器的 window 物件)
// 1.4 將 variables, class, function 分到記憶體
// =>  a -> undefined, result -> undefined, area is a function
// */

// /*
// 2. creation phase 結束後, 進入執行階段 exection phase
// 2.1 a = 3, 執行 function area(a), result = 9;
// 2.2 執行 console.log(result)
// */

// // 這也是為什麼 function 定義在其他地方, 依然可以被呼叫執行

// Hoisting 說明
// hello();

/* 
一旦 Hoisting 發生時(在 creation phase 第4步驟),
會將宣告的 function, variable, class 分到記憶體並移動到最頂層
*/
function hello() {
  console.log("hello");
}

// ReferenceError: Cannot access 'x' before initialization
// -> 在 hoisting 發生時, let x 只被宣告, 但沒有初始值
// console.log(x);
// let x;

// undefined
// -> 在 hoisting 發生時, var y 已經被定義(初始化)是 undefined
// console.log(y);
// var y;

// undefined
/* 
在 hoisting, 已經宣告了 let z 變數. 但到了 exection phase
執行了 console.log(), 發現 z 的值沒有初始值, 因此會顯示 undefined.
*/
// let z;
// console.log(z);

// SyntaxError: Missing initializer in const declaration
/* 在宣告 const 就必須要有初始值 */
// const c;

// if (true) {
//   let i = 10;
//   var j = 10;
//   const k = 10;
// }

// console.log(i); // ReferenceError: i is not defined
// console.log(j); // 10
// console.log(k); // ReferenceError: k is not defined

// Closure 說明
// let myName = "Eric";
// function sayHi() {
//   let myName = "Sapphire";
//   console.log("sayHi(): " + myName + " say hi.");
//   sayHi2();
//   sayHi3();
//   function sayHi3() {
//     console.log("sayHi3(): " + myName + " say hi.");
//   }
// }

// function sayHi2() {
//   console.log("sayHi2(): " + myName + " say hi.");
// }

// sayHi();
// sayHi(): Sapphire say hi.
// sayHi2(): Eric say hi.
// sayHi3(): Sapphire say hi.

// call stack and recursion
// function f1() {
//   console.log("f1 exec.");
//   f2();
//   console.log("f1 exec end.");
// }

// function f2() {
//   console.log("f2 exec.");
//   console.log("f2 exec end.");
// }

// f1();

function fib(n) {
  if (n <= 1) return n;
  return fib(n - 1) + fib(n - 2);
}

// console.log(fib(10));
