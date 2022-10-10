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

// メイン関数
async function main() {
    // クイズ作成APIを叩く
    const questions = await getAPI(`https://project-research.azurewebsites.net/feature/create-questions/quiz/${rank}`);

    const quizProgress = document.querySelector('.quiz-progress');
    for (let i = 0; i < questions.length; i++) {
        const line = document.createElement('div');
        line.classList.add('line');
        quizProgress.appendChild(line);
    }

    // セッションストレージを初期化
    sessionStorage.clear();

    const word = [],              // 問題
          wordId = [],            // 問題の英単語ID
          answer = [],            // 正解
          userAnswer = [],        // ユーザーの解答
          answerState = [],       // 正誤判定の結果を記憶
          responseSpan = [],      // 解答時間を算出
          clone = [];             // クイズページのクローンを記憶

    let index = 0,                // 問題番号
        score = 0,                // 得点
        allResponse = [],         // 全体の出題数
        allCorrect = [],          // 全体の正解数
        answerImage,              // 正誤判定時のイメージ
        startTime,                // 解答開始時刻
        endTime,                  // 解答完了時刻
        nextButton;               // クイズページを切り替えるボタン

    const quizPage = document.querySelector('.quiz-page'),
          currentNumber = document.querySelector('.current-number'),
          maxNumber = document.querySelector('.max-number'),
          lines = [...document.querySelectorAll('.line')],
          statementSpan = document.querySelector('.statement > span'),
          englishWord = document.querySelector('.english-word'),
          optionsContent = document.querySelector('.options-content'),
          nextContent = document.querySelector('.next-content');
    
    // 問題・選択肢を表示する関数===========================================================
    function setQuiz() {
        // 問題の英単語を格納
        word[index] = questions[index].word;
        // 英単語IDを格納
        wordId[index] = questions[index].ID;
        // 日本語訳（正解）を格納
        answer[index] = questions[index].answer;
        // 解答された累計を格納
        allResponse[index] = questions[index].response;
        // 正解された累計を格納
        allCorrect[index] = questions[index].correct;

        if ((index + 1) >= 10) {
            currentNumber.innerText = (index + 1);
        }
        else {
            currentNumber.innerText = '0' + (index + 1);
        }
        maxNumber.innerText = '/' + questions.length;
        lines[index].classList.add('current');        
        statementSpan.innerText = `ユーザー正解率 ：${Math.floor(allCorrect[index] / allResponse[index] * 100)}%`;
        englishWord.innerText = word[index];

        // 解答開始時刻取得
        startTime = new Date();

        // スピーカーアイコン生成
        const speakIcon = document.createElement('span');
        speakIcon.classList.add('material-symbols-outlined', 'speak-icon');
        englishWord.appendChild(speakIcon);
        speakIcon.innerText = 'volume_up';

        // Web Speech API Synthesisを利用して英単語の発音を確認できる機能を実装
        speakIcon.addEventListener('click', () => {
            // ブラウザにWeb Speech API Speech Synthesisがあるか判定
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
            }
            else {
                alert('このブラウザは音声合成に対応していません。');
            }
        });

        // コンソール確認用
        console.log(`第${index + 1}問: ${word[index]}  ID: ${wordId[index]}`);

        // 前問の選択肢を削除
        while (optionsContent.firstChild) {
            optionsContent.removeChild(optionsContent.firstChild);
        }

        // 4つの選択肢を表示
        questions[index].options.forEach((option, i) => {
            // コンソール確認用
            console.log(`選択肢${i + 1}: ${option}`);

            const japaneseWord = document.createElement('div');
            japaneseWord.classList.add('japanese-word');

            const input = document.createElement('input');
            input.type = 'button';
            input.value = option;
            if (input.value == answer[index]) {
                input.classList.add('model-answer');
            }
            input.addEventListener('click', () => checkAnswer(input));
            
            japaneseWord.appendChild(input);
            optionsContent.appendChild(japaneseWord);
        });
    };
    setQuiz();

    // 正誤判定する関数====================================================================
    async function checkAnswer(input) {
        // 解答完了時刻取得
        endTime = new Date();
        responseSpan[index] = endTime.getTime() - startTime.getTime();
        
        // ユーザーの解答を格納
        userAnswer[index] = input.value;

        // 正解時の処理
        if (userAnswer[index] == answer[index]) {
            answerImage = '<i class="bx bx-check-circle answer-image correct"></i>';
            lines[index].classList.add('correct');
            input.classList.add('correct');
            answerState[index] = 'correct';
            score++;
        }
        // 不正解時の処理
        else {
            answerImage = '<i class="bx bx-x-circle answer-image incorrect"></i>';
            lines[index].classList.add('incorrect');
            input.classList.add('incorrect');
            answerState[index] = 'incorrect';

            const modelAnswer = document.querySelector('.model-answer');
            modelAnswer.classList.add('correct')
            const modelAnswerImage = '<i class="bx bx-check-circle answer-image correct"></i>';
            modelAnswer.insertAdjacentHTML('afterend', `${modelAnswerImage}`);
        }
        input.insertAdjacentHTML('afterend', `${answerImage}`);

        // コンソール確認用
        console.log(`解答時間: ${responseSpan[index]}ms`);
        console.log(`ユーザーの回答: ${userAnswer[index]}`);
        console.log(`正解: ${answer[index]}`);
        console.log(`成績: ${score}/${questions.length}`);
        
        optionsContent.classList.add('none-events');
        nextContent.classList.add('active');

        // クイズ更新APIに送信するPOSTデータを設定
        const updateData = {
            'word_id': wordId[index],
            'answer_state': answerState[index],
            'response_span': responseSpan[index]
        };
        // クイズ更新APIを叩く
        await postAPI(`https://project-research.azurewebsites.net/api/quiz-update/${rank}`, updateData);

        // 前問のボタンを削除
        while (nextContent.firstChild) {
            nextContent.removeChild(nextContent.firstChild);
        }
        
        // クイズの最後の問題を解答した時の処理
        if ((index + 1) == questions.length) {
            window.removeEventListener('beforeunload', browserReload);
            window.removeEventListener('popstate', browserBack);

            nextButton = document.createElement('a');
            nextButton.classList.add('next-button');
            nextButton.href = `/mypage/learnings/quiz/${rank}/result?score=${score}`;
            nextButton.innerText = '終了する';
        }
        else {
            nextButton = document.createElement('button');
            nextButton.classList.add('next-button');
            nextButton.innerText = '次の問題へ';
            nextButton.addEventListener('click', () => nextQuiz());
        }
        nextContent.appendChild(nextButton);

        // クイズページのクローンを取得
        clone[index] = quizPage.cloneNode(true);
        // セッションストレージにクローンを保存
        sessionStorage.setItem(`quiz-${index + 1}`, `${clone[index].innerHTML}`);
    };

    // 次の問題へ遷移する関数============================================================
    function nextQuiz() {       
        optionsContent.classList.remove('none-events');
        nextContent.classList.remove('active');
        index++;
        if (index < questions.length) {
            setQuiz();
        }
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
