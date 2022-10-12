const loginState = [...document.querySelectorAll('.login-state')],
      loginDate = [...document.querySelectorAll('.login-date')];
let dateFormat;

users.forEach((user, index) => {
    if (user.login_state == 'active') {
        loginState[index].innerText = 'Login';
        loginState[index].classList.add('login');
    }
    else {
        loginState[index].innerText = 'Logout';
        loginState[index].classList.add('logout');
    }

    dateFormat = user.login_date.replace(/-/g, '/');
    dateFormat = dateFormat.substr(0, dateFormat.indexOf('.'));
    loginDate[index].innerText = dateFormat;
});

const deleteSpans = [...document.querySelectorAll('.delete > span')],
      modalWindow = document.querySelector('.modal-window'),
      modalUsername = document.querySelector('.modal-username'),
      modalButton = document.querySelector('.modal-button > button'),
      modalDelete = document.querySelector('.modal-button > a');

deleteSpans.forEach((deleteSpan, index) => {
    deleteSpan.addEventListener('click', () => {
        modalWindow.classList.add('active');
        modalUsername.innerText = `ユーザー名 : ${users[index].username}`;
        modalDelete.href = `/api/database/delete/${users[index].ID}`;
    });
});

modalButton.addEventListener('click', () => {
    modalWindow.classList.remove('active');
});
