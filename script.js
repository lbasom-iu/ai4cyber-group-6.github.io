let slideIndex = 0; // Start with the first image

function changeSlide(moveStep) {
    let slides = document.querySelectorAll(".carousel-images img");
    slideIndex += moveStep;
    
    if (slideIndex >= slides.length) {
        slideIndex = 0;
    } else if (slideIndex < 0) {
        slideIndex = slides.length - 1;
    }
    
    // Hide all images
    slides.forEach(slide => slide.style.display = "none");
    
    // Show the current image
    slides[slideIndex].style.display = "block";
    
    // Update the image counter
    document.getElementById("imageCounter").innerText = `${slideIndex + 1}/${slides.length}`;
}

// Initialize the carousel to display the first image
document.addEventListener('DOMContentLoaded', (event) => {
    changeSlide(0);
});