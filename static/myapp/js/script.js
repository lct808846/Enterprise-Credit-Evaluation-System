const canvas = document.getElementById('backgroundCanvas');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

class Particle {
    constructor(x, y, radius, color) {
        this.x = x;
        this.y = y;
        this.radius = radius;
        this.color = color;
        this.velocity = {
            x: (Math.random() - 0.5) * 2,
            y: (Math.random() - 0.5) * 2
        };
    }
    draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2, false);
        ctx.fillStyle = this.color;
        ctx.fill();
        ctx.closePath();
    }
    update() {
        this.x += this.velocity.x;
        this.y += this.velocity.y;
        if (this.x - this.radius < 0 || this.x + this.radius > canvas.width) {
            this.velocity.x = -this.velocity.x;
        }
        if (this.y - this.radius < 0 || this.y + this.radius > canvas.height) {
            this.velocity.y = -this.velocity.y;
        }
        this.draw();
    }
}

const particles = [];
for (let i = 0; i < 100; i++) {
    const radius = 3; // Slightly smaller particles for a more delicate effect.
    const x = Math.random() * (canvas.width - 2 * radius) + radius;
    const y = Math.random() * (canvas.height - 2 * radius) + radius;
    const color = `rgba(${Math.floor(Math.random() * 50 + 200)}, ${Math.floor(Math.random() * 50 + 200)}, 255, 0.5)`; // Light blue and white shades.
    particles.push(new Particle(x, y, radius, color));
}

function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    particles.forEach(particle => particle.update());
    requestAnimationFrame(animate);
}

animate();

// Ensure canvas resizes with the window.
window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
});