const colorTheme = document.querySelector('.color-theme'),
      switchBars = [...document.querySelectorAll('.switch-bar')],
      colorThemeIcon = document.querySelector('.color-theme-icon'),
      currentTheme = document.querySelector('.current-theme'),
      languageSwitch = document.querySelector('.language > .switch-bar'),
      colorThemeSwitch = document.querySelector('.color-theme > .switch-bar');

languageSwitch.addEventListener('click', () => {
    alert('申し訳ありません。この機能は現在使用できません。');
});

colorThemeSwitch.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    
    if (document.body.classList.contains('dark-mode')) {
        colorThemeIcon.classList.remove('bx-sun');
        colorThemeIcon.classList.add('bx-moon')
        currentTheme.innerText = 'ダークモード';
        localStorage.setItem('color-theme', 'dark-mode');

    } else if (colorThemeIcon.classList.contains('bx-moon')) {
        colorThemeIcon.classList.remove('bx-moon');
        colorThemeIcon.classList.add('bx-sun');
        currentTheme.innerText = 'ライトモード';
        localStorage.setItem('color-theme', 'light-mode');
    }
});

if (localStorage.getItem('color-theme') === 'dark-mode') {
    colorThemeIcon.classList.remove('bx-sun');
    colorThemeIcon.classList.add('bx-moon');
    currentTheme.innerText = 'ダークモード';
}
