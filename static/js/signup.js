const imageArea = document.querySelector('.header > img');
const images = ['../static/images/undraw_programmer_re_owql.svg', 
                '../static/images/undraw_my_documents_re_13dc.svg', 
                '../static/images/undraw_relaunch_day_902d.svg',
                '../static/images/undraw_taken_re_yn20.svg'];
window.addEventListener('load', () => {
    const imageNumber = Math.floor(Math.random() * images.length);
    imageArea.src = images[imageNumber];
});

const ShowHide = [...document.querySelectorAll('.show-hide')];
const passwords = [...document.querySelectorAll('#password')];
ShowHide.forEach(eyeIcon => {
    eyeIcon.addEventListener('click', () => {
        passwords.forEach(password => {
            if (password.type === "password") {
                password.type = "text";
                ShowHide.forEach(icon => {
                    icon.classList.replace('bx-hide', 'bx-show');
                });
            } else {
                password.type = "password";
                ShowHide.forEach(icon => {
                    icon.classList.replace('bx-show', 'bx-hide');
                });
            }
        });
    });
});
