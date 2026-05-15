// Get references to HTML elements
const uploadBox = document.getElementById('upload-box');
const imageInput = document.getElementById('image-input');
const previewImage = document.getElementById('preview-image');
const uploadPlaceholder = document.getElementById('upload-placeholder');
const identifyBtn = document.getElementById('identify-btn');

// When user clicks the upload box, open file picker
uploadBox.addEventListener('click', function() {
    imageInput.click();
});

// When user selects a file
imageInput.addEventListener('change', function() {
    const file = imageInput.files[0];

    // If no file selected, do nothing
    if (!file) return;

    // FileReader reads the file and converts it to a URL we can display
    const reader = new FileReader();

    reader.onload = function(e) {
        // Show the preview image
        previewImage.src = e.target.result;
        previewImage.hidden = false;

        // Hide the placeholder text
        uploadPlaceholder.hidden = true;

        // Enable the identify button
        identifyBtn.disabled = false;
    };

    reader.readAsDataURL(file);
});

// When user clicks Identify Landmark
identifyBtn.addEventListener('click', function() {
    // Save the image to localStorage so result page can show it
    const file = imageInput.files[0];
    const reader = new FileReader();

    reader.onload = function(e) {
        localStorage.setItem('uploadedImage', e.target.result);
        // Go to result page
        window.location.href = 'result.html';
    };

    reader.readAsDataURL(file);
});