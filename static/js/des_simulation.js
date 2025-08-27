// Complete DES Algorithm Implementation with Visualization

class DESSimulation {
    constructor() {
        this.setupTables();
        this.reset();
        this.setupEventListeners();
        this.animationSpeed = 1000; // milliseconds
    }

    setupTables() {
        // Initial Permutation Table
        this.IP = [
            58, 50, 42, 34, 26, 18, 10, 2,
            60, 52, 44, 36, 28, 20, 12, 4,
            62, 54, 46, 38, 30, 22, 14, 6,
            64, 56, 48, 40, 32, 24, 16, 8,
            57, 49, 41, 33, 25, 17, 9, 1,
            59, 51, 43, 35, 27, 19, 11, 3,
            61, 53, 45, 37, 29, 21, 13, 5,
            63, 55, 47, 39, 31, 23, 15, 7
        ];

        // Final Permutation Table
        this.FP = [
            40, 8, 48, 16, 56, 24, 64, 32,
            39, 7, 47, 15, 55, 23, 63, 31,
            38, 6, 46, 14, 54, 22, 62, 30,
            37, 5, 45, 13, 53, 21, 61, 29,
            36, 4, 44, 12, 52, 20, 60, 28,
            35, 3, 43, 11, 51, 19, 59, 27,
            34, 2, 42, 10, 50, 18, 58, 26,
            33, 1, 41, 9, 49, 17, 57, 25
        ];

        // Expansion Table
        this.E = [
            32, 1, 2, 3, 4, 5,
            4, 5, 6, 7, 8, 9,
            8, 9, 10, 11, 12, 13,
            12, 13, 14, 15, 16, 17,
            16, 17, 18, 19, 20, 21,
            20, 21, 22, 23, 24, 25,
            24, 25, 26, 27, 28, 29,
            28, 29, 30, 31, 32, 1
        ];

        // P-Box (Permutation after S-boxes)
        this.P = [
            16, 7, 20, 21, 29, 12, 28, 17,
            1, 15, 23, 26, 5, 18, 31, 10,
            2, 8, 24, 14, 32, 27, 3, 9,
            19, 13, 30, 6, 22, 11, 4, 25
        ];

        // S-boxes
        this.S = [
            // S1
            [
                [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
                [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
                [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
                [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
            ],
            // S2
            [
                [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
                [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
                [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
                [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
            ],
            // S3
            [
                [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
                [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
                [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
                [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
            ],
            // S4
            [
                [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
                [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
                [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
                [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
            ],
            // S5
            [
                [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
                [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
                [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
                [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
            ],
            // S6
            [
                [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
                [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
                [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
                [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
            ],
            // S7
            [
                [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
                [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
                [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
                [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
            ],
            // S8
            [
                [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
                [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
                [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
                [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
            ]
        ];

        // Key Schedule Tables
        this.PC1 = [
            57, 49, 41, 33, 25, 17, 9,
            1, 58, 50, 42, 34, 26, 18,
            10, 2, 59, 51, 43, 35, 27,
            19, 11, 3, 60, 52, 44, 36,
            63, 55, 47, 39, 31, 23, 15,
            7, 62, 54, 46, 38, 30, 22,
            14, 6, 61, 53, 45, 37, 29,
            21, 13, 5, 28, 20, 12, 4
        ];

        this.PC2 = [
            14, 17, 11, 24, 1, 5,
            3, 28, 15, 6, 21, 10,
            23, 19, 12, 4, 26, 8,
            16, 7, 27, 20, 13, 2,
            41, 52, 31, 37, 47, 55,
            30, 40, 51, 45, 33, 48,
            44, 49, 39, 56, 34, 53,
            46, 42, 50, 36, 29, 32
        ];

        this.leftShifts = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1];
    }

    setupEventListeners() {
        document.getElementById('startBtn').addEventListener('click', () => this.start());
        document.getElementById('stepBtn').addEventListener('click', () => this.step());
        document.getElementById('resetBtn').addEventListener('click', () => this.reset());
        document.getElementById('autoBtn').addEventListener('click', () => this.autoRun());
        document.getElementById('speedSlider').addEventListener('input', (e) => {
            this.animationSpeed = 2000 - (e.target.value * 1800);
        });

        // Input validation
        document.getElementById('plaintext').addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^0-9A-Fa-f]/g, '').toUpperCase();
            if (e.target.value.length > 16) {
                e.target.value = e.target.value.slice(0, 16);
            }
        });

        document.getElementById('key').addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^0-9A-Fa-f]/g, '').toUpperCase();
            if (e.target.value.length > 16) {
                e.target.value = e.target.value.slice(0, 16);
            }
        });
    }

    // Utility functions
    hexToBinary(hex) {
        return hex.split('').map(char => 
            parseInt(char, 16).toString(2).padStart(4, '0')
        ).join('');
    }

    binaryToHex(binary) {
        return binary.match(/.{4}/g).map(nibble =>
            parseInt(nibble, 2).toString(16).toUpperCase()
        ).join('');
    }

    permute(input, table) {
        let output = '';
        for (let i = 0; i < table.length; i++) {
            output += input[table[i] - 1];
        }
        return output;
    }

    xor(a, b) {
        let result = '';
        for (let i = 0; i < a.length; i++) {
            result += (parseInt(a[i]) ^ parseInt(b[i])).toString();
        }
        return result;
    }

    leftShift(bits, shifts) {
        return bits.substring(shifts) + bits.substring(0, shifts);
    }

    // Key Schedule Generation
    generateKeys(key) {
        const keyBinary = this.hexToBinary(key);
        const pc1Key = this.permute(keyBinary, this.PC1);
        
        let C = pc1Key.substring(0, 28);
        let D = pc1Key.substring(28, 56);
        
        this.roundKeys = [];
        
        for (let i = 0; i < 16; i++) {
            C = this.leftShift(C, this.leftShifts[i]);
            D = this.leftShift(D, this.leftShifts[i]);
            
            const combined = C + D;
            this.roundKeys[i] = this.permute(combined, this.PC2);
        }
    }

    // S-box substitution
    sBoxSubstitution(input) {
        let output = '';
        for (let i = 0; i < 8; i++) {
            const block = input.substring(i * 6, (i + 1) * 6);
            const row = parseInt(block[0] + block[5], 2);
            const col = parseInt(block.substring(1, 5), 2);
            const sBoxValue = this.S[i][row][col];
            output += sBoxValue.toString(2).padStart(4, '0');
        }
        return output;
    }

    // Feistel function
    feistelFunction(R, K) {
        const expandedR = this.permute(R, this.E);
        const xoredWithKey = this.xor(expandedR, K);
        const sBoxOutput = this.sBoxSubstitution(xoredWithKey);
        return this.permute(sBoxOutput, this.P);
    }

    // Main DES algorithm
    async start() {
        const plaintext = document.getElementById('plaintext').value;
        const key = document.getElementById('key').value;
        const operation = document.querySelector('input[name="operation"]:checked').value;

        if (plaintext.length !== 16 || key.length !== 16) {
            this.showError('Please enter valid 16-character hexadecimal plaintext and key');
            return;
        }

        this.reset();
        this.updateAlgorithmSummary('Initializing DES algorithm...');
        this.updateFlowStep(1);
        
        this.generateKeys(key);
        this.updateKeySchedule();
        
        const plaintextBinary = this.hexToBinary(plaintext);
        const permutedInput = this.permute(plaintextBinary, this.IP);
        
        this.L = permutedInput.substring(0, 32);
        this.R = permutedInput.substring(32, 64);
        
        this.isEncryption = operation === 'encrypt';
        this.isRunning = true;
        
        document.getElementById('stepBtn').disabled = false;
        document.getElementById('startBtn').disabled = true;
        document.getElementById('autoBtn').disabled = false;
        
        this.updateFlowStep(2);
        this.updateAlgorithmSummary(`Initial permutation applied. Starting ${operation} with 16 rounds...`);
        
        await this.updateVisualization();
    }

    async step() {
        if (this.currentRound >= 16) return;

        this.updateFlowStep(3);
        this.updateAlgorithmSummary(`Round ${this.currentRound + 1}/16: Applying Feistel function...`);

        const roundKey = this.isEncryption ? 
            this.roundKeys[this.currentRound] : 
            this.roundKeys[15 - this.currentRound];

        await this.animateRoundFunction(this.R, roundKey);
        
        const fResult = this.feistelFunction(this.R, roundKey);
        const newL = this.R;
        const newR = this.xor(this.L, fResult);
        
        this.L = newL;
        this.R = newR;
        this.currentRound++;
        
        await this.updateVisualization();
        this.updateKeySchedule();
        
        if (this.currentRound >= 16) {
            await this.finalize();
        } else {
            this.updateAlgorithmSummary(`Round ${this.currentRound} completed. L=${this.binaryToHex(this.L)}, R=${this.binaryToHex(this.R)}`);
        }
    }

    async autoRun() {
        if (!this.isRunning) return;
        
        document.getElementById('autoBtn').disabled = true;
        document.getElementById('stepBtn').disabled = true;
        
        while (this.currentRound < 16 && this.isRunning) {
            await this.step();
            await this.delay(this.animationSpeed);
        }
        
        document.getElementById('autoBtn').disabled = false;
    }

    async finalize() {
        this.updateFlowStep(4);
        this.updateAlgorithmSummary('Applying final permutation...');
        
        const preOutput = this.R + this.L; // Note: R and L are swapped
        const finalOutput = this.permute(preOutput, this.FP);
        const hexOutput = this.binaryToHex(finalOutput);
        
        await this.animateResult(hexOutput);
        
        this.updateAlgorithmSummary(
            `DES ${this.isEncryption ? 'encryption' : 'decryption'} completed! ` +
            `Input: ${document.getElementById('plaintext').value}, ` +
            `Output: ${hexOutput}`
        );
        
        document.getElementById('stepBtn').disabled = true;
        document.getElementById('startBtn').disabled = false;
        this.isRunning = false;
    }

    async animateRoundFunction(R, K) {
        // Animate expansion
        const expandedR = this.permute(R, this.E);
        await this.animateElement('expansion', this.binaryToHex(expandedR));
        await this.delay(this.animationSpeed / 4);
        
        // Animate key XOR
        await this.animateElement('roundKey', this.binaryToHex(K));
        await this.delay(this.animationSpeed / 4);
        
        // Animate XOR result
        const xoredWithKey = this.xor(expandedR, K);
        await this.animateElement('xorResult', this.binaryToHex(xoredWithKey));
        await this.delay(this.animationSpeed / 4);
        
        // Update S-box visualization
        await this.updateSBoxVisualization(xoredWithKey);
        await this.delay(this.animationSpeed / 4);
        
        // Animate S-box substitution
        const sBoxOutput = this.sBoxSubstitution(xoredWithKey);
        await this.animateElement('sboxOutput', this.binaryToHex(sBoxOutput));
        await this.delay(this.animationSpeed / 4);
        
        // Animate permutation
        const permuted = this.permute(sBoxOutput, this.P);
        await this.animateElement('permutation', this.binaryToHex(permuted));
        await this.delay(this.animationSpeed / 4);
    }

    async animateElement(elementId, value) {
        const element = document.getElementById(elementId);
        if (!element) return;
        
        element.classList.add('animate-update', 'step-highlight');
        element.textContent = value;
        await this.delay(300);
        element.classList.remove('animate-update');
        
        // Keep highlight for a bit longer
        setTimeout(() => {
            element.classList.remove('step-highlight');
        }, 1000);
    }

    async updateVisualization() {
        // Update round counter
        document.getElementById('currentRound').textContent = this.currentRound;
        document.getElementById('progressBar').style.width = `${(this.currentRound / 16) * 100}%`;
        
        // Update halves
        document.getElementById('leftIndex').textContent = this.currentRound;
        document.getElementById('rightIndex').textContent = this.currentRound;
        
        await this.animateElement('leftHalf', this.binaryToHex(this.L));
        await this.animateElement('rightHalf', this.binaryToHex(this.R));
        
        // Update key index
        document.getElementById('keyIndex').textContent = this.currentRound + 1;
    }

    async animateResult(result) {
        await this.animateElement('output', result);
        const binaryResult = this.hexToBinary(result);
        const formattedBinary = binaryResult.match(/.{4}/g).join(' ');
        await this.animateElement('binaryOutput', formattedBinary);
    }

    reset() {
        this.currentRound = 0;
        this.L = '0'.repeat(32);
        this.R = '0'.repeat(32);
        this.isRunning = false;
        this.roundKeys = [];
        
        document.getElementById('stepBtn').disabled = true;
        document.getElementById('startBtn').disabled = false;
        document.getElementById('autoBtn').disabled = false;
        
        // Reset all displays
        document.getElementById('currentRound').textContent = '0';
        document.getElementById('progressBar').style.width = '0%';
        document.getElementById('leftHalf').textContent = '00000000';
        document.getElementById('rightHalf').textContent = '00000000';
        document.getElementById('expansion').textContent = '000000000000';
        document.getElementById('roundKey').textContent = '000000000000';
        document.getElementById('sboxOutput').textContent = '00000000';
        document.getElementById('permutation').textContent = '00000000';
        document.getElementById('output').textContent = '0000000000000000';
        document.getElementById('binaryOutput').textContent = '0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000';
        
        this.hideError();
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    showError(message) {
        const errorDiv = document.getElementById('errorMessage');
        const errorText = document.getElementById('errorText');
        errorText.textContent = message;
        errorDiv.classList.remove('hidden');
    }

    hideError() {
        const errorDiv = document.getElementById('errorMessage');
        errorDiv.classList.add('hidden');
    }

    updateAlgorithmSummary(message) {
        const summary = document.getElementById('algorithmSummary');
        summary.textContent = message;
    }

    updateFlowStep(stepNumber) {
        // Remove active class from all steps
        document.querySelectorAll('.flow-step').forEach(step => {
            step.classList.remove('active');
        });
        
        // Add active class to current step
        const currentStep = document.getElementById(`step${stepNumber}`);
        if (currentStep) {
            currentStep.classList.add('active');
        }
    }

    async updateSBoxVisualization(xoredInput) {
        // Update S-box inputs with sequential animation
        for (let i = 0; i < 8; i++) {
            const sboxInput = xoredInput.substring(i * 6, (i + 1) * 6);
            const sboxElement = document.getElementById(`sbox${i + 1}`);
            if (sboxElement) {
                // Calculate S-box output for this input
                const block = sboxInput;
                const row = parseInt(block[0] + block[5], 2);
                const col = parseInt(block.substring(1, 5), 2);
                const sBoxValue = this.S[i][row][col];
                const binaryOutput = sBoxValue.toString(2).padStart(4, '0');
                
                sboxElement.innerHTML = `S${i + 1}<br>${sboxInput}<br>→ ${binaryOutput}`;
                sboxElement.classList.add('active', 'processing');
                
                // Sequential animation delay
                await this.delay(this.animationSpeed / 16);
                
                setTimeout(() => {
                    sboxElement.classList.remove('active', 'processing');
                }, 800);
            }
        }
    }

    updateKeySchedule() {
        // Update key schedule visualization
        for (let i = 0; i < 16; i++) {
            const keyElement = document.getElementById(`key${i + 1}`);
            if (keyElement && this.roundKeys[i]) {
                const keyHex = this.binaryToHex(this.roundKeys[i]);
                keyElement.innerHTML = `K${i + 1}<br>${keyHex.substring(0, 6)}`;
                
                // Highlight current key
                if (i === this.currentRound) {
                    keyElement.classList.add('active');
                } else {
                    keyElement.classList.remove('active');
                }
            }
        }
    }
}

// Initialize the DES simulation when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new DESSimulation();
});
