// Mono-alphabetic Cipher Implementation
class MonoAlphabeticCipher {
    constructor() {
        this.alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
        this.substitutionKey = {};
        this.generateNewKey();
    }

    generateNewKey() {
        const shuffled = [...this.alphabet].sort(() => Math.random() - 0.5);
        this.substitutionKey = {};
        this.alphabet.forEach((letter, index) => {
            this.substitutionKey[letter] = shuffled[index];
        });
    }

    encrypt(text) {
        return text.toUpperCase().split('').map(char => {
            return this.alphabet.includes(char) ? this.substitutionKey[char] : char;
        }).join('');
    }

    decrypt(text) {
        const reverseKey = Object.fromEntries(
            Object.entries(this.substitutionKey).map(([k, v]) => [v, k])
        );
        return text.toUpperCase().split('').map(char => {
            return this.alphabet.includes(char) ? reverseKey[char] : char;
        }).join('');
    }

    getFrequencyAnalysis(text) {
        const freq = {};
        this.alphabet.forEach(letter => freq[letter] = 0);
        let total = 0;

        text.toUpperCase().split('').forEach(char => {
            if (this.alphabet.includes(char)) {
                freq[char]++;
                total++;
            }
        });

        return Object.fromEntries(
            Object.entries(freq).map(([letter, count]) => [
                letter,
                total > 0 ? (count / total) * 100 : 0
            ])
        );
    }
}

// UI Controller
class CipherUI {
    constructor() {
        this.cipher = new MonoAlphabeticCipher();
        this.animationSpeed = 500;
        this.setupEventListeners();
        this.initializeUI();
    }

    setupEventListeners() {
        // Buttons
        document.getElementById('new-key-btn')?.addEventListener('click', () => this.generateNewKey());
        document.getElementById('encrypt-btn')?.addEventListener('click', () => this.startEncryption());
        document.getElementById('decrypt-btn')?.addEventListener('click', () => this.startDecryption());

        // Inputs
        document.getElementById('plaintext')?.addEventListener('input', (e) => this.handlePlaintextInput(e));
        document.getElementById('ciphertext')?.addEventListener('input', (e) => this.handleCiphertextInput(e));
        document.getElementById('animation-speed')?.addEventListener('input', (e) => {
            this.animationSpeed = 1000 - parseInt(e.target.value);
        });
    }

    initializeUI() {
        this.displaySubstitutionKey();
        this.setupFrequencyChart();
        this.setupLetterMappings();
    }

    displaySubstitutionKey() {
        const originalAlphabet = document.getElementById('original-alphabet');
        const substitutionAlphabet = document.getElementById('substitution-alphabet');

        if (!originalAlphabet || !substitutionAlphabet) return;

        originalAlphabet.innerHTML = '';
        substitutionAlphabet.innerHTML = '';

        this.cipher.alphabet.forEach(letter => {
            // Original letter
            const origBox = document.createElement('div');
            origBox.className = 'w-8 h-8 border rounded flex items-center justify-center font-mono bg-white';
            origBox.textContent = letter;
            originalAlphabet.appendChild(origBox);

            // Substitution letter
            const subBox = document.createElement('div');
            subBox.className = 'w-8 h-8 border rounded flex items-center justify-center font-mono bg-white';
            subBox.textContent = this.cipher.substitutionKey[letter];
            substitutionAlphabet.appendChild(subBox);
        });
    }

    async animateEncryption(text) {
        const animation = document.getElementById('encryption-animation');
        if (!animation) return;

        animation.innerHTML = '';
        const result = [];

        for (const char of text.toUpperCase()) {
            const step = document.createElement('div');
            step.className = 'flex items-center space-x-4 font-mono';

            if (this.cipher.alphabet.includes(char)) {
                step.innerHTML = `
                    <span class="w-8 h-8 border rounded flex items-center justify-center bg-blue-100">${char}</span>
                    <span class="text-gray-500">→</span>
                    <span class="w-8 h-8 border rounded flex items-center justify-center bg-green-100">${this.cipher.substitutionKey[char]}</span>
                `;
                result.push(this.cipher.substitutionKey[char]);
            } else {
                step.innerHTML = `
                    <span class="w-8 h-8 border rounded flex items-center justify-center">${char}</span>
                `;
                result.push(char);
            }

            animation.innerHTML = '';
            animation.appendChild(step);
            await new Promise(resolve => setTimeout(resolve, this.animationSpeed));
        }

        return result.join('');
    }

