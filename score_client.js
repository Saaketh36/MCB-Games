(function () {
    const API_ROOT = (location.port === '5000' ? '' : 'http://127.0.0.1:5000') + '/api';
    const params = new URLSearchParams(location.search);
    const assignmentId = params.get('aid');
    const hasStudent = !!(params.get('student') && params.get('roll'));
    const cfg = typeof gameConfig !== 'undefined' ? gameConfig : {};

    function banner(text, kind) {
        let bar = document.getElementById('scoreBanner');
        if (!bar) {
            bar = document.createElement('div');
            bar.id = 'scoreBanner';
            bar.style.cssText = 'padding:12px;text-align:center;font-weight:bold;font-family:Arial,sans-serif;position:sticky;top:0;z-index:999;';
            document.body.insertBefore(bar, document.body.firstChild);
        }
        bar.textContent = text;
        bar.style.background = kind === 'error' ? '#f8d7da' : '#fff3cd';
        bar.style.color = kind === 'error' ? '#721c24' : '#856404';
    }

    function showStatus(text, ok, retry) {
        const card = document.querySelector('#resultsScreen .game-card');
        if (!card) return;
        let el = document.getElementById('saveStatus');
        if (!el) {
            el = document.createElement('div');
            el.id = 'saveStatus';
            el.style.cssText = 'margin-top:15px;padding:12px;border-radius:8px;font-weight:bold;text-align:center;';
            card.appendChild(el);
        }
        el.textContent = text;
        el.style.background = ok ? '#d4edda' : '#fff3cd';
        el.style.color = ok ? '#155724' : '#856404';
        if (retry) {
            const btn = document.createElement('button');
            btn.textContent = 'Retry saving';
            btn.style.cssText = 'display:block;margin:10px auto 0;padding:8px 20px;border:none;border-radius:6px;background:#667eea;color:#fff;font-weight:bold;cursor:pointer;';
            btn.onclick = saveScore;
            el.appendChild(btn);
        }
    }

    function backToAssignments() {
        const btn = document.querySelector('.restart-btn');
        if (!btn) return;
        btn.textContent = 'Back to My Assignments';
        btn.onclick = function () { location.href = 'index.html'; };
    }

    // A completed assignment can't be opened or replayed (the server decides).
    async function guardCompleted() {
        if (!assignmentId) return;
        try {
            const res = await fetch(API_ROOT + '/portal/assignments/' + encodeURIComponent(assignmentId), { cache: 'no-store' });
            if (res.status === 404) { banner('This assignment no longer exists. Scores for this attempt will not be recorded.', 'error'); return; }
            const body = await res.json();
            const a = body.assignment;
            if (a && a.status === 'completed') {
                alert('This game is already completed (' + a.score + '/' + a.max_score + ' points).');
                location.replace('index.html');
            }
        } catch (e) {
            banner('Cannot reach the server. Start it with: python app.py. Your score cannot be saved until it is running.', 'error');
        }
    }

    function buildPayload() {
        const responses = quizData.questions.map(q => ({
            question_id: q.id,
            user_answer: (typeof userAnswers !== 'undefined' && userAnswers[q.id]) || '',
            correct_answer: q.correct
        }));
        if (assignmentId) return { assignment_id: Number(assignmentId), responses: responses };
        return {
            student: params.get('student'), roll: params.get('roll'),
            class: params.get('class') || cfg.class, subject: params.get('subject'),
            skill: params.get('skill') || cfg.skill, game: params.get('game') || cfg.title,
            file: location.pathname.split('/').pop(), responses: responses
        };
    }

    async function saveScore() {
        if (!assignmentId && !hasStudent) {
            showStatus('Not recorded: practice mode. Start the game from an assignment (index.html, Student tab, PLAY) to record scores.', false);
            return;
        }
        try {
            const res = await fetch(API_ROOT + '/scoring/submit-by-name', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(buildPayload())
            });
            const body = await res.json();
            if (res.ok && body.status === 'success') {
                const d = body.score_data;
                showStatus('Completed. Score saved: ' + d.score + '/' + d.max_score + ' points (' + Math.round(d.percentage) + '%).', true);
            } else if (res.status === 409) {
                showStatus('This assignment was already completed earlier, so this attempt was not counted.', false);
            } else {
                showStatus('The score was NOT saved: ' + (body.message || res.status), false, true);
            }
        } catch (e) {
            showStatus('The score was NOT saved: server not reachable (start it with python app.py).', false, true);
        }
    }

    if (!assignmentId && !hasStudent) {
        banner('Practice mode: this attempt will NOT be recorded. To get a recorded score, open index.html, choose Student, and press PLAY on the assignment.', 'warn');
    }
    guardCompleted();

    if (typeof showResults === 'function' && typeof quizData !== 'undefined') {
        const original = showResults;
        window.showResults = function () {
            original.apply(this, arguments);
            backToAssignments();
            saveScore();
        };
    }
})();
