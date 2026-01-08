/**
 * LIFECOINS GAMIFICATION ENGINE
 * Handles currency, XP, levels, and rewards persistence.
 */

const Lifecoins = {
    state: {
        balance: 0,
        xp: 0,
        level: 1,
        history: [] // { date, action, amount }
    },

    levels: [
        { level: 1, name: "Mochilero", minXP: 0 },
        { level: 2, name: "Explorador", minXP: 1000 },
        { level: 3, name: "Sherpa", minXP: 5000 },
        { level: 4, name: "Leyenda", minXP: 10000 }
    ],

    init() {
        // Load from LocalStorage
        const saved = localStorage.getItem('lifecoins_state');
        if (saved) {
            this.state = JSON.parse(saved);
        } else {
            // New User Bonus
            this.earn('signup_bonus', 500); // Silent init earn
        }
        this.updateUI();
    },

    save() {
        localStorage.setItem('lifecoins_state', JSON.stringify(this.state));
        this.updateUI();
    },

    earn(actionType, amountOverride = 0) {
        let amount = amountOverride;
        let xpGain = amountOverride; // 1 Coin = 1 XP usually
        let label = "Bono";

        // Define Actions
        switch (actionType) {
            case 'share_whatsapp':
                amount = 50;
                xpGain = 100;
                label = "Compartir en WhatsApp";
                break;
            case 'refer_friend':
                // Check if already clicked recently to prevent spam (simple check)
                amount = 0; // Just showing the link doesn't earn immediately in real app, but for demo:
                this.showToast('Enlace Copiado', '¡Comparte este link! Ganarás 200 LC cuando se registren.');
                navigator.clipboard.writeText('https://lifextreme.com?ref=USER123');
                return;
            case 'review_google':
                amount = 100;
                xpGain = 200;
                label = "Reseña Google Maps";
                window.open('https://maps.google.com/?q=Lifextreme+Cusco', '_blank');
                break;
            case 'signup_bonus':
                amount = 500;
                xpGain = 500;
                label = "Bono de Bienvenida";
                break;
        }

        if (amount > 0) {
            this.state.balance += amount;
            this.state.xp += xpGain;
            this.state.history.push({
                date: new Date().toISOString(),
                action: label,
                amount: amount
            });

            this.checkLevelUp();
            this.save();
            this.showToast('¡+' + amount + ' Lifecoins!', 'Acción: ' + label);
        }
    },

    redeem(rewardId, cost) {
        if (this.state.balance >= cost) {
            if (confirm('¿Confirmar canje por ' + cost + ' Lifecoins?')) {
                this.state.balance -= cost;
                this.state.history.push({
                    date: new Date().toISOString(),
                    action: "Canje Recompensa: " + rewardId,
                    amount: -cost
                });
                this.save();

                // Demo Redemption UI
                alert('¡CANJE EXITOSO! \n\nTu código de cupón es: LIFE-2026-X892\n\nÚsalo en el checkout para aplicar tu descuento.');
            }
        } else {
            alert('Saldo insuficiente. Necesitas ' + (cost - this.state.balance) + ' Lifecoins más.');
        }
    },

    checkLevelUp() {
        const currentLevel = this.levels.find(l => l.level === this.state.level);
        const nextLevel = this.levels.find(l => l.level === this.state.level + 1);

        if (nextLevel && this.state.xp >= nextLevel.minXP) {
            this.state.level = nextLevel.level;
            this.showToast('¡NIVEL DESBLOQUEADO!', 'Ahora eres ' + nextLevel.name);
            // Confetti effect could go here
        }
    },

    updateUI() {
        // Update Balance Texts
        const balanceEls = document.querySelectorAll('#hero-balance, #nav-coin-balance');
        balanceEls.forEach(el => el.innerText = this.state.balance);

        // Update USD Value
        const usdEl = document.getElementById('usd-value');
        if (usdEl) usdEl.innerText = '$' + (this.state.balance / 100).toFixed(2) + ' USD';

        // Update Level
        const levelConfig = this.levels.find(l => l.level === this.state.level);
        const levelBadge = document.getElementById('user-level');
        if (levelBadge) levelBadge.innerText = `Nivel ${this.state.level}: ${levelConfig.name}`;

        // Update Progress Bar
        const nextLevel = this.levels.find(l => l.level === this.state.level + 1);
        const progressBar = document.getElementById('xp-progress');

        if (progressBar && nextLevel) {
            const currentLevelMin = this.levels.find(l => l.level === this.state.level).minXP;
            const range = nextLevel.minXP - currentLevelMin;
            const progress = this.state.xp - currentLevelMin;
            const percentage = Math.min(100, Math.max(0, (progress / range) * 100));

            progressBar.style.width = percentage + '%';
        }
    },

    showToast(title, msg) {
        const toast = document.getElementById('toast');
        if (!toast) return;

        document.getElementById('toast-title').innerText = title;
        document.getElementById('toast-msg').innerText = msg;

        toast.classList.remove('translate-y-24', 'opacity-0');

        setTimeout(() => {
            toast.classList.add('translate-y-24', 'opacity-0');
        }, 4000);
    }
};

// Auto-Init
document.addEventListener('DOMContentLoaded', () => {
    Lifecoins.init();
});
