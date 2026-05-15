// ── DUMMY DATA (we replace this with real AI data in Phase 5) ──
const dummyData = {
    name: "Taj Mahal",
    confidence: 94,
    location: "Agra, Uttar Pradesh, India",
    history: "The Taj Mahal was built by Mughal emperor Shah Jahan between 1632 and 1653 in memory of his beloved wife Mumtaz Mahal. It took over 20,000 artisans and craftsmen to complete. The monument is considered the finest example of Mughal architecture, blending Persian, Islamic, and Indian styles into one perfect structure.",
    facts: [
        "The Taj Mahal took 22 years to build — from 1631 to 1653.",
        "Over 1,000 elephants were used to transport building materials.",
        "The white marble changes color — pinkish at dawn, white at noon, golden at night.",
        "The four minarets are built slightly tilted outward to protect the tomb if they fall.",
        "It is a UNESCO World Heritage Site since 1983."
    ],
    culture: "The Taj Mahal is a symbol of eternal love and one of India's most treasured cultural icons. It represents the pinnacle of Mughal artistry and continues to draw millions of visitors from around the world every year. It reflects India's rich composite culture blending multiple architectural traditions."
};

// ── LOAD DATA INTO THE PAGE ──
function loadResult() {
    // Set landmark name
    document.getElementById('landmark-name').textContent = dummyData.name;

    // Set location
    document.getElementById('landmark-location').textContent = dummyData.location;

    // Animate confidence bar
    const fill = document.getElementById('confidence-fill');
    const percent = document.getElementById('confidence-percent');
    percent.textContent = dummyData.confidence + '%';

    // Small delay so animation is visible
    setTimeout(function() {
        fill.style.width = dummyData.confidence + '%';
    }, 300);

    // Set history text
    document.getElementById('history-text').textContent = dummyData.history;

    // Set culture text
    document.getElementById('culture-text').textContent = dummyData.culture;

    // Build facts list
    const factsList = document.getElementById('facts-list');
    dummyData.facts.forEach(function(fact) {
        const li = document.createElement('li');
        li.textContent = fact;
        factsList.appendChild(li);
    });

    // Show uploaded image if stored
    const storedImage = localStorage.getItem('uploadedImage');
    if (storedImage) {
        document.getElementById('uploaded-img').src = storedImage;
    }
}

// ── TAB SWITCHING ──
function showTab(tabName) {
    // Hide all tab contents
    document.querySelectorAll('.tab-content').forEach(function(tab) {
        tab.classList.add('hidden');
    });

    // Remove active from all buttons
    document.querySelectorAll('.tab-btn').forEach(function(btn) {
        btn.classList.remove('active');
    });

    // Show selected tab
    document.getElementById(tabName).classList.remove('hidden');

    // Mark clicked button as active
    event.target.classList.add('active');
}

// Run when page loads
loadResult();