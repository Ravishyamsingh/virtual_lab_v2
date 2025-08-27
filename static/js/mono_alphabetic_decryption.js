// Global variables
let substitutionKey = {};
let alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    initializeSubstitution();
    setupEventListeners();
});

function initializeSubstitution() {
    generateRandomKey();
    displayAlphabets();
}

function generateRandomKey() {
    const shuffledAlphabet = [...alphabet];
    for (let i = shuffledAlphabet.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffledAlphabet[i], shuffledAlphabet[j]] = [shuffledAlphabet[j], shuffledAlphabet[i]];
    }
    alphabet.forEach((letter, index) => {
        substitutionKey[letter] = shuffledAlphabet[index];
    });
}

function displayAlphabets() {
    const originalDiv = document.getElementById('alphabet-original');
    const substitutionDiv = document.getElementById('alphabet-substitution');
    
    if (!originalDiv || !substitutionDiv) return;
    
    originalDiv.innerHTML = '';
    substitutionDiv.innerHTML = '';
    
    alphabet.forEach(letter => {
        // Original alphabet
        const originalLetter = document.createElement('div');
        originalLetter.className = 'letter-box';
        originalLetter.textContent = letter;
        originalDiv.appendChild(originalLetter);
        
        // Substitution alphabet
        const subLetter = document.createElement('div');
        subLetter.className = 'letter-box';
        subLetter.textContent = substitutionKey[letter];
        substitutionDiv.appendChild(subLetter);
    });
}

function setupEventListeners() {
    const inputText = document.getElementById('input-text');
    if (inputText) {
        inputText.addEventListener('input', handleTextInput);
    }
}

function handleTextInput(event) {
    const text = event.target.value.toUpperCase();
    const encrypted = encryptText(text);
    const resultDiv = document.getElementById('result');
    if (resultDiv) {
        resultDiv.textContent = encrypted;
    }
}

function encryptText(text) {
    return text.split('').map(char => {
        if (!/[A-Z]/.test(char)) return char;
        return substitutionKey[char] || char;
    }).join('');
}

function generateNewKey() {
    generateRandomKey();
    displayAlphabets();
    // Re-encrypt current text with new key
    const inputText = document.getElementById('input-text');
    if (inputText && inputText.value) {
        handleTextInput({ target: inputText });
    }
}

function setupEventListeners() {
    // Speed control
    const speedSlider = document.getElementById('speed-slider');
    if (speedSlider) {
        speedSlider.addEventListener('input', (e) => {
            state.animationSpeed = 1000 - parseInt(e.target.value);
        });
    }

    // Decrypt button
    const decryptBtn = document.getElementById('decrypt-button');
    if (decryptBtn) {
        decryptBtn.addEventListener('click', startDecryption);
    }

    // Ciphertext input
    const ciphertextInput = document.getElementById('ciphertext');
    if (ciphertextInput) {
        ciphertextInput.addEventListener('input', () => {
            if (!state.isAnimating) {
                const decryptionProgress = document.getElementById('decryption-progress');
                if (decryptionProgress) {
                    decryptionProgress.innerHTML = 'Type ciphertext and click "Start Decryption" to begin...';
                }
            }
        });
    }
}

function displayAlphabets(alphabet) {
    const cipherAlphabet = document.getElementById('cipher-alphabet');
    const plainAlphabet = document.getElementById('plain-alphabet');

    if (!cipherAlphabet || !plainAlphabet) return;

    // Clear existing content
    cipherAlphabet.innerHTML = '';
    plainAlphabet.innerHTML = '';

    // Create letter boxes
    alphabet.forEach(letter => {
        // Cipher letter box
        const cipherBox = createLetterBox(letter);
        cipherBox.addEventListener('click', () => selectCipherLetter(letter, cipherBox));
        cipherAlphabet.appendChild(cipherBox);

        // Plain letter box
        const plainBox = createLetterBox('_');
        plainBox.addEventListener('click', () => selectPlainLetter(letter, plainBox));
        plainAlphabet.appendChild(plainBox);
    });
}

function createLetterBox(letter) {
    const box = document.createElement('div');
    box.className = 'letter-box';
    box.textContent = letter;
    return box;
}

function selectCipherLetter(letter, element) {
    // Remove previous selection
    document.querySelectorAll('#cipher-alphabet .letter-box').forEach(box => {
        box.classList.remove('selected');
    });
    
    // Add new selection
    element.classList.add('selected');
    state.selectedCipher = letter;
}

function selectPlainLetter(letter, element) {
    if (!state.selectedCipher) return;

    // Update mapping
    state.substitutionMap[state.selectedCipher] = letter;
    
    // Update display
    document.querySelectorAll('#plain-alphabet .letter-box').forEach(box => {
        if (box === element) {
            box.textContent = letter;
            box.classList.add('mapped');
        }
    });

    // Clear selection
    document.querySelectorAll('#cipher-alphabet .letter-box').forEach(box => {
        box.classList.remove('selected');
    });
    state.selectedCipher = null;

    // Update decryption display
    updateDecryptionDisplay();
}

function updateDecryptionDisplay() {
    const ciphertext = document.getElementById('ciphertext').value.toUpperCase();
    const decryptionProgress = document.getElementById('decryption-progress');
    
    if (!decryptionProgress || !ciphertext) return;

    const decrypted = ciphertext.split('').map(char => {
        if (!/[A-Z]/.test(char)) return char;
        return state.substitutionMap[char] || '_';
    }).join('');

    decryptionProgress.textContent = decrypted;
}

async function startDecryption() {
    if (state.isAnimating) return;
    state.isAnimating = true;

    const ciphertext = document.getElementById('ciphertext').value.toUpperCase();
    const decryptionProgress = document.getElementById('decryption-progress');
    
    if (!decryptionProgress || !ciphertext) {
        state.isAnimating = false;
        return;
    }

    const letters = ciphertext.split('');
    let currentText = '';

    for (let i = 0; i < letters.length; i++) {
        const char = letters[i];
        if (/[A-Z]/.test(char)) {
            const decryptedChar = state.substitutionMap[char] || '_';
            currentText += decryptedChar;
        } else {
            currentText += char;
        }

        // Create animated display with highlighting
        const displayText = currentText.padEnd(ciphertext.length, '_');
        const html = displayText.split('').map((l, index) => {
            if (index === i) {
                return `<span class="bg-yellow-200 transition-colors duration-300">${l}</span>`;
            }
            return l;
        }).join('');

        decryptionProgress.innerHTML = html;
        await new Promise(resolve => setTimeout(resolve, state.animationSpeed));
    }

    state.isAnimating = false;
}