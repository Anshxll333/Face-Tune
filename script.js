document.addEventListener('DOMContentLoaded', () => {
    const items = document.querySelectorAll('.carousel .list .item');
    const thumbnails = document.querySelectorAll('.thumbnail .item');
    const prevButton = document.getElementById('prev');
    const nextButton = document.getElementById('next');
    
    let currentIndex = 0;
    let autoSlideInterval;

    function showItem(index) {
        items.forEach(item => item.classList.remove('active'));
        thumbnails.forEach(thumb => thumb.classList.remove('active'));
        
        items[index].classList.add('active');
        thumbnails[index].classList.add('active');
    }

    function nextSlide() {
        currentIndex = (currentIndex + 1) % items.length;
        showItem(currentIndex);
    }

    function prevSlide() {
        currentIndex = (currentIndex - 1 + items.length) % items.length;
        showItem(currentIndex);
    }

    function startAutoSlide() {
        autoSlideInterval = setInterval(nextSlide, 5000);
    }

    nextButton.addEventListener('click', nextSlide);
    prevButton.addEventListener('click', prevSlide);
    
    thumbnails.forEach((thumb, index) => {
        thumb.addEventListener('click', () => {
            currentIndex = index;
            showItem(currentIndex);
        });
    });

    showItem(0);
    startAutoSlide();

    document.querySelector('.carousel').addEventListener('mouseenter', () => {
        clearInterval(autoSlideInterval);
    });
    
    document.querySelector('.carousel').addEventListener('mouseleave', startAutoSlide);
});
