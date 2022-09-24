if (localStorage.getItem('color-theme') === 'dark-mode') {
    document.body.classList.add('dark-mode');
}
else if (localStorage.getItem('color-theme') === 'light-mode') {
    document.body.classList.remove('dark-mode');
}

// if (localStorage.getItem('notice') === 'presence') {
//     const notice = document.querySelector('#notice > .menu-icon'),
//           noticeIcon = '<span class="material-symbols-outlined notice-icon">add_circle</span>';

//     notice.insertAdjacentHTML('afterbegin', `${noticeIcon}`);
// }
