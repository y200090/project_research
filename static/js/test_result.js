const resultComment = document.querySelector('#result-comment'),
      circular = document.querySelector('.circular'),
      review = document.querySelector('#review');

circular.style.background = `conic-gradient(var(--correct) ${score * 1.8 * 10}deg, var(--contents) 0deg)`;

if (score == wordId.length) {
    resultComment.innerText = 'Perfect!';
    happy();
}
else if ((70 * wordId.length / 100) <= score < wordId.length) {
    resultComment.innerText = 'Congratulations!';
    happy();
}
else if ((40 * wordId.length / 100) <= score < (70 * wordId.length / 100)) {
    resultComment.innerText = 'Nice Challenge!';
    happy();
}
else if (score < (40 * wordId.length / 100)) {
    resultComment.innerText = 'Do Your Best!';
}

function happy() {
    confetti({
        particleCount: 100,
        spread: 70,
        origin: {
            x: 1,
            y: 0.6
        },
        ticks: 1000,
    });
    confetti({
        particleCount: 100,
        spread: 70,
        origin: {
            x: 0,
            y: 0.6
        },
        ticks: 1000,
    });
};
