"use strict"

const lazyImages = document.querySelectorAll('#cap_image');
const windowHeight = document.documentElement.clientHeight;

let lazyImagesPositions = [];
if (lazyImages.length > 0) {
    lazyImages.forEach(img => {
        if (img.dataset.src) {
            lazyImagesPositions.push(img.getBoundingClientRect().top + pageYOffset);
            lazyScrollCheck();
        }
    });
}
window.addEventListener("scroll", lazyScroll)


function lazyScroll() {
    if (document.querySelectorAll('#cap_image').length > 0) {
        lazyScrollCheck();
    }
}


function lazyScrollCheck() {
    let imgIndex = lazyImagesPositions.findIndex(
        item => pageYOffset > item - windowHeight
    );
    if (imgIndex >= 0) {
        if (lazyImages[imgIndex].dataset.src) {
            lazyImages[imgIndex].src = lazyImages[imgIndex].dataset.src;
            lazyImages[imgIndex].removeAttribute('data-src');
        }
        delete lazyImagesPositions[imgIndex];
    }
}