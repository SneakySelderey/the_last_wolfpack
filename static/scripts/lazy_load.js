"use strict"

const images = document.querySelectorAll("img[data-src]");

function LazyFunc(entries, imgObserver) {
    entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
    
        const img = entry.target;
        img.src = img.getAttribute('data-src');
        img.removeAttribute('data-src');
        imgObserver.unobserve(entry.target);
    });
}

const imgObserver = new IntersectionObserver(LazyFunc, {});

function main() {
  images.forEach((img) => {
    imgObserver.observe(img);
  });
  
}

main();