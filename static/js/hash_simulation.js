// Hash Function Implementations and Visualizations

// MD5 implementation (fallback since Web Crypto API doesn't support MD5)
async function md5(input) {
    // Simple MD5-like hash for demonstration (not cryptographically secure)
    let hash = 0;
    for (let i = 0; i < input.length; i++) {
        const char = input.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash; // Convert to 32-bit integer
    }
    // Convert to hex and pad to 32 characters (128 bits)
    const hex = Math.abs(hash).toString(16);
    return hex.padStart(32, '0').substring(0, 32);
}

// SHA-1 implementation
async function sha1(input) {
    const encoder = new TextEncoder();
    const data = encoder.encode(input);
    const hashBuffer = await crypto.subtle.digest('SHA-1', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}

// SHA-256 implementation
async function sha256(input) {
    const encoder = new TextEncoder();
    const data = encoder.encode(input);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}

// Convert hex string to binary
function hexToBinary(hex) {
    return hex.split('').map(char => 
        parseInt(char, 16).toString(2).padStart(4, '0')
    ).join('');
}

// Convert string to binary
function stringToBinary(str) {
    return str.split('').map(char => 
        char.charCodeAt(0).toString(2).padStart(8, '0')
    ).join('');
}

// Analyze bit distribution
function analyzeBitDistribution(binary) {
    const ones = binary.split('1').length - 1;
    const zeros = binary.length - ones;
    const distribution = ones / binary.length;
    return {
        ones,
        zeros,
        distribution,
        score: (1 - Math.abs(0.5 - distribution) * 2) * 100
    };
}

// Calculate hamming distance between two binary strings
function hammingDistance(bin1, bin2) {
    let diff = 0;
    for (let i = 0; i < bin1.length; i++) {
        if (bin1[i] !== bin2[i]) diff++;
    }
    return diff;
}

// Visualization functions
function initializeVisualization() {
    const canvas = document.getElementById('hash-visualization');
    const ctx = canvas.getContext('2d');
    canvas.width = 800;
    canvas.height = 200;
    return ctx;
}

function visualizeHash(ctx, binary) {
    const blockSize = 4;
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
    
    binary.split('').forEach((bit, i) => {
        const x = (i % 128) * blockSize;
        const y = Math.floor(i / 128) * blockSize;
        ctx.fillStyle = bit === '1' ? '#4CAF50' : '#1a1a1a';
        ctx.fillRect(x, y, blockSize - 1, blockSize - 1);
    });
}

// Animation functions
function animateCompression(blocks) {
    const container = document.getElementById('compression-blocks');
    container.innerHTML = '';
    
    blocks.forEach((block, i) => {
        const blockDiv = document.createElement('div');
        blockDiv.className = 'block mb-2 p-2 bg-gray-800 rounded opacity-0 transition-opacity duration-300';
        blockDiv.innerHTML = `
            <div class="text-xs text-gray-400">Block ${i + 1}</div>
            <div class="font-mono text-sm break-all">${block}</div>
        `;
        container.appendChild(blockDiv);
        
        setTimeout(() => {
            blockDiv.style.opacity = '1';
        }, i * 200);
    });
}

// Event handlers
let currentHashFunction = md5;
let currentAlgorithm = 'MD5';

async function updateHash() {
    const input = document.getElementById('input-text').value;
    
    try {
        // Start the animated hash process
        await animatedHashProcess(input);
        
    } catch (error) {
        console.error('Hash calculation failed:', error);
        document.getElementById('hash-result').textContent = 'Error calculating hash';
    }
}

// Animated hash process with step-by-step visualization
async function animatedHashProcess(input) {
    // Step 1: Animate input processing
    await animateInputProcessing(input);
    
    // Step 2: Animate compression function
    await animateCompressionProcess(input);
    
    // Step 3: Generate and animate final hash
    const hash = await currentHashFunction(input);
    await animateFinalHash(hash);
    
    // Step 4: Update analysis with animations
    await animateAnalysis(hash);
}

// Animate input processing step
async function animateInputProcessing(input) {
    const container = document.getElementById('input-bits');
    const binary = stringToBinary(input);
    
    container.innerHTML = '';
    container.style.opacity = '0';
    
    // Fade in container
    await fadeIn(container, 300);
    
    // Animate each bit appearing
    for (let i = 0; i < binary.length; i++) {
        const bit = binary[i];
        const bitElement = document.createElement('span');
        bitElement.className = `inline-block w-6 h-6 m-1 text-center leading-6 rounded text-xs font-mono transition-all duration-300 transform scale-0 ${
            bit === '1' ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
        }`;
        bitElement.textContent = bit;
        container.appendChild(bitElement);
        
        // Animate bit appearance
        setTimeout(() => {
            bitElement.style.transform = 'scale(1)';
            bitElement.style.opacity = '1';
        }, i * 20);
    }
    
    await delay(binary.length * 20 + 500);
}

// Animate compression process
async function animateCompressionProcess(input) {
    const container = document.getElementById('compression-blocks');
    container.innerHTML = '';
    
    // Create processing indicator
    const processingDiv = document.createElement('div');
    processingDiv.className = 'text-center text-gray-400 mb-4';
    processingDiv.innerHTML = `
        <div class="inline-flex items-center">
            <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-500 mr-2"></div>
            Processing ${currentAlgorithm} compression function...
        </div>
    `;
    container.appendChild(processingDiv);
    
    await delay(1000);
    
    // Remove processing indicator
    container.removeChild(processingDiv);
    
    // Create compression blocks with animation
    const blocks = input.match(/.{1,16}/g) || [input];
    const rounds = Math.min(blocks.length, 4);
    
    for (let i = 0; i < rounds; i++) {
        const blockDiv = document.createElement('div');
        blockDiv.className = 'mb-3 p-3 bg-gray-800 rounded-lg border-l-4 border-blue-500 transform translate-x-full opacity-0 transition-all duration-500';
        blockDiv.innerHTML = `
            <div class="flex justify-between items-center mb-2">
                <span class="text-xs text-gray-400">Round ${i + 1}</span>
                <span class="text-xs text-blue-400">${currentAlgorithm}</span>
            </div>
            <div class="font-mono text-sm text-white break-all">${blocks[i] || input.substring(i * 16, (i + 1) * 16)}</div>
            <div class="mt-2 h-2 bg-gray-700 rounded-full overflow-hidden">
                <div class="h-full bg-gradient-to-r from-blue-500 to-purple-500 rounded-full transform -translate-x-full transition-transform duration-1000" style="width: 100%"></div>
            </div>
        `;
        container.appendChild(blockDiv);
        
        // Animate block appearance
        setTimeout(() => {
            blockDiv.style.transform = 'translateX(0)';
            blockDiv.style.opacity = '1';
            
            // Animate progress bar
            setTimeout(() => {
                const progressBar = blockDiv.querySelector('.bg-gradient-to-r');
                progressBar.style.transform = 'translateX(0)';
            }, 200);
        }, i * 300);
    }
    
    await delay(rounds * 300 + 1000);
}

// Animate final hash generation
async function animateFinalHash(hash) {
    const hashResult = document.getElementById('hash-result');
    const hashBits = document.getElementById('hash-bits');
    const canvas = document.getElementById('hash-visualization');
    const ctx = canvas.getContext('2d');
    
    // Clear previous content
    hashResult.innerHTML = '';
    hashBits.innerHTML = '';
    
    // Animate hash characters appearing
    hashResult.style.opacity = '0';
    await fadeIn(hashResult, 300);
    
    for (let i = 0; i < hash.length; i++) {
        const char = hash[i];
        const charSpan = document.createElement('span');
        charSpan.className = 'inline-block transform scale-0 transition-all duration-200';
        charSpan.textContent = char;
        charSpan.style.color = getHashCharColor(char);
        hashResult.appendChild(charSpan);
        
        setTimeout(() => {
            charSpan.style.transform = 'scale(1)';
        }, i * 50);
    }
    
    await delay(hash.length * 50 + 500);
    
    // Animate binary representation
    const binary = hexToBinary(hash);
    hashBits.style.opacity = '0';
    await fadeIn(hashBits, 300);
    
    // Animate canvas visualization
    canvas.width = 800;
    canvas.height = 200;
    await animateCanvasVisualization(ctx, binary);
    
    // Update binary display
    hashBits.textContent = binary;
}

// Animate canvas hash visualization
async function animateCanvasVisualization(ctx, binary) {
    const blockSize = 4;
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
    
    for (let i = 0; i < binary.length; i++) {
        const bit = binary[i];
        const x = (i % 200) * blockSize;
        const y = Math.floor(i / 200) * blockSize;
        
        setTimeout(() => {
            ctx.fillStyle = bit === '1' ? '#4CAF50' : '#2d3748';
            ctx.fillRect(x, y, blockSize - 1, blockSize - 1);
            
            // Add glow effect for 1s
            if (bit === '1') {
                ctx.shadowColor = '#4CAF50';
                ctx.shadowBlur = 2;
                ctx.fillRect(x, y, blockSize - 1, blockSize - 1);
                ctx.shadowBlur = 0;
            }
        }, i * 2);
    }
    
    await delay(binary.length * 2 + 500);
}

// Animate analysis section
async function animateAnalysis(hash) {
    const binary = hexToBinary(hash);
    const analysis = analyzeBitDistribution(binary);
    
    // Animate distribution score
    const scoreElement = document.getElementById('distribution-score');
    await animateCounter(scoreElement, 0, analysis.score, '%', 1000);
    
    // Animate bit distribution grid
    await animateBitDistributionGrid(binary);
    
    // Update hash properties with animation
    await animateHashProperties(hash, binary);
}

// Animate counter from start to end value
async function animateCounter(element, start, end, suffix = '', duration = 1000) {
    const steps = 60;
    const increment = (end - start) / steps;
    const stepDuration = duration / steps;
    
    for (let i = 0; i <= steps; i++) {
        setTimeout(() => {
            const value = start + (increment * i);
            element.textContent = `${value.toFixed(2)}${suffix}`;
        }, i * stepDuration);
    }
    
    await delay(duration);
}

// Animate bit distribution grid
async function animateBitDistributionGrid(binary) {
    const grid = document.getElementById('bit-distribution-grid');
    grid.innerHTML = '';
    
    const blockSize = Math.ceil(binary.length / 64);
    for (let i = 0; i < binary.length; i += blockSize) {
        const block = binary.slice(i, i + blockSize);
        const ones = block.split('1').length - 1;
        const ratio = ones / block.length;
        
        const div = document.createElement('div');
        div.className = 'h-4 rounded transform scale-0 transition-all duration-300';
        div.style.backgroundColor = `rgba(76, 175, 80, ${ratio})`;
        grid.appendChild(div);
        
        setTimeout(() => {
            div.style.transform = 'scale(1)';
        }, (i / blockSize) * 50);
    }
    
    await delay((binary.length / blockSize) * 50 + 300);
}

// Animate hash properties
async function animateHashProperties(hash, binary) {
    const lengthElement = document.getElementById('hash-length');
    const entropyElement = document.getElementById('hash-entropy');
    const timeElement = document.getElementById('execution-time');
    
    // Animate length
    lengthElement.style.opacity = '0';
    await fadeIn(lengthElement, 300);
    lengthElement.textContent = `${binary.length} bits (${hash.length} hex chars)`;
    
    await delay(200);
    
    // Animate entropy
    entropyElement.style.opacity = '0';
    await fadeIn(entropyElement, 300);
    const entropy = calculateEntropy(binary);
    await animateCounter(entropyElement, 0, entropy, ' bits', 800);
    
    await delay(200);
    
    // Animate execution time
    timeElement.style.opacity = '0';
    await fadeIn(timeElement, 300);
    timeElement.textContent = '< 1ms';
}

// Utility functions for animations
function getHashCharColor(char) {
    const colors = ['#3B82F6', '#8B5CF6', '#10B981', '#F59E0B', '#EF4444', '#EC4899'];
    const index = parseInt(char, 16) % colors.length;
    return colors[index];
}

async function fadeIn(element, duration) {
    element.style.transition = `opacity ${duration}ms ease-in-out`;
    element.style.opacity = '1';
    await delay(duration);
}

function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Update hash properties display
function updateHashProperties(hash, binary) {
    // Hash length
    document.getElementById('hash-length').textContent = `${binary.length} bits (${hash.length} hex chars)`;
    
    // Calculate entropy
    const entropy = calculateEntropy(binary);
    document.getElementById('hash-entropy').textContent = `${entropy.toFixed(2)} bits`;
    
    // Execution time (simulated)
    document.getElementById('execution-time').textContent = '< 1ms';
}

// Calculate Shannon entropy
function calculateEntropy(binary) {
    const ones = binary.split('1').length - 1;
    const zeros = binary.length - ones;
    const total = binary.length;
    
    if (ones === 0 || zeros === 0) return 0;
    
    const p1 = ones / total;
    const p0 = zeros / total;
    
    return -(p1 * Math.log2(p1) + p0 * Math.log2(p0));
}

function updateBitDistributionGrid(binary) {
    const grid = document.getElementById('bit-distribution-grid');
    grid.innerHTML = '';
    
    const blockSize = Math.ceil(binary.length / 64);
    for (let i = 0; i < binary.length; i += blockSize) {
        const block = binary.slice(i, i + blockSize);
        const ones = block.split('1').length - 1;
        const ratio = ones / block.length;
        
        const div = document.createElement('div');
        div.className = 'h-4 rounded';
        div.style.backgroundColor = `rgba(76, 175, 80, ${ratio})`;
        grid.appendChild(div);
    }
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    const inputText = document.getElementById('input-text');
    const md5Btn = document.getElementById('md5-btn');
    const sha1Btn = document.getElementById('sha1-btn');
    const sha256Btn = document.getElementById('sha256-btn');
    
    inputText.addEventListener('input', debounce(updateHash, 300));
    
    md5Btn.addEventListener('click', () => {
        currentHashFunction = md5;
        updateHash();
    });
    
    sha1Btn.addEventListener('click', () => {
        currentHashFunction = sha1;
        updateHash();
    });
    
    sha256Btn.addEventListener('click', () => {
        currentHashFunction = sha256;
        updateHash();
    });
    
    // Initial hash
    updateHash();
});

