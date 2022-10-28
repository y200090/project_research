const empty = document.querySelector('.if-empty'),
      tasks = [...document.querySelectorAll('.task')],
      topImage = [...document.querySelectorAll('.top-image')],
      rankIcon = [...document.querySelectorAll('.rank-icon')],
      stackicon = [...document.querySelectorAll('.stack-icon')];

for (let i = 0; i < 4; i++) {
    if (stacks[i] == 0) {
        stackicon[i].style.display = 'none';
        tasks[i].style.display = 'none';
    }
}

if (stacks[0] > 0 || stacks[1] > 0 || stacks[2] > 0 || stacks[3] > 0) {
    // ローカルストレージに保存（キーの更新）
    localStorage.setItem('notice', 'presence');
}

if (stacks[0] == 0 && stacks[1] == 0 && stacks[2] == 0 && stacks[3] == 0) {
    empty.style.display = 'block';

    // ローカルストレージに保存（キーの更新）
    localStorage.setItem('notice', 'absence');
}

let height;

window.addEventListener('load', () => {
    topImage.forEach((image, index) => {
        height = image.clientHeight;
        rankIcon[index].style.height = `${height * 0.7}px`;
        rankIcon[index].style.width = `${height * 0.7}px`;
    });

    stackicon.forEach(icon => {
        height = icon.clientHeight;
        icon.style.height = `${height}px`;
        icon.style.width = `${height}px`;
    });
});

window.addEventListener('resize', () => {
    topImage.forEach((image, index) => {
        height = image.clientHeight;
        rankIcon[index].style.height = `${height * 0.7}px`;
        rankIcon[index].style.width = `${height * 0.7}px`;
    });

    stackicon.forEach(icon => {
        height = icon.clientHeight;
        icon.style.height = `${height}px`;
        icon.style.width = `${height}px`;
    });
});
