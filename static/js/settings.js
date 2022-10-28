const userInfoContent = document.querySelector('.user-info-content'),
      medal = document.querySelector('.medal'),
      colorTheme = document.querySelector('.color-theme'),
      switchBars = [...document.querySelectorAll('.switch-bar')],
      colorThemeIcon = document.querySelector('.color-theme-icon'),
      currentTheme = document.querySelector('.current-theme'),
      colorThemeSwitch = document.querySelector('.color-theme > .switch-bar');

if (remembered == 0) {
    medal.classList.add('inactive');
}
else {
    if (remembered <= 100) {
        medal.src = '../../../../static/images/bronze-medal-icon.svg';
    }
    else if (remembered <= 1000) {
        medal.src = '../../../../static/images/silver-medal-icon.svg';
    }
    else if (remembered > 1000) {
        medal.src = '../../../../static/images/gold-medal-icon.svg';
    }
}

colorThemeSwitch.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    
    if (document.body.classList.contains('dark-mode')) {
        colorThemeIcon.classList.remove('bx-sun');
        colorThemeIcon.classList.add('bx-moon')
        currentTheme.innerText = 'ダークモード';
        // ローカルストレージに保存（キーの更新）
        localStorage.setItem('color-theme', 'dark-mode');

    } else if (colorThemeIcon.classList.contains('bx-moon')) {
        colorThemeIcon.classList.remove('bx-moon');
        colorThemeIcon.classList.add('bx-sun');
        currentTheme.innerText = 'ライトモード';
        // ローカルストレージに保存（キーの更新）
        localStorage.setItem('color-theme', 'light-mode');
    }
});

// ローカルストレージから取得
if (localStorage.getItem('color-theme') === 'dark-mode') {
    colorThemeIcon.classList.remove('bx-sun');
    colorThemeIcon.classList.add('bx-moon');
    currentTheme.innerText = 'ダークモード';
}
