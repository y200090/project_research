const heroContent = document.querySelector('.hero-content'),
      launching = document.querySelector('.launching'),
      caret = document.querySelector('.caret'),
      playButton = document.querySelector('.play-button'),
      modal = document.querySelector('.modal'),
      closeIcon = document.querySelector('.close-icon');

playButton.addEventListener('click', () => {
    heroContent.classList.toggle('inactive');
    modal.classList.toggle('active');
});

closeIcon.addEventListener('click', () => {
    heroContent.classList.toggle('inactive');
    modal.classList.toggle('active');
});
