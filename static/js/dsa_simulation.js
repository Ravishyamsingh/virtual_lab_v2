// Complete DSA Algorithm Implementation with Visualization

class DSASimulation {
    constructor() {
        this.reset();
        this.setupEventListeners();
        this.animationSpeed = 1000;
        this.currentStep = 0;
        this.totalSteps = 6;
        
        // DSA parameters (using smaller values for demonstration)
        this.parameters = {
            p: null,  // Prime modulus
            q: null,  // Prime divisor
            g: null,  // Generator
            x: null,  // Private key
            y: null,  // Public key
            k: null,  // Random number for signature
            h: null,  // Hash of message
            r: null,  // First part of signature
            s: null   // Second part of signature
        };
    }

    setupEventListeners() {
        document.getElementById('generateKeysBtn').addEventListener('click', () => this.generateKeys());
        document.getElementById('signMessageBtn').addEventListener('click', () => this.signMessage());
        document.getElementById('verifySignatureBtn').addEventListener('click', () => this.verifySignature());
        document.getElementById('resetBtn').addEventListener('click', () => this.reset());
        document.getElementById('autoRunBtn').addEventListener('click', () => this.autoRun());
        document.getElementById('speedSlider').addEventListener('input', (e) => {
            this.animationSpeed = 2000 - (e.target.value * 1800);
        });

        // Input validation
        document.getElementById('message').addEventListener('input', (e) => {
            this.validateInput();
        });
    }

    // Mathematical utility functions
    modPow(base, exponent, modulus) {
        if (modulus === 1) return 0;
        let result = 1;
        base = base % modulus;
        while (exponent > 0) {
            if (exponent % 2 === 1) {
                result = (result * base) % modulus;
            }
            exponent = Math.floor(exponent / 2);
            base = (base * base) % modulus;
        }
        return result;
    }

    modInverse(a, m) {
        // Extended Euclidean Algorithm
        if (this.gcd(a, m) !== 1) return null;
        
        let m0 = m, x0 = 0, x1 = 1;
        while (a > 1) {
            let q = Math.floor(a / m);
            let t = m;
            m = a % m;
            a = t;
            t = x0;
            x0 = x1 - q * x0;
            x1 = t;
        }
        return x1 < 0 ? x1 + m0 : x1;
    }

    gcd(a, b) {
        while (b !== 0) {
            let temp = b;
            b = a % b;
            a = temp;
        }
        return a;
    }

    isPrime(n) {
        if (n <= 1) return false;
        if (n <= 3) return true;
        if (n % 2 === 0 || n % 3 === 0) return false;
        
        for (let i = 5; i * i <= n; i += 6) {
            if (n % i === 0 || n % (i + 2) === 0) return false;
        }
        return true;
    }

    findPrimitiveRoot(p) {
        // Find a primitive root modulo p (simplified)
        for (let g = 2; g < p; g++) {
            let found = true;
            for (let i = 1; i < p - 1; i++) {
                if (this.modPow(g, i, p) === 1) {
                    found = false;
                    break;
                }
            }
            if (found) return g;
        }
        return 2; // fallback
    }

    simpleHash(message) {
        // Simple hash function for demonstration
        let hash = 0;
        for (let i = 0; i < message.length; i++) {
            hash = ((hash << 5) - hash + message.charCodeAt(i)) & 0xffffffff;
        }
        return Math.abs(hash) % 1000 + 1; // Keep it small for demo
    }

    generateRandomInRange(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }

    async generateKeys() {
        this.reset();
        this.updateProgress(1);
        this.updateAlgorithmSummary('Generating DSA key pair...');

        try {
            // Step 1: Generate prime q
            await this.animateStep(1, 'Generating prime q...');
            this.parameters.q = this.generateSmallPrime();
            await this.updateParameter('q', this.parameters.q);

            // Step 2: Generate prime p such that q divides (p-1)
            await this.animateStep(2, 'Generating prime p...');
            this.parameters.p = this.generateP(this.parameters.q);
            await this.updateParameter('p', this.parameters.p);

            // Step 3: Find generator g
            await this.animateStep(3, 'Finding generator g...');
            this.parameters.g = this.findGenerator(this.parameters.p, this.parameters.q);
            await this.updateParameter('g', this.parameters.g);

            // Step 4: Generate private key x
            await this.animateStep(4, 'Generating private key x...');
            this.parameters.x = this.generateRandomInRange(1, this.parameters.q - 1);
            await this.updateParameter('x', this.parameters.x);

            // Step 5: Calculate public key y = g^x mod p
            await this.animateStep(5, 'Calculating public key y = g^x mod p...');
            this.parameters.y = this.modPow(this.parameters.g, this.parameters.x, this.parameters.p);
            await this.updateParameter('y', this.parameters.y);

            this.updateAlgorithmSummary('DSA key pair generated successfully!');
            this.enableButtons(['signMessageBtn']);
            
        } catch (error) {
            this.showError('Error generating keys: ' + error.message);
        }
    }

