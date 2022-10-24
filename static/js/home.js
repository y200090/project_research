const notice = document.querySelector('.notice');

if (localStorage.getItem('notice') == 'presence') {
    notice.classList.add('presence');
    notice.parentNode.classList.add('presence');
}