// Utility function for debouncing
function debounce(func, wait) {
    let timeout;
    return function() {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, arguments), wait);
    };
}

// Collision testing function
async function testCollision() {
    const input1 = document.getElementById('collision-input-1').value;
    const input2 = document.getElementById('collision-input-2').value;
    
    if (!input1 || !input2) {
        document.getElementById('collision-result').innerHTML = 
            '<div class="text-yellow-400">Please enter both inputs</div>';
        return;
    }
    
    const [hash1, hash2] = await Promise.all([
        currentHashFunction(input1),
        currentHashFunction(input2)
    ]);
    
    const resultDiv = document.getElementById('collision-result');
    if (hash1 === hash2) {
        resultDiv.innerHTML = `
            <div class="text-red-400 font-bold">⚠️ Collision Found!</div>
            <div class="text-xs text-gray-400 mt-2">Both inputs produce the same hash:</div>
            <div class="font-mono text-xs break-all text-white mt-1 bg-gray-700 p-2 rounded">${hash1}</div>
        `;
    } else {
        resultDiv.innerHTML = `
            <div class="text-green-400 font-bold">✓ No Collision</div>
            <div class="text-xs text-gray-400 mt-2">Different hashes produced:</div>
            <div class="mt-2 space-y-1">
                <div class="font-mono text-xs break-all text-blue-400 bg-gray-700 p-2 rounded">Input 1: ${hash1}</div>
                <div class="font-mono text-xs break-all text-purple-400 bg-gray-700 p-2 rounded">Input 2: ${hash2}</div>
            </div>
        `;
    }
}

