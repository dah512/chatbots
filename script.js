// Particles Animation
function createParticles() {
    const particlesContainer = document.getElementById('particles');
    const particleCount = 50;
    
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        
        // Random starting position
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        
        // Random animation duration
        const duration = 10 + Math.random() * 20;
        particle.style.animationDuration = duration + 's';
        
        // Random delay
        particle.style.animationDelay = Math.random() * 5 + 's';
        
        // Random size
        const size = 2 + Math.random() * 3;
        particle.style.width = size + 'px';
        particle.style.height = size + 'px';
        
        particlesContainer.appendChild(particle);
    }
}

// Intersection Observer for scroll animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('aos-animate');
        }
    });
}, observerOptions);

// Observe all elements with data-aos attribute
function initScrollAnimations() {
    const animatedElements = document.querySelectorAll('[data-aos]');
    animatedElements.forEach(el => observer.observe(el));
}

// Smooth scroll for navigation links
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Add parallax effect to hero section
function initParallax() {
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const hero = document.querySelector('.hero');
        if (hero) {
            hero.style.transform = `translateY(${scrolled * 0.5}px)`;
            hero.style.opacity = 1 - (scrolled / 700);
        }
    });
}

// Card hover effect with mouse tracking
function initCardEffects() {
    const cards = document.querySelectorAll('.app-card');
    
    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = (y - centerY) / 20;
            const rotateY = (centerX - x) / 20;
            
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-10px)`;
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateY(0)';
        });
    });
}

// Animate stats on scroll
function animateStats() {
    const stats = document.querySelectorAll('.stat-value');
    
    stats.forEach(stat => {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const text = stat.textContent;
                    if (!isNaN(text)) {
                        animateNumber(stat, 0, parseInt(text), 1500);
                    }
                    observer.unobserve(stat);
                }
            });
        });
        
        observer.observe(stat);
    });
}

// Animate number counting
function animateNumber(element, start, end, duration) {
    const range = end - start;
    const increment = range / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= end) {
            element.textContent = end;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current);
        }
    }, 16);
}

// Add glow effect on hover for icons
function initIconGlow() {
    const iconContainers = document.querySelectorAll('.app-icon-container');
    
    iconContainers.forEach(container => {
        container.addEventListener('mouseenter', () => {
            const glow = container.querySelector('.icon-glow');
            if (glow) {
                glow.style.transform = 'translate(-50%, -50%) scale(1.5)';
                glow.style.opacity = '1';
            }
        });
        
        container.addEventListener('mouseleave', () => {
            const glow = container.querySelector('.icon-glow');
            if (glow) {
                glow.style.transform = 'translate(-50%, -50%) scale(1)';
                glow.style.opacity = '0.6';
            }
        });
    });
}

// Add typing effect to hero title
function initTypingEffect() {
    const titleLines = document.querySelectorAll('.hero-title-line');
    
    titleLines.forEach((line, index) => {
        const text = line.textContent;
        line.textContent = '';
        line.style.opacity = '1';
        
        let i = 0;
        const typeInterval = setInterval(() => {
            if (i < text.length) {
                line.textContent += text.charAt(i);
                i++;
            } else {
                clearInterval(typeInterval);
            }
        }, 50 + (index * 20));
    });
}

// Add loading screen
function initLoadingScreen() {
    window.addEventListener('load', () => {
        document.body.style.opacity = '0';
        setTimeout(() => {
            document.body.style.transition = 'opacity 0.5s ease';
            document.body.style.opacity = '1';
        }, 100);
    });
}

// Header scroll effect
function initHeaderScroll() {
    const header = document.querySelector('.header');
    let lastScroll = 0;
    
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll > 100) {
            header.style.background = 'rgba(10, 14, 39, 0.95)';
            header.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.3)';
        } else {
            header.style.background = 'rgba(10, 14, 39, 0.8)';
            header.style.boxShadow = 'none';
        }
        
        lastScroll = currentScroll;
    });
}

// Feature tags animation
function initFeatureTags() {
    const tags = document.querySelectorAll('.feature-tag');
    
    tags.forEach((tag, index) => {
        tag.style.opacity = '0';
        tag.style.transform = 'scale(0.8)';
        
        setTimeout(() => {
            tag.style.transition = 'all 0.3s ease';
            tag.style.opacity = '1';
            tag.style.transform = 'scale(1)';
        }, 100 * index);
    });
}

// Initialize all animations and effects
function init() {
    createParticles();
    initScrollAnimations();
    initSmoothScroll();
    initParallax();
    initCardEffects();
    animateStats();
    initIconGlow();
    initLoadingScreen();
    initHeaderScroll();
    
    // Trigger feature tags animation when cards are in view
    const cards = document.querySelectorAll('.app-card');
    cards.forEach(card => {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const tags = entry.target.querySelectorAll('.feature-tag');
                    tags.forEach((tag, index) => {
                        setTimeout(() => {
                            tag.style.transition = 'all 0.3s ease';
                            tag.style.opacity = '1';
                            tag.style.transform = 'scale(1)';
                        }, 100 * index);
                    });
                    observer.unobserve(entry.target);
                }
            });
        });
        observer.observe(card);
    });
}

// Run initialization when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

// Add Easter egg - Konami code
let konamiCode = [];
const konamiSequence = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a'];

document.addEventListener('keydown', (e) => {
    konamiCode.push(e.key);
    konamiCode = konamiCode.slice(-10);
    
    if (konamiCode.join(',') === konamiSequence.join(',')) {
        document.body.style.animation = 'rainbow 2s linear infinite';
        setTimeout(() => {
            document.body.style.animation = '';
        }, 5000);
    }
});

// Rainbow animation for Easter egg
const style = document.createElement('style');
style.textContent = `
    @keyframes rainbow {
        0% { filter: hue-rotate(0deg); }
        100% { filter: hue-rotate(360deg); }
    }
`;
document.head.appendChild(style);
