const loginStates = [...document.querySelectorAll('.user-login-state')],
      signupDates = [...document.querySelectorAll('.user-signup-date')],
      loginDates = [...document.querySelectorAll('.user-login-date')];



users.forEach((user, index) => {
    if (user.login_state == 'active') {
        loginStates[index].innerText = 'ログイン中';
        loginStates[index].style.color = 'red';

    } else {
        loginStates[index].innerText = 'ログアウト中';
    }
    signupDates[index].innerText = user.signup_date.slice(0, -7);
    loginDates[index].innerText = user.login_date.slice(0, -7);
});

const usersTable = document.querySelector('.users'),
      usergradeSapns = [...document.querySelectorAll('.user-grade > span')],
      recordsTable = document.querySelector('.records'),
      closeIcon = document.querySelector('.close-icon'),
      recordsTableTbody = document.querySelector('.records > table > tbody');

usergradeSapns.forEach((usergradeSapn, index) => {
    usergradeSapn.addEventListener('click', () => {
        usersTable.classList.toggle('inactive');
        recordsTable.classList.toggle('active');

        fetch(`http://127.0.0.1:8000/api/user-id-search/${users[index].user_id}`)
            .then(response => {
                return response.json();
            })
            .then(datas => main(datas, users[index].total_remembered))
            .catch(error => console.error('APIの取得に失敗しました。', error));
    });

    closeIcon.addEventListener('click', () => {
        usersTable.classList.toggle('inactive');
        recordsTable.classList.toggle('active');
    });
});

function main(datas, total_remembered) {
    records(datas, total_remembered);
};

function records(records, total_remembered) {
    records.forEach(record => {
        const recordTr = document.createElement('tr');
        recordTr.classList.add('record-info');

        const wordId = document.createElement('td');
        wordId.classList.add('word-id');
        wordId.innerText = record.word_id;

        recordTr.appendChild(wordId);

        const rank = document.createElement('td');
        rank.classList.add('rank');
        rank.innerText = record.rank;

        recordTr.appendChild(rank);

        const testCorrect = document.createElement('td');
        testCorrect.classList.add('test-correct');
        testCorrect.innerText = record.test_correct;

        recordTr.appendChild(testCorrect);

        const testState = document.createElement('td');
        testState.classList.add('test-state');
        testState.innerText = record.test_state;

        recordTr.appendChild(testState);

        const totalRemembered = document.createElement('td');
        totalRemembered.classList.add('total-remembered');
        totalRemembered.innerText = total_remembered;

        recordTr.appendChild(totalRemembered);

        recordsTableTbody.appendChild(recordTr);
    });
};
