fetch('http://127.0.0.1:8000/api/quiz-achivement-calculation')
    .then(response => response.json())
    .then(datas => {
        datas.forEach((data, index) => {
            const progressCircular = [...document.querySelectorAll('.progress-circular')],
                  parameter = [...document.querySelectorAll('.parameter')];
      
            let startValue = 0,
                endValue = data,
                speed = 20;

            const progress = setInterval(() => {
                if (endValue != 0) {
                    startValue++;
                };
                progressCircular[index].style.background = `conic-gradient(#fff ${startValue * 3.6}deg, var(--bg) 0deg)`;
                parameter[index].innerText = `${startValue}%`;
                if (startValue == endValue) {
                    clearInterval(progress);
                }
            }, speed);
        });
    })
    .catch(error => console.error('APIの取得に失敗しました。', error));

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
