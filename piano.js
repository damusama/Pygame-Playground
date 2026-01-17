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
  0.65, 1.65, 3.65, 4.65, 5.65,  // 1オクターブ（C#4, D#4, F#4, G#4, A#4）
  7.65, 8.65, 10.65, 11.65, 12.65 // 2オクターブ（C#5, D#5, F#5, G#5, A#5）
];

blackKeys.forEach((key, i) => {
  if (i < blackOffsets.length) {
    key.style.width = `${whiteWidth * 0.6}px`;
    key.style.height = "60%";
    key.style.left = `${blackOffsets[i] * whiteWidth}px`;
    key.style.top = "0";
  }
});

// 鍵盤全体のクリック
document.querySelectorAll(".key").forEach(key => {
  const play = () => {
    const note = key.dataset.note;
    const filename = note.replace('#', 'b');
    console.log(`再生: ${note} -> ${filename}`);
    const audio = new Audio(`sounds/${filename}.wav`);
    audio.currentTime = 0;
    audio.play().catch(err => console.error(`エラー: ${filename}`, err));
  };

  key.addEventListener("mousedown", play);
  key.addEventListener("touchstart", e => {
    e.preventDefault(); // スクロール誤動作防止
    key.classList.add("pressed");
    play();
  });
  
  key.addEventListener("touchend", e => {
    key.classList.remove("pressed");
  });
});