    generateSmallPrime() {
        // Generate a small prime for demonstration
        const primes = [23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97];
        return primes[Math.floor(Math.random() * primes.length)];
    }

    generateP(q) {
        // Generate p such that q divides (p-1)
        // For simplicity, we'll use p = 2*q + 1 if it's prime
        let p = 2 * q + 1;
        if (this.isPrime(p)) return p;
        
        // Otherwise, find a suitable p
        for (let k = 2; k < 20; k++) {
            p = k * q + 1;
            if (this.isPrime(p)) return p;
        }
        return 2 * q + 1; // fallback
    }

    findGenerator(p, q) {
        // Find g such that g^q ≡ 1 (mod p) and g^1 ≢ 1 (mod p)
        for (let h = 2; h < p; h++) {
            let g = this.modPow(h, (p - 1) / q, p);
            if (g > 1) return g;
        }
        return 2; // fallback
    }

    async signMessage() {
        const message = document.getElementById('message').value.trim();
        if (!message) {
            this.showError('Please enter a message to sign');
            return;
        }

        if (!this.parameters.p || !this.parameters.q || !this.parameters.g || !this.parameters.x) {
            this.showError('Please generate keys first');
            return;
        }

        this.updateProgress(2);
        this.updateAlgorithmSummary('Signing message...');

        try {
            // Step 1: Hash the message
            await this.animateStep(1, 'Hashing message...');
            this.parameters.h = this.simpleHash(message);
            await this.updateParameter('h', this.parameters.h);

            // Step 2: Generate random k
            await this.animateStep(2, 'Generating random k...');
            this.parameters.k = this.generateRandomInRange(1, this.parameters.q - 1);
            await this.updateParameter('k', this.parameters.k);

            // Step 3: Calculate r = (g^k mod p) mod q
            await this.animateStep(3, 'Calculating r = (g^k mod p) mod q...');
            this.parameters.r = this.modPow(this.parameters.g, this.parameters.k, this.parameters.p) % this.parameters.q;
            await this.updateParameter('r', this.parameters.r);

            // Step 4: Calculate s = k^-1 * (h + x*r) mod q
            await this.animateStep(4, 'Calculating s = k^-1 * (h + x*r) mod q...');
            const kInverse = this.modInverse(this.parameters.k, this.parameters.q);
            this.parameters.s = (kInverse * (this.parameters.h + this.parameters.x * this.parameters.r)) % this.parameters.q;
            await this.updateParameter('s', this.parameters.s);

            this.updateAlgorithmSummary(`Message signed successfully! Signature: (${this.parameters.r}, ${this.parameters.s})`);
            this.enableButtons(['verifySignatureBtn']);

        } catch (error) {
            this.showError('Error signing message: ' + error.message);
        }
    }

    async verifySignature() {
        if (!this.parameters.r || !this.parameters.s) {
            this.showError('Please sign a message first');
            return;
        }

        this.updateProgress(3);
        this.updateAlgorithmSummary('Verifying signature...');

        try {
            // Step 1: Calculate w = s^-1 mod q
            await this.animateStep(1, 'Calculating w = s^-1 mod q...');
            const w = this.modInverse(this.parameters.s, this.parameters.q);
            await this.updateComputationStep(1, `w = ${w}`);

            // Step 2: Calculate u1 = h * w mod q
            await this.animateStep(2, 'Calculating u1 = h * w mod q...');
            const u1 = (this.parameters.h * w) % this.parameters.q;
            await this.updateComputationStep(2, `u1 = ${u1}`);

            // Step 3: Calculate u2 = r * w mod q
            await this.animateStep(3, 'Calculating u2 = r * w mod q...');
            const u2 = (this.parameters.r * w) % this.parameters.q;
            await this.updateComputationStep(3, `u2 = ${u2}`);

            // Step 4: Calculate v = ((g^u1 * y^u2) mod p) mod q
            await this.animateStep(4, 'Calculating v = ((g^u1 * y^u2) mod p) mod q...');
            const gu1 = this.modPow(this.parameters.g, u1, this.parameters.p);
            const yu2 = this.modPow(this.parameters.y, u2, this.parameters.p);
            const v = ((gu1 * yu2) % this.parameters.p) % this.parameters.q;
            await this.updateComputationStep(4, `v = ${v}`);

            // Step 5: Verify if v == r
            await this.animateStep(5, 'Verifying if v == r...');
            const isValid = v === this.parameters.r;
            
            await this.showVerificationResult(isValid, v, this.parameters.r);
            
            this.updateAlgorithmSummary(
                `Signature ${isValid ? 'verified successfully' : 'verification failed'}! ` +
                `v = ${v}, r = ${this.parameters.r}`
            );

        } catch (error) {
            this.showError('Error verifying signature: ' + error.message);
        }
    }

