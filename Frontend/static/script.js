// DOM Elements
const codeInput = document.getElementById('code-input');
const languageSelect = document.getElementById('language-select');
const analyzeBtn = document.getElementById('analyze-btn');
const optimizeBtn = document.getElementById('optimize-btn');
const explainBtn = document.getElementById('explain-btn');
const refactorBtn = document.getElementById('refactor-btn');
const clearBtn = document.getElementById('clear-btn');
const progressSection = document.getElementById('progress-section');
const progressFill = document.getElementById('progress-fill');
const progressText = document.getElementById('progress-text');

// Tab elements
const tabBtns = document.querySelectorAll('.tab-btn');
const tabPanes = document.querySelectorAll('.tab-pane');

// State
let lastMetrics = null;

// Event Listeners
analyzeBtn.addEventListener('click', analyzeCode);
optimizeBtn.addEventListener('click', getOptimization);
explainBtn.addEventListener('click', explainCode);
refactorBtn.addEventListener('click', getRefactoring);
clearBtn.addEventListener('click', clearAll);

tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const tabName = btn.getAttribute('data-tab');
        switchTab(tabName);
    });
});

codeInput.addEventListener('input', () => {
    if (codeInput.value.trim()) {
        analyzeBtn.disabled = false;
    } else {
        analyzeBtn.disabled = true;
        optimizeBtn.disabled = true;
        explainBtn.disabled = true;
        refactorBtn.disabled = true;
    }
});

// Functions
async function analyzeCode() {
    const code = codeInput.value.trim();
    const language = languageSelect.value;

    if (!code) {
        showError('Please enter some code to analyze');
        return;
    }

    showProgress(true, 'Analyzing code...');

    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code, language })
        });

        const data = await response.json();

        if (!response.ok) {
            showError(`Analysis failed: ${data.error}`);
            return;
        }

        lastMetrics = data.metrics;
        displayMetrics(data.metrics);
        
        // Enable optimization buttons
        optimizeBtn.disabled = false;
        explainBtn.disabled = false;
        refactorBtn.disabled = false;

        switchTab('metrics');
        showSuccess('Code analysis completed successfully!');
    } catch (error) {
        showError(`Error: ${error.message}`);
    } finally {
        showProgress(false);
    }
}

function displayMetrics(metrics) {
    const loc = metrics.raw.loc || 0;
    const lloc = metrics.raw.lloc || 0;
    const complexity = metrics.avg_complexity || 1;
    const volume = metrics.halstead?.volume || 0;

    document.getElementById('loc').textContent = loc;
    document.getElementById('lloc').textContent = lloc;
    document.getElementById('complexity').textContent = complexity.toFixed(2);
    document.getElementById('volume').textContent = volume.toFixed(2);

    // Display detailed metrics
    const detailsDiv = document.getElementById('metrics-details');
    let html = '<h4>Detailed Metrics</h4>';
    
    if (metrics.raw) {
        html += `
            <p><strong>Comments:</strong> ${metrics.raw.comments}</p>
            <p><strong>Blank Lines:</strong> ${metrics.raw.blank}</p>
        `;
    }

    if (metrics.halstead) {
        html += `
            <h4>Halstead Metrics</h4>
            <p><strong>Difficulty:</strong> ${metrics.halstead.difficulty?.toFixed(2)}</p>
            <p><strong>Effort:</strong> ${metrics.halstead.effort?.toFixed(2)}</p>
            <p><strong>Time to Program:</strong> ${metrics.halstead.time_to_program?.toFixed(2)} minutes</p>
            <p><strong>Estimated Bugs:</strong> ${metrics.halstead.bugs?.toFixed(2)}</p>
        `;
    }

    detailsDiv.innerHTML = html;
}

async function getOptimization() {
    const code = codeInput.value.trim();
    const language = languageSelect.value;

    if (!code || !lastMetrics) {
        showError('Please analyze code first');
        return;
    }

    showProgress(true, 'Generating optimization suggestions...');
    switchTab('optimization');

    const contentDiv = document.getElementById('optimization-content');
    contentDiv.innerHTML = '<p>Processing optimization suggestions...</p>';

    try {
        const response = await fetch('/api/optimize/suggestions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code, metrics: lastMetrics, language })
        });

        if (!response.ok) {
            showError('Optimization failed');
            return;
        }

        // Handle streaming response
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let suggestions = '';

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value);
            const lines = chunk.split('\n');

            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    try {
                        const event = JSON.parse(line.substring(6));
                        
                        progressFill.style.width = event.progress + '%';
                        progressText.textContent = event.status;

                        if (event.content) {
                            suggestions = event.content;
                            contentDiv.innerHTML = formatContent(suggestions);
                        }
                    } catch (e) {
                        // Continue on parse error
                    }
                }
            }
        }

        showSuccess('Optimization suggestions generated!');
    } catch (error) {
        showError(`Error: ${error.message}`);
    } finally {
        showProgress(false);
    }
}

