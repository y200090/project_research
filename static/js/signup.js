const setFillHeight = () => {
    const vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty('--vh', `${vh}px`);
};
window.addEventListener('resize', setFillHeight);
window.addEventListener('load', setFillHeight);
setFillHeight();

const signupIcon = document.querySelector('.signup-icon');
const icons = ['../static/images/undraw_female_avatar_w3jk.svg', 
                '../static/images/undraw_male_avatar_323b.svg', 
                '../static/images/undraw_profile_pic_ic-5-t.svg',
                '../static/images/undraw_profile_pic_re_754n.svg'];
window.addEventListener('load', () => {
    const iconNumber = Math.floor(Math.random() * icons.length);
    signupIcon.src = icons[iconNumber];
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
            }
            else {
                password.type = "password";
                ShowHide.forEach(icon => {
                    icon.classList.replace('bx-show', 'bx-hide');
                });
            }
        });
    });
});

const validate = document.querySelector('.validate-field');
if (validate) {
    validate.parentElement.classList.add('invalidate');
}