    async autoRun() {
        if (!document.getElementById('message').value.trim()) {
            this.showError('Please enter a message first');
            return;
        }

        this.disableButtons(['autoRunBtn']);
        
        try {
            await this.generateKeys();
            await this.delay(this.animationSpeed);
            await this.signMessage();
            await this.delay(this.animationSpeed);
            await this.verifySignature();
        } catch (error) {
            this.showError('Error in auto run: ' + error.message);
        } finally {
            this.enableButtons(['autoRunBtn']);
        }
    }

    async animateStep(stepNumber, description) {
        const stepElement = document.getElementById(`step${stepNumber}`);
        if (stepElement) {
            stepElement.classList.add('active');
            stepElement.querySelector('.flow-description').textContent = description;
        }
        await this.delay(this.animationSpeed / 2);
    }

    async updateParameter(name, value) {
        const element = document.getElementById(name);
        if (element) {
            element.classList.add('animate-update');
            element.textContent = value;
            await this.delay(300);
            element.classList.remove('animate-update');
        }
    }

    async updateComputationStep(stepNumber, result) {
        const stepElement = document.getElementById(`computationStep${stepNumber}`);
        if (stepElement) {
            stepElement.classList.add('completed');
            const resultElement = stepElement.querySelector('.step-result');
            if (resultElement) {
                resultElement.textContent = result;
            }
        }
        await this.delay(300);
    }

    async showVerificationResult(isValid, computed, expected) {
        const resultDiv = document.getElementById('verificationResult');
        const iconDiv = document.getElementById('verificationIcon');
        const textDiv = document.getElementById('verificationText');
        const detailsDiv = document.getElementById('verificationDetails');

        if (isValid) {
            iconDiv.className = 'verification-icon verification-success';
            iconDiv.innerHTML = '✓';
            textDiv.textContent = 'Signature Valid';
            detailsDiv.textContent = `Computed value ${computed} matches signature component r = ${expected}`;
            resultDiv.classList.add('verified');
        } else {
            iconDiv.className = 'verification-icon verification-failure';
            iconDiv.innerHTML = '✗';
            textDiv.textContent = 'Signature Invalid';
            detailsDiv.textContent = `Computed value ${computed} does not match signature component r = ${expected}`;
            resultDiv.classList.add('failed');
        }

        resultDiv.style.display = 'block';
    }

    updateProgress(step) {
        this.currentStep = step;
        const progress = (step / this.totalSteps) * 100;
        document.getElementById('progressBar').style.width = `${progress}%`;
        document.getElementById('currentStep').textContent = step;
    }

    updateAlgorithmSummary(message) {
        const summary = document.getElementById('algorithmSummary');
        if (summary) {
            summary.textContent = message;
        }
    }

    enableButtons(buttonIds) {
        buttonIds.forEach(id => {
            const button = document.getElementById(id);
            if (button) {
                button.disabled = false;
            }
        });
    }

    disableButtons(buttonIds) {
        buttonIds.forEach(id => {
            const button = document.getElementById(id);
            if (button) {
                button.disabled = true;
            }
        });
    }

    validateInput() {
        const message = document.getElementById('message').value.trim();
        const generateBtn = document.getElementById('generateKeysBtn');
        const autoRunBtn = document.getElementById('autoRunBtn');
        
        if (message.length > 0) {
            generateBtn.disabled = false;
            autoRunBtn.disabled = false;
        } else {
            autoRunBtn.disabled = true;
        }
    }

    showError(message) {
        const errorDiv = document.getElementById('errorMessage');
        const errorText = document.getElementById('errorText');
        if (errorDiv && errorText) {
            errorText.textContent = message;
            errorDiv.classList.remove('hidden');
        }
    }

    hideError() {
        const errorDiv = document.getElementById('errorMessage');
        if (errorDiv) {
            errorDiv.classList.add('hidden');
        }
    }

    reset() {
        this.currentStep = 0;
        this.parameters = {
            p: null, q: null, g: null, x: null, y: null,
            k: null, h: null, r: null, s: null
        };

        // Reset UI
        this.updateProgress(0);
        this.hideError();
        
        // Reset parameter displays
        ['p', 'q', 'g', 'x', 'y', 'k', 'h', 'r', 's'].forEach(param => {
            const element = document.getElementById(param);
            if (element) {
                element.textContent = '-';
            }
        });

        // Reset flow steps
        document.querySelectorAll('.flow-step').forEach(step => {
            step.classList.remove('active', 'verified', 'failed');
        });

        // Reset computation steps
        document.querySelectorAll('.computation-step').forEach(step => {
            step.classList.remove('active', 'completed');
        });

        // Reset buttons
        this.disableButtons(['signMessageBtn', 'verifySignatureBtn']);
        this.enableButtons(['generateKeysBtn', 'resetBtn']);
        
        // Reset verification result
        const resultDiv = document.getElementById('verificationResult');
        if (resultDiv) {
            resultDiv.style.display = 'none';
            resultDiv.classList.remove('verified', 'failed');
        }

        this.updateAlgorithmSummary('Ready to start DSA simulation...');
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Initialize the DSA simulation when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new DSASimulation();
});
