const setFillHeight = () => {
    const vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty('--vh', `${vh}px`);
};
window.addEventListener('resize', setFillHeight);
setFillHeight();

const heroSection = document.querySelector('.hero-section'),
      modalButton = document.querySelector('.modal-button'),
      modalWindow = document.querySelector('.modal-window'),
      closeIcon = document.querySelector('.close-icon');

modalButton.addEventListener('click', () => {
    heroSection.classList.toggle('inactive');
    modalWindow.classList.toggle('active');
});

closeIcon.addEventListener('click', () => {
    heroSection.classList.toggle('inactive');
    modalWindow.classList.toggle('active');
});
