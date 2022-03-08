"use strict"

// const lazyImages = document.querySelectorAll('#cap_image');
// const windowHeight = document.documentElement.clientHeight;

// let lazyImagesPositions = [];
// if (lazyImages.length > 0) {
//     lazyImages.forEach(img => {
//         if (img.dataset.src) {
//             lazyImagesPositions.push(img.getBoundingClientRect().top + scrollY);
//             lazyScrollCheck();
//         }
//     });
// }
// window.addEventListener("scroll", lazyScroll);
// setInterval(lazyScroll, 100);


// function lazyScroll() {
//     if (document.querySelectorAll('#cap_image').length > 0) {
//         lazyScrollCheck();
//     }
// }


// function lazyScrollCheck() {
//     let imgIndex = lazyImagesPositions.findIndex(
//         item => scrollY > item - windowHeight
//     );
//     if (imgIndex >= 0) {
//         if (lazyImages[imgIndex].dataset.src) {
//             lazyImages[imgIndex].src = lazyImages[imgIndex].dataset.src;
//             lazyImages[imgIndex].removeAttribute('data-src');
//         }
//         delete lazyImagesPositions[imgIndex];
//     }
// }

const images = document.querySelectorAll("img[data-src]");

const imgOptions = {};
const imgObserver = new IntersectionObserver((entries, imgObserver) => {
  entries.forEach((entry) => {
    if (!entry.isIntersecting) return;

    const img = entry.target;
    img.src = img.getAttribute('data-src');
    img.removeAttribute('data-src');
    imgObserver.unobserve(entry.target);
  });
}, imgOptions);

images.forEach((img) => {
  imgObserver.observe(img);
});