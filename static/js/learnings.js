<<<<<<< HEAD
const topIcons = [...document.querySelectorAll('.top-icon')],
      barParameter = [...document.querySelectorAll('.bar-parameter')],
=======
const barParameter = [...document.querySelectorAll('.bar-parameter')],
>>>>>>> c5bc740594fe2ff02c60bff2eaa94b485c12ee6e
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
<<<<<<< HEAD

counts.forEach((count, index) => {
    challengeNumber[index].innerText = `${count}`;
});

const mediaQueryTablet = window.matchMedia('(min-width: 768px'),
      mediaQueryDesktop = window.matchMedia('(min-width: 1024px');
=======

counts.forEach((count, index) => {
    challengeNumber[index].innerText = `${count}`;
});
>>>>>>> c5bc740594fe2ff02c60bff2eaa94b485c12ee6e

window.addEventListener('load', () => {
    challengeNumber.forEach(number => {
        height = number.clientWidth;
        number.style.height = `${height}px`;
    });
    progressCircle.forEach(circle => {
        width = circle.clientHeight;
        circle.style.width = `${width}px`;
    });
    if (mediaQueryTablet.matches) {
        topIcons.forEach(topIcon => {
            topIcon.innerText = 'tablet_mac';
        });
    }
    if (mediaQueryDesktop.matches) {
        topIcons.forEach(topIcon => {
            topIcon.innerText = 'computer';
        });
    }
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
    if (mediaQueryTablet.matches) {
        topIcons.forEach(topIcon => {
            topIcon.innerText = 'tablet_mac';
        });
    }
    if (mediaQueryDesktop.matches) {
        topIcons.forEach(topIcon => {
            topIcon.innerText = 'computer';
        });
    }
});
