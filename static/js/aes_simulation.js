// Enhanced AES Simulation with Perfect Visualization and Animation
class AESSimulation {
    constructor() {
        // Ensure init is called after DOM is fully loaded
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.init());
        } else {
            this.init();
        }
    }

    init() {
        this.setupConstants();
        this.setupVariables();
        this.setupEventListeners();
        this.initializeVisualization();
        this.setupAnimationFramework();
    }

    setupConstants() {
        // AES S-Box
        this.sBox = [
            0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
            0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
            0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
            0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
            0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
            0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
            0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
            0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
            0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
            0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
            0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
            0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
            0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
            0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
            0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
            0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
        ];

        // AES Inverse S-Box
        this.invSBox = [
            0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
            0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
            0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
            0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
            0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
            0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
            0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
            0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
            0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
            0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
            0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
            0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
            0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
            0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
            0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
            0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D
        ];

        // Round constants
        this.rcon = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36];

        // Mix columns matrix
        this.mixMatrix = [
            [0x02, 0x03, 0x01, 0x01],
            [0x01, 0x02, 0x03, 0x01],
            [0x01, 0x01, 0x02, 0x03],
            [0x03, 0x01, 0x01, 0x02]
        ];

        // Inverse mix columns matrix
        this.invMixMatrix = [
            [0x0e, 0x0b, 0x0d, 0x09],
            [0x09, 0x0e, 0x0b, 0x0d],
            [0x0d, 0x09, 0x0e, 0x0b],
            [0x0b, 0x0d, 0x09, 0x0e]
        ];
    }

    setupVariables() {
        this.state = Array(4).fill().map(() => Array(4).fill(0));
        this.keySchedule = [];
        this.currentRound = 0;
        this.totalRounds = 10;
        this.isRunning = false;
        this.isPaused = false;
        this.animationSpeed = 1000;
        this.isEncrypting = true;
        this.keySize = 128;
        this.stepHistory = [];
        this.currentStep = 0;
        this.originalKey = [];
        this.animationQueue = [];
        this.currentAnimation = null;
    }

    setupEventListeners() {
        // Button events
        document.getElementById('startBtn').addEventListener('click', () => this.startSimulation());
        document.getElementById('stepBtn').addEventListener('click', () => this.nextStep());
        document.getElementById('resetBtn').addEventListener('click', () => this.resetSimulation());
        document.getElementById('pauseBtn')?.addEventListener('click', () => this.pauseSimulation());
        document.getElementById('playBtn')?.addEventListener('click', () => this.playSimulation());

        // Input validation
        document.getElementById('plaintext').addEventListener('input', (e) => this.validateHexInput(e, 32));
        document.getElementById('key').addEventListener('input', (e) => this.validateKeyInput(e));

        // Key size change
        document.querySelectorAll('input[name="keySize"]').forEach(radio => {
            radio.addEventListener('change', () => this.updateKeySize());
        });

        // Operation mode change
        document.querySelectorAll('input[name="operation"]').forEach(radio => {
            radio.addEventListener('change', () => this.updateOperation());
        });

        // Animation speed control
        document.getElementById('speedSlider')?.addEventListener('input', (e) => {
            this.animationSpeed = 2000 - (e.target.value * 19);
            this.updateSpeedDisplay();
        });

        // Matrix cell hover effects
        this.setupMatrixHoverEffects();
    }

    setupAnimationFramework() {
        this.animationQueue = [];
        this.isAnimating = false;
    }

    async executeAnimationQueue() {
        if (this.isAnimating) return;
        this.isAnimating = true;

        while (this.animationQueue.length > 0) {
            if (this.isPaused) {
                await this.waitForResume();
            }

            const animation = this.animationQueue.shift();
            await animation();
        }

        this.isAnimating = false;
    }

    async waitForResume() {
        while (this.isPaused) {
            await this.delay(100);
        }
    }

    validateHexInput(event, maxLength) {
        const value = event.target.value.replace(/[^0-9A-Fa-f]/g, '').toUpperCase();
        event.target.value = value.slice(0, maxLength);
        this.updateInputValidation(event.target);
    }

    validateKeyInput(event) {
        const keySize = parseInt(document.querySelector('input[name="keySize"]:checked').value);
        const maxLength = keySize / 4;
        this.validateHexInput(event, maxLength);
    }

    updateInputValidation(input) {
        const isValid = input.value.length === parseInt(input.maxLength);
        input.classList.toggle('valid', isValid);
        input.classList.toggle('invalid', !isValid);
    }

    updateKeySize() {
        const keySize = parseInt(document.querySelector('input[name="keySize"]:checked').value);
        this.keySize = keySize;
        this.totalRounds = keySize === 128 ? 10 : keySize === 192 ? 12 : 14;
        
        const keyInput = document.getElementById('key');
        const maxLength = keySize / 4;
        keyInput.maxLength = maxLength;
        keyInput.placeholder = `Enter ${maxLength} hexadecimal characters`;
        
        this.updateTotalRounds();
        this.validateKeyInput({target: keyInput});
    }

    updateOperation() {
        this.isEncrypting = document.querySelector('input[name="operation"]:checked').value === 'encrypt';
        this.updateOperationDisplay();
    }

    updateTotalRounds() {
        document.getElementById('totalRounds').textContent = this.totalRounds;
        this.updateProgressBar();
    }

    updateSpeedDisplay() {
        const speedText = this.animationSpeed > 1500 ? 'Slow' : 
                         this.animationSpeed > 800 ? 'Medium' : 'Fast';
        document.getElementById('speedDisplay').textContent = speedText;
    }

    setupMatrixHoverEffects() {
        for (let i = 0; i < 4; i++) {
            for (let j = 0; j < 4; j++) {
                const cell = document.getElementById(`state${i}${j}`);
                if (cell) {
                    cell.addEventListener('mouseenter', () => this.highlightCell(i, j));
                    cell.addEventListener('mouseleave', () => this.unhighlightCell(i, j));
                }
            }
        }
    }

    highlightCell(row, col) {
        const cell = document.getElementById(`state${row}${col}`);
        if (cell && !cell.classList.contains('processing')) {
            cell.classList.add('highlighted');
        }
    }

    unhighlightCell(row, col) {
        const cell = document.getElementById(`state${row}${col}`);
        if (cell) {
            cell.classList.remove('highlighted');
        }
    }

    initializeVisualization() {
        this.updateRoundDisplay();
        this.updateStateMatrix();
        this.updateOperationDisplay();
        this.createSBoxVisualization();
        this.createKeyScheduleVisualization();
        this.updateControls();
    }

    createSBoxVisualization() {
        const container = document.getElementById('sboxContainer');
        if (!container) return;

        container.innerHTML = '';
        
        for (let i = 0; i < 256; i++) {
            const cell = document.createElement('div');
            cell.className = 'sbox-cell';
            cell.id = `sbox-${i}`;
            cell.textContent = this.sBox[i].toString(16).padStart(2, '0').toUpperCase();
            cell.setAttribute('data-tooltip', `Input: ${i.toString(16).padStart(2, '0')} → Output: ${this.sBox[i].toString(16).padStart(2, '0')}`);
            
            cell.addEventListener('mouseenter', () => {
                cell.style.transform = 'scale(1.2)';
                cell.style.zIndex = '10';
            });
            
            cell.addEventListener('mouseleave', () => {
                cell.style.transform = 'scale(1)';
                cell.style.zIndex = '1';
            });
            
            container.appendChild(cell);
        }
    }

    createKeyScheduleVisualization() {
        const container = document.getElementById('keyScheduleContainer');
        if (!container) return;

        container.innerHTML = '';
        for (let round = 0; round <= this.totalRounds; round++) {
            const roundDiv = document.createElement('div');
            roundDiv.className = 'key-round';
            roundDiv.id = `keyRound-${round}`;

            const label = document.createElement('div');
            label.className = 'key-round-label';
            label.textContent = round === 0 ? 'Initial' : `Round ${round}`;

            const values = document.createElement('div');
            values.className = 'key-values';

            for (let i = 0; i < 16; i++) {
                const byte = document.createElement('div');
                byte.className = 'key-byte';
                byte.id = `keyByte-${round}-${i}`;
                byte.textContent = '00';
                values.appendChild(byte);
            }

            roundDiv.appendChild(label);
            roundDiv.appendChild(values);
            container.appendChild(roundDiv);
        }
    }

    async startSimulation() {
        if (!this.validateInputs()) return;

        this.resetSimulation();
        this.parseInputs();
        this.generateKeySchedule();
        this.isRunning = true;
        this.updateControls();

        try {
            await this.runSimulation();
        } catch (error) {
            console.error('Simulation error:', error);
            this.showError('Simulation error occurred: ' + error.message);
        }
    }

    validateInputs() {
        const plaintext = document.getElementById('plaintext').value;
        const key = document.getElementById('key').value;
        const requiredKeyLength = this.keySize / 4;

        if (plaintext.length !== 32) {
            this.showError('Plaintext must be exactly 32 hexadecimal characters');
            return false;
        }

        if (key.length !== requiredKeyLength) {
            this.showError(`Key must be exactly ${requiredKeyLength} hexadecimal characters for ${this.keySize}-bit AES`);
            return false;
        }

        if (!/^[0-9A-Fa-f]+$/.test(plaintext)) {
            this.showError('Plaintext must contain only hexadecimal characters');
            return false;
        }

        if (!/^[0-9A-Fa-f]+$/.test(key)) {
            this.showError('Key must contain only hexadecimal characters');
            return false;
        }

        return true;
    }

    parseInputs() {
        const plaintext = document.getElementById('plaintext').value;
        const key = document.getElementById('key').value;

        // Parse plaintext into state matrix (column-major order)
        for (let i = 0; i < 4; i++) {
            for (let j = 0; j < 4; j++) {
                const index = (j * 4 + i) * 2;
                this.state[i][j] = parseInt(plaintext.substr(index, 2), 16);
            }
        }

        // Parse key
        this.originalKey = [];
        for (let i = 0; i < key.length; i += 2) {
            this.originalKey.push(parseInt(key.substr(i, 2), 16));
        }

        this.updateStateMatrix();
        this.updateKeyDisplay();
        this.addToHistory('Initial State', this.copyState());
    }

    generateKeySchedule() {
        const keyWords = Math.floor(this.keySize / 32);
        const totalWords = 4 * (this.totalRounds + 1);
        
        this.keySchedule = [];
        
        // Initial key words
        for (let i = 0; i < keyWords; i++) {
            this.keySchedule[i] = [
                this.originalKey[i * 4],
                this.originalKey[i * 4 + 1],
                this.originalKey[i * 4 + 2],
                this.originalKey[i * 4 + 3]
            ];
        }

        // Generate remaining key words
        for (let i = keyWords; i < totalWords; i++) {
            let temp = [...this.keySchedule[i - 1]];
            
            if (i % keyWords === 0) {
                // Rotate word
                temp = [temp[1], temp[2], temp[3], temp[0]];
                
                // SubBytes
                for (let j = 0; j < 4; j++) {
                    temp[j] = this.sBox[temp[j]];
                }
                
                // XOR with round constant
                temp[0] ^= this.rcon[Math.floor(i / keyWords) - 1];
            } else if (keyWords > 6 && i % keyWords === 4) {
                // Additional SubBytes for 256-bit key
                for (let j = 0; j < 4; j++) {
                    temp[j] = this.sBox[temp[j]];
                }
            }
            
            // XOR with word keyWords positions back
            this.keySchedule[i] = [];
            for (let j = 0; j < 4; j++) {
                this.keySchedule[i][j] = this.keySchedule[i - keyWords][j] ^ temp[j];
            }
        }

        this.updateKeyScheduleDisplay();
    }

    async runSimulation() {
        this.showMessage('Starting AES ' + (this.isEncrypting ? 'Encryption' : 'Decryption'), 'info');
        
        if (this.isEncrypting) {
            await this.encrypt();
        } else {
            await this.decrypt();
        }
        
        this.showMessage('Simulation completed successfully!', 'success');
        this.isRunning = false;
        this.updateControls();
    }

    async encrypt() {
        // Initial AddRoundKey
        await this.addRoundKey(0, 'Initial AddRoundKey');
        
        // Main rounds
        for (let round = 1; round <= this.totalRounds; round++) {
            this.currentRound = round;
            this.updateRoundDisplay();
            
            await this.subBytes(`Round ${round}: SubBytes`);
            await this.shiftRows(`Round ${round}: ShiftRows`);
            
            if (round < this.totalRounds) {
                await this.mixColumns(`Round ${round}: MixColumns`);
            }
            
            await this.addRoundKey(round, `Round ${round}: AddRoundKey`);
        }
        
        this.updateOutput();
    }

    async decrypt() {
        // Initial AddRoundKey
        await this.addRoundKey(this.totalRounds, 'Initial AddRoundKey (Decryption)');
        
        // Main rounds (in reverse)
        for (let round = this.totalRounds - 1; round >= 0; round--) {
            this.currentRound = this.totalRounds - round;
            this.updateRoundDisplay();
            
            await this.invShiftRows(`Round ${this.currentRound}: InvShiftRows`);
            await this.invSubBytes(`Round ${this.currentRound}: InvSubBytes`);
            await this.addRoundKey(round, `Round ${this.currentRound}: AddRoundKey`);
            
            if (round > 0) {
                await this.invMixColumns(`Round ${this.currentRound}: InvMixColumns`);
            }
        }
        
        this.updateOutput();
    }

    async subBytes(operationName) {
        this.updateCurrentOperation(operationName);
        this.updateOperationDetails('Substituting bytes using AES S-Box...');
        
        for (let i = 0; i < 4; i++) {
            for (let j = 0; j < 4; j++) {
                if (this.isPaused) await this.waitForResume();
                
                const oldValue = this.state[i][j];
                const newValue = this.sBox[oldValue];
                
                // Highlight S-Box lookup
                this.highlightSBoxLookup(oldValue, newValue);
                
                // Animate cell change
                await this.animateCellChange(i, j, oldValue, newValue);
                
                this.state[i][j] = newValue;
            }
        }
        
        this.updateStateMatrix();
        this.addToHistory('SubBytes', this.copyState());
        this.clearSBoxHighlights();
    }

    async invSubBytes(operationName) {
        this.updateCurrentOperation(operationName);
        this.updateOperationDetails('Substituting bytes using AES Inverse S-Box...');
        
        for (let i = 0; i < 4; i++) {
            for (let j = 0; j < 4; j++) {
                if (this.isPaused) await this.waitForResume();
                
                const oldValue = this.state[i][j];
                const newValue = this.invSBox[oldValue];
                
                await this.animateCellChange(i, j, oldValue, newValue);
                this.state[i][j] = newValue;
            }
        }
        
        this.updateStateMatrix();
        this.addToHistory('InvSubBytes', this.copyState());
    }

    async shiftRows(operationName) {
        this.updateCurrentOperation(operationName);
        this.updateOperationDetails('Shifting rows cyclically left...');
        
        const newState = Array(4).fill().map(() => Array(4).fill(0));
        
        // Animate row shifts with visual feedback
        for (let row = 0; row < 4; row++) {
            // Highlight the entire row
            this.highlightRow(row);
            
            for (let col = 0; col < 4; col++) {
                const newCol = (col - row + 4) % 4;
                newState[row][newCol] = this.state[row][col];
            }
            
            // Show the shift animation
            await this.animateRowShift(row, row);
            await this.delay(this.animationSpeed / 4);
        }
        
        this.state = newState;
        this.updateStateMatrix();
        this.addToHistory('ShiftRows', this.copyState());
        this.clearRowHighlights();
    }

    async invShiftRows(operationName) {
        this.updateCurrentOperation(operationName);
        this.updateOperationDetails('Shifting rows cyclically right...');
        
        const newState = Array(4).fill().map(() => Array(4).fill(0));
        
        for (let row = 0; row < 4; row++) {
            this.highlightRow(row);
            
            for (let col = 0; col < 4; col++) {
                const newCol = (col + row) % 4;
                newState[row][newCol] = this.state[row][col];
            }
            
            await this.animateRowShift(row, -row);
            await this.delay(this.animationSpeed / 4);
        }
        
        this.state = newState;
        this.updateStateMatrix();
        this.addToHistory('InvShiftRows', this.copyState());
        this.clearRowHighlights();
    }

    async mixColumns(operationName) {
        this.updateCurrentOperation(operationName);
        this.updateOperationDetails('Mixing columns using finite field arithmetic...');
        
        const newState = Array(4).fill().map(() => Array(4).fill(0));
        
        for (let col = 0; col < 4; col++) {
            this.highlightColumn(col);
            
            for (let row = 0; row < 4; row++) {
                newState[row][col] = 0;
                for (let k = 0; k < 4; k++) {
                    newState[row][col] ^= this.galoisMultiply(this.mixMatrix[row][k], this.state[k][col]);
                }
            }
            
            await this.animateColumnMix(col);
            await this.delay(this.animationSpeed / 4);
        }
        
        this.state = newState;
        this.updateStateMatrix();
        this.addToHistory('MixColumns', this.copyState());
        this.clearColumnHighlights();
    }

    async invMixColumns(operationName) {
        this.updateCurrentOperation(operationName);
        this.updateOperationDetails('Inverse mixing columns using finite field arithmetic...');
        
        const newState = Array(4).fill().map(() => Array(4).fill(0));
        
        for (let col = 0; col < 4; col++) {
            this.highlightColumn(col);
            
            for (let row = 0; row < 4; row++) {
                newState[row][col] = 0;
                for (let k = 0; k < 4; k++) {
                    newState[row][col] ^= this.galoisMultiply(this.invMixMatrix[row][k], this.state[k][col]);
                }
            }
            
            await this.animateColumnMix(col);
            await this.delay(this.animationSpeed / 4);
        }
        
        this.state = newState;
        this.updateStateMatrix();
        this.addToHistory('InvMixColumns', this.copyState());
        this.clearColumnHighlights();
    }

    async addRoundKey(round, operationName) {
        this.updateCurrentOperation(operationName);
        this.updateOperationDetails(`XORing state with round ${round} key...`);
        
        const roundKey = this.getRoundKey(round);
        this.updateKeyDisplay(roundKey);
        
        for (let i = 0; i < 4; i++) {
            for (let j = 0; j < 4; j++) {
                if (this.isPaused) await this.waitForResume();
                
                const oldValue = this.state[i][j];
                const keyValue = roundKey[i][j];
                const newValue = oldValue ^ keyValue;
                
                await this.animateCellChange(i, j, oldValue, newValue);
                this.state[i][j] = newValue;
            }
        }
        
        this.updateStateMatrix();
        this.addToHistory(`AddRoundKey Round ${round}`, this.copyState());
        this.highlightKeyRound(round);
    }

    // Helper Functions
    galoisMultiply(a, b) {
        let p = 0;
        let hiBitSet;
        
        for (let i = 0; i < 8; i++) {
            if (b & 1) {
                p ^= a;
            }
            
            hiBitSet = a & 0x80;
            a <<= 1;
            
            if (hiBitSet) {
                a ^= 0x1b;
            }
            
            b >>= 1;
        }
        
        return p & 0xFF;
    }

    getRoundKey(round) {
        const roundKey = Array(4).fill().map(() => Array(4).fill(0));
        
        for (let i = 0; i < 4; i++) {
            for (let j = 0; j < 4; j++) {
                const wordIndex = round * 4 + j;
                if (wordIndex < this.keySchedule.length) {
                    roundKey[i][j] = this.keySchedule[wordIndex][i];
                }
            }
        }
        
        return roundKey;
    }

    // Animation Functions
    async animateCellChange(row, col, oldValue, newValue) {
        const cell = document.getElementById(`state${row}${col}`);
        if (!cell) return;
        
        cell.classList.add('processing');
        cell.textContent = oldValue.toString(16).padStart(2, '0').toUpperCase();
        
        await this.delay(this.animationSpeed / 8);
        
        cell.textContent = newValue.toString(16).padStart(2, '0').toUpperCase();
        cell.classList.remove('processing');
        cell.classList.add('changed');
        
        await this.delay(this.animationSpeed / 8);
        
        cell.classList.remove('changed');
    }

    async animateRowShift(row, shiftAmount) {
        for (let col = 0; col < 4; col++) {
            const cell = document.getElementById(`state${row}${col}`);
            if (cell) {
                cell.classList.add('processing');
            }
        }
        
        await this.delay(this.animationSpeed / 2);
        
        for (let col = 0; col < 4; col++) {
            const cell = document.getElementById(`state${row}${col}`);
            if (cell) {
                cell.classList.remove('processing');
            }
        }
    }

    async animateColumnMix(col) {
        for (let row = 0; row < 4; row++) {
            const cell = document.getElementById(`state${row}${col}`);
            if (cell) {
                cell.classList.add('processing');
            }
        }
        
        await this.delay(this.animationSpeed / 2);
        
        for (let row = 0; row < 4; row++) {
            const cell = document.getElementById(`state${row}${col}`);
            if (cell) {
                cell.classList.remove('processing');
            }
        }
    }

    // Highlighting Functions
    highlightRow(row) {
        for (let col = 0; col < 4; col++) {
            const cell = document.getElementById(`state${row}${col}`);
            if (cell) {
                cell.classList.add('highlighted');
            }
        }
    }

    highlightColumn(col) {
        for (let row = 0; row < 4; row++) {
            const cell = document.getElementById(`state${row}${col}`);
            if (cell) {
                cell.classList.add('highlighted');
            }
        }
    }

    clearRowHighlights() {
        for (let row = 0; row < 4; row++) {
            for (let col = 0; col < 4; col++) {
                const cell = document.getElementById(`state${row}${col}`);
                if (cell) {
                    cell.classList.remove('highlighted');
                }
            }
        }
    }

    clearColumnHighlights() {
        this.clearRowHighlights();
    }

    highlightSBoxLookup(inputValue, outputValue) {
        const inputCell = document.getElementById(`sbox-${inputValue}`);
        if (inputCell) {
            inputCell.classList.add('lookup');
        }
    }

    clearSBoxHighlights() {
        const cells = document.querySelectorAll('.sbox-cell');
        cells.forEach(cell => {
            cell.classList.remove('lookup');
        });
    }

    highlightKeyRound(round) {
        const roundElement = document.getElementById(`keyRound-${round}`);
        if (roundElement) {
            roundElement.classList.add('active');
            
            setTimeout(() => {
                roundElement.classList.remove('active');
            }, this.animationSpeed);
        }
    }

    // Display Update Functions
    updateStateMatrix() {
        for (let i = 0; i < 4; i++) {
            for (let j = 0; j < 4; j++) {
                const cell = document.getElementById(`state${i}${j}`);
                if (cell) {
                    cell.textContent = this.state[i][j].toString(16).padStart(2, '0').toUpperCase();
                }
            }
        }
    }

    updateKeyDisplay(key = null) {
        const displayKey = key || this.getRoundKey(this.currentRound);
        
        for (let i = 0; i < 4; i++) {
            for (let j = 0; j < 4; j++) {
                const cell = document.getElementById(`key${i}${j}`);
                if (cell) {
                    cell.textContent = displayKey[i][j].toString(16).padStart(2, '0').toUpperCase();
                }
            }
        }
    }

    updateKeyScheduleDisplay() {
        for (let round = 0; round <= this.totalRounds; round++) {
            const roundKey = this.getRoundKey(round);
            
            for (let i = 0; i < 16; i++) {
                const row = i % 4;
                const col = Math.floor(i / 4);
                const cell = document.getElementById(`keyByte-${round}-${i}`);
                
                if (cell) {
                    cell.textContent = roundKey[row][col].toString(16).padStart(2, '0').toUpperCase();
                }
            }
        }
    }

    updateRoundDisplay() {
        document.getElementById('currentRound').textContent = this.currentRound;
        this.updateProgressBar();
    }

    updateProgressBar() {
        const progress = (this.currentRound / this.totalRounds) * 100;
        document.getElementById('progressBar').style.width = `${progress}%`;
    }

    updateOperationDisplay() {
        const mode = this.isEncrypting ? 'Encryption' : 'Decryption';
        document.getElementById('operationMode').textContent = mode;
    }

    updateCurrentOperation(operation) {
        document.getElementById('currentOperation').textContent = operation;
    }

    updateOperationDetails(details) {
        document.getElementById('operationDetails').textContent = details;
    }

    updateControls() {
        const startBtn = document.getElementById('startBtn');
        const stepBtn = document.getElementById('stepBtn');
        const resetBtn = document.getElementById('resetBtn');
        const pauseBtn = document.getElementById('pauseBtn');
        const playBtn = document.getElementById('playBtn');
        
        startBtn.disabled = this.isRunning;
        stepBtn.disabled = this.isRunning;
        resetBtn.disabled = false;
        
        if (pauseBtn) {
            pauseBtn.style.display = this.isRunning && !this.isPaused ? 'inline-block' : 'none';
        }
        
        if (playBtn) {
            playBtn.style.display = this.isRunning && this.isPaused ? 'inline-block' : 'none';
        }
    }

    updateOutput() {
        let output = '';
        for (let j = 0; j < 4; j++) {
            for (let i = 0; i < 4; i++) {
                output += this.state[i][j].toString(16).padStart(2, '0').toUpperCase();
            }
        }
        
        document.getElementById('output').textContent = output;
        this.updateBinaryOutput(output);
    }

    updateBinaryOutput(hexString) {
        let binary = '';
        for (let i = 0; i < hexString.length; i += 2) {
            const byte = parseInt(hexString.substr(i, 2), 16);
            binary += byte.toString(2).padStart(8, '0') + ' ';
        }
        
        document.getElementById('binaryOutput').textContent = binary;
    }

    // Control Functions
    async nextStep() {
        if (this.currentStep < this.stepHistory.length - 1) {
            this.currentStep++;
            this.state = this.copyState(this.stepHistory[this.currentStep].state);
            this.updateStateMatrix();
            this.updateRoundDisplay();
        }
    }

    pauseSimulation() {
        this.isPaused = true;
        this.updateControls();
    }

    playSimulation() {
        this.isPaused = false;
        this.updateControls();
    }

    resetSimulation() {
        this.isRunning = false;
        this.isPaused = false;
        this.currentRound = 0;
        this.currentStep = 0;
        this.stepHistory = [];
        this.state = Array(4).fill().map(() => Array(4).fill(0));
        
        this.updateStateMatrix();
        this.updateRoundDisplay();
        this.updateControls();
        this.updateCurrentOperation('Ready to start...');
        this.updateOperationDetails('Click "Start Simulation" to begin the AES encryption/decryption process.');
        
        document.getElementById('output').textContent = '0000000000000000000000000000000000000000000000000000000000000000';
        document.getElementById('binaryOutput').textContent = '';
        
        this.clearSBoxHighlights();
        this.clearRowHighlights();
    }

    // Utility Functions
    copyState(state = null) {
        const sourceState = state || this.state;
        return sourceState.map(row => [...row]);
    }

    addToHistory(operation, state) {
        this.stepHistory.push({
            operation: operation,
            state: this.copyState(state)
        });
    }

    async delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    showMessage(message, type = 'info') {
        const messageContainer = document.getElementById('messageContainer');
        if (!messageContainer) return;
        
        const messageElement = document.createElement('div');
        messageElement.className = `message ${type}-message`;
        messageElement.textContent = message;
        
        messageContainer.appendChild(messageElement);
        
        setTimeout(() => {
            messageElement.remove();
        }, 5000);
    }

    showError(message) {
        this.showMessage(message, 'error');
    }
}

// Initialize the simulation when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new AESSimulation();
});
