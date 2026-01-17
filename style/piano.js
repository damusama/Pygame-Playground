let ctx = null;

// Audio有効化
const enableAudio = () => {
  ctx = new (window.AudioContext || window.webkitAudioContext)();
  document.removeEventListener("touchstart", enableAudio);
};
document.addEventListener("touchstart", enableAudio);

// 鍵盤レイアウト
const whiteKeys = document.querySelectorAll(".white");
const blackKeys = document.querySelectorAll(".black");

const whiteWidth = window.innerWidth / whiteKeys.length;

whiteKeys.forEach((key, i) => {
  key.style.width = `${whiteWidth}px`;
  key.style.height = "100%";
  key.style.left = `${i * whiteWidth}px`;
});

const blackOffsets = [0.7, 1.7, 3.7, 4.7, 5.7];

blackKeys.forEach((key, i) => {
  const octave = Math.floor(i / 5);
  const pos = blackOffsets[i % 5];
  key.style.width = `${whiteWidth * 0.6}px`;
  key.style.height = "60%";
  key.style.left = `${(octave * 7 + pos) * whiteWidth}px`;
});

// 和音
document.querySelectorAll(".key").forEach(key => {
  const play = () => {
    const note = key.dataset.note;
    const audio = new Audio(`/static/sounds/${note}.wav`);
    audio.currentTime = 0;
    audio.play();
  };

  key.addEventListener("mousedown", play);
  key.addEventListener("touchstart", e => {
    e.preventDefault();
    play();
  });
});
