const days = document.querySelector('.days > .number'),
      hours = document.querySelector('.hours > .number'),
      minutes = document.querySelector('.minutes > .number'),
      seconds = document.querySelector('.seconds > .number');

let countdownTimer = setInterval(() => {
    const currentTime = new Date(),                      // 現在時刻取得
          targetTime = new Date('2022/9/17 0:00:00'),    // 到達目標時刻設定
          remainTime = targetTime - currentTime;         // 差分計算

    // 差分の日、時、分、秒を計算
    const diffDays = Math.floor(remainTime / 1000 / 60 / 60 / 24),
          diffHours = Math.floor(remainTime / 1000 / 60 / 60) % 24,
          diffMinutes = Math.floor(remainTime / 1000 / 60) % 60,
          diffSeconds = Math.floor(remainTime / 1000) % 60;

    // 時刻の更新
    days.innerText = diffDays < 10 ? '0' + diffDays : diffDays;
    hours.innerText = diffHours < 10 ? '0' + diffHours : diffHours;
    minutes.innerText = diffMinutes < 10 ? '0' + diffMinutes : diffMinutes;
    seconds.innerText = diffSeconds < 10 ? '0' + diffSeconds : diffSeconds;

    // 目標時刻に到達すればカウントを止める
    if (remainTime < 0) clearInterval(countdownTimer);

}, 1000);   // 1000ms = 1s １秒間に１度処理

const modal = document.querySelector('.modal'),
      openButton = document.querySelector('#open-button'),
      closeIcon = document.querySelector('#close-icon');

openButton.addEventListener('click', () => {
    modal.classList.toggle('active');
});

closeIcon.addEventListener('click', () => {
    modal.classList.toggle('active');
});
