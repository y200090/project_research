// セッションストレージの数を取得
const quizCount = sessionStorage.length;

const resultPage = document.querySelector('.result-page'),
      resultWord = document.querySelector('#result-word'),
      userScore = document.querySelector('#user-score'),
      maxScore = document.querySelector('#max-score'),
      nextContent = document.querySelector('.next-content'),
      reviewButton = document.querySelector('#review-button'),
      browserBack = document.querySelector('#browser-back');

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
maxScore.innerText = '/' + quizCount;

if (quizCount * 0.7 < score && score <= quizCount) {
    resultWord.innerText = 'Congratulations!';
    happy();
}
else if (quizCount * 0.3 < score && score <= quizCount * 0.7) {
    resultWord.innerText = 'Nice Challenge!';
    happy();
}
else if (score <= quizCount * 0.3) {
    resultWord.innerText = 'Hang in There!';
}

window.addEventListener('load', () => {
    height = nextContent.clientHeight;
    browserBack.style.height = `${height * 1.2}px`;
});

window.addEventListener('resize', () => {
    height = nextContent.clientHeight;
    browserBack.style.height = `${height * 1.2}px`;
});

for (let i = 0; i < quizCount; i++) {
    clone[i] = sessionStorage.getItem(`quiz-${i + 1}`);

    const quizPage = document.createElement('div');
    quizPage.classList.add('swiper-slide', 'quiz-page', `quiz-${i + 1}`);
    quizPage.insertAdjacentHTML('beforeend', `${clone[i]}`);
    
    swiperWrapper.appendChild(quizPage);
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
