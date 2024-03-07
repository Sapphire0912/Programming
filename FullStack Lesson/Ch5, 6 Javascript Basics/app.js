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
console.log(1 && 100); // True, return 100 (right side value)
console.log(0 && 100); // False, return 0 (left side value)

console.log("Sapphire" || "資料讀取失敗"); // True, return Sapphire (left side value)
console.log("" || "資料讀取失敗"); // False, return 資料讀取失敗 (right side value)
console.log(NaN || 100); // False, return 100 (right side value)
