const resultPage = document.querySelector('.result-page'),
      resultWord = document.querySelector('#result-word'),
      userScore = document.querySelector('#user-score'),
      maxScore = document.querySelector('#max-score'),
      reviewButton = document.querySelector('#review-button');

const clone = [],
      reviewWindow = document.querySelector('.review-window'),
      swiperWrapper = document.querySelector('.swiper-wrapper');

if (score < 10) {
    userScore.innerText = '0' + score;
}
else {
    userScore.innerText = score;
}

if (7 < score && score <= 10) {
    resultWord.innerText = 'Congratulations!';
    happy();
}
else if (3 < score && score <= 7) {
    resultWord.innerText = 'Nice Challenge!';
    happy();
}
else if (score <= 3) {
    resultWord.innerText = 'Do Your Best!';
}

for (let i = 0; i < 10; i++) {
    clone[i] = sessionStorage.getItem(`question.${i + 1}`);

    const quizPage = document.createElement('div');
    quizPage.classList.add('swiper-slide', 'quiz-page', `question.${i + 1}`);
    quizPage.insertAdjacentHTML('beforeend', `${clone[i]}`);
    
    swiperWrapper.appendChild(quizPage);
}

reviewButton.addEventListener('click', () => {
    resultPage.classList.add('inactive');
    reviewWindow.classList.add('active');
});

// function review(data, index) {    
//     if (answerState[index] == "correct") {
//         revieweeCard[index].classList.add('correct');

//     } else {
//         revieweeCard[index].classList.add('incorrect');
//     }

//     quizWord[index].innerText = data.word;

//     const speakIcon = document.createElement('span');
//     speakIcon.classList.add('material-symbols-outlined', 'speak-icon');
//     quizWord[index].appendChild(speakIcon);
//     speakIcon.innerText = 'volume_up';
//     // ブラウザにWeb Speech API Speech Synthesis機能があるか判定
//     speakIcon.addEventListener('click', () => {
//         if ('speechSynthesis' in window) {
//             const uttr = new SpeechSynthesisUtterance();
//             uttr.text = data.word;
//             uttr.lang = 'en-US';
//             uttr.rate = 0.8;
//             const voices = speechSynthesis.getVoices();
//             voices.forEach(voice => {
//                 if (voice.lang === 'en-US') {
//                     uttr.voice = voice;
//                 }
//             });
//             window.speechSynthesis.speak(uttr);

//         } else {
//             alert('このブラウザは音声合成に対応していません。');
//         }
//     });

//     quizAnswer[index].innerText = "日本語訳 : " + data.translation;

//     const editIcon = document.createElement('span');
//     editIcon.classList.add('material-symbols-outlined', 'edit-icon');
//     quizAnswer[index].appendChild(editIcon);
//     editIcon.innerText = 'edit';
//     editIcon.addEventListener('click', () => {
//         editForm.classList.add('active');
//         editButton.setAttribute('id', `${data.word_id}`)
//     });

// };

// revieweeCloseIcon.addEventListener('click', () => {
//     quitIcon.classList.remove('inactive');
//     reviewee.classList.remove('active');
//     revieweeCloseIcon.classList.remove('active');
// });

// editCloseIcon.addEventListener('click', () => {
//     editForm.classList.remove('active');
// });

// editButton.addEventListener('click', async () => {
//     const editInput = document.querySelector('.edit-field > input');

//     // 英単語ID検索APIに送信するPOSTデータを設定
//     const updateDate = {
//         'new_translation': editInput.value
//     };
//     // 英単語ID検索APIを叩く（POSTメソッド）
//     // await postAPI(`https://project-research.azurewebsites.net/api/word-id-search/${editButton.id}`, updateDate);
//     await postAPI(`http://127.0.0.1:5000/api/word-id-search/${editButton.id}`, updateDate);

//     alert('更新が完了しました。');
//     editForm.classList.remove('active');
// });

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

// APIにPOSTデータを送る関数
async function postAPI(url, data) {
    const param = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    };
    return await fetch(url, param)
        .then(response => {
            return response.json();
        })
        .then(data => {
            return data;
        })
        .catch(error => {
            console.error('APIへデータの送信に失敗しました。', error);
        });
};
