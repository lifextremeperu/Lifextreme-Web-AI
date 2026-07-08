/**
 * LIFEXTREME GAMIFICATION ENGINE (TEMU-STYLE)
 * Handles Lifecoins, Streaks, and User Engagement Loops
 */

const Lifecoins = {
    balance: 0,
    usdRate: 0.01, // 100 coins = $1 USD

    init() {
        // Load balance from local storage or default to 800
        const stored = localStorage.getItem('lifecoins_balance');
        this.balance = stored ? parseInt(stored) : 800;
        this.updateUI();

        // Check Daily Streak
        this.checkDailyIn();
    },

    updateUI() {
        // Update Balance Displays
        document.querySelectorAll('[id^="nav-coin-balance"]').forEach(el => el.innerText = this.balance);
        const heroBalance = document.getElementById('hero-balance');
        if (heroBalance) heroBalance.innerText = this.balance;

        // Update USD Value
        const usdEl = document.getElementById('usd-value');
        if (usdEl) usdEl.innerText = `$${(this.balance * this.usdRate).toFixed(2)} USD`;

        // Animate Progress Bar (XP to Level 2)
        const progressEl = document.getElementById('xp-progress');
        if (progressEl) {
            // Level 2 requires 1600 total. Current base 800.
            // Progress % = (Balance - 800) / 800 * 100? No, let's just do simple:
            // % = (Balance % 1000) / 10
            const percent = Math.min((this.balance / 1600) * 100, 100);
            progressEl.style.width = `${percent}%`;
        }

        // Save
        localStorage.setItem('lifecoins_balance', this.balance);
    },

    earn(action) {
        let amount = 0;
        let title = "¡Monedas Ganadas!";
        let msg = "";

        switch (action) {
            case 'daily_checkin':
                if (this.hasDoneActionToday('daily_checkin')) {
                    this.showToast('Vuelve Mañana', 'Ya reclamaste tu recompensa diaria.', 'info');
                    return;
                }
                amount = 20;
                title = "¡Racha Diario +1!";
                msg = "Has ganado 20 LC. ¡Vuelve mañana por más!";
                this.markActionDone('daily_checkin');

                // Trigger confetti or visual effect here
                break;

            case 'spin_wheel':
                if (this.hasDoneActionToday('spin_wheel')) {
                    this.showToast('Sin Giros', 'Ya giraste la ruleta hoy.', 'info');
                    return;
                }
                // Simulate spin delay
                const spinBtn = event.currentTarget;
                spinBtn.innerText = "Girando...";
                setTimeout(() => {
                    const prize = [50, 100, 10, 500, 0][Math.floor(Math.random() * 5)];
                    this.addCoins(prize);
                    this.showToast('¡Ruleta Mágica!', `La suerte te ha dado ${prize} LC.`, 'success');
                    this.markActionDone('spin_wheel');
                    spinBtn.innerText = "Girar Gratis";
                    spinBtn.disabled = true;
                    spinBtn.classList.add('opacity-50', 'cursor-not-allowed');
                }, 1500);
                return; // Async handle

            case 'watch_video':
                // Simulate watching
                const vidBtn = event.currentTarget;
                const originalText = vidBtn.innerText;
                vidBtn.innerText = "Viendo anuncio (3s)...";
                vidBtn.disabled = true;

                setTimeout(() => {
                    this.addCoins(50);
                    this.showToast('¡Video Completado!', 'Has aprendido sobre Huacachina +50 LC.', 'success');
                    vidBtn.innerText = "Ver Otro";
                    vidBtn.disabled = false;
                }, 3000);
                return;

            case 'share_whatsapp':
                amount = 50;
                title = "Misión Cumplida";
                msg = "Compartido en WhatsApp.";
                window.open('https://wa.me/?text=¡Chequea%20Lifextreme!%20Tienen%20tours%20increíbles%20en%20Perú.%20https://lifextreme.store', '_blank');
                break;

            case 'refer_friend':
                // Use Clipboard API
                navigator.clipboard.writeText('https://lifextreme.store?ref=user123');
                this.showToast('Link Copiado', 'Compártelo con tus amigos para ganar 200 LC por registro.', 'success');
                return; // No immediate coins

            case 'complete_profile':
                this.showToast('Redirigiendo...', 'Vamos a completar tu perfil.', 'info');
                // Simulate redirect
                setTimeout(() => window.location.href = 'index.html#socio', 1000);
                return;

            default:
                break;
        }

        if (amount > 0) {
            this.addCoins(amount);
            this.showToast(title, msg, 'success');
        }
    },

    addCoins(amount) {
        this.balance += amount;
        this.updateUI();

        // Visual Feedback on Hero Balance
        const hero = document.getElementById('hero-balance');
        if (hero) {
            hero.classList.add('scale-125', 'text-yellow-400');
            setTimeout(() => hero.classList.remove('scale-125', 'text-yellow-400'), 200);
        }
    },

    redeem(itemId, cost) {
        if (this.balance >= cost) {
            this.balance -= cost;
            this.updateUI();
            this.showToast('¡Canje Exitoso!', 'Revisa tu correo con el cupón.', 'success');
        } else {
            this.showToast('Saldo Insuficiente', `Necesitas ${cost - this.balance} LC más.`, 'error');
        }
    },

    // --- UTILS ---
    showToast(title, msg, type = 'success') {
        const toast = document.getElementById('toast');
        const tTitle = document.getElementById('toast-title');
        const tMsg = document.getElementById('toast-msg');

        tTitle.innerText = title;
        tMsg.innerText = msg;

        toast.style.transform = 'translate(-50%, 0)';
        toast.style.opacity = '1';

        // Hide after 3s
        setTimeout(() => {
            toast.style.transform = 'translate(-50%, 100px)';
            toast.style.opacity = '0';
        }, 3000);
    },

    hasDoneActionToday(actionKey) {
        const last = localStorage.getItem(`last_${actionKey}`);
        if (!last) return false;

        const today = new Date().toDateString(); // "Wed Jan 08 2026"
        return last === today;
    },

    markActionDone(actionKey) {
        localStorage.setItem(`last_${actionKey}`, new Date().toDateString());
    },

    checkDailyIn() {
        // Logic to check streaks could go here
        console.log("Welcome back to Lifextreme Rewards");
    }
};

// Auto Init
window.addEventListener('DOMContentLoaded', () => {
    Lifecoins.init();
});
