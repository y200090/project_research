const barParameter = [...document.querySelectorAll('.bar-parameter')],
      percentage = [...document.querySelectorAll('.percentage')],
      progressCircle= [...document.querySelectorAll('.progress-circle')],
      circleParameter = [...document.querySelectorAll('.circle-parameter')],
      challengeNumber = [...document.querySelectorAll('.challenge-number')];

params.forEach((param, index) => {
    let startValue = 0.0,
        endValue = param,
        speed = 8;

    const progress = setInterval(() => {
        if (endValue > 0.0) {
            startValue += 0.1;
        };
        barParameter[index].style.width = `${startValue}%`;
        percentage[index].innerText = `達成度 : ${startValue.toFixed(1)}%`;
        progressCircle[index].style.background = `conic-gradient(#fff ${startValue * 3.6}deg, var(--bg) 0deg)`;
        circleParameter[index].innerText = `${startValue.toFixed(1)}%`;
        if (endValue <= 0.0 || Number(startValue.toFixed(1)) % Number(startValue.toFixed(0)) == 0) {
            percentage[index].innerText = `達成度 : ${startValue.toFixed(0)}%`;
            circleParameter[index].innerText = `${startValue.toFixed(0)}%`;
        }
        if (startValue.toFixed(1) == endValue) {
            clearInterval(progress);
        }
    }, speed);
});

counts.forEach((count, index) => {
    challengeNumber[index].innerText = `${count}`;
});

window.addEventListener('load', () => {
    challengeNumber.forEach(number => {
        height = number.clientWidth;
        number.style.height = `${height}px`;
    });
    progressCircle.forEach(circle => {
        width = circle.clientHeight;
        circle.style.width = `${width}px`;
    });
});

window.addEventListener('resize', () => {
    challengeNumber.forEach(number => {
        height = number.clientWidth;
        number.style.height = `${height}px`;
    });
    progressCircle.forEach(circle => {
        width = circle.clientHeight;
        circle.style.width = `${width}px`;
    });
});
