if (localStorage.getItem('color-theme') === 'dark-mode') {
    document.body.classList.add('dark-mode');
}
else if (localStorage.getItem('color-theme') === 'light-mode') {
    document.body.classList.remove('dark-mode');
}
