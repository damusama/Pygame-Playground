const keys = document.querySelectorAll(".key");

keys.forEach(key => {
  key.addEventListener("touchstart", playNote);
  key.addEventListener("mousedown", playNote);
});

function playNote(e) {
  const note = e.target.dataset.note;
  const audio = new Audio(`/static/sounds/${note}.wav`);
  audio.currentTime = 0;
  audio.play();
}


