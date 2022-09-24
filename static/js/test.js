const testProgress = document.querySelector('.test-progress');
for (let i = 0; i < 20; i++) {
    const line = document.createElement('div');
    line.classList.add('line');
    testProgress.appendChild(line);
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

// メイン関数
async function main() {
    // Create Questions APIを叩く
    const questions = await getAPI(`https://project-research.azurewebsites.net/feature/create_questions/test/${rank}`);

    const word = [],              // 問題
          wordId = [],            // 問題の英単語ID
          answer = [],            // 正解
          userAnswer = [],        // ユーザーの解答
          answerState = [];       // 正誤状態
    
    let index = 0,                // 問題番号
        score = 0,                // 得点
        allResponse = [],         // 全体の出題数
        allCorrect = [];          // 全体の正解数
    
    const currentNumber = document.querySelector('#current-number'),
          maxNumber = document.querySelector('#max-number'),
          lines = [...document.querySelectorAll('.line')],
          statementSpan = document.querySelector('.statement > span'),
          testWord = document.querySelector('#test-word'),
          options = document.querySelector('#options'),
          nextForm = document.querySelector('.next-form');
          
    // 問題・選択肢を表示する関数===========================================================
    function setTest() {
        word[index] = questions[index].word;
        wordId[index] = questions[index].ID;
        answer[index] = questions[index].answer;
        allResponse[index] = questions[index].response;
        allCorrect[index] = questions[index].correct;

        if ((index + 1) >= 10) currentNumber.innerText = index + 1;
        else currentNumber.innerText = '0' + (index + 1);
        maxNumber.innerText = '/' + questions.length;
        lines[index].classList.add('current');
        statementSpan.innerText = `ユーザー正解率 : ${Math.floor(allCorrect[index] / allResponse[index] * 100)}%`;
        testWord.innerText = word[index];

        console.log(`第${index + 1}問: ${word[index]}  ID: ${wordId[index]}`);

        while (options.firstChild) {
            options.removeChild(options.firstChild);
        }

        questions[index].option.forEach((opt, i) => {
            // コンソール出力、確認
            console.log(`選択肢${i + 1}: ${opt}`);

            const input = document.createElement('input');
            input.type = 'button';
            input.value = opt;
            input.addEventListener('click', () => checkAnswer(input));

            options.appendChild(input);
        });
    };
    setTest();

    // 正誤判定する関数============================================================
    async function checkAnswer(input) {
        userAnswer[index] = input.value;

        // 正解時の処理
        if (userAnswer[index] == answer[index]) {
            answerState[index] = 'correct';
            score++;
        }
        // 不正解時の処理
        else {
            answerState[index] = 'incorrect';
        }
        // コンソール出力、確認用
        console.log(`ユーザーの回答: ${userAnswer[index]}`);

        // Update by Test APIに送信するPOSTデータを設定
        const updateData = {
            'word_id': wordId[index],
            'answer_state': answerState[index]
        };
        // Update by Test APIを叩く
        await postAPI(`https://project-research.azurewebsites.net/api/update-by-test`, updateData);

        // テストの最後の問題を解答した時の処理
        if (index == questions.length -1) {
            options.classList.add('none-events');
            nextForm.classList.add('active');
            toResult();
            window.removeEventListener('beforeunload', browserReload);
            window.removeEventListener('popstate', browserBack);
        }

        index++;
        if (index < questions.length) setTest();
    };

    function toResult() {
        document.resultForm.action = 'test/result';       // ページ遷移先をリザルトページへ変更
        document.resultForm.method = 'POST';

        wordId.forEach((id, i) => {
            const post1 = document.createElement('input');
            post1.type = 'hidden';
            post1.name = `word_id${i}`;
            post1.value = id;
            nextForm.appendChild(post1);
        });

        answerState.forEach((anss, j) => {
            const post2 = document.createElement('input');
            post2.type = 'hidden';
            post2.name = `answer_state${j}`;
            post2.value = anss;
            nextForm.appendChild(post2);
        });

        const post3 = document.createElement('input');
        post3.type = 'hidden';
        post3.name = 'score';
        post3.value = score;
        nextForm.appendChild(post3);
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
