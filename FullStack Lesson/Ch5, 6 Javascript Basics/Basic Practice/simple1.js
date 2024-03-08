// 1. 編寫一個名為“printEvery3()”的函式，它打印出等差數列 1, 4, 7, …, 88。
function printEvery3() {
  for (let i = 1; i <= 88; i += 3) {
    if (i === 88) {
      break;
    }
    console.log(i);
  }
}

// 2. 編寫一個名為table9to9的函式，它打印出九九乘法表的內容。
function table9to9() {
  for (let i = 1; i < 10; i++) {
    for (let j = 1; j < 10; j++) {
      console.log(i + "x" + j + "=" + i * j);
    }
  }
}

/* 3. 編寫一個名為isUpperCase的函式，唯一的參數是一個String，
      其功能為來檢查參數中String的第一個字母是否為大寫。 */
function isUpperCase(string) {
  if (string.length == 0) {
    return false;
  } else {
    let checkString = string.toUpperCase();
    return string[0] == checkString[0];
  }
}

/* 4. 編寫一個名為isAllUpperCase的函式，唯一的參數是一個String，
      其功能為來檢查參數中String的所有字母是否為大寫。*/
function isAllUpperCase(string) {
  if (string.length == 0) {
    return false;
  } else {
    let checkString = string.toUpperCase();
    return string == checkString;
  }
}

/* 5. 編寫一個名為position的函式，唯一的參數是一個String，
      其功能為找到參數String當中的第一個大寫字母，並且回傳大寫字母的值以及其index位置。 */
function position(string) {
  if (string.length == 0) {
    return NaN;
  } else {
    for (let i = 0; i < string.length - 1; i++) {
      let check = string[i].toUpperCase();
      if (check == string[i]) {
        return string[i], i;
      }
    }
  }
}

/* 6. 編寫一個名為findSmallCount的函式，其參數為一個整數的array以及另一個整數，功能是回傳一個整數，
      來表示array中有多少元素小於第二個參數。*/
function findSmallCount(array, number) {
  let count = 0;
  for (let i = 0; i < array.length; i++) {
    if (array[i] < number) {
      count++;
    }
  }
  return count;
}

/* 7. 編寫一個名為findSmallerTotal的函式，其參數為一個整數的array以及另一個整數，
      回傳值為array中小於第二個參數的所有元素的總和。*/
function findSmallTotal(array, number) {
  let total = 0;
  for (let i = 0; i < array.length; i++) {
    if (array[i] < number) {
      total += array[i];
    }
  }
  return total;
}

/* 8. 編寫一個名為stars的函式，功能為按以下模式打印出星星層 
    stars(1);
    // *
    stars(4);
    // *
    // **
    // ***
    // **** 
*/
function stars(number) {
  for (let i = 1; i <= number; i++) {
    let star = "";
    for (let j = 1; j <= i; j++) {
      star += "*";
    }
    console.log(star);
  }
}

/* 9. 編寫一個名為stars2的函式，功能為按以下模式打印出星星層： 
    stars2(1);
    // *
    stars2(2);
    // *
    // **
    // *
    stars2(3);
    // *
    // **
    // ***
    // **
    // *
    stars2(4);
    // *
    // **
    // ***
    // ****
    // ***
    // **
    // *
*/
function stars2(number) {
  for (let i = 1; i <= number; i++) {
    let up_star = "";
    for (let j = 1; j <= i; j++) {
      up_star += "*";
    }
    console.log(up_star);
  }
  for (let k = number - 1; k > 0; k--) {
    let low_star = "";
    for (let j = 1; j <= k; j++) {
      low_star += "*";
    }
    console.log(low_star);
  }
}

/* 10. 在數學上，費波那契數是以遞迴的方法來定義：
       F_0 = 0, F_1 = 1, F_n = F_{n-1} + F_{n - 2},n >= 2 */
function fib(n) {
  if (n == 0) {
    return 0;
  } else if (n == 1) {
    return 1;
  } else {
    return fib(n - 1) + fib(n - 2);
  }
}