async function explainCode() {
    const code = codeInput.value.trim();
    const language = languageSelect.value;

    if (!code) {
        showError('Please enter code to explain');
        return;
    }

    showProgress(true, 'Generating code explanation...');
    switchTab('explanation');

    const contentDiv = document.getElementById('explanation-content');
    contentDiv.innerHTML = '<p>Analyzing code...</p>';

    try {
        const response = await fetch('/api/explain', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code, language })
        });

        const data = await response.json();

        if (!response.ok) {
            showError(`Explanation failed: ${data.error}`);
            return;
        }

        contentDiv.innerHTML = formatContent(data.explanation);
        showSuccess('Code explanation generated!');
    } catch (error) {
        showError(`Error: ${error.message}`);
    } finally {
        showProgress(false);
    }
}

async function getRefactoring() {
    const code = codeInput.value.trim();
    const language = languageSelect.value;

    if (!code || !lastMetrics) {
        showError('Please analyze code first');
        return;
    }

    showProgress(true, 'Generating refactoring suggestions...');
    switchTab('refactoring');

    const contentDiv = document.getElementById('refactoring-content');
    contentDiv.innerHTML = '<p>Analyzing refactoring opportunities...</p>';

    try {
        const response = await fetch('/api/optimize/refactoring', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code, metrics: lastMetrics, language })
        });

        if (!response.ok) {
            showError('Refactoring analysis failed');
            return;
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let suggestions = '';

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value);
            const lines = chunk.split('\n');

            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    try {
                        const event = JSON.parse(line.substring(6));
                        
                        progressFill.style.width = event.progress + '%';
                        progressText.textContent = event.status;

                        if (event.content) {
                            suggestions = event.content;
                            contentDiv.innerHTML = formatContent(suggestions);
                        }
                    } catch (e) {
                        // Continue on parse error
                    }
                }
            }
        }

        showSuccess('Refactoring suggestions generated!');
    } catch (error) {
        showError(`Error: ${error.message}`);
    } finally {
        showProgress(false);
    }
}

function switchTab(tabName) {
    tabBtns.forEach(btn => btn.classList.remove('active'));
    tabPanes.forEach(pane => pane.classList.remove('active'));

    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
    document.getElementById(tabName).classList.add('active');
}

function showProgress(show, message = 'Processing...') {
    if (show) {
        progressSection.style.display = 'block';
        progressText.textContent = message;
        progressFill.style.width = '0%';
    } else {
        progressSection.style.display = 'none';
    }
}

function showError(message) {
    const contentDiv = document.querySelector('.tab-pane.active .content-section') || 
                      document.querySelector('.tab-pane.active');
    if (contentDiv) {
        contentDiv.innerHTML = `<div class="error">❌ ${message}</div>`;
    }
    console.error(message);
}

function showSuccess(message) {
    console.log(message);
}

function formatContent(content) {
    if (!content) return '<p>No content available</p>';

    // Handle JSON objects
    if (typeof content === 'object') {
        content = JSON.stringify(content, null, 2);
    }

    // Convert plain text to formatted HTML
    return `<div><p>${content.replace(/\n/g, '<br>')}</p></div>`;
}

function clearAll() {
    codeInput.value = '';
    lastMetrics = null;
    analyzeBtn.disabled = true;
    optimizeBtn.disabled = true;
    explainBtn.disabled = true;
    refactorBtn.disabled = true;
    
    document.getElementById('metrics-details').innerHTML = '';
    document.getElementById('optimization-content').innerHTML = '';
    document.getElementById('explanation-content').innerHTML = '';
    document.getElementById('refactoring-content').innerHTML = '';
    
    ['loc', 'lloc', 'complexity', 'volume'].forEach(id => {
        document.getElementById(id).textContent = '-';
    });

    switchTab('metrics');
    codeInput.focus();
}

// Initialize
codeInput.addEventListener('paste', () => {
    setTimeout(() => {
        if (codeInput.value.trim()) {
            analyzeBtn.disabled = false;
        }
    }, 10);
});
