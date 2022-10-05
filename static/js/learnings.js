params.forEach((param, index) => {
    const progressCircular = [...document.querySelectorAll('.progress-circular')],
          parameter = [...document.querySelectorAll('.parameter')];
      
    let startValue = 0.0,
        endValue = param,
        speed = 8;

    const progress = setInterval(() => {
        if (endValue > 0.0) {
            startValue += 0.1;
        };
        progressCircular[index].style.background = `conic-gradient(#fff ${startValue * 3.6}deg, var(--bg) 0deg)`;
        parameter[index].innerText = `${startValue.toFixed(1)}%`;
        if (endValue <= 0.0 || Number(startValue.toFixed(1)) % Number(startValue.toFixed(0)) == 0) {
            parameter[index].innerText = `${startValue.toFixed(0)}%`;
        }
        if (startValue.toFixed(1) == endValue) {
            clearInterval(progress);
        }
    }, speed);
})

const circleHeight = [...document.querySelectorAll('.progress-circular')];

window.addEventListener('load', () => {
    circleHeight.forEach(circle => {
        width = circle.clientHeight;
        circle.style.width = `${width}px`;
    });
});

window.addEventListener('resize', () => {
    circleHeight.forEach(circle => {
        width = circle.clientHeight;
        circle.style.width = `${width}px`;
    });
});
