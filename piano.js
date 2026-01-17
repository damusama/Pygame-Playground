// iOS対策
let audioEnabled = false;
document.addEventListener("touchstart", () => { audioEnabled = true; }, { once: true });

// 白鍵・黒鍵
const whiteKeys = document.querySelectorAll(".white");
const blackKeys = document.querySelectorAll(".black");

// 白鍵幅
const whiteWidth = window.innerWidth / whiteKeys.length;

// 白鍵配置
whiteKeys.forEach((key, i) => {
  key.style.width = `${whiteWidth}px`;
  key.style.height = "100%";
  key.style.left = `${i * whiteWidth}px`;
});

// 黒鍵配置
const blackOffsets = [
  0.65, 1.65, 3.65, 4.65, 5.65,  // 1オクターブ
  7.65, 8.65, 10.65, 11.65, 12.65 // 2オクターブ
];

blackKeys.forEach((key, i) => {
  key.style.width = `${whiteWidth * 0.6}px`;
  key.style.height = "60%";
  key.style.left = `${blackOffsets[i] * whiteWidth}px`;
});

// 鍵盤全体のクリック
document.querySelectorAll(".key").forEach(key => {
  const play = () => {
    const note = key.dataset.note;
    console.log(`再生: ${note}`);
    const audio = new Audio(`sounds/${encodeURIComponent(note)}.wav`);
    audio.currentTime = 0;
    audio.play().catch(err => console.error(`エラー: ${note}`, err));
  };

  key.addEventListener("mousedown", play);
  key.addEventListener("touchstart", e => {
    e.preventDefault(); // スクロール誤動作防止
    play();
  });
});


