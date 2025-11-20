AOS.init({ once: true, offset: 50, duration: 800 });

window.addEventListener('scroll', () => {
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrollPercent = (scrollTop / docHeight) * 100;
    document.getElementById('scroll-progress').style.width = scrollPercent + '%';

    const nav = document.getElementById('navbar');
    if (scrollTop > 20) {
        nav.classList.add('glass-nav');
        nav.classList.remove('bg-transparent');
    } else {
        nav.classList.remove('glass-nav');
        nav.classList.add('bg-transparent');
    }

    const backToTop = document.getElementById('back-to-top');
    if (scrollTop > 500) {
        backToTop.classList.remove('translate-y-20', 'opacity-0');
    } else {
        backToTop.classList.add('translate-y-20', 'opacity-0');
    }
});

// Mobile Menu
const mobileMenu = document.getElementById('mobile-menu');
function toggleMobile() {
    mobileMenu.classList.toggle('translate-x-full');
    document.body.style.overflow = mobileMenu.classList.contains('translate-x-full') ? 'auto' : 'hidden';
}
document.getElementById('mobile-btn').addEventListener('click', toggleMobile);
document.getElementById('close-mobile').addEventListener('click', toggleMobile);

// Lightbox
const lightbox = document.getElementById('lightbox');
const lightboxImg = document.getElementById('lightbox-img');
function openLightbox(el) {
    lightboxImg.src = el.querySelector('img').src;
    lightbox.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}
function closeLightboxForce() {
    lightbox.classList.add('hidden');
    document.body.style.overflow = 'auto';
}
function closeLightbox(e) {
    if(e.target === lightbox) closeLightboxForce();
}

// Modal
const modal = document.getElementById('modal');
function openModal(role) {
    document.getElementById('modal-role').innerText = role;
    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}
function closeModal() {
    modal.classList.add('hidden');
    document.body.style.overflow = 'auto';
}

// Toast
function showToast(msg) {
    const toast = document.getElementById('toast');
    document.getElementById('toast-msg').innerText = msg;
    toast.classList.remove('translate-y-40');
    setTimeout(() => toast.classList.add('translate-y-40'), 3000);
}
function handleApply(e) {
    e.preventDefault();
    const form = e.target;
    const data = Array.from(new FormData(form)).reduce((obj, [k, v]) => (obj[k || k === '' ? k : k] = v, obj), {});
    // get role from modal
    data.role = document.getElementById('modal-role').innerText;
    fetch('/apply', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    }).then(r => r.json()).then(res => {
        if (res.success) {
            form.reset();
            closeModal();
            showToast(res.message || 'Application submitted!');
        } else {
            showToast(res.message || 'Submission failed');
        }
    }).catch(err => {
        console.error(err);
        showToast('Network error');
    });
}
function handleSubmit(e) {
    e.preventDefault();
    const form = e.target;
    const fd = new FormData(form);
    const data = {};
    fd.forEach((v, k) => data[k] = v);
    fetch('/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    }).then(r => r.json()).then(res => {
        if (res.success) {
            form.reset();
            showToast(res.message || 'Message sent!');
        } else {
            showToast(res.message || 'Send failed');
        }
    }).catch(err => {
        console.error(err);
        showToast('Network error');
    });
}