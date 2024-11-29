let currentSlide = 0;
const slides = document.querySelectorAll('.slide-container img');
const totalSlides = slides.length;
let autoSlideInterval; // Declare variable for auto-slide interval

// Show the first slide initially
slides[currentSlide].style.opacity = 1; // Set the first slide to be visible

function showSlide(index) {
    // Fade out current slide
    slides[currentSlide].style.opacity = 0; // Hide current slide

    // Update the current slide index
    currentSlide = (index + totalSlides) % totalSlides; // Loop back to the start

    // Fade in new slide
    slides[currentSlide].style.opacity = 1; // Show new slide
}

function startAutoSlide() {
    autoSlideInterval = setInterval(() => {
        showSlide(currentSlide + 1);
    }, 5000); // Change slides every 5 seconds
}

function stopAutoSlide() {
    clearInterval(autoSlideInterval); // Stop auto sliding
}

// Event listeners for the navigation buttons
document.querySelector('.nav-button.left').addEventListener('click', () => {
    stopAutoSlide(); // Stop auto-slide when button is clicked
    showSlide(currentSlide - 1);
    startAutoSlide(); // Restart auto-slide after changing slide
});

document.querySelector('.nav-button.right').addEventListener('click', () => {
    stopAutoSlide(); // Stop auto-slide when button is clicked
    showSlide(currentSlide + 1);
    startAutoSlide(); // Restart auto-slide after changing slide
});

// Start auto-slide on initial load
startAutoSlide();
