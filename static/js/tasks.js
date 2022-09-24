if (tasks[0] == 0 && tasks[1] == 0 && tasks[2] == 0 && tasks[3] == 0) {
    const empty = document.querySelector('#empty');
    empty.style.display = 'block';
    localStorage.setItem('notice', 'absence');
}
const ranks = ['A1', 'A2', 'B1', 'B2'],
      cards = [];
for (let i in ranks) {
    if (tasks[i] == 0) {
        cards[i] = document.querySelector(`.${ranks[i]}`);
        cards[i].style.display = 'none';
    }
}

if (tasks[0] > 0 || tasks[1] > 0 || tasks[2] > 0 || tasks[3] > 0) {
    localStorage.setItem('notice', 'presence');
}
