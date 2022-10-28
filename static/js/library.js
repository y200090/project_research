async function main() {
    // 英単語全検索APIを叩く
    const words = await getAPI('https://project-research.azurewebsites.net/api/word-all-search');
    console.log(words)

    const search = document.querySelector('#search'),
          clearIcon = document.querySelector('.clear-icon'),
          library = document.querySelector('.library');

    createLibrary(words);

    // 検索
    search.addEventListener('input', () => {
        clearIcon.style.display = 'flex';
        search.className = 'contain';

        while (library.firstChild) {
            library.removeChild(library.firstChild);
        }

        const results = words.filter(word => word.word.includes(search.value));

        if (results.length) {
            createLibrary(results);
        }
        else {
            const empty = document.createElement('p');
            empty.className = 'empty';
            empty.innerText = '一致する英単語が存在しません。';
            library.appendChild(empty);
        }
    });

    // 検索ワードリセット
    clearIcon.addEventListener('click', () => {
        search.value = '';
        search.classList.remove('contain');
        clearIcon.style.display = 'none';

        while (library.firstChild) {
            library.removeChild(library.firstChild);
        }

        createLibrary(words);
    });
    
};
main();

function createLibrary(words) {
    const library = document.querySelector('.library');
    
    words.forEach(word => {
        const flashcard = document.createElement('div');
        flashcard.className = 'flashcard';
        
        const cardTopBlock = document.createElement('div');
        cardTopBlock.className = 'card-top-block';
        flashcard.appendChild(cardTopBlock);

        const english = document.createElement('p');
        english.className = 'english';
        cardTopBlock.appendChild(english);
        english.innerText = word.word;

        const speakIcon = document.createElement('span');
        speakIcon.classList.add('material-symbols-outlined', 'speak-icon');
        cardTopBlock.appendChild(speakIcon);
        speakIcon.innerText = 'volume_up';
        speakIcon.addEventListener('click', () => {
            if ('speechSynthesis' in window) {
                const uttr = new SpeechSynthesisUtterance();
                uttr.text = word.word;
                uttr.lang = 'en-US';
                uttr.rate = 0.8;
                const voices = speechSynthesis.getVoices();
                voices.forEach(voice => {
                    if (voice.lang === 'en-US') {
                        uttr.voice = voice;
                    }
                });
                window.speechSynthesis.speak(uttr);
            }
            else {
                alert('このブラウザは音声合成に対応していません。');
            }
        });

        const cardBottomBlock = document.createElement('div');
        cardBottomBlock.className = 'card-bottom-block';
        flashcard.appendChild(cardBottomBlock);

        const translation = document.createElement('span');
        translation.className = 'translation';
        cardBottomBlock.appendChild(translation);
        translation.innerText = `日本語訳：${word.translation}`;

        const part = document.createElement('span');
        part.className = 'part';
        cardBottomBlock.appendChild(part); 
        part.innerText = `品詞：${word.part_jp}`;
        
        const rank = document.createElement('span');
        rank.className = 'rank';
        cardBottomBlock.appendChild(rank);
        rank.innerText = `CEFRランク：${word.rank}`;

        const freqRank = document.createElement('span');
        freqRank.className = 'freq-rank';
        cardBottomBlock.appendChild(freqRank);
        freqRank.innerText = `頻度：${word.freq_rank}`;

        const correctAnswerRate = document.createElement('span');
        correctAnswerRate.className = 'correct-answer-rate';
        cardBottomBlock.appendChild(correctAnswerRate);
        let rate = Math.floor(word.correct / word.response * 100);
        if (isNaN(rate)) {
            rate = 0.0;
        }
        correctAnswerRate.innerText = `ユーザー正解率：${rate}%`;
        
        library.appendChild(flashcard);
    });
};

// APIからデータを受け取る関数
async function getAPI(url) {
    return await fetch(url)
        .then(response => {
            return response.json();
        })
        .then(datas => {
            return datas;
        })
        .catch(error => {
            console.error('APIの取得に失敗しました。', error);
        });
};
