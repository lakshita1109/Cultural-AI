// ── TRACKING VARIABLES ──
let quizData = [];
let currentQuestion = 0;
let score = 0;
let answered = false;

// ── FETCH QUIZ FROM FLASK ──
async function fetchQuiz() {
    const landmark = localStorage.getItem('predictedLandmark') || 'taj_mahal';
    console.log('Fetching quiz for:', landmark);

    try {
        const response = await fetch(`/quiz/${landmark}`);
        const data = await response.json();
        console.log('Quiz data received:', data);
        quizData = data.questions;

        if (!quizData || quizData.length === 0) {
            console.error('No questions received!');
            return;
        }

        loadQuestion();
    } catch (error) {
        console.error('Could not fetch quiz:', error);
        quizData = [
            {
                question: 'Which of these is a UNESCO World Heritage Site in India?',
                options: ['Taj Mahal', 'Eiffel Tower', 'Statue of Liberty', 'Big Ben'],
                answer: 'Taj Mahal'
            },
            {
                question: 'Which Indian monument is known as the symbol of love?',
                options: ['Red Fort', 'Taj Mahal', 'Qutub Minar', 'India Gate'],
                answer: 'Taj Mahal'
            },
            {
                question: 'In which city is the Charminar located?',
                options: ['Chennai', 'Bangalore', 'Hyderabad', 'Mumbai'],
                answer: 'Hyderabad'
            },
            {
                question: 'Which empire built the temples of Hampi?',
                options: ['Mughal Empire', 'Maratha Empire', 'Vijayanagara Empire', 'Chola Empire'],
                answer: 'Vijayanagara Empire'
            },
            {
                question: 'What is the architectural style of Belur and Halebidu temples?',
                options: ['Mughal', 'Dravidian', 'Hoysala', 'Chalukya'],
                answer: 'Hoysala'
            }
        ];
        loadQuestion();
    }
}

// ── LOAD A QUESTION ──
function loadQuestion() {
    if (!quizData || quizData.length === 0) return;

    const data = quizData[currentQuestion];

    document.getElementById('question-text').textContent = data.question;

    const progressPercent = ((currentQuestion + 1) / quizData.length) * 100;
    document.getElementById('progress-fill').style.width = progressPercent + '%';

    document.getElementById('question-counter').textContent =
        'Question ' + (currentQuestion + 1) + ' of ' + quizData.length;

    const grid = document.getElementById('options-grid');
    grid.innerHTML = '';

    data.options.forEach(function (option) {
        const btn = document.createElement('button');
        btn.classList.add('option-btn');
        btn.textContent = option;
        btn.onclick = function () { checkAnswer(option, btn); };
        grid.appendChild(btn);
    });

    document.getElementById('next-btn').disabled = true;
    answered = false;
}

// ── CHECK ANSWER ──
function checkAnswer(selected, clickedBtn) {
    if (answered) return;
    answered = true;

    const correct = quizData[currentQuestion].answer;

    document.querySelectorAll('.option-btn').forEach(function (btn) {
        btn.disabled = true;
        if (btn.textContent === correct) {
            btn.classList.add('correct');
        }
    });

    if (selected !== correct) {
        clickedBtn.classList.add('wrong');
    } else {
        score++;
        document.getElementById('score').textContent = score;
    }

    document.getElementById('next-btn').disabled = false;
}

// ── NEXT QUESTION ──
function nextQuestion() {
    currentQuestion++;
    if (currentQuestion < quizData.length) {
        loadQuestion();
    } else {
        showResult();
    }
}

// ── SHOW FINAL RESULT ──
function showResult() {
    document.getElementById('quiz-screen').classList.add('hidden');
    document.getElementById('result-screen').classList.remove('hidden');
    document.getElementById('final-score').textContent = score;

    if (score === quizData.length) {
        document.getElementById('result-emoji').textContent = '🏆';
        document.getElementById('result-title').textContent = 'Perfect Score!';
        document.getElementById('result-message').textContent = 'You are a history expert!';
    } else if (score >= quizData.length / 2) {
        document.getElementById('result-emoji').textContent = '⭐';
        document.getElementById('result-title').textContent = 'Well Done!';
        document.getElementById('result-message').textContent = 'You know your history pretty well!';
    } else {
        document.getElementById('result-emoji').textContent = '📚';
        document.getElementById('result-title').textContent = 'Keep Learning!';
        document.getElementById('result-message').textContent = 'Read more about the landmark and try again!';
    }
}

// ── RESTART ──
function restartQuiz() {
    currentQuestion = 0;
    score = 0;
    answered = false;
    document.getElementById('score').textContent = '0';
    document.getElementById('quiz-screen').classList.remove('hidden');
    document.getElementById('result-screen').classList.add('hidden');
    loadQuestion();
}

// ── MAKE FUNCTIONS GLOBAL ──
window.nextQuestion = nextQuestion;
window.restartQuiz = restartQuiz;

// ── START ──
fetchQuiz();