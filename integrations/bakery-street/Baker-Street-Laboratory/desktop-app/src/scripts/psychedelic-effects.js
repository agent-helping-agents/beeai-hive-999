// Baker Street Laboratory - Psychedelic Effects
// Handles visual effects, animations, and particle systems for the psychedelic detective theme

class PsychedelicEffects {
    constructor() {
        this.canvas = null;
        this.ctx = null;
        this.particles = [];
        this.animationId = null;
        this.theme = 'detective';
        this.intensity = 'medium';
        this.isAnimating = false;
        
        this.init();
    }

    init() {
        this.setupCanvas();
        this.setupParticles();
        this.setupThemeColors();
    }

    setupCanvas() {
        this.canvas = document.getElementById('psychedelic-canvas');
        if (!this.canvas) {
            this.canvas = document.createElement('canvas');
            this.canvas.id = 'psychedelic-canvas';
            this.canvas.className = 'background-canvas';
            document.body.appendChild(this.canvas);
        }

        this.ctx = this.canvas.getContext('2d');
        this.resizeCanvas();

        // Handle window resize
        window.addEventListener('resize', () => {
            this.resizeCanvas();
        });
    }

    resizeCanvas() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    setupThemeColors() {
        this.themes = {
            detective: {
                primary: '#2C1810',
                secondary: '#8B4513',
                accent: '#DAA520',
                particles: ['#DAA520', '#8B4513', '#FF6B35']
            },
            laboratory: {
                primary: '#0F4C75',
                secondary: '#3282B8',
                accent: '#BBE1FA',
                particles: ['#BBE1FA', '#3282B8', '#00CED1']
            },
            psychedelic: {
                primary: '#FF1493',
                secondary: '#8A2BE2',
                accent: '#00CED1',
                particles: ['#FF1493', '#00CED1', '#FFD700', '#32CD32', '#FF4500', '#8A2BE2']
            }
        };
    }

    setupParticles() {
        this.particles = [];
        const particleCount = this.getParticleCount();
        
        for (let i = 0; i < particleCount; i++) {
            this.particles.push(this.createParticle());
        }
    }

    getParticleCount() {
        const counts = {
            none: 0,
            low: 20,
            medium: 50,
            high: 100
        };
        return counts[this.intensity] || counts.medium;
    }

    createParticle() {
        const colors = this.themes[this.theme].particles;
        return {
            x: Math.random() * this.canvas.width,
            y: Math.random() * this.canvas.height,
            vx: (Math.random() - 0.5) * 2,
            vy: (Math.random() - 0.5) * 2,
            radius: Math.random() * 3 + 1,
            color: colors[Math.floor(Math.random() * colors.length)],
            opacity: Math.random() * 0.5 + 0.2,
            life: Math.random() * 100 + 50,
            maxLife: 100,
            pulse: Math.random() * Math.PI * 2
        };
    }

    startParticles() {
        if (this.intensity === 'none') return;
        
        this.isAnimating = true;
        this.animate();
    }

