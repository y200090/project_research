// View All Words APIを叩く
fetch('https://project-research.azurewebsites.net/api/view-all-words')
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
    // 検索
    search.addEventListener('input', () => {
        clearIcon.style.display = 'flex';
        search.className = 'contain';

        while (flashcards.firstChild) {
            flashcards.removeChild(flashcards.firstChild);
        }
        const results = datas.filter(data => data.word.includes(search.value));
        wordsForEach(results);
    });
    // 検索ワードリセット
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
    words.forEach(word => {
        const flashcard = document.createElement('div');
        flashcard.classList.add('flashcard');

        const cardTop = document.createElement('article');
        cardTop.classList.add('card-top');

        const englishWord = document.createElement('span');
        englishWord.classList.add('english-word');
        cardTop.appendChild(englishWord);
        
        englishWord.innerText = word.word;

        const openIcon = document.createElement('i');
        openIcon.classList.add('bx', 'bx-chevron-down', 'open-icon');
        cardTop.appendChild(openIcon);

        const translationWord = document.createElement('span');
        translationWord.classList.add('translation-word');
        cardTop.appendChild(translationWord);
        
        translationWord.innerText = `和訳：${word.translation}`;
        
        const partWord = document.createElement('span');
        partWord.classList.add('part-word');
        cardTop.appendChild(partWord);
        
        partWord.innerText = `品詞：${word.part_jp}`;
        
        openIcon.addEventListener('click', () => {
            openIcon.classList.toggle('bx-chevron-down');
            openIcon.classList.toggle('bx-chevron-up');
            cardTop.classList.toggle('active');
        });
        
        flashcard.appendChild(cardTop);

        flashcards.appendChild(flashcard);
    });
};
