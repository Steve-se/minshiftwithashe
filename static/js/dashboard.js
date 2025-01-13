const sidebarToggle =  document.querySelector("#sidebar-toggle");
sidebarToggle.addEventListener("click", function(){
    document.querySelector("#sidebar").classList.toggle("collapsed");
});

// Select all navigation links
const navLinks = document.querySelectorAll('.nav-link');

// Add click event listener to each link
navLinks.forEach(link => {
    link.addEventListener('click', function() {
        // Remove the 'active' class from all links
        navLinks.forEach(link => link.classList.remove('active'));
        
        // Add the 'active' class to the clicked link
        this.classList.add('active');
    });
});

// blog File and Image //

// blog fiile and image ends here //


// Function to upload Image and Videos
const uploadMediaButton = document.getElementById('uploadMediaButton');
const mediaInput = document.getElementById('mediaInput');
const mediaList = document.getElementById('mediaList');

// When the button is clicked, trigger the file input click
uploadMediaButton.addEventListener('click', () => {
    mediaInput.click();
});

// Handle the media selection
mediaInput.addEventListener('change', (event) => {
    // Clear previous media list
    mediaList.innerHTML = '';

    // Get the selected files
    const files = event.target.files;

    // Display the selected images and videos
    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const listItem = document.createElement('div');
        listItem.classList.add('media-container');

        // Display image files
        if (file.type.startsWith('image/')) {
            const img = document.createElement('img');
            img.src = URL.createObjectURL(file);
            img.alt = file.name;
            listItem.appendChild(img);
        }

        // Display video files
        if (file.type.startsWith('video/')) {
            const video = document.createElement('video');
            video.src = URL.createObjectURL(file);
            video.controls = true;
            listItem.appendChild(video);
        }

        mediaList.appendChild(listItem);
    }
});






