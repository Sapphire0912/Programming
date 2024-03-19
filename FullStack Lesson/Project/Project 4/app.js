let hero = document.querySelector(".hero"); // 圖片動畫
let slider = document.querySelector(".slider"); // 顯示漸層動畫
let animation = document.querySelector("section.animation-wrapper"); // 最下層的背景(容器)

const time_line = new TimelineMax();

/* 
parameter1: 要控制的對象, 
parameter2: duration, 設定 1 代表 1 秒
parameter3: 控制對象的原始狀態 
parameter4: 控制對象的動畫結束後的狀態
parameter5: 設定控制對象的動畫的起始時間, 設定 "-=1.2", 代表提早 1.2 秒就執行動畫
*/
time_line
  .fromTo(hero, 1, { height: "0%" }, { height: "100%", ease: Power2.easeInOut })
  .fromTo(
    hero,
    1.2,
    { width: "80%" },
    { width: "100%", ease: Power2.easeInOut }
  )
  .fromTo(
    slider,
    1,
    { x: "-100%" },
    { x: "0%", ease: Power2.easeInOut },
    "-=1.2"
  )
  .fromTo(animation, 0.3, { opacity: 1 }, { opacity: 0 });

// .fromTo(animation, 0.3, { opacity: 1 }, { opacity: 0 }); 動畫結束之後讓整個容器(和內容)都隱藏起來

window.setTimeout(() => {
  animation.style.pointerEvents = "none";
}, 2500);