    stopParticles() {
        this.isAnimating = false;
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
            this.animationId = null;
        }
        this.clearCanvas();
    }

    animate() {
        if (!this.isAnimating) return;

        this.clearCanvas();
        this.updateParticles();
        this.drawParticles();
        this.drawConnections();

        this.animationId = requestAnimationFrame(() => this.animate());
    }

    clearCanvas() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    }

    updateParticles() {
        for (let i = this.particles.length - 1; i >= 0; i--) {
            const particle = this.particles[i];
            
            // Update position
            particle.x += particle.vx;
            particle.y += particle.vy;
            
            // Update pulse for breathing effect
            particle.pulse += 0.05;
            
            // Wrap around screen edges
            if (particle.x < 0) particle.x = this.canvas.width;
            if (particle.x > this.canvas.width) particle.x = 0;
            if (particle.y < 0) particle.y = this.canvas.height;
            if (particle.y > this.canvas.height) particle.y = 0;
            
            // Update life
            particle.life--;
            
            // Respawn particle if it dies
            if (particle.life <= 0) {
                this.particles[i] = this.createParticle();
            }
        }
    }

    drawParticles() {
        this.particles.forEach(particle => {
            const pulseRadius = particle.radius + Math.sin(particle.pulse) * 0.5;
            const pulseOpacity = particle.opacity + Math.sin(particle.pulse) * 0.1;
            
            this.ctx.beginPath();
            this.ctx.arc(particle.x, particle.y, pulseRadius, 0, Math.PI * 2);
            this.ctx.fillStyle = this.hexToRgba(particle.color, pulseOpacity);
            this.ctx.fill();
            
            // Add glow effect for psychedelic theme
            if (this.theme === 'psychedelic') {
                this.ctx.shadowBlur = 10;
                this.ctx.shadowColor = particle.color;
                this.ctx.fill();
                this.ctx.shadowBlur = 0;
            }
        });
    }

    drawConnections() {
        if (this.theme !== 'psychedelic') return;
        
        const maxDistance = 100;
        
        for (let i = 0; i < this.particles.length; i++) {
            for (let j = i + 1; j < this.particles.length; j++) {
                const p1 = this.particles[i];
                const p2 = this.particles[j];
                
                const distance = Math.sqrt(
                    Math.pow(p1.x - p2.x, 2) + Math.pow(p1.y - p2.y, 2)
                );
                
                if (distance < maxDistance) {
                    const opacity = (1 - distance / maxDistance) * 0.2;
                    
                    this.ctx.beginPath();
                    this.ctx.moveTo(p1.x, p1.y);
                    this.ctx.lineTo(p2.x, p2.y);
                    this.ctx.strokeStyle = this.hexToRgba('#FFFFFF', opacity);
                    this.ctx.lineWidth = 1;
                    this.ctx.stroke();
                }
            }
        }
    }

    startBackgroundAnimation() {
        if (this.theme === 'psychedelic') {
            this.animateBackground();
        }
    }

    stopBackgroundAnimation() {
        // Stop any background animations
        document.body.style.animation = '';
    }

    animateBackground() {
        const keyframes = `
            @keyframes psychedelicBackground {
                0% { filter: hue-rotate(0deg) brightness(1); }
                25% { filter: hue-rotate(90deg) brightness(1.1); }
                50% { filter: hue-rotate(180deg) brightness(0.9); }
                75% { filter: hue-rotate(270deg) brightness(1.1); }
                100% { filter: hue-rotate(360deg) brightness(1); }
            }
        `;
        
        // Add keyframes to document
        const style = document.createElement('style');
        style.textContent = keyframes;
        document.head.appendChild(style);
        
        // Apply animation to background elements
        const backgroundElements = document.querySelectorAll('.background-canvas, .particles-container');
        backgroundElements.forEach(el => {
            el.style.animation = 'psychedelicBackground 10s ease-in-out infinite';
        });
    }

    setTheme(themeName) {
        this.theme = themeName;
        this.setupParticles();
        
        if (this.isAnimating) {
            this.stopParticles();
            this.startParticles();
        }
        
        this.updateThemeEffects();
    }

    updateThemeEffects() {
        const body = document.body;
        
        // Remove existing theme classes
        body.classList.remove('detective-theme', 'laboratory-theme', 'psychedelic-theme');
        
        // Add new theme class
        body.classList.add(`${this.theme}-theme`);
        
        // Apply theme-specific effects
        switch (this.theme) {
            case 'detective':
                this.applyDetectiveEffects();
                break;
            case 'laboratory':
                this.applyLaboratoryEffects();
                break;
            case 'psychedelic':
                this.applyPsychedelicEffects();
                break;
        }
    }

    applyDetectiveEffects() {
        // Subtle vintage paper texture effect
        document.documentElement.style.setProperty('--theme-filter', 'sepia(0.1) contrast(1.1)');
    }

    applyLaboratoryEffects() {
        // Clean, clinical look
        document.documentElement.style.setProperty('--theme-filter', 'brightness(1.05) contrast(1.05)');
    }

    applyPsychedelicEffects() {
        // Vibrant, colorful effects
        document.documentElement.style.setProperty('--theme-filter', 'saturate(1.2) brightness(1.1)');
        this.startBackgroundAnimation();
    }

    setParticleIntensity(intensity) {
        this.intensity = intensity;
        this.setupParticles();
        
        if (intensity === 'none') {
            this.stopParticles();
        } else if (!this.isAnimating) {
            this.startParticles();
        }
    }

    setArtwork(imagePath) {
        // Set custom background artwork
        const canvas = this.canvas;
        const img = new Image();
        
        img.onload = () => {
            // Draw the artwork as background
            this.ctx.globalAlpha = 0.3;
            this.ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
            this.ctx.globalAlpha = 1.0;
        };
        
        img.src = imagePath;
    }

    createKaleidoscopeEffect(element) {
        if (typeof element === 'string') {
            element = document.getElementById(element);
        }
        
        if (element) {
            element.style.background = `
                conic-gradient(from 0deg, 
                    #FF1493, #00CED1, #FFD700, #32CD32, 
                    #FF4500, #8A2BE2, #FF1493)
            `;
            element.style.animation = 'spin 20s linear infinite';
        }
    }

    addGlowEffect(element, color = '#DAA520') {
        if (typeof element === 'string') {
            element = document.getElementById(element);
        }
        
        if (element) {
            element.style.boxShadow = `0 0 20px ${color}`;
            element.style.transition = 'box-shadow 0.3s ease';
        }
    }

    removeGlowEffect(element) {
        if (typeof element === 'string') {
            element = document.getElementById(element);
        }
        
        if (element) {
            element.style.boxShadow = '';
        }
    }

    hexToRgba(hex, alpha = 1) {
        const r = parseInt(hex.slice(1, 3), 16);
        const g = parseInt(hex.slice(3, 5), 16);
        const b = parseInt(hex.slice(5, 7), 16);
        return `rgba(${r}, ${g}, ${b}, ${alpha})`;
    }

    // Initialize particles.js if available
    initParticlesJS() {
        if (typeof particlesJS !== 'undefined') {
            const particlesConfig = this.getParticlesConfig();
            particlesJS('particles-js', particlesConfig);
        }
    }

    getParticlesConfig() {
        const colors = this.themes[this.theme].particles;
        
        return {
            particles: {
                number: {
                    value: this.getParticleCount(),
                    density: {
                        enable: true,
                        value_area: 800
                    }
                },
                color: {
                    value: colors
                },
                shape: {
                    type: "circle"
                },
                opacity: {
                    value: 0.5,
                    random: true,
                    anim: {
                        enable: true,
                        speed: 1,
                        opacity_min: 0.1
                    }
                },
                size: {
                    value: 3,
                    random: true,
                    anim: {
                        enable: true,
                        speed: 2,
                        size_min: 0.1
                    }
                },
                line_linked: {
                    enable: this.theme === 'psychedelic',
                    distance: 150,
                    color: "#ffffff",
                    opacity: 0.2,
                    width: 1
                },
                move: {
                    enable: true,
                    speed: 2,
                    direction: "none",
                    random: true,
                    straight: false,
                    out_mode: "out",
                    bounce: false
                }
            },
            interactivity: {
                detect_on: "canvas",
                events: {
                    onhover: {
                        enable: true,
                        mode: "repulse"
                    },
                    onclick: {
                        enable: true,
                        mode: "push"
                    }
                }
            },
            retina_detect: true
        };
    }
}
