const resultComment = document.querySelector('#result-comment'),
      resultImage = document.querySelector('.result-image'),
      review = document.querySelector('#review');

if (score == wordId.length) {
    resultComment.innerText = 'Perfect!';
    resultImage.src = '../../../../static/images/undraw_happy_music_g6wc.svg';
    happy();
}
else if ((70 * wordId.length / 100) <= score < wordId.length) {
    resultComment.innerText = 'Congratulations!';
    resultImage.src = '../../../../static/images/undraw_happy_news_re_tsbd.svg';
    happy();
}
else if ((40 * wordId.length / 100) <= score < (70 * wordId.length / 100)) {
    resultComment.innerText = 'Nice Challenge!';
    resultImage.src = '../../../../static/images/undraw_winners_re_wr1l.svg';
    happy();
}
else if (score < (40 * wordId.length / 100)) {
    resultComment.innerText = 'Do Your Best!';
    resultImage.src = '../../../../static/images/undraw_celebrating_rtuv.svg';
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

console.log(review)

review.addEventListener('click', () => {
    alert('この機能は現在使用できません。')
});