    async animateDecryption(text) {
        const animation = document.getElementById('decryption-animation');
        if (!animation) return;

        animation.innerHTML = '';
        const reverseKey = Object.fromEntries(
            Object.entries(this.cipher.substitutionKey).map(([k, v]) => [v, k])
        );
        const result = [];

        for (const char of text.toUpperCase()) {
            const step = document.createElement('div');
            step.className = 'flex items-center space-x-4 font-mono';

            if (this.cipher.alphabet.includes(char)) {
                step.innerHTML = `
                    <span class="w-8 h-8 border rounded flex items-center justify-center bg-blue-100">${char}</span>
                    <span class="text-gray-500">→</span>
                    <span class="w-8 h-8 border rounded flex items-center justify-center bg-green-100">${reverseKey[char]}</span>
                `;
                result.push(reverseKey[char]);
            } else {
                step.innerHTML = `
                    <span class="w-8 h-8 border rounded flex items-center justify-center">${char}</span>
                `;
                result.push(char);
            }

            animation.innerHTML = '';
            animation.appendChild(step);
            await new Promise(resolve => setTimeout(resolve, this.animationSpeed));
        }

        return result.join('');
    }

    setupFrequencyChart() {
        const ctx = document.getElementById('frequency-chart');
        if (!ctx) return;

        this.frequencyChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: this.cipher.alphabet,
                datasets: [{
                    label: 'Letter Frequency (%)',
                    data: new Array(26).fill(0),
                    backgroundColor: 'rgba(59, 130, 246, 0.5)',
                    borderColor: 'rgba(59, 130, 246, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Frequency (%)'
                        }
                    }
                }
            }
        });
    }

    updateFrequencyChart(text) {
        if (!this.frequencyChart) return;
        
        const frequencies = this.cipher.getFrequencyAnalysis(text);
        this.frequencyChart.data.datasets[0].data = this.cipher.alphabet.map(letter => frequencies[letter]);
        this.frequencyChart.update();
    }

    setupLetterMappings() {
        const cipherLetters = document.getElementById('cipher-letters');
        const plainLetters = document.getElementById('plain-letters');

        if (!cipherLetters || !plainLetters) return;

        cipherLetters.innerHTML = '';
        plainLetters.innerHTML = '';

        this.cipher.alphabet.forEach(letter => {
            const cipherBox = document.createElement('div');
            cipherBox.className = 'w-8 h-8 border rounded flex items-center justify-center font-mono bg-white cursor-pointer hover:bg-blue-50';
            cipherBox.textContent = this.cipher.substitutionKey[letter];
            cipherLetters.appendChild(cipherBox);

            const plainBox = document.createElement('div');
            plainBox.className = 'w-8 h-8 border rounded flex items-center justify-center font-mono bg-white cursor-pointer hover:bg-green-50';
            plainBox.textContent = '_';
            plainBox.dataset.original = letter;
            plainLetters.appendChild(plainBox);
        });
    }

    async startEncryption() {
        const input = document.getElementById('plaintext')?.value || '';
        if (!input) return;

        const ciphertext = await this.animateEncryption(input);
        document.getElementById('ciphertext-result').textContent = ciphertext;
    }

    async startDecryption() {
        const input = document.getElementById('ciphertext')?.value || '';
        if (!input) return;

        const plaintext = await this.animateDecryption(input);
        document.getElementById('plaintext-result').textContent = plaintext;
    }

    generateNewKey() {
        this.cipher.generateNewKey();
        this.displaySubstitutionKey();
        this.setupLetterMappings();
    }

    handlePlaintextInput(event) {
        const text = event.target.value;
        document.getElementById('encryption-step').textContent = 
            text ? 'Click "Encrypt" to start encryption' : 'Type text above to start encryption';
    }

    handleCiphertextInput(event) {
        const text = event.target.value;
        this.updateFrequencyChart(text);
        document.getElementById('decryption-step').textContent = 
            text ? 'Click "Decrypt" to start decryption' : 'Enter ciphertext above to start decryption';
    }
}

// Initialize when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new CipherUI();
});
