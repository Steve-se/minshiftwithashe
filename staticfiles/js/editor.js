// To handle file selection for blog post //
  function displayFileName() {
    var fileInput = document.getElementById('fileInput');
    var fileNameDisplay = document.getElementById('fileNameDisplay');
    
    if (fileInput.files.length > 0) {
        var file = fileInput.files[0];
        fileNameDisplay.textContent = "Uploaded file: " + file.name;
    } else {
        fileNameDisplay.textContent = "No file uploaded";
    }
}



// JavaScript to handle file selection for blog description //
document.getElementById('uploadInput').addEventListener('change', function() {
    var file = this.files[0]; // Get the selected file

    if (file) {
        // Create a FileReader to read the file
        var reader = new FileReader();

        // Set up the FileReader to insert the image after loading
        reader.addEventListener('load', function() {
            var imgElement = document.createElement('img');
            imgElement.src = reader.result;
            imgElement.style.maxWidth = '100%'; // Optional: Set maximum width

            // Display the uploaded image
            var displayArea = document.getElementById('imageDisplay');
            displayArea.innerHTML = ''; // Clear previous image
            displayArea.appendChild(imgElement);
        });

        // Read the selected file as a data URL
        reader.readAsDataURL(file);
    }
});


function execCommand(command, value = null) {
    document.execCommand(command, false, value);
}




function execCmd(command, value = null) {
    document.execCommand(command, false, value);
}

function insertLink() {
    const url = prompt("Enter the URL:");
    if (url) {
        document.execCommand('createLink', false, url);
    }
}

function uploadImage() {
    const file = document.getElementById('imageUpload').files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const img = document.createElement('img');
            img.src = e.target.result;
            document.querySelector('.editor').appendChild(img);
        };
        reader.readAsDataURL(file);
    }
}

function countWords() {
    const text = document.querySelector('.editor').innerText;
    const wordCount = text.split(/\s+/).filter(word => word.length > 0).length;
    document.getElementById('wordCount').innerText = `Words: ${wordCount}`;
}
