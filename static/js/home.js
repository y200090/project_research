if (stacks[0] > 0 || stacks[1] > 0 || stacks[2] > 0 || stacks[3] > 0) {
    // ローカルストレージに保存（キーの更新）
    localStorage.setItem('notice', 'presence');
}
if (stacks[0] == 0 && stacks[1] == 0 && stacks[2] == 0 && stacks[3] == 0) {
    // ローカルストレージに保存（キーの更新）
    localStorage.setItem('notice', 'absence');
}

const notice = document.querySelector('.notice');

if (localStorage.getItem('notice') == 'presence') {
    notice.classList.add('presence');
    notice.parentNode.classList.add('presence');
}
