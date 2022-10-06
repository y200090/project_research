if (localStorage.getItem('color-theme') === 'dark-mode') {
    document.body.classList.add('dark-mode');
}
else if (localStorage.getItem('color-theme') === 'light-mode') {
    document.body.classList.remove('dark-mode');
}

const setFillHeight = () => {
    const vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty('--vh', `${vh}px`);
};
window.addEventListener('resize', setFillHeight);
setFillHeight();
