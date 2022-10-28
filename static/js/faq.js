const accordion = document.querySelectorAll('.acc-top-block');

accordion.forEach(e => {
    e.addEventListener('click', () => {
        e.classList.toggle('active');
    });
});
