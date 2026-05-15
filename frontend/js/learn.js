// ── QUOTES DATA ──
const quotes = [
    { text: "The world is a book, and those who do not travel read only one page.", author: "Saint Augustine" },
    { text: "To travel is to live.", author: "Hans Christian Andersen" },
    { text: "History is not a burden on the memory but an illumination of the soul.", author: "Lord Acton" },
    { text: "The more that you read, the more things you will know.", author: "Dr. Seuss" },
    { text: "Every monument tells a story. You just have to listen.", author: "Unknown" },
    { text: "Adventure is worthwhile in itself.", author: "Amelia Earhart" },
    { text: "In every walk with nature, one receives far more than he seeks.", author: "John Muir" },
    { text: "A child who reads will be an adult who thinks.", author: "Unknown" }
];

// ── TICKER FACTS ──
const tickerFacts = [
    "🏛️ The Taj Mahal took 22 years to build!",
    "🔴 Red Fort was the main residence of Mughal emperors for 200 years!",
    "🌊 Hampi was once one of the largest cities in the world!",
    "⭐ Qutub Minar is the tallest brick minaret in the world!",
    "🐘 Over 1000 elephants carried materials for the Taj Mahal!",
    "🌙 The Taj Mahal changes color — pink at dawn, white at noon, golden at night!",
    "🏔️ Ajanta Caves were carved out of rock over 2000 years ago!",
    "🎨 Konark Sun Temple was built in the shape of a giant chariot!",
    "📜 Charminar was built in 1591 to mark the end of a deadly plague!",
    "🦁 The Lion Capital of Ashoka is India's national emblem!"
];

// ── LANDMARK CARDS DATA ──
const landmarks = [
    {
        emoji: "🕌",
        title: "Taj Mahal",
        location: "📍 Agra, Uttar Pradesh",
        desc: "A symbol of eternal love built by Emperor Shah Jahan for his queen Mumtaz Mahal.",
        tag: "Mughal Era"
    },
    {
        emoji: "🏯",
        title: "Red Fort",
        location: "📍 Delhi",
        desc: "The majestic red sandstone fortress that was home to Mughal emperors for 200 years.",
        tag: "Mughal Era"
    },
    {
        emoji: "🗼",
        title: "Qutub Minar",
        location: "📍 Delhi",
        desc: "The world's tallest brick minaret standing 73 metres tall, built in 1193 AD.",
        tag: "Delhi Sultanate"
    },
    {
        emoji: "🌅",
        title: "Konark Sun Temple",
        location: "📍 Odisha",
        desc: "A 13th century marvel built in the shape of a giant chariot of the Sun God.",
        tag: "Medieval India"
    },
    {
        emoji: "🏔️",
        title: "Hampi",
        location: "📍 Karnataka",
        desc: "Ancient ruins of the Vijayanagara Empire — once one of the world's largest cities.",
        tag: "Vijayanagara Era"
    },
    {
        emoji: "🌙",
        title: "Charminar",
        location: "📍 Hyderabad, Telangana",
        desc: "Built in 1591 to celebrate the end of a plague, this mosque is Hyderabad's icon.",
        tag: "Qutb Shahi Era"
    },
    {
        emoji: "🎨",
        title: "Ajanta Caves",
        location: "📍 Aurangabad, Maharashtra",
        desc: "Buddhist caves featuring stunning 2000-year-old paintings carved into solid rock.",
        tag: "Ancient India"
    },
    {
        emoji: "🦁",
        title: "Ellora Caves",
        location: "📍 Maharashtra",
        desc: "A UNESCO site with Hindu, Buddhist and Jain temples carved from a single mountain.",
        tag: "Ancient India"
    },
    {
        emoji: "🛕",
        title: "Brihadeeswarar Temple",
        location: "📍 Thanjavur, Tamil Nadu",
        desc: "A 1000-year-old Chola masterpiece whose shadow never falls on the ground at noon.",
        tag: "Chola Dynasty"
    }
];

// ── CURRENT QUOTE INDEX ──
let currentQuoteIndex = 0;

// ── SHOW A NEW QUOTE ──
function newQuote() {
    currentQuoteIndex = (currentQuoteIndex + 1) % quotes.length;
    const quoteText = document.getElementById('quote-text');
    const quoteAuthor = document.getElementById('quote-author');

    // Fade out
    quoteText.style.opacity = '0';
    quoteAuthor.style.opacity = '0';

    setTimeout(function() {
        quoteText.textContent = quotes[currentQuoteIndex].text;
        quoteAuthor.textContent = '— ' + quotes[currentQuoteIndex].author;

        // Fade in
        quoteText.style.opacity = '1';
        quoteAuthor.style.opacity = '1';
    }, 400);
}

// ── BUILD TICKER ──
function buildTicker() {
    const content = document.getElementById('ticker-content');

    // Duplicate facts so ticker loops seamlessly
    const allFacts = [...tickerFacts, ...tickerFacts];
    content.textContent = allFacts.join('     ·     ');
}

// ── BUILD LANDMARK CARDS ──
function buildCards() {
    const grid = document.getElementById('cards-grid');

    landmarks.forEach(function(landmark, index) {
        const card = document.createElement('div');
        card.classList.add('landmark-card');

        card.innerHTML = `
            <span class="card-emoji">${landmark.emoji}</span>
            <div class="card-title">${landmark.title}</div>
            <div class="card-location">${landmark.location}</div>
            <div class="card-desc">${landmark.desc}</div>
            <span class="card-tag">${landmark.tag}</span>
        `;

        // Click card → go to quiz
        card.addEventListener('click', function() {
            window.location.href = 'quiz.html';
        });

        grid.appendChild(card);

        // Staggered entrance animation
        setTimeout(function() {
            card.classList.add('visible');
        }, index * 100);
    });
}

// ── SCROLL ANIMATION (cards animate when visible on screen) ──
function setupScrollAnimation() {
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.landmark-card').forEach(function(card) {
        observer.observe(card);
    });
}

// ── AUTO ROTATE QUOTES every 8 seconds ──
setInterval(newQuote, 8000);

// ── RUN EVERYTHING ──
buildTicker();
buildCards();
setupScrollAnimation();