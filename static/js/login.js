const setFillHeight = () => {
    const vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty('--vh', `${vh}px`);
};
window.addEventListener('resize', setFillHeight);
window.addEventListener('load', setFillHeight);
setFillHeight();

const loginIcon = document.querySelector('.login-icon'),
      icons = ['../static/images/undraw_conversation_re_c26v.svg',
               '../static/images/undraw_designer_re_5v95.svg',
               '../static/images/undraw_programmer_re_owql.svg',
               '../static/images/undraw_my_documents_re_13dc.svg',
               '../static/images/undraw_relaunch_day_902d.svg',
               '../static/images/undraw_taken_re_yn20.svg',
               '../static/images/undraw_developer_activity_re_39tg.svg',
               '../static/images/undraw_urban_design_kpu8.svg',
               '../static/images/undraw_working_late_re_0c3y.svg',
               '../static/images/undraw_my_universe_803e.svg',
               '../static/images/undraw_to_the_moon_re_q21i.svg',
               '../static/images/undraw_refreshing_beverage_td3r.svg'];
window.addEventListener('load', () => {
    const iconNumber = Math.floor(Math.random() * icons.length);
    loginIcon.src = icons[iconNumber];
});

const showHide = [...document.querySelectorAll('.show-hide')],
      passwords = [...document.querySelectorAll('#password')];
showHide.forEach(eyeIcon => {
    eyeIcon.addEventListener('click', () => {
        passwords.forEach(password => {
            if (password.type === "password") {
                password.type = "text";
                showHide.forEach(icon => {
                    icon.classList.replace('bx-hide', 'bx-show');
                });
            }
            else {
                password.type = "password";
                showHide.forEach(icon => {
                    icon.classList.replace('bx-show', 'bx-hide');
                });
            }
        });
    });
});

const inputFields = [...document.querySelectorAll('.input-field')],
      flash = document.querySelector('.flash');
if (flash) {
    inputFields.forEach(inputField => {
        inputField.addEventListener('input', () => {
            flash.style.display = 'none';
        });
    });
}

// const perEntries = performance.getEntriesByType('navigation');
// let type = null;
// perEntries.forEach(function(perEntrie) {
//     type = perEntrie.type;
// });
// if (type == 'reload') {
//     alert('alert');
// }