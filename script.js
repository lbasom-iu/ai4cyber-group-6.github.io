let slideIndex = 0; // Start with the first image

function changeSlide(moveStep) {
    let slides = document.getElementsByClassName("carousel-images")[0].getElementsByTagName("img");
    slideIndex += moveStep;
    
    if (slideIndex >= slides.length) {
        slideIndex = 0; // Wrap back to the first image
    } else if (slideIndex < 0) {
        slideIndex = slides.length - 1; // Wrap around to the last image
    }
    
    // Hide all images
    for (let i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";  
    }
    
    // Show the current image
    slides[slideIndex].style.display = "block";
}

// Initialize the carousel to display the first image
window.onload = function() {
    changeSlide(0);
};