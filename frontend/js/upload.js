const uploadBox = document.getElementById('upload-box');
const imageInput = document.getElementById('image-input');
const previewImage = document.getElementById('preview-image');
const uploadPlaceholder = document.getElementById('upload-placeholder');
const identifyBtn = document.getElementById('identify-btn');

// Click upload box → open file picker
uploadBox.addEventListener('click', function () {
    imageInput.click();
});

// When user selects a file → show preview
imageInput.addEventListener('change', function () {
    const file = imageInput.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function (e) {
        previewImage.src = e.target.result;
        previewImage.hidden = false;
        uploadPlaceholder.hidden = true;
        identifyBtn.disabled = false;
    };
    reader.readAsDataURL(file);
});

// When user clicks Identify Landmark
identifyBtn.addEventListener('click', async function () {

    const file = imageInput.files[0];
    if (!file) return;

    // Change button text to show loading
    identifyBtn.textContent = 'Identifying...';
    identifyBtn.disabled = true;

    // Create FormData to send image to Flask
    const formData = new FormData();
    formData.append('image', file);

    try {
        // Send image to Flask backend
        const response = await fetch('https://zunzunn-cltural-ai-backend.hf.space/predict', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        // Save result to localStorage so result page can use it
        localStorage.setItem('predictionResult', JSON.stringify(data));

        // Also save image preview
        const reader = new FileReader();
        reader.onload = function (e) {
            localStorage.setItem('uploadedImage', e.target.result);
            // Go to result page
            window.location.href = 'result.html';
        };
        reader.readAsDataURL(file);

    } catch (error) {
        // If Flask is not running, show error
        alert('Could not connect to the Cultural AI backend. Please try again later.');
        identifyBtn.textContent = 'Identify Landmark';
        identifyBtn.disabled = false;
    }
});