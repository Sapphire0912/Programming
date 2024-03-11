// 可以用 object method 和 math method 做

/* 1. 電腦科學中String的subsequence是指，可以通過刪除零個或多個元素而不改變剩餘元素的順序，
      從而產生的新的String，就是原先String的subsequence。
      例如: book是brooklyn的subsequence。寫出一個被稱為 isSubsequence 的函式。
      此函式能夠給定任兩個String，並且回傳一個 boolean 值，
      判斷第一個string是不是第二個string的subsequence。 
*/
function isSubsequence(target, string) {
  if (target.length == 0) return true;
  let targetIndex = 0;
  for (let i = 0; i < string.length; i++) {
    if (target[targetIndex] == string[i]) {
      targetIndex += 1;
    }
    if (targetIndex == target.length) return true;
  }
  return false;
}
// console.log(isSubsequence("book", "brooklyn")); // true
// console.log(isSubsequence("CAATCGA", "TCAATCAGGATCCGCTGA")); // true
// console.log(isSubsequence("AATTAA", "TCAATCAGGATCCGCTGA")); // false

/* 2. 老鼠毒藥問題: 有 100 個一模一樣的瓶子，其中有 99 瓶是普通的水，有一瓶是毒藥。
      任何喝下毒藥的生物都會在一星期之後死亡。現在，你有一星期的時間，
      請問你最少可以用幾隻老鼠就檢測出毒藥是哪一瓶，以及如何檢驗出哪個瓶子裡有毒藥？
      若有1000個一模一樣的瓶子，其中有 999 瓶是普通的水，有一瓶是毒藥，那又需要最少用幾隻老鼠呢? 
*/
function mousePoison(bottle) {
  let mouse = 1;
  while (2 ** mouse <= bottle) {
    mouse += 1;
  }
  return mouse;
}
// console.log(mousePoison(100));
// console.log(mousePoison(1000));

/* 3. 100位囚犯排排站，站在奇數位的人槍斃，偶數位留下，不斷重複這個過程直到剩下一個人。
      請問，若要活到最後，一開始要站在100中的第幾號位置? 若有1000名囚犯呢?一開始要站在第幾號位置? 
*/
function alg(number) {
  let n = 1;
  while (2 ** n <= number) {
    n++;
  }
  return 2 ** (n - 1);
}
// console.log(alg(1000));

/* 4. 請證明，任何使用比較array元素大小來做排序的演算法，其最好的時間複雜度是： O(n log2_n)*/
/* A. Merge sort */
function merge(left, right) {
  let result = [];
  while (left.length > 0 && right.length > 0) {
    if (left[0] < right[0]) {
      result.push(left.shift());
    } else {
      result.push(right.shift());
    }
  }
  console.log(result.concat(left, right));
  return result.concat(left, right);
}

function mergeSort(array) {
  if (array.length <= 1) return array;
  let middle = Math.floor(array.length / 2);
  let left = array.slice(0, middle);
  let right = array.slice(middle);

  return merge(mergeSort(left), mergeSort(right));
}

// mergeSort([2, 11, 8, 9, 34, 51, 17, 6, 1, -8, 30, 13]);

/* 5. 8皇后問題, 改成輸入 n 皇后來計算出獨立解答數 */
let Perfect = 0;
queen(8);
console.log("Number of Perfect Solution is " + Perfect);

function queen(n) {
  let arr = [];
  for (let i = 0; i < n; i++) {
    let reg = [];
    for (let j = 0; j < n; j++) {
      reg.push(null);
    }
    arr.push(reg);
  }

  let i = 0;
  let j = 0;
  let loop = true;
  while (loop) {
    console.log(i, j);
    arr[i][j] = "Q";

    // 檢查 Q 是否可以放置
    let violation = false;
    let k = 0;
    while (k < i) {
      // 檢查 column 是否衝突
      if (arr[k][j] == "Q") violation = true;
      k++;
    }
    k = 0;
    while (k < j) {
      // 檢查 row 是否衝突
      if (arr[i][k] == "Q") violation = true;
      k++;
    }
    k = 1;
    let l = -1;
    while (i + k < n && j + l >= 0) {
      // 檢查左下角是否衝突
      if (arr[i + k][j + l] == "Q") violation = true;
      k++;
      l--;
    }
    k = -1;
    while (i + k >= 0 && j + k >= 0) {
      // 檢查右上角是否衝突
      if (arr[i + k][j + k] == "Q") violation = true;
      k--;
    }
    // 當沒有衝突的時候, 代表該位置可以放置 Q
    if (!violation) {
      console.log("OK");
      console.log(arr);
      // 當已經放置到最後一個 column 時, 要顯示 array 並且換下個 row 繼續開始檢查
      if (j == n - 1) {
        Perfect++;
        console.log("Perfect");
        console.log(arr);
        arr[i][j] = null;
        i++;
      } else {
        i = 0;
        j++;
      }
    }
    if (violation) {
      console.log("Not OK");
      console.log(arr);
      arr[i][j] = null;
      i++;
    }

    function check() {
      // go back to the previous column
      j--;
      for (let b = 0; b < arr.length; b++) {
        if (arr[b][j] == "Q") {
          arr[b][j] = null;
          console.log("b and j is ");
          console.log(b, j);
          i = b + 1;
          break;
        }
      }
    }

    while (i >= n) {
      check();
      if (j < 0) {
        console.log("dead end");
        loop = false;
        break;
      }
    }
  }
}
