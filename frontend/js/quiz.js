// ── QUIZ DATA (will come from Flask later) ──
const quizData = [
    {
        question: "In which city is the Taj Mahal located?",
        options: ["Delhi", "Agra", "Jaipur", "Lucknow"],
        answer: "Agra"
    },
    {
        question: "Which Mughal emperor built the Taj Mahal?",
        options: ["Akbar", "Humayun", "Shah Jahan", "Aurangzeb"],
        answer: "Shah Jahan"
    },
    {
        question: "How many years did it take to build the Taj Mahal?",
        options: ["10 years", "15 years", "22 years", "30 years"],
        answer: "22 years"
    },
    {
        question: "The Taj Mahal was built in memory of whom?",
        options: ["Nur Jahan", "Mumtaz Mahal", "Razia Sultana", "Jodha Bai"],
        answer: "Mumtaz Mahal"
    },
    {
        question: "The Taj Mahal became a UNESCO World Heritage Site in which year?",
        options: ["1972", "1978", "1983", "1990"],
        answer: "1983"
    }
];

// ── TRACKING VARIABLES ──
let currentQuestion = 0;
let score = 0;
let answered = false;

// ── LOAD A QUESTION ──
function loadQuestion() {
    const data = quizData[currentQuestion];

    // Update question text
    document.getElementById('question-text').textContent = data.question;

    // Update progress bar
    const progressPercent = ((currentQuestion + 1) / quizData.length) * 100;
    document.getElementById('progress-fill').style.width = progressPercent + '%';

    // Update counter
    document.getElementById('question-counter').textContent =
        'Question ' + (currentQuestion + 1) + ' of ' + quizData.length;

    // Clear previous options
    const grid = document.getElementById('options-grid');
    grid.innerHTML = '';

    // Create option buttons
    data.options.forEach(function(option) {
        const btn = document.createElement('button');
        btn.classList.add('option-btn');
        btn.textContent = option;
        btn.onclick = function() { checkAnswer(option, btn); };
        grid.appendChild(btn);
    });

    // Reset next button
    document.getElementById('next-btn').disabled = true;
    answered = false;
}

// ── CHECK ANSWER ──
function checkAnswer(selected, clickedBtn) {
    // Prevent answering twice
    if (answered) return;
    answered = true;

    const correct = quizData[currentQuestion].answer;

    // Disable all buttons
    document.querySelectorAll('.option-btn').forEach(function(btn) {
        btn.disabled = true;

        // Highlight correct answer green
        if (btn.textContent === correct) {
            btn.classList.add('correct');
        }
    });

    // If wrong, highlight selected red
    if (selected !== correct) {
        clickedBtn.classList.add('wrong');
    } else {
        score++;
        document.getElementById('score').textContent = score;
    }

    // Enable next button
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

    // Different message based on score
    if (score === 5) {
        document.getElementById('result-emoji').textContent = '🏆';
        document.getElementById('result-title').textContent = 'Perfect Score!';
        document.getElementById('result-message').textContent = 'You are a history expert!';
    } else if (score >= 3) {
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

// Start the quiz on page load
loadQuestion();