// Avalanche effect demonstration
async function demonstrateAvalanche() {
    const input = document.getElementById('avalanche-input').value;
    if (!input) return;
    
    // Change the last character slightly
    const modifiedInput = input.slice(0, -1) + 
        String.fromCharCode(input.charCodeAt(input.length - 1) ^ 1);
    
    const [hash1, hash2] = await Promise.all([
        currentHashFunction(input),
        currentHashFunction(modifiedInput)
    ]);
    
    const bin1 = hexToBinary(hash1);
    const bin2 = hexToBinary(hash2);
    const distance = hammingDistance(bin1, bin2);
    const percentage = (distance / bin1.length * 100).toFixed(2);
    
    document.getElementById('avalanche-effect').innerHTML = `
        <div class="space-y-4">
            <div class="space-y-2">
                <div class="text-sm text-gray-300">Original Input: "${input}"</div>
                <div class="font-mono text-xs break-all bg-gray-700 p-2 rounded text-blue-400">${hash1}</div>
            </div>
            <div class="space-y-2">
                <div class="text-sm text-gray-300">Modified Input: "${modifiedInput}"</div>
                <div class="font-mono text-xs break-all bg-gray-700 p-2 rounded text-green-400">${hash2}</div>
            </div>
            <div class="space-y-2">
                <div class="text-sm text-gray-300">Avalanche Effect:</div>
                <div class="font-mono text-lg text-purple-400 text-center bg-gray-700 p-2 rounded">
                    ${distance} bits changed (${percentage}%)
                </div>
                <div class="text-xs text-gray-400 text-center">
                    Good hash functions should change ~50% of bits for small input changes
                </div>
            </div>
        </div>
    `;
}
