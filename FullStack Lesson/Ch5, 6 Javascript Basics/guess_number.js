let number = Math.round(Math.random() * 100, 0);
let low = 0;
let high = 99;

while (user_number != number) {
  let user_number = Number(
    prompt("請輸入 " + low + " ~ " + high + " 之間的整數：")
  );

  if (user_number < low || user_number > high) {
    alert("輸入數字無效，請重新輸入！");
    continue;
  } else {
    if (user_number > number) {
      high = user_number;
    } else if (user_number < number) {
      low = user_number;
    } else {
      alert("猜到了!");
    }
  }
}
