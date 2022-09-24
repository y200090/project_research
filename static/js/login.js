const imageArea = document.querySelector('.header > img');
const images = ['../static/images/undraw_male_avatar_323b.svg', 
                '../static/images/undraw_female_avatar_w3jk.svg', 
                '../static/images/undraw_profile_pic_ic-5-t.svg'];
window.addEventListener('load', () => {
    const imageNumber = Math.floor(Math.random() * images.length);
    imageArea.src = images[imageNumber];
});

const showHide = [...document.querySelectorAll('.show-hide')];
const passwords = [...document.querySelectorAll('#password')];
showHide.forEach(eyeIcon => {
    eyeIcon.addEventListener('click', () => {
        passwords.forEach(password => {
            if (password.type === "password") {
                password.type = "text";
                showHide.forEach(icon => {
                    icon.classList.replace('bx-hide', 'bx-show');
                });
            } else {
                password.type = "password";
                showHide.forEach(icon => {
                    icon.classList.replace('bx-show', 'bx-hide');
                });
            }
        });
    });
});
