/* 1. 編寫一個名為mySort的函式，參數為一個array of numbers，回傳值為一個將元素由小到大排序的array。*/
function mySort(array) {
  if (array.length == 0) {
    return [];
  }
  // bubble sort
  for (let i = 0; i < array.length; i++) {
    for (let j = i + 1; j < array.length; j++) {
      if (array[i] > array[j]) {
        let temp = array[i];
        array[i] = array[j];
        array[j] = temp;
      }
    }
  }
  return array;
}

// console.log(mySort([17, 0, -3, 2, 1, 0.5, -9, 11]));

/* 2. 落地問題: 一球從h米高度自由落下，每次落地後反跳回原高度的一半，再落下。求小球在第n次落地時，總共經過多少公尺？
      編寫一個名為distance的函式，參數為h與n，回傳值為小球經過的總距離。*/
function distance(h, n) {
  let dis = h;
  let i = 1;

  while (i < n) {
    dis += h;
    h /= 2;
    i++;
  }
  return dis;
}
// console.log(distance(100, 4)); // 275
// console.log(distance(500, 7)); // 1484.375

/* 3. 打印出所有的"水仙花數"。所謂"水仙花數"是指一個三位數，其各位數字立方和等於該數本身。例如：153是一個"水仙花數"，
      因為$153=1^3+5^3+3^3$，或370也是水仙花數，因為$370=3^3+7^3+0^3$。*/
function PPDI() {
  for (let a = 1; a < 10; a++) {
    for (let b = 0; b < 10; b++) {
      for (let c = 0; c < 10; c++) {
        if (a ** 3 + b ** 3 + c ** 3 == a * 100 + b * 10 + c) {
          console.log("" + a + b + c);
        }
      }
    }
  }
}
// PPDI();

/* 4. 求s=a+aa+aaa+aaaa+aa...a的值，其中a是小於10的數字，相加的項數為n。例如，當a = 2，n=5時，s=2+22+222+2222+22222。
      若a = 2, n = 3，則輸出結果的形式如：2+22+222 = 246。
      編寫一個名為calc的函式，參數為a與n，回傳值為s。*/
function calc(a, n) {
  let result = 0;
  for (let i = 1; i <= n; i++) {
    result += i * 10 ** (n - i);
  }
  return result * a;
}
// console.log(calc(2, 3)); // returns 246
// console.log(calc(8, 5)); // returns 98760

/* 5. 編寫一個名為"shuffle()”的函數，唯一的參數為一個array of integers，return type也是array of integers，
      返回的array與參數array的元素相同，但元素順序為隨機排序的結果。*/
function shuffle(array) {
  let length = array.length;
  let bitArray = [];

  // 轉成 2 進制表示 array.length
  while (length >= 1) {
    bit_ = length % 2;
    if (bit_ != 0) {
      length = (length - 1) / 2;
    } else {
      length = length / 2;
    }
    bitArray.push(bit_);
  }

  // 做偽隨機數運算 例如: 100: 1 xor 0 = 1, add to LSB and move MSB -> 001
  let bit_length = bitArray.length;

  // 停止條件: 當數字 = array.length 時
  let num;
  let indexArray = [];
  while (num != array.length) {
    num = 0;
    let b1 = bitArray[bit_length - 1];
    let b2 = bitArray[bit_length - 2];
    let new_bit = b1 ^ b2; // b1 xor b2;

    // update bitArray
    for (let i = bit_length - 2; i >= 0; i--) {
      bitArray[i + 1] = bitArray[i];
    }
    bitArray[0] = new_bit;

    // 計算 bit 的 10 進制是多少
    for (let i = 0; i < bit_length; i++) {
      num = num + bitArray[i] * 2 ** i;
    }

    // 若數字小於 array.length 的長度, 再加到索引值裡面
    if (num <= array.length) {
      indexArray.push(num - 1);
    }
    console.log(indexArray);
  }

  // 將 array 中的數字打散(從最後一個數字開始)
  let result = [];
  for (let i = indexArray.length - 1; i >= 0; i--) {
    result.push(array[indexArray[i]]);
  }

  return result;
}

console.log(shuffle([2, 11, 37, 42, 80, 66, 97, 5]));
