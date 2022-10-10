const curShowHide = [...document.querySelectorAll('.curpwd > .show-hide')],
      chgShowHide = [...document.querySelectorAll('.chgpwd > .show-hide')],
      cfmShowHide = [...document.querySelectorAll('.cfmpwd > .show-hide')],
      curpwds = [...document.querySelectorAll('#curpwd')],
      chgpwds = [...document.querySelectorAll('#chgpwd')],
      cfmpwds = [...document.querySelectorAll('#cfmpwd')];

curShowHide.forEach(eyeIcon => {
    eyeIcon.addEventListener('click', () => {
        curpwds.forEach(curpwd => {
            if (curpwd.type === "password") {
                curpwd.type = "text";
                curShowHide.forEach(icon => {
                    icon.classList.replace('bx-hide', 'bx-show');
                });
            }
            else {
                curpwd.type = "password";
                curShowHide.forEach(icon => {
                    icon.classList.replace('bx-show', 'bx-hide');
                });
            }
        });
    });
});
chgShowHide.forEach(eyeIcon => {
    eyeIcon.addEventListener('click', () => {
        chgpwds.forEach(chgpwd => {
            if (chgpwd.type === "password") {
                chgpwd.type = "text";
                chgShowHide.forEach(icon => {
                    icon.classList.replace('bx-hide', 'bx-show');
                });
            }
            else {
                chgpwd.type = "password";
                chgShowHide.forEach(icon => {
                    icon.classList.replace('bx-show', 'bx-hide');
                });
            }
        });
    });
});
cfmShowHide.forEach(eyeIcon => {
    eyeIcon.addEventListener('click', () => {
        cfmpwds.forEach(cfmpwd => {
            if (cfmpwd.type === "password") {
                cfmpwd.type = "text";
                cfmShowHide.forEach(icon => {
                    icon.classList.replace('bx-hide', 'bx-show');
                });
            }
            else {
                cfmpwd.type = "password";
                cfmShowHide.forEach(icon => {
                    icon.classList.replace('bx-show', 'bx-hide');
                });
            }
        });
    });
});

const postFields = [...document.querySelectorAll('.post-field')],
      validate = document.querySelector('.validate');
if (validate) {
    postFields.forEach(postField => {
        postField.addEventListener('input', () => {
            validate.style.display = 'none';
        });
    });
}
