const userIcon = document.querySelector('.user-icon'),
      editFields = [...document.querySelectorAll('.edit-field')],
      unedited = [...document.querySelectorAll('.unedited')],
      editIcons = [...document.querySelectorAll('.edit-icon')],
      editInput = [...document.querySelectorAll('.unedited > input')],
      editButton = document.querySelector('#edit-button'),
      update = document.querySelector('#update');

editFields.forEach(editField => {
    editField.classList.add('inactive');
});
editIcons.forEach(editIcon => {
    editIcon.classList.add('inactive');
});
update.classList.add('inactive');

editButton.addEventListener('click', () => {
    editIcons.forEach((editIcon, index) => {
        editIcon.classList.remove('inactive');
        editIcon.addEventListener('click', () => {
            unedited[index].classList.remove('inactive');
            editInput[index].focus();
        });
    });
    editButton.classList.add('inactive');
    update.classList.remove('inactive');
});

const validate = document.querySelector('.validate');
if (validate) {
    editFields.forEach(editField => {
        editField.addEventListener('input', () => {
            validate.style.display = 'none';
        });
    });
}

const singupDateInput = document.querySelector('.signup-date > input');
let str;
str = signupDate.replace(/-/g, '/');
str = str.substr(0, str.indexOf('.'));
singupDateInput.value = str;
