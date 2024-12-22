function createImageArray(numImages) {
    let images = [];
    for (let i = 1; i <= numImages; i++) {
        images.push(`page_${i}.jpg`);
    }
    return images;
}

const images = createImageArray(4)
function changeImage() {
    document.getElementById("dapoza").src =
      "static/images/" + images[Math.floor(Math.random() * images.length)];
}

function showFileName() {
    const fileInput = document.getElementById('file');
    const fileNameDisplay = document.getElementById('file-name');
    if (fileInput.files.length > 0) {
        fileNameDisplay.textContent = fileInput.files[0].name;
    } else {
        fileNameDisplay.textContent = 'No file chosen';
    }
}