const heroContainer = document.querySelector('.hero-container'),
      startButton = document.querySelector('.start-button'),
      modalWindow = document.querySelector('.modal-window'),
      closeIcon = document.querySelector('.close-icon');

startButton.addEventListener('click', () => {
    heroContainer.classList.toggle('inactive');
    modalWindow.classList.toggle('active');
});

closeIcon.addEventListener('click', () => {
    heroContainer.classList.toggle('inactive');
    modalWindow.classList.toggle('active');
});
