// 1. 編寫一個名為reverse的函式，參數為一個String，回傳值為順序反轉的String。
function reverse(string) {
  let new_string = "";
  for (let i = string.length - 1; i >= 0; i--) {
    new_string += string[i];
  }
  return new_string;
}
// console.log(reverse("abcd")); // returns "dcba"
// console.log(reverse("I am a good guy.")); // returns ".yug doog a ma I"

// 2. 編寫一個名為swap的函式，參數為一個String，回傳值為大小寫反轉的String。
function swap(string) {
  let new_string = "";
  for (let i = 0; i < string.length; i++) {
    if (string[i].toUpperCase() == string[i]) {
      new_string += string[i].toLowerCase();
    } else {
      new_string += string[i].toUpperCase();
    }
  }
  return new_string;
}
// console.log(swap("Aloha")); // returns "aLOHA"
// console.log(swap("Love you.")); // returns "lOVE YOU."

/* 3. 編寫一個名為isPrime的函式，它接受一個整數作為參數，
      回傳值為一個boolean，告訴我們參數是否為一個質數。 */
function isPrime(number) {
  if (number == 1) return false;
  let n = 2;
  while (n < number) {
    if (number % n == 0) {
      return false;
    }
    n++;
  }
  return true;
}

// console.log(isPrime(2));
// console.log(isPrime(5));
// console.log(isPrime(91));
// console.log(isPrime(1000000));

/* 4. 回文是指，正著讀或反著讀都一樣的句子。例如:【上海自來水來自海上】是迴文。寫一個名為palindrome的函式，
      它接受一個String作為參數，回傳值為一個boolean，告訴我們參數是否為回文。*/
function palindrome(string) {
  let end = string.length / 2;
  if (string.length % 2 != 0) {
    end = end - 1;
  }
  for (let i = 0; i <= end; i++) {
    if (string[i] != string[string.length - 1 - i]) {
      return false;
    }
  }
  return true;
}

// console.log(palindrome("bearaeb"));
// console.log(palindrome("whatever revetahw"));
// console.log(palindrome("Aloha, how are you today?"));

/* 5. 編寫一個名為pyramid的函式，功能為按以下模式打印出星星層 
        pyramid(1);
        //*
        pyramid(2);
        //  *
        // ***
        pyramid(4);
        //    *
        //   ***
        //  *****
        // *******
*/
function pyramid(n) {
  for (let i = 1; i <= n; i++) {
    let star = "";
    for (let j = i; j <= n - 1; j++) {
      star += " ";
    }
    for (let k = 1; k <= 2 * i - 1; k++) {
      star += "*";
    }
    console.log(star);
  }
}

// pyramid(6);

/* 6. 編寫一個名為inversePyramid的函式，功能為按以下模式打印出星星層：
        inversePyramid(4);
        // *******
        //  *****
        //   ***
        //    *
 */
function inversePyramid(n) {
  for (let i = 1; i <= n; i++) {
    let star = "";
    for (let j = 1; j <= i - 1; j++) {
      star += " ";
    }
    for (let k = 1; k <= 2 * (n - i) + 1; k++) {
      star += "*";
    }
    console.log(star);
  }
}
// inversePyramid(4);

/* 7. 編寫一個名為factorPrime的函式，唯一的參數是個整數n，回傳值是一個String，表示n的質因數分解結果。 */
function factorPrime(number) {
  let result = "";
  let factor = 2;
  while (factor <= number) {
    if (number % factor == 0) {
      number /= factor;
      result += factor;
      if (number == 1) {
        return result;
      } else {
        result += " x ";
      }
      factor = 2;
    } else {
      factor++;
    }
  }
  return result;
}
// console.log(factorPrime(96));
