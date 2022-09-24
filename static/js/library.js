fetch('http://127.0.0.1:8000/api/view-all-words')
    .then(response => {
        return response.json();
    })
    .then(datas => main(datas))
    .catch(error => console.error('APIの取得に失敗しました。', error))

const search = document.querySelector('.search-bar > input'),
      clearIcon = document.querySelector('.clear-icon'),
      flashcards = document.querySelector('.flashcards');

function main(datas) {
    wordsForEach(datas);
    // 検索処理
    search.addEventListener('input', () => {
        clearIcon.style.display = 'flex';
        search.className = 'contain';

        while (flashcards.firstChild) {
            flashcards.removeChild(flashcards.firstChild);
        }
        const results = datas.filter(data => data.word.includes(search.value));
        wordsForEach(results);
    });
    // 検索ワードリセット処理
    clearIcon.addEventListener('click', () => {
        search.value = '';
        search.classList.remove('contain');
        clearIcon.style.display = 'none';

        while (flashcards.firstChild) {
            flashcards.removeChild(flashcards.firstChild);
        }
        wordsForEach(datas);
    });
};

function wordsForEach(words) {
    for (let i = 0; i < words.length; i++) {
        const flashcard = document.createElement('div');
        flashcard.classList.add('flashcard');

        const cardTop = document.createElement('article');
        cardTop.classList.add('card-top');

        const englishWord = document.createElement('span');
        englishWord.classList.add('english-word');
        cardTop.appendChild(englishWord);

        const openIcon = document.createElement('i');
        openIcon.classList.add('bx', 'bx-chevron-down', 'open-icon');
        cardTop.appendChild(openIcon);

        flashcard.appendChild(cardTop);

        const cardBottom = document.createElement('article');
        cardBottom.classList.add('card-bottom');

        const translationWord = document.createElement('span');
        translationWord.classList.add('translation-word');
        cardBottom.appendChild(translationWord);

        const partWord = document.createElement('span');
        partWord.classList.add('part-word');
        cardBottom.appendChild(partWord);

        flashcard.appendChild(cardBottom);

        flashcards.appendChild(flashcard);
    }

    const englishWords = [...document.querySelectorAll('.english-word')],
          translationWords = [...document.querySelectorAll('.translation-word')],
          partWords = [...document.querySelectorAll('.part-word')];

    words.forEach((word, index) => {
        englishWords[index].innerText = word.word;
        translationWords[index].innerText = `和訳：${word.translation}`;
        partWords[index].innerText = `品詞：${word.part_jp}`;
    });

    const openIcons = [...document.querySelectorAll('.open-icon')];
    openIcons.forEach((icon, index) => {
        icon.addEventListener('click', () => {
            openBoxes[index].classList.toggle('bx-chevron-down');
            openBoxes[index].classList.toggle('bx-chevron-up');
        });
    });
};
