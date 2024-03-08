// let x = 2 ** 53; // js 數字的最大值
// console.log(x);
// console.log(x + 1);

// let y = -(2 ** 53); // js 數字的最小值
// console.log(y);
// console.log(y - 1);

// let a = 10;
// console.log(typeof a);
// console.log(typeof a.toString());

// let pi = 3.1415926525;
// console.log(typeof pi);
// console.log(typeof pi.toFixed(2)); // String

// let str = "Sapphire";
// console.log(str.slice(0, 4));
// console.log(str.indexOf("p"));
// console.log(str.indexOf("w"));

// console.log(str.toLowerCase());
// console.log(str);

// let sentence = "My name is Eric.";
// console.log(sentence.split(" "));
// console.log(sentence.charCodeAt(sentence.indexOf("a")));

// logical operator 在不同 data type 的運算
// console.log(1 && 100); // True, return 100 (right side value)
// console.log(0 && 100); // False, return 0 (left side value)

// console.log("Sapphire" || "資料讀取失敗"); // True, return Sapphire (left side value)
// console.log("" || "資料讀取失敗"); // False, return 資料讀取失敗 (right side value)
// console.log(NaN || 100); // False, return 100 (right side value)

// function f() {
//   console.log("This is my first function.");
// }

// f();

// let array1 = [1, 2, 3, 4, 5];
// let array2 = array1;
// array2[2] = 100;

// console.log(array1); // [1, 2, 100, 4, 5]
// console.log(array2); // [1, 2, 100, 4, 5]

// let a = [1, 2, 3];
// let b = [1, 2, 3];
// let c = a;

// console.log(a == b); // false
// console.log(a === b); // false
// console.log(a == c); // true
// console.log(a === c); // true

// let count = [1, 2, 3, 4, 5];
// count.push(6);
// console.log(count);
// count.shift();
// console.log(count);
// count.pop();
// console.log(count);
// count.unshift(100);
// console.log(count);

// let obj = {
//   // properties (key-value-pair), methods
//   name: "Eric",
//   sayHi() {
//     console.log(this.name + " says hi,");
//   },
// };

// obj.sayHi();

// let arr = [1, 2, 3];
// function f() {
//   return 0;
// }

// console.log(typeof arr); // object
// console.log(Array.isArray(arr)); // true
// console.log(typeof f); // function
