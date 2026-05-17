function loadResult() {

    const stored = localStorage.getItem('predictionResult');

    if (!stored) {
        document.getElementById('history-text').textContent = 'No result found. Please go back and upload an image.';
        return;
    }

    const data = JSON.parse(stored);

    document.getElementById('landmark-name').textContent = data.landmark;
    document.getElementById('landmark-location').textContent = data.location;

    const fill = document.getElementById('confidence-fill');
    const percent = document.getElementById('confidence-percent');
    percent.textContent = data.confidence + '%';
    setTimeout(function() {
        fill.style.width = data.confidence + '%';
    }, 300);

    // Fill history
    document.getElementById('history-text').textContent = data.history;

    // Fill culture
    document.getElementById('culture-text').textContent = data.culture;

    // Build facts list
    const factsList = document.getElementById('facts-list');
    factsList.innerHTML = '';

    if (data.facts && data.facts.length > 0) {
        data.facts.forEach(function(fact) {
            const li = document.createElement('li');
            li.textContent = fact;
            factsList.appendChild(li);
        });
// Save predicted landmark for quiz page
localStorage.setItem('predictedLandmark', data.landmark.toLowerCase().replace(/ /g, '_'));
    }

    // Show uploaded image
    const storedImage = localStorage.getItem('uploadedImage');
    if (storedImage) {
        document.getElementById('uploaded-img').src = storedImage;
    }
}
function showTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(function(tab) {
        tab.classList.add('hidden');
    });
    document.querySelectorAll('.tab-btn').forEach(function(btn) {
        btn.classList.remove('active');
    });
    document.getElementById(tabName).classList.remove('hidden');
    event.target.classList.add('active');
}

// ── MAKE FUNCTIONS GLOBAL ──
window.showTab = showTab;


loadResult();