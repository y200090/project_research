const topImage = [...document.querySelectorAll('.top-image')],
      rankIcon = [...document.querySelectorAll('.rank-icon')],
      quizMain = [...document.querySelectorAll('.quiz-content > .main')],
      quizCircle = [...document.querySelectorAll('.quiz-circle')],
      track = [...document.querySelectorAll('.track')],
      progress = [...document.querySelectorAll('.progress')],
      percentage = [...document.querySelectorAll('.percentage')];
      
let height, length;
window.addEventListener('load', () => {
    topImage.forEach((image, index) => {
        height = image.clientHeight;
        rankIcon[index].style.height = `${height * 50 / 100}px`;
        rankIcon[index].style.width = `${height * 50 / 100}px`;
    });

    quizMain.forEach((main, index) => {
        height = main.clientHeight;
        quizCircle[index].style.height = `${height * 70 / 100}px`;
        quizCircle[index].style.width = `${height * 70 / 100}px`;

        length = quizCircle[index].clientHeight;
        track[index].r.baseVal.value = length * 45 / 100;
        progress[index].r.baseVal.value = length * 45 / 100;
    });
    setProgress();
});

window.addEventListener('resize', () => {
    topImage.forEach((image, index) => {
        height = image.clientHeight;
        rankIcon[index].style.height = `${height * 50 / 100}px`;
        rankIcon[index].style.width = `${height * 50 / 100}px`;
    })
    
    quizMain.forEach((main, index) => {
        height = main.clientHeight;
        quizCircle[index].style.height = `${height * 70 / 100}px`;
        quizCircle[index].style.width = `${height * 70 / 100}px`;

        length = quizCircle[index].clientHeight;
        track[index].r.baseVal.value = length * 45 / 100;
        progress[index].r.baseVal.value = length * 45 / 100;
    });
    setProgress();
});

function setProgress() {
    params.forEach((param, index) => {
        let startValue = 0.0, 
            endValue = param,
            speed = 8,
            radius = progress[index].r.baseVal.value,
            circumference = radius * 2 * Math.PI;

        progress[index].style.strokeDasharray = circumference;

        const workProgress = setInterval(() => {
            if (endValue > 0.0) {
                startValue += 0.1;
            }
            progress[index].style.strokeDashoffset = circumference - (startValue / 100) * circumference;
            if (endValue <= 0.0 || Number(startValue.toFixed(1)) % Number(startValue.toFixed(0)) == 0) {
                percentage[index].innerHTML = `${startValue.toFixed(0)}%`;
            }
            else {
                percentage[index].innerHTML = `${startValue.toFixed(1)}%`;
            }
            if (startValue.toFixed(1) == endValue) {
                clearInterval(workProgress);
            }
        }, speed);
    });
};

const ctx = document.querySelector('#quiz-answer-chart');
const datas = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 0],[2, 3, 4, 2, 6, 5, 7, 2 ,9, 1], [4, 6, 2, 7, 5, 4, 8, 8, 9, 6], [6, 4, 2, 4, 8, 7, 9, 8, 10, 9]];
const quizAnswerChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
        datasets: [
            {
                label: 'A1',
                data: datas[0],
                borderColor: '#FFCA03',
                fill: false,
                borderWidth: 2,
                tension: 0.5,
                pointRadius: 3,
                pointBackgroundColor: '#FFCA03'
            },
            {
                label: 'A2',
                data: datas[1],
                borderColor: '#01daa3',
                fill: false,
                borderWidth: 2,
                tension: 0.5,
                pointRadius: 3,
                pointBackgroundColor: '#01daa3'
            },
            {
                label: 'B1',
                data: datas[2],
                borderColor: '#f94144',
                fill: false,
                borderWidth: 2,
                tension: 0.5,
                pointRadius: 3,
                pointBackgroundColor: '#f94144'
            },
            {
                label: 'B2',
                data: datas[3],
                borderColor: '#033FFF',
                fill: false,
                borderWidth: 2,
                tension: 0.5,
                pointRadius: 3,
                pointBackgroundColor: '#033FFF'
            }
        ]
    },
    options: {
        maintainAspectRatio: false,
        title: {
            display: true,
            text: '直近10回のクイズの正答数',
            fontSize: 14,
            fontColor: '#fff'
        },
        scales: {
            yAxes: [{
                ticks: {
                    suggestedMax: 10,
                    suggestedMin: 0,
                    stepSize: 1,
                    fontColor: '#fff',
                    fontSize: 14,
                    callback: function(value, index, values) {
                        return value;
                    }
                },
                gridLines: {
                    display: false
                }
            }],
            xAxes: [{
                gridLines: {
                    display: false
                },
                ticks: {
                    fontColor: '#fff',
                    fontSize: 14
                }
            }]
        },
        legend: {
            labels: {
                usePointStyle: true,
                fontSize: 14,
                fontColor: '#fff'
            }
        }
    }
});
quizAnswerChart.canvas.parentNode.style.position = 'relative';
quizAnswerChart.canvas.parentNode.style.height = `${ctx.clientHeight * 2}px`;
quizAnswerChart.canvas.parentNode.style.width = '100%';
