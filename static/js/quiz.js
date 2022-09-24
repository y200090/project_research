const quizProgress = document.querySelector('.quiz-progress');
for (let i = 0; i < 10; i++) {
    const line = document.createElement('div');
    line.classList.add('line');
    quizProgress.appendChild(line);
}

// ブラウザのリロード・タブ閉じをアラート
window.addEventListener('beforeunload', browserReload);
function browserReload(e) {
    e.preventDefault();
    e.returnValue = '';
};

// ブラウザバックをアラート
history.pushState(null, null, location.href);
window.addEventListener('popstate', browserBack);
function browserBack() {
    alert('行った変更が保存されない可能性があります。');
    history.go(1);
};

const word = [],              // 問題
      wordId = [],            // 問題の英単語ID
      answer = [],            // 正解
      userAnswer = [],        // ユーザーの解答
      answerState = [];       // 正誤状態

let index = 0,                // 問題番号
    score = 0,                // 得点
    allResponse = [],         // 全体の出題数
    allCorrect = [],          // 全体の正解数
    answerImage;              // 正誤判定時のイメージ

const currentNumber = document.querySelector('#current-number'),
      maxNumber = document.querySelector('#max-number'),
      lines = [...document.querySelectorAll('.line')],
      statementSpan = document.querySelector('.statement > span'),
      quizWord = document.querySelector('#quiz-word'),
      options = document.querySelector('#options'),
      nextForm = document.querySelector('.next-form'),
      nextButton = document.querySelector('#next-button');

// メイン関数
async function main() {
    // Create Quiz APIを叩く
    const questions = await getAPI(`http://127.0.0.1:8000/feature/create_questions/quiz/${rank}`);
    
    // 問題・選択肢を表示する関数===========================================================
    function setQuiz() {
        word[index] = questions[index].word;              // index問目の問題を格納
        wordId[index] = questions[index].ID;              // index問目の英単語IDを格納
        answer[index] = questions[index].answer;          // index問目の正解を格納
        allResponse[index] = questions[index].response;   // index問目の全ユーザーの出題数を格納
        allCorrect[index] = questions[index].correct;     // index問目の全ユーザーの正解数を格納

        if ((index +1) >= 10) {
            currentNumber.innerText = (index + 1);

        } else {
            currentNumber.innerText = '0' + (index + 1);
        }
        maxNumber.innerText = '/' + questions.length;
        lines[index].classList.add('current');        
        statementSpan.innerText = `ユーザー正解率：${Math.floor(allCorrect[index] / allResponse[index] * 100)}%`;
        quizWord.innerText = word[index];

        const speakIcon = document.createElement('span');
        speakIcon.classList.add('material-symbols-outlined', 'speak-icon');
        quizWord.appendChild(speakIcon);
        speakIcon.innerText = 'volume_up';
        // ブラウザにWeb Speech API Speech Synthesis機能があるか判定
        speakIcon.addEventListener('click', () => {
            if ('speechSynthesis' in window) {
                const uttr = new SpeechSynthesisUtterance();
                uttr.text = word[index];
                uttr.lang = 'en-US';
                uttr.rate = 0.8;
                const voices = speechSynthesis.getVoices();
                voices.forEach(voice => {
                    if (voice.lang === 'en-US') {
                        uttr.voice = voice;
                    }
                });
                window.speechSynthesis.speak(uttr);

            } else {
                alert('このブラウザは音声合成に対応していません。');
            }
        });

        // コンソール出力、確認用
        console.log(`第${index + 1}問: ${word[index]}  ID: ${wordId[index]}`);

        // 前問の選択肢を削除
        while (options.firstChild) {
            options.removeChild(options.firstChild);
        }

        // 4つの選択肢を表示
        questions[index].option.forEach((opt, i) => {
            // コンソール出力、確認
            console.log(`選択肢${i + 1}: ${opt}`);

            const div = document.createElement('div');
            div.classList.add('option-content');

            const input = document.createElement('input');
            input.type = "button";
            input.value = opt;
            input.addEventListener('click', () => checkAnswer(input));
            
            div.appendChild(input);
            options.appendChild(div);
        });
    };
    setQuiz();

    // 正誤判定する関数====================================================================
    async function checkAnswer(input) {
        userAnswer[index] = input.value;                  // ユーザーの解答を格納

        // 正解・不正解時の処理
        if (userAnswer[index] == answer[index]) {
            answerImage = '<i class="bx bx-check-circle answer-image correct"></i>';
            lines[index].classList.add('correct');
            input.classList.add('correct');
            answerState[index] = 'correct';
            score++;                                      // 得点+1

        } else {

            answerImage = '<i class="bx bx-x-circle answer-image incorrect"></i>';
            lines[index].classList.add('incorrect');
            input.classList.add('incorrect');
            answerState[index] = 'incorrect';
        }
        // コンソール出力、確認用
        console.log(`ユーザーの回答: ${userAnswer[index]}`);
        console.log(`正解: ${answer[index]}`);
        console.log(`成績: ${score}/${questions.length}`);
        
        input.insertAdjacentHTML('afterend', `${answerImage}`);
        options.classList.add('none-events');
        nextForm.classList.add('active');

        // Update by Quiz APIに送信するPOSTデータを設定
        const updateData = {
            'word_id': wordId[index],
            'answer_state': answerState[index]
        };
        // Update by Quiz APIを叩く
        await postAPI(`http://127.0.0.1:8000/api/update-by-quiz/${rank}`, updateData);

        // クイズの最後の問題を解答した時の処理
        if (index == questions.length - 1) {
            toResult();
            window.removeEventListener('beforeunload', browserReload);
            window.removeEventListener('popstate', browserBack);
        }
    };

    // 次の問題を表示する関数============================================================
    function nextQuiz() {
        options.classList.remove('none-events');
        nextForm.classList.remove('active');        
        index++;
        if (index < questions.length) setQuiz();
    };
    nextButton.addEventListener('click', () => nextQuiz());

    // リザルトページへ遷移する関数=========================================================
    function toResult() {
        document.resultForm.action = 'quiz/result';       // ページ遷移先をリザルトページへ変更
        document.resultForm.method = 'POST';
        nextButton.type = 'submit';
        nextButton.value = '終了する';

        wordId.forEach((id, i) => {
            const post1 = document.createElement('input');
            post1.type = 'hidden';
            post1.name = `word_id${i}`;
            post1.value = id;
            nextForm.appendChild(post1);
        });

        answerState.forEach((anss, i) => {
            const post2 = document.createElement('input');
            post2.type = 'hidden';
            post2.name = `answer_state${i}`;
            post2.value = anss;
            nextForm.appendChild(post2);
        });

        const post3 = document.createElement('input');
        post3.type = 'hidden';
        post3.name = 'rank';
        post3.value = rank;
        nextForm.appendChild(post3);

        const post4 = document.createElement('input');
        post4.type = 'hidden';
        post4.name = 'score';
        post4.value = score;
        nextForm.appendChild(post4);
    };
};
main();

// APIからデータを受け取る関数
async function getAPI(url) {
    return await fetch(url)
        .then(response => {
            return response.json();
        })
        .then(datas => {
            return datas;
        })
        .catch(error => {
            console.error('APIの取得に失敗しました。', error);
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
