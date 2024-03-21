let age = 75;
let price;

// price = age <= 18 ? 50 : 150;
// console.log(price);

// 3 個 condition
price = age <= 18 ? 50 : age <= 60 ? 150 : 75;
// console.log(price);

function multiply(a = 0, b = 0) {
  return a * b;
}
// console.log(multiply());

// IIFE 宣告
(function f1() {
  console.log(0);
})();

let f1 = 10;

// // Destructuring Assignment
// let arr = [1, 2, 3, 4, 5, 6, 7];
// let [a1, a2, a3, a4, a5, a6, a7] = arr;
// let [b1, b2, ...everything] = arr;
// // console.log(everything);

// let food = {
//   name: "rice",
//   prices: 100,
//   weight: 500,
// };
// let { name, prices, weight } = food;
// console.log(name, prices, weight);

// try syntax
// try {
//   whatever();
// } catch (error) {
//   if (error instanceof ReferenceError) {
//     console.log("發生 ReferenceError: " + error.message);
//   } else {
//     console.log("發生其他種類的錯誤");
//   }
// }

// throw and catch
// 客製化錯誤訊息
class NotArrayError extends TypeError {
  constructor(message) {
    super(message);
  }
  printSolution() {
    return "確定參數是 array, 再執行";
  }
}

function sum(arr) {
  if (!Array.isArray(arr)) {
    throw new NotArrayError("參數並非 array");
  }
  let result = 0;
  arr.forEach((element) => {
    result += element;
  });
  return result;
}

try {
  sum("hello");
} catch (e) {
  console.log(e);
  console.log(e.printSolution()); // 確定參數是 array, 再執行
  //   NotArrayError [TypeError]: 參數並非 array
}
