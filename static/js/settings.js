const colorTheme = document.querySelector('.color-theme');
const currentTheme = document.querySelector('.current-theme');
const switchBar = document.querySelector('.switch-bar');

switchBar.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    
    if (document.body.classList.contains('dark-mode')) {
        colorTheme.classList.remove('bx-sun');
        colorTheme.classList.add('bx-moon')
        currentTheme.innerText = 'Dark Mode';
        localStorage.setItem('color-theme', 'dark-mode');
    }
    else if (colorTheme.classList.contains('bx-moon')) {
        colorTheme.classList.remove('bx-moon');
        colorTheme.classList.add('bx-sun');
        currentTheme.innerText = 'Light Mode';
        localStorage.setItem('color-theme', 'light-mode');
    }
});

if (localStorage.getItem('color-theme') === 'dark-mode') {
    colorTheme.classList.remove('bx-sun');
    colorTheme.classList.add('bx-moon');
    currentTheme.innerText = 'Dark Mode';
}
