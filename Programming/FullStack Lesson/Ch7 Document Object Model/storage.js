localStorage.setItem("name", "Sapphire");
// localStorage.setItem("age", "24");

// let myName = localStorage.getItem("name");
// let myAge = localStorage.getItem("age");

// console.log(myName);
// console.log(myAge);

// localStorage.removeItem("age");
// localStorage.clear();

// 將資料轉成 JSON 格式並儲存成 JSON
// localStorage.setItem("Array", [1, 2, 3, 4, 5]);
localStorage.setItem("birth", "2000-10-02");
// localStorage.clear();

// 若直接將 Data 儲存到 localStorage, 不管甚麼 object 都會變成 string,
// 即使是 array 也是, 因此才利用 JSON 的方式做轉換
// let array = localStorage.getItem("Array");
// Uncaught TypeError: array.forEach is not a function
// array.forEach((n) => {
//   console.log(n);
// });

// 以下是正確的做法
let myArray = [1, 2, 3, 4, 5];
localStorage.setItem("myArray", JSON.stringify(myArray));
let dataArray = JSON.parse(localStorage.getItem("myArray"));
console.log(dataArray);
dataArray.forEach((n) => {
  console.log(n);
});
