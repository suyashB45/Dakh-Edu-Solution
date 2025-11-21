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

// Reveal-on-scroll using IntersectionObserver (works alongside AOS)
function initRevealOnScroll() {
    const opts = { root: null, rootMargin: '0px', threshold: 0.12 };
    const io = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('in-view');
                // If you want non-repeating reveals, unobserve after intersecting
                io.unobserve(entry.target);
            }
        });
    }, opts);

    document.querySelectorAll('.reveal').forEach(el => io.observe(el));
}

// Simple parallax for elements with .parallax-bg
function initParallax() {
    const el = document.querySelector('.parallax-bg');
    if (!el) return;
    window.addEventListener('scroll', () => {
        const sc = window.scrollY;
        // move slower than scroll for parallax effect
        const y = sc * 0.2;
        el.style.transform = `translate3d(0, ${y}px, 0)`;
    }, { passive: true });
}

document.addEventListener('DOMContentLoaded', () => {
    initRevealOnScroll();
    initParallax();
});

// Scroll-spy: highlight nav links when sections are in view
function initScrollSpy() {
    const links = Array.from(document.querySelectorAll('.nav-link'));
    const sections = links.map(l => document.querySelector(l.getAttribute('href'))).filter(Boolean);
    if (sections.length === 0) return;
    const opts = { root: null, rootMargin: '-40% 0px -40% 0px', threshold: 0 };
    const io = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (!entry.target.id) return;
            const id = '#' + entry.target.id;
            const link = document.querySelector(`.nav-link[href="${id}"]`);
            if (entry.isIntersecting) {
                links.forEach(l => l.classList.remove('active'));
                if (link) link.classList.add('active');
            }
        });
    }, opts);
    sections.forEach(s => io.observe(s));
}

document.addEventListener('DOMContentLoaded', () => {
    // run scroll spy after DOM ready
    initScrollSpy();
});

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
    const data = Array.from(new FormData(form)).reduce((obj, [k, v]) => (obj[k] = v, obj), {});
    // get role from modal
    data.role = document.getElementById('modal-role').innerText;
    const submitBtn = document.getElementById('apply-submit');
    const orig = submitBtn ? submitBtn.innerHTML : null;
    if (submitBtn) { submitBtn.disabled = true; submitBtn.innerHTML = 'Sending...'; }
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
    }).finally(() => { if (submitBtn) { submitBtn.disabled = false; submitBtn.innerHTML = orig; } });
}
function handleSubmit(e) {
    e.preventDefault();
    const form = e.target;
    const fd = new FormData(form);
    const data = {};
    fd.forEach((v, k) => data[k] = v);
    const submitBtn = document.getElementById('contact-submit');
    const orig = submitBtn ? submitBtn.innerHTML : null;
    if (submitBtn) { submitBtn.disabled = true; submitBtn.innerHTML = 'Sending...'; }
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
    }).finally(() => { if (submitBtn) { submitBtn.disabled = false; submitBtn.innerHTML = orig; } });
}