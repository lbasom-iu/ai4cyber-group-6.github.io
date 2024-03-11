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
function toggleEnlarge(img) {
    img.classList.toggle('enlarged');
    // To prevent scrolling when the image is enlarged and ensure the background is darkened
    if (img.classList.contains('enlarged')) {
        document.body.style.overflow = 'hidden';
        document.body.style.background = 'rgba(0,0,0,0.5)'; // Add a dark background overlay
    } else {
        document.body.style.overflow = '';
        document.body.style.background = '';
    }
}

// Initialize the carousel to display the first image
document.addEventListener('DOMContentLoaded', (event) => {
    changeSlide(0);
});