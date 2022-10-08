// セッションストレージの数を取得
const testCount = sessionStorage.length;

const resultPage = document.querySelector('.result-page'),
      resultWord = document.querySelector('#result-word'),
      userScore = document.querySelector('#user-score'),
      maxScore = document.querySelector('#max-score'),
      nextContent = document.querySelector('.next-content'),
      reviewButton = document.querySelector('#review-button'),
      backpageButton = document.querySelector('#backpage-button');

const clone = [],
      reviewWindow = document.querySelector('.review-window'),
      closeIcon = document.querySelector('.close-icon'),
      swiperWrapper = document.querySelector('.swiper-wrapper');

if (score >= 10) {
    userScore.innerText = score;
}
else {
    userScore.innerText = '0' + score;
}
maxScore.innerText = '/' + testCount;

if (testCount * 0.7 < score && score <= testCount) {
    resultWord.innerText = 'Congratulations!';
    happy();
}
else if (testCount * 0.3 < score && score <= testCount * 0.7) {
    resultWord.innerText = 'Nice Challenge!';
    happy();
}
else if (score <= testCount * 0.3) {
    resultWord.innerText = 'Hang in There!';
}

for (let i = 0; i < testCount; i++) {
    clone[i] = sessionStorage.getItem(`test-${i + 1}`);

    const testPage = document.createElement('div');
    testPage.classList.add('swiper-slide', 'test-page', `test-${i + 1}`);
    testPage.insertAdjacentHTML('beforeend', `${clone[i]}`);
    
    swiperWrapper.appendChild(testPage);
}

reviewButton.addEventListener('click', () => {
    resultPage.classList.add('inactive');
    reviewWindow.classList.add('active');
});

closeIcon.addEventListener('click', () => {
    resultPage.classList.remove('inactive');
    reviewWindow.classList.remove('active');
});

const englishWord = [...document.querySelectorAll('.english-word')],
      speakIcons = [...document.querySelectorAll('.speak-icon')];
speakIcons.forEach((speakIcon, index) => {
    // Web Speech API Synthesisを利用して英単語の発音を確認できる機能を実装
    speakIcon.addEventListener('click', () => {
        // ブラウザにWeb Speech API Speech Synthesisがあるか判定
        if ('speechSynthesis' in window) {
            const uttr = new SpeechSynthesisUtterance();
            uttr.text = englishWord[index].textContent.replace('volume_up', '');
            uttr.lang = 'en-US';
            uttr.rate = 0.8;
            const voices = speechSynthesis.getVoices();
            voices.forEach(voice => {
                if (voice.lang === 'en-US') {
                    uttr.voice = voice;
                }
            });
            window.speechSynthesis.speak(uttr);
        }
        else {
            alert('このブラウザは音声合成に対応していません。');
        }
    });
});
      
function happy() {
    confetti({
        particleCount: 100,
        spread: 70,
        origin: {
            x: 1,
            y: 0.6
        },
        ticks: 1000,
    });
    confetti({
        particleCount: 100,
        spread: 70,
        origin: {
            x: 0,
            y: 0.6
        },
        ticks: 1000,
    });
};
