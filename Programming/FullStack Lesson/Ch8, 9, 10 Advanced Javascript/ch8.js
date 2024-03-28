// console.log(typeof Infinity);
// console.log(typeof NaN);

let num1 = [1, 2, 3];
let num2 = [4, 5, 6];

// concat array method 1
// let result = num1 + num2; // typeof result -> string
// let result = num1.concat(num2);
// console.log(result);

// Spread Syntax and Rest Parameters
const parts = ["肩膀", "膝蓋"];
const otherParts = ["頭", ...parts, "身體", "腳"]; // 將 parts 插入 otherParts 中
// console.log(otherParts);

// Spread Syntax 作法不是 copy by reference
const arr1 = [1, 2, 3];
const arr2 = [...arr1];

arr2.push(4);
// console.log(arr1, arr2); // [ 1, 2, 3 ] [ 1, 2, 3, 4 ]

// concat array method 2
// console.log([...arr1, ...arr2]);

function sum(x, y, z, i = 1, j = 1) {
  return x + y + z + i + j;
}

// 可以做為參數傳遞給 function
let arr3 = [1, 2, 3];
// console.log(sum(...arr3));
// console.log(sum(10, ...arr3, 8));

function sum2(...theArgs) {
  //   console.log(theArgs);
  let total = 0;
  for (let i = 0; i < theArgs.length; i++) {
    total += theArgs[i];
  }
  return total;
}

// console.log(sum2(1, 2, 3, 4, 5, 6, 7, 8));

// const { performance } = require("perf_hooks");  // 此為 node.js 提供的功能
// let startTime = performance.now();
// const times = 100000000;

// for (let i = 0; i < times; i++) {
//   let a = new String("abcabcabcabc");
// }
// let endTime = performance.now();
// let timeDiff = (endTime - startTime).toFixed(2);

// console.log("wrapper object 建立 1 億次時 execution time: ", timeDiff, " ms.");

// let startTime2 = performance.now();

// for (let i = 0; i < times; i++) {
//   let a = "abcabcabcabc";
// }
// let endTime2 = performance.now();
// let timeDiff2 = (endTime2 - startTime2).toFixed(2);

// console.log(
//   "primitive data type 建立 1 億次時 execution time: ",
//   timeDiff2,
//   " ms."
// );

// string comparsion
// console.log("abandon" < "apple"); // true
// console.log("12" < "2"); // true

// advanced array method
const Languages = [
  { name: "Python", rating: 9.5, popularity: 9.7, trending: "super hot" },
  { name: "Java", rating: 9.4, popularity: 8.5, trending: "hot" },
  { name: "C++", rating: 9.2, popularity: 7.7, trending: "hot" },
  { name: "PHP", rating: 9.0, popularity: 5.7, trending: "decreasing" },
  { name: "JS", rating: 8.5, popularity: 8.7, trending: "hot" },
];

// let languages = ["Java", "Python", "C++", "JavaScript"];
// let result = languages.map((lang) => lang.toUpperCase());
// console.log(result);

// 在後端的資料通常會以 object 方式呈現, 所以要熟悉這裡的應用
let result2 = Languages.map((lang) => {
  return lang.name.toUpperCase();
});
// console.log(result2);

let result3 = Languages.find((lang) => {
  //   return lang.popularity > 9.8; // undefined
  return lang.popularity > 8.0; // { name: 'Python', rating: 9.5, popularity: 9.7, trending: 'super hot' }
});
// console.log(result3);

let result4 = Languages.filter((lang) => {
  return lang.popularity >= 8.0; // 所有符合條件的元素都會被存到 result array 裡面
});
// console.log(result4);

let result5 = Languages.some((lang) => lang.popularity < 6);
// console.log(result5); // true

let result6 = Languages.every((lang) => lang.popularity < 6);
// console.log(result6); // false

let arr4 = [1, 2, 3, 4, 5];
let newArr = arr4.forEach((i) => {
  //   console.log(i ** 2);
  return i; // undefined
});
// console.log(newArr); // undefined

let sol = arr4.map((i) => i ** 2);
// console.log(sol); // [ 1, 4, 9, 16, 25 ]

// Sort
let myArr = [1, 5, 3, 2, 4, 7, 8, 0];
let mySortedArr = [...myArr];
mySortedArr.sort();
// console.log(myArr);
// console.log(mySortedArr);

let data = [4, 1, 9, 25, 16];
data.sort();
// console.log(data); // [ 1, 16, 25, 4, 9 ]
// 但是理想的是想要由數字的小到大排序 [1, 4, 9, 16, 25]
// JS 預設排序是利用 Unicode 來做排序
// 若要按照數字大小排序則如下:
data.sort((a, b) => a - b);
// console.log(data); // [ 1, 4, 9, 16, 25 ]
data.sort((a, b) => b - a);
// console.log(data); // [ 25, 16, 9, 4, 1 ]

let fruits = ["Watermelon", "Apple", "Banana"];
// 按照字串長度做排序
fruits.sort((a, b) => {
  if (a.length > b.length) {
    return 1;
  } else {
    return -1;
  }
});
// console.log(fruits); // [ 'Apple', 'Banana', 'Watermelon' ]

// for of loop & for in loop
let numbers = [10, 20, 30, 40];
for (n of numbers) {
  console.log(n); // return value
}

for (i in numbers) {
  console.log(i); // return index
  console.log(numbers[i]);
}

let info = {
  name: "Eric",
  age: 24,
};
for (let key in info) {
  console.log("key: ", key);
  console.log(info[key]);
}
