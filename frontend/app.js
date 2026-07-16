document.getElementById('scan-btn').addEventListener('click', async () => {
    const promptInput = document.getElementById('prompt-input');
    const promptText = promptInput.value.trim();

    // Elements to update
    const idleState = document.getElementById('idle-state');
    const resultDetails = document.getElementById('result-details');
    const resultCard = document.getElementById('result-card');
    const statusBadge = document.getElementById('status-badge');
    const riskScoreText = document.getElementById('risk-score-text');
    const riskBar = document.getElementById('risk-bar');
    const patternsList = document.getElementById('patterns-list');
    const resultFooter = document.getElementById('result-footer');
    const scanBtn = document.getElementById('scan-btn');

    if (!promptText) {
        alert("Please enter a prompt to scan!");
        return;
    }

    // Set Loading State on Button
    scanBtn.disabled = true;
    scanBtn.innerHTML = "⏳ Scanning...";

    try {
        // Send request to your FastAPI container running on localhost:8000
        const response = await fetch('http://localhost:8000/api/v1/shield/scan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ prompt: promptText })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const result = await response.json();

        // Reveal the results UI
        idleState.classList.add('hidden');
        resultDetails.classList.remove('hidden');
        resultFooter.classList.remove('hidden');

        // Update status UI based on threat level
        if (result.safe) {
            // Clean/Safe Prompt
            resultCard.className = "bg-gray-900 border border-emerald-950 rounded-xl p-6 min-h-[290px] flex flex-col justify-between shadow-[0_0_15px_rgba(16,185,129,0.15)] transition-all duration-300";
            statusBadge.className = "px-2.5 py-1 text-xs font-bold rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20";
            statusBadge.textContent = "🛡️ SECURE PROMPT";
            riskBar.className = "h-full bg-emerald-500 transition-all duration-500";
        } else {
            // Malicious Injection Detected!
            resultCard.className = "bg-gray-900 border border-rose-950 rounded-xl p-6 min-h-[290px] flex flex-col justify-between shadow-[0_0_20px_rgba(244,63,94,0.2)] transition-all duration-300";
            statusBadge.className = "px-2.5 py-1 text-xs font-bold rounded-full bg-rose-500/10 text-rose-400 border border-rose-500/20";
            statusBadge.textContent = "🚨 THREAT DETECTED";
            riskBar.className = "h-full bg-rose-500 transition-all duration-500";
        }

        // Update risk score
        riskScoreText.textContent = result.risk_score;
        riskBar.style.width = `${result.risk_score * 100}%`;

        // Update matched patterns list
        patternsList.innerHTML = '';
        if (result.matched_patterns.length === 0) {
            const noMatch = document.createElement('span');
            noMatch.className = "text-xs text-gray-500 italic";
            noMatch.textContent = "None matched (Heuristics clean)";
            patternsList.appendChild(noMatch);
        } else {
            result.matched_patterns.forEach(pattern => {
                const badge = document.createElement('span');
                badge.className = "px-2 py-0.5 text-xs rounded bg-gray-800 border border-gray-700 font-mono text-cyan-400";
                badge.textContent = pattern;
                patternsList.appendChild(badge);
            });
        }

    } catch (error) {
        console.error('Error scanning prompt:', error);
        alert('Could not connect to LLM Shield backend. Make sure your Docker container is running!');
    } finally {
        // Reset Button
        scanBtn.disabled = false;
        scanBtn.innerHTML = "⚡ Scan Prompt";
    }
});