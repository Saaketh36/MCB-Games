/* ============================================================================
   LEARN THROUGH PLAY - PLATFORM ENGINE
   Exclusively grounded in the provided Learning Outcomes dataset.
   ============================================================================ */

(function (window) {
    'use strict';

    // State
    const LtpState = {
        activeTab: 'content', // 'content' | 'quizzes' | 'minigames' | 'results'
        selectedSubject: 'all',
        selectedClass: 'all',
        searchQuery: '',
        activeQuiz: null,
        quizStep: 0,
        quizAnswers: {},
        quizLocked: false,
        activeMiniGame: null,
        miniGameState: null,
        results: []
    };

    const STORAGE_KEY = 'mcb_ltp_results_v1';

    // Web Audio Synthesizer for Immediate Feedback
    let audioCtx = null;
    function playTone(freq, duration, type = 'sine', vol = 0.2, delay = 0) {
        try {
            audioCtx = audioCtx || new (window.AudioContext || window.webkitAudioContext)();
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = type;
            osc.frequency.value = freq;
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            const now = audioCtx.currentTime + delay;
            gain.gain.setValueAtTime(vol, now);
            gain.gain.exponentialRampToValueAtTime(0.001, now + duration);
            osc.start(now);
            osc.stop(now + duration);
        } catch (e) { }
    }

    const sound = {
        correct() {
            playTone(587, 0.12, 'sine', 0.2);
            playTone(880, 0.18, 'sine', 0.25, 0.1);
        },
        wrong() {
            playTone(220, 0.28, 'sawtooth', 0.18);
        },
        win() {
            [523, 659, 784, 1047].forEach((f, i) => playTone(f, 0.22, 'sine', 0.25, i * 0.12));
        }
    };

    function loadResults() {
        try {
            const raw = localStorage.getItem(STORAGE_KEY);
            LtpState.results = raw ? JSON.parse(raw) : [];
        } catch (e) {
            LtpState.results = [];
        }
    }

    function saveResult(entry) {
        try {
            LtpState.results.unshift(entry);
            if (LtpState.results.length > 50) LtpState.results.pop();
            localStorage.setItem(STORAGE_KEY, JSON.stringify(LtpState.results));
            updateHeroMetrics();
        } catch (e) { }
    }

    function updateHeroMetrics() {
        const outcomesCount = (window.LEARNING_OUTCOMES_DATA || []).length;
        const quizzesCount = (window.LTP_QUIZZES || []).length;
        const miniGamesCount = (window.LTP_MINI_GAMES || []).length;
        const completedCount = LtpState.results.length;

        const elOutcomes = document.getElementById('ltpHeroOutcomesCount');
        const elQuizzes = document.getElementById('ltpHeroQuizzesCount');
        const elMiniGames = document.getElementById('ltpHeroMiniGamesCount');
        const elCompleted = document.getElementById('ltpHeroCompletedCount');

        if (elOutcomes) elOutcomes.textContent = outcomesCount;
        if (elQuizzes) elQuizzes.textContent = quizzesCount;
        if (elMiniGames) elMiniGames.textContent = miniGamesCount;
        if (elCompleted) elCompleted.textContent = completedCount;
    }

    function switchLtpTab(tab) {
        LtpState.activeTab = tab;
        document.querySelectorAll('.ltp-tab-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.tab === tab);
        });

        const panelContent = document.getElementById('ltpTabPanelContent');
        const panelQuizzes = document.getElementById('ltpTabPanelQuizzes');
        const panelMiniGames = document.getElementById('ltpTabPanelMiniGames');
        const panelResults = document.getElementById('ltpTabPanelResults');

        if (panelContent) panelContent.style.display = tab === 'content' ? 'block' : 'none';
        if (panelQuizzes) panelQuizzes.style.display = tab === 'quizzes' ? 'block' : 'none';
        if (panelMiniGames) panelMiniGames.style.display = tab === 'minigames' ? 'block' : 'none';
        if (panelResults) panelResults.style.display = tab === 'results' ? 'block' : 'none';

        if (tab === 'content') renderLearningContent();
        else if (tab === 'quizzes') renderQuizzesView();
        else if (tab === 'minigames') renderMiniGamesView();
        else if (tab === 'results') renderResultsView();
    }

    // =========================================================================
    // 1. LEARNING CONTENT EXPLORER
    // =========================================================================
    function renderLearningContent() {
        const container = document.getElementById('ltpOutcomesList');
        const countBadge = document.getElementById('ltpOutcomesCountBadge');
        if (!container) return;

        const data = window.LEARNING_OUTCOMES_DATA || [];
        const query = (LtpState.searchQuery || '').toLowerCase().trim();

        const filtered = data.filter(item => {
            if (LtpState.selectedSubject !== 'all' && item.subject !== LtpState.selectedSubject) return false;
            if (LtpState.selectedClass !== 'all' && item.class !== LtpState.selectedClass) return false;
            if (query) {
                const matchId = String(item.id) === query;
                const matchOutcome = item.learningOutcome.toLowerCase().includes(query);
                const matchSkill = item.skillArea.toLowerCase().includes(query);
                const matchSubSkill = item.subSkillArea.toLowerCase().includes(query);
                if (!matchId && !matchOutcome && !matchSkill && !matchSubSkill) return false;
            }
            return true;
        });

        if (countBadge) {
            countBadge.textContent = `Showing ${filtered.length} of ${data.length} Outcomes`;
        }

        if (filtered.length === 0) {
            container.innerHTML = `
                <div style="grid-column: 1 / -1; padding: 48px; text-align: center; background: #ffffff; border-radius: 20px; border: 1.5px dashed #cbd5e1;">
                    <div style="font-size: 40px; margin-bottom: 8px;">🔍</div>
                    <h4 style="font-family: var(--font-heading); font-size: 18px; color: #1e1b4b; margin-bottom: 6px;">No learning outcomes match your search</h4>
                    <p style="color: #64748b; font-size: 14px; margin-bottom: 16px;">Try clearing filters or search term to explore all 440 curriculum outcomes.</p>
                    <button type="button" class="ltp-chip-btn active" onclick="window.resetLtpContentFilters()">Reset Filters ↺</button>
                </div>
            `;
            return;
        }

        const subjectBadgeClass = {
            'Mathematics': 'badge-sub-math',
            'English': 'badge-sub-eng',
            'EVS': 'badge-sub-evs',
            'Science': 'badge-sub-sci',
            'Social Science': 'badge-sub-soc'
        };

        container.innerHTML = filtered.map(item => {
            const badgeCls = subjectBadgeClass[item.subject] || 'badge-sub-eng';
            return `
                <div class="ltp-outcome-card">
                    <div>
                        <div class="ltp-card-header">
                            <span class="ltp-badge-id">#${item.id}</span>
                            <div style="display: flex; gap: 6px; align-items: center;">
                                <span class="ltp-badge-class">Class ${item.class}</span>
                                <span class="ltp-badge-subject ${badgeCls}">${item.subject}</span>
                            </div>
                        </div>
                        <div class="ltp-skill-info" style="margin: 10px 0 8px;">
                            <span>🎯 ${escapeHtml(item.skillArea)}</span>
                            <span>•</span>
                            <span>⚡ ${escapeHtml(item.subSkillArea)}</span>
                        </div>
                        <p class="ltp-outcome-text">${escapeHtml(item.learningOutcome)}</p>
                    </div>
                    <div style="display: flex; gap: 8px; align-items: center; justify-content: flex-end; margin-top: 10px; border-top: 1px solid #f1f5f9; padding-top: 10px;">
                        <button type="button" class="ltp-chip-btn" style="font-size: 11.5px; padding: 4px 10px;" onclick="window.jumpToPractice('${item.subject}')">
                            <span>✍️</span> Practice Quiz
                        </button>
                    </div>
                </div>
            `;
        }).join('');
    }

    function filterContentBySubject(sub, btn) {
        LtpState.selectedSubject = sub;
        document.querySelectorAll('#ltpSubjectChips .ltp-chip-btn').forEach(b => b.classList.remove('active'));
        if (btn) btn.classList.add('active');
        renderLearningContent();
    }

    function filterContentByClass(cls) {
        LtpState.selectedClass = cls;
        renderLearningContent();
    }

    function handleContentSearch(val) {
        LtpState.searchQuery = val || '';
        renderLearningContent();
    }

    function resetContentFilters() {
        LtpState.selectedSubject = 'all';
        LtpState.selectedClass = 'all';
        LtpState.searchQuery = '';
        const searchInput = document.getElementById('ltpContentSearch');
        if (searchInput) searchInput.value = '';
        const classSelect = document.getElementById('ltpClassSelect');
        if (classSelect) classSelect.value = 'all';
        document.querySelectorAll('#ltpSubjectChips .ltp-chip-btn').forEach((b, idx) => {
            b.classList.toggle('active', idx === 0);
        });
        renderLearningContent();
    }

    function jumpToPractice(subject) {
        switchLtpTab('quizzes');
    }

    // =========================================================================
    // 2. INTERACTIVE QUIZZES ENGINE
    // =========================================================================
    function renderQuizzesView() {
        const container = document.getElementById('ltpQuizzesList');
        const activeRunner = document.getElementById('ltpQuizRunner');
        if (!container) return;

        // Reset any active runner
        if (activeRunner) activeRunner.style.display = 'none';
        container.style.display = 'grid';

        const quizzes = window.LTP_QUIZZES || [];
        container.innerHTML = quizzes.map(quiz => {
            const qCount = quiz.questions.length;
            return `
                <div class="ltp-activity-card">
                    <div>
                        <div class="ltp-act-top">
                            <span class="tac-badge tac-badge-subject badge-sub-eng" style="font-size: 11px;">${quiz.subject}</span>
                            <span class="ltp-badge-class">${quiz.class}</span>
                        </div>
                        <h3 class="ltp-act-title" style="margin-top: 10px;">${escapeHtml(quiz.title)}</h3>
                        <div class="ltp-act-meta" style="margin: 8px 0 12px;">
                            <span>🎯 ${escapeHtml(quiz.skillArea)}</span>
                            <span>•</span>
                            <span>📝 ${qCount} Questions</span>
                        </div>
                        <p class="ltp-act-desc">${escapeHtml(quiz.description)}</p>
                    </div>
                    <button type="button" class="ltp-btn-play" onclick="window.startLtpQuiz('${quiz.id}')">
                        <span>▶</span> Start Assessment
                    </button>
                </div>
            `;
        }).join('');
    }

    function startLtpQuiz(quizId) {
        const quiz = (window.LTP_QUIZZES || []).find(q => q.id === quizId);
        if (!quiz) return;

        LtpState.activeQuiz = quiz;
        LtpState.quizStep = 0;
        LtpState.quizAnswers = {};
        LtpState.quizLocked = false;

        document.getElementById('ltpQuizzesList').style.display = 'none';
        const runner = document.getElementById('ltpQuizRunner');
        runner.style.display = 'block';

        renderQuizStep();
    }

    function closeQuizRunner() {
        LtpState.activeQuiz = null;
        document.getElementById('ltpQuizRunner').style.display = 'none';
        document.getElementById('ltpQuizzesList').style.display = 'grid';
    }

    function renderQuizStep() {
        const quiz = LtpState.activeQuiz;
        if (!quiz) return;

        const runner = document.getElementById('ltpQuizRunner');
        const total = quiz.questions.length;
        const q = quiz.questions[LtpState.quizStep];

        const userAns = LtpState.quizAnswers[LtpState.quizStep];
        const isAnswered = userAns !== undefined;
        LtpState.quizLocked = isAnswered;

        const pct = Math.round(((LtpState.quizStep + 1) / total) * 100);

        let optionsHtml = '';
        const keys = ['A', 'B', 'C', 'D'];
        (q.options || []).forEach((opt, idx) => {
            let optCls = '';
            if (isAnswered) {
                if (idx === q.answer) optCls = 'selected-correct';
                else if (idx === userAns) optCls = 'selected-wrong';
            }
            optionsHtml += `
                <button type="button" class="ltp-option-btn ${optCls}" onclick="window.selectQuizAnswer(${idx})" ${isAnswered ? 'disabled' : ''}>
                    <span style="width: 26px; height: 26px; border-radius: 50%; background: #e2e8f0; display: inline-flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 800; flex-shrink: 0;">${keys[idx]}</span>
                    <span>${escapeHtml(opt)}</span>
                </button>
            `;
        });

        let feedbackHtml = '';
        if (isAnswered) {
            const isCorrect = userAns === q.answer;
            feedbackHtml = `
                <div class="ltp-feedback-banner ${isCorrect ? 'correct' : 'wrong'}">
                    <div style="font-weight: 800; font-size: 15px; margin-bottom: 4px;">
                        ${isCorrect ? '✅ Correct Answer!' : '❌ Incorrect.'}
                    </div>
                    <div>${escapeHtml(q.explanation)}</div>
                </div>
            `;
        }

        runner.innerHTML = `
            <div class="ltp-runner-container">
                <div class="ltp-runner-header">
                    <div class="ltp-runner-title-wrap">
                        <span style="font-size: 22px;">✍️</span>
                        <div>
                            <h3 class="ltp-runner-title">${escapeHtml(quiz.title)}</h3>
                            <div style="font-size: 12px; color: #64748b; font-weight: 600;">Question ${LtpState.quizStep + 1} of ${total}</div>
                        </div>
                    </div>
                    <button type="button" class="ltp-btn-close-runner" onclick="window.closeQuizRunner()">✕ Quit</button>
                </div>

                <div class="ltp-progress-track">
                    <div class="ltp-progress-fill" style="width: ${pct}%;"></div>
                </div>

                <div class="ltp-question-card">
                    <h4 class="ltp-question-title">${LtpState.quizStep + 1}. ${escapeHtml(q.prompt)}</h4>
                    <div class="ltp-options-list">
                        ${optionsHtml}
                    </div>
                    ${feedbackHtml}
                </div>

                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
                    <button type="button" class="ltp-chip-btn" onclick="window.navQuizStep(-1)" style="visibility: ${LtpState.quizStep > 0 ? 'visible' : 'hidden'};">
                        ← Previous
                    </button>
                    ${isAnswered ? `
                        <button type="button" class="ltp-btn-play" style="width: auto; padding: 10px 24px;" onclick="window.navQuizStep(1)">
                            ${LtpState.quizStep === total - 1 ? 'See Results 🏆' : 'Next Question →'}
                        </button>
                    ` : `
                        <div style="font-size: 13px; color: #64748b; font-weight: 600;">Choose an answer above to continue</div>
                    `}
                </div>
            </div>
        `;
    }

    function selectQuizAnswer(idx) {
        if (LtpState.quizLocked) return;
        LtpState.quizAnswers[LtpState.quizStep] = idx;
        const q = LtpState.activeQuiz.questions[LtpState.quizStep];
        if (idx === q.answer) {
            sound.correct();
        } else {
            sound.wrong();
        }
        renderQuizStep();
    }

    function navQuizStep(dir) {
        const nextStep = LtpState.quizStep + dir;
        const total = LtpState.activeQuiz.questions.length;
        if (nextStep >= total) {
            finishQuizAndShowResults();
        } else if (nextStep >= 0) {
            LtpState.quizStep = nextStep;
            renderQuizStep();
        }
    }

    function finishQuizAndShowResults() {
        const quiz = LtpState.activeQuiz;
        const total = quiz.questions.length;
        let score = 0;
        quiz.questions.forEach((q, idx) => {
            if (LtpState.quizAnswers[idx] === q.answer) score++;
        });

        const pct = Math.round((score / total) * 100);
        const stars = pct >= 80 ? 3 : pct >= 50 ? 2 : 1;
        const starStr = '⭐'.repeat(stars) + '☆'.repeat(3 - stars);

        let feedbackMsg = 'Good effort! Review the explanations below and retry to achieve mastery.';
        if (pct === 100) feedbackMsg = 'Perfect score! You mastered every concept in this assessment!';
        else if (pct >= 80) feedbackMsg = 'Excellent work! You demonstrated strong understanding of the learning material.';

        if (pct >= 60) sound.win();

        // Save result
        saveResult({
            id: 'res-' + Date.now(),
            title: quiz.title,
            type: 'Quiz',
            subject: quiz.subject,
            score: score,
            total: total,
            percentage: pct,
            date: new Date().toLocaleDateString()
        });

        // Review list HTML
        const reviewHtml = quiz.questions.map((q, idx) => {
            const userAns = LtpState.quizAnswers[idx];
            const isCorrect = userAns === q.answer;
            const chosenText = q.options[userAns] || 'Not answered';
            const correctText = q.options[q.answer];

            return `
                <div style="background: #ffffff; border: 1.5px solid ${isCorrect ? '#a7f3d0' : '#fecaca'}; border-radius: 14px; padding: 14px 18px; margin-bottom: 12px; text-align: left;">
                    <div style="display: flex; align-items: center; justify-content: space-between; gap: 8px; margin-bottom: 6px;">
                        <span style="font-weight: 700; font-size: 14.5px; color: #1e293b;">Question ${idx + 1}</span>
                        <span style="font-weight: 800; font-size: 13px; color: ${isCorrect ? '#059669' : '#dc2626'};">${isCorrect ? '✓ Correct' : '✕ Needs Review'}</span>
                    </div>
                    <p style="font-size: 14px; color: #334155; margin: 0 0 8px;">${escapeHtml(q.prompt)}</p>
                    <div style="font-size: 13px; margin-bottom: 6px;">
                        <strong>Your answer:</strong> <span style="color: ${isCorrect ? '#059669' : '#dc2626'};">${escapeHtml(chosenText)}</span>
                        ${!isCorrect ? ` • <strong>Correct answer:</strong> <span style="color: #059669;">${escapeHtml(correctText)}</span>` : ''}
                    </div>
                    <div style="font-size: 12.5px; color: #64748b; background: #f8fafc; padding: 6px 10px; border-radius: 8px;">
                        <strong>Note:</strong> ${escapeHtml(q.explanation)}
                    </div>
                </div>
            `;
        }).join('');

        const runner = document.getElementById('ltpQuizRunner');
        runner.innerHTML = `
            <div class="ltp-runner-container" style="text-align: center;">
                <div style="font-size: 46px; margin-bottom: 8px;">🏆</div>
                <h3 style="font-family: var(--font-heading); font-size: 26px; font-weight: 800; color: #0f172a; margin: 0 0 4px;">Quiz Completed!</h3>
                <div style="font-size: 28px; margin-bottom: 8px;">${starStr}</div>
                <div style="font-family: var(--font-heading); font-size: 32px; font-weight: 800; color: #4338ca; margin-bottom: 6px;">${score} / ${total}</div>
                <p style="font-size: 15px; color: #475569; max-width: 540px; margin: 0 auto 20px;">${feedbackMsg}</p>

                <div style="display: flex; justify-content: center; gap: 12px; margin-bottom: 24px; flex-wrap: wrap;">
                    <button type="button" class="ltp-btn-play" style="width: auto; padding: 12px 28px;" onclick="window.startLtpQuiz('${quiz.id}')">
                        <span>↻</span> Retry Quiz
                    </button>
                    <button type="button" class="ltp-chip-btn" style="padding: 12px 24px; font-size: 14px; font-weight: 700;" onclick="window.closeQuizRunner()">
                        ← Back to Quizzes
                    </button>
                </div>

                <h4 style="font-family: var(--font-heading); font-size: 17px; font-weight: 700; color: #1e1b4b; text-align: left; margin: 20px 0 12px;">Detailed Question Review:</h4>
                <div>${reviewHtml}</div>
            </div>
        `;
    }

    // =========================================================================
    // 3. MINI GAMES ENGINE (LABEL: "MINI GAME" ON CARDS & SCREENS)
    // =========================================================================
    function renderMiniGamesView() {
        const container = document.getElementById('ltpMiniGamesList');
        const activeRunner = document.getElementById('ltpMiniGameRunner');
        if (!container) return;

        if (activeRunner) activeRunner.style.display = 'none';
        container.style.display = 'grid';

        const games = window.LTP_MINI_GAMES || [];
        container.innerHTML = games.map(game => {
            return `
                <div class="ltp-activity-card">
                    <div>
                        <div class="ltp-act-top">
                            <span class="badge-mini-game badge-mini-game-pulse">🏷️ MINI GAME</span>
                            <span class="ltp-badge-class">${game.format}</span>
                        </div>
                        <h3 class="ltp-act-title" style="margin-top: 10px;">${escapeHtml(game.title)}</h3>
                        <div class="ltp-act-meta" style="margin: 8px 0 12px;">
                            <span>🎮 ${escapeHtml(game.subject)}</span>
                            <span>•</span>
                            <span>⏱️ ${game.time}</span>
                        </div>
                        <p class="ltp-act-desc">${escapeHtml(game.instructions)}</p>
                    </div>
                    <button type="button" class="ltp-btn-play ltp-btn-play-mg" onclick="window.startLtpMiniGame('${game.id}')">
                        <span>🎮</span> Play Mini Game
                    </button>
                </div>
            `;
        }).join('');
    }

    function startLtpMiniGame(gameId) {
        const game = (window.LTP_MINI_GAMES || []).find(g => g.id === gameId);
        if (!game) return;

        LtpState.activeMiniGame = game;
        document.getElementById('ltpMiniGamesList').style.display = 'none';
        const runner = document.getElementById('ltpMiniGameRunner');
        runner.style.display = 'block';

        // Initialize game based on format
        if (game.format === 'Match the Pairs') initMatchPairs(game);
        else if (game.format === 'Fill in the Blank') initFillBlank(game);
        else if (game.format === 'True or False') initTrueFalse(game);
        else if (game.format === 'Arrange in Order') initArrangeOrder(game);
        else if (game.format === 'Quick Quiz Challenge') initQuickChallenge(game);
    }

    function closeMiniGameRunner() {
        if (LtpState.miniGameState && LtpState.miniGameState.timer) {
            clearInterval(LtpState.miniGameState.timer);
        }
        LtpState.activeMiniGame = null;
        LtpState.miniGameState = null;
        document.getElementById('ltpMiniGameRunner').style.display = 'none';
        document.getElementById('ltpMiniGamesList').style.display = 'grid';
    }

    /* --- Mini-Game 1: Match the Pairs --- */
    function initMatchPairs(game) {
        const leftItems = shuffle(game.pairs.map((p, idx) => ({ text: p[0], pairId: idx })));
        const rightItems = shuffle(game.pairs.map((p, idx) => ({ text: p[1], pairId: idx })));

        LtpState.miniGameState = {
            pairs: game.pairs,
            leftItems,
            rightItems,
            selectedLeft: null,
            selectedRight: null,
            matchedCount: 0,
            mistakes: 0,
            total: game.pairs.length
        };

        renderMatchPairs();
    }

    function renderMatchPairs() {
        const state = LtpState.miniGameState;
        const game = LtpState.activeMiniGame;
        const runner = document.getElementById('ltpMiniGameRunner');

        const leftHtml = state.leftItems.map(item => `
            <button type="button" class="ltp-match-item-btn ${item.matched ? 'matched' : ''} ${state.selectedLeft && state.selectedLeft.pairId === item.pairId ? 'selected' : ''}" id="match-l-${item.pairId}" onclick="window.handleMatchClick('L', ${item.pairId})" ${item.matched ? 'disabled' : ''}>
                ${escapeHtml(item.text)}
            </button>
        `).join('');

        const rightHtml = state.rightItems.map(item => `
            <button type="button" class="ltp-match-item-btn ${item.matched ? 'matched' : ''} ${state.selectedRight && state.selectedRight.pairId === item.pairId ? 'selected' : ''}" id="match-r-${item.pairId}" onclick="window.handleMatchClick('R', ${item.pairId})" ${item.matched ? 'disabled' : ''}>
                ${escapeHtml(item.text)}
            </button>
        `).join('');

        const pct = Math.round((state.matchedCount / state.total) * 100);

        runner.innerHTML = `
            <div class="ltp-runner-container">
                <div class="ltp-runner-header">
                    <div class="ltp-runner-title-wrap">
                        <span class="badge-mini-game">🏷️ MINI GAME</span>
                        <h3 class="ltp-runner-title">${escapeHtml(game.title)}</h3>
                    </div>
                    <button type="button" class="ltp-btn-close-runner" onclick="window.closeMiniGameRunner()">✕ Quit</button>
                </div>

                <div style="background: #fffbeb; border-left: 4px solid #f59e0b; padding: 10px 16px; border-radius: 8px; font-size: 13.5px; color: #92400e; margin-bottom: 16px;">
                    <strong>Instructions:</strong> ${escapeHtml(game.instructions)}
                </div>

                <div class="ltp-progress-track">
                    <div class="ltp-progress-fill" style="width: ${pct}%; background: linear-gradient(90deg, #f59e0b, #10b981);"></div>
                </div>

                <div style="display: flex; justify-content: space-between; font-weight: 700; font-size: 13.5px; color: #475569; margin-bottom: 12px;">
                    <span>Matched: ${state.matchedCount} / ${state.total}</span>
                    <span>Mistakes: ${state.mistakes}</span>
                </div>

                <div class="ltp-match-columns">
                    <div>
                        <h4 style="font-family: var(--font-heading); font-size: 14px; color: #64748b; margin-bottom: 8px; text-transform: uppercase;">Curriculum Term</h4>
                        ${leftHtml}
                    </div>
                    <div>
                        <h4 style="font-family: var(--font-heading); font-size: 14px; color: #64748b; margin-bottom: 8px; text-transform: uppercase;">Matched Concept</h4>
                        ${rightHtml}
                    </div>
                </div>
            </div>
        `;
    }

    function handleMatchClick(side, pairId) {
        const state = LtpState.miniGameState;
        if (!state) return;

        if (side === 'L') {
            const item = state.leftItems.find(x => x.pairId === pairId);
            if (item.matched) return;
            state.selectedLeft = item;
        } else {
            const item = state.rightItems.find(x => x.pairId === pairId);
            if (item.matched) return;
            state.selectedRight = item;
        }

        renderMatchPairs();

        if (state.selectedLeft && state.selectedRight) {
            const elL = document.getElementById(`match-l-${state.selectedLeft.pairId}`);
            const elR = document.getElementById(`match-r-${state.selectedRight.pairId}`);

            if (state.selectedLeft.pairId === state.selectedRight.pairId) {
                // Match!
                sound.correct();
                state.selectedLeft.matched = true;
                state.selectedRight.matched = true;
                state.matchedCount++;
                state.selectedLeft = null;
                state.selectedRight = null;
                setTimeout(() => {
                    renderMatchPairs();
                    if (state.matchedCount === state.total) {
                        finishMiniGame(state.total, state.total - state.mistakes);
                    }
                }, 200);
            } else {
                // Mismatch
                sound.wrong();
                state.mistakes++;
                if (elL) elL.classList.add('mismatch');
                if (elR) elR.classList.add('mismatch');
                setTimeout(() => {
                    state.selectedLeft = null;
                    state.selectedRight = null;
                    renderMatchPairs();
                }, 500);
            }
        }
    }

    /* --- Mini-Game 2: Fill in the Blank --- */
    function initFillBlank(game) {
        LtpState.miniGameState = {
            step: 0,
            score: 0,
            items: game.items,
            answered: false,
            userChoice: null
        };
        renderFillBlank();
    }

    function renderFillBlank() {
        const state = LtpState.miniGameState;
        const game = LtpState.activeMiniGame;
        const runner = document.getElementById('ltpMiniGameRunner');
        const item = state.items[state.step];
        const total = state.items.length;
        const pct = Math.round(((state.step + 1) / total) * 100);

        let optionsHtml = item.options.map(opt => {
            let cls = '';
            if (state.answered) {
                if (opt === item.answer) cls = 'selected-correct';
                else if (opt === state.userChoice) cls = 'selected-wrong';
            }
            return `
                <button type="button" class="ltp-option-btn ${cls}" onclick="window.handleFillAnswer('${escapeHtml(opt)}')" ${state.answered ? 'disabled' : ''}>
                    <span>${escapeHtml(opt)}</span>
                </button>
            `;
        }).join('');

        let fbHtml = '';
        if (state.answered) {
            const isCorrect = state.userChoice === item.answer;
            fbHtml = `
                <div class="ltp-feedback-banner ${isCorrect ? 'correct' : 'wrong'}">
                    <div style="font-weight: 800; font-size: 15px; margin-bottom: 4px;">
                        ${isCorrect ? '✅ Well Done!' : '❌ Not quite.'}
                    </div>
                    <div>${escapeHtml(item.explain)}</div>
                </div>
            `;
        }

        runner.innerHTML = `
            <div class="ltp-runner-container">
                <div class="ltp-runner-header">
                    <div class="ltp-runner-title-wrap">
                        <span class="badge-mini-game">🏷️ MINI GAME</span>
                        <h3 class="ltp-runner-title">${escapeHtml(game.title)}</h3>
                    </div>
                    <button type="button" class="ltp-btn-close-runner" onclick="window.closeMiniGameRunner()">✕ Quit</button>
                </div>

                <div style="background: #fffbeb; border-left: 4px solid #f59e0b; padding: 10px 16px; border-radius: 8px; font-size: 13.5px; color: #92400e; margin-bottom: 16px;">
                    <strong>Instructions:</strong> ${escapeHtml(game.instructions)}
                </div>

                <div class="ltp-progress-track">
                    <div class="ltp-progress-fill" style="width: ${pct}%; background: linear-gradient(90deg, #f59e0b, #10b981);"></div>
                </div>

                <div style="font-size: 13px; color: #64748b; font-weight: 700; margin-bottom: 12px;">Sentence ${state.step + 1} of ${total}</div>

                <div class="ltp-question-card">
                    <h4 class="ltp-question-title" style="font-size: 19px;">${escapeHtml(item.sentence)}</h4>
                    <div class="ltp-options-list" style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                        ${optionsHtml}
                    </div>
                    ${fbHtml}
                </div>

                <div style="display: flex; justify-content: flex-end; margin-top: 14px;">
                    ${state.answered ? `
                        <button type="button" class="ltp-btn-play ltp-btn-play-mg" style="width: auto; padding: 10px 24px;" onclick="window.nextFillStep()">
                            ${state.step === total - 1 ? 'See Completion Score 🏆' : 'Next Sentence →'}
                        </button>
                    ` : ''}
                </div>
            </div>
        `;
    }

    function handleFillAnswer(opt) {
        const state = LtpState.miniGameState;
        if (!state || state.answered) return;

        state.answered = true;
        state.userChoice = opt;
        const item = state.items[state.step];
        if (opt === item.answer) {
            state.score++;
            sound.correct();
        } else {
            sound.wrong();
        }
        renderFillBlank();
    }

    function nextFillStep() {
        const state = LtpState.miniGameState;
        if (!state) return;
        state.step++;
        state.answered = false;
        state.userChoice = null;
        if (state.step >= state.items.length) {
            finishMiniGame(state.items.length, state.score);
        } else {
            renderFillBlank();
        }
    }

    /* --- Mini-Game 3: True or False --- */
    function initTrueFalse(game) {
        LtpState.miniGameState = {
            step: 0,
            score: 0,
            items: game.items,
            answered: false,
            userChoice: null
        };
        renderTrueFalse();
    }

    function renderTrueFalse() {
        const state = LtpState.miniGameState;
        const game = LtpState.activeMiniGame;
        const runner = document.getElementById('ltpMiniGameRunner');
        const item = state.items[state.step];
        const total = state.items.length;
        const pct = Math.round(((state.step + 1) / total) * 100);

        let fbHtml = '';
        if (state.answered) {
            const isCorrect = state.userChoice === item.answer;
            fbHtml = `
                <div class="ltp-feedback-banner ${isCorrect ? 'correct' : 'wrong'}">
                    <div style="font-weight: 800; font-size: 15px; margin-bottom: 4px;">
                        ${isCorrect ? '✅ Correct Decision!' : '❌ Incorrect.'}
                    </div>
                    <div>${escapeHtml(item.explain)}</div>
                </div>
            `;
        }

        runner.innerHTML = `
            <div class="ltp-runner-container">
                <div class="ltp-runner-header">
                    <div class="ltp-runner-title-wrap">
                        <span class="badge-mini-game">🏷️ MINI GAME</span>
                        <h3 class="ltp-runner-title">${escapeHtml(game.title)}</h3>
                    </div>
                    <button type="button" class="ltp-btn-close-runner" onclick="window.closeMiniGameRunner()">✕ Quit</button>
                </div>

                <div style="background: #fffbeb; border-left: 4px solid #f59e0b; padding: 10px 16px; border-radius: 8px; font-size: 13.5px; color: #92400e; margin-bottom: 16px;">
                    <strong>Instructions:</strong> ${escapeHtml(game.instructions)}
                </div>

                <div class="ltp-progress-track">
                    <div class="ltp-progress-fill" style="width: ${pct}%; background: linear-gradient(90deg, #f59e0b, #10b981);"></div>
                </div>

                <div style="font-size: 13px; color: #64748b; font-weight: 700; margin-bottom: 12px;">Statement ${state.step + 1} of ${total}</div>

                <div class="ltp-question-card" style="text-align: center; padding: 32px 24px;">
                    <h4 style="font-family: var(--font-heading); font-size: 20px; font-weight: 700; color: #0f172a; line-height: 1.5; margin-bottom: 24px;">
                        "${escapeHtml(item.statement)}"
                    </h4>

                    <div style="display: flex; gap: 18px; justify-content: center; flex-wrap: wrap;">
                        <button type="button" class="ltp-btn-play" style="width: 150px; background: #10b981; font-size: 16px; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);" onclick="window.handleTrueFalseAnswer(true)" ${state.answered ? 'disabled' : ''}>
                            ✅ TRUE
                        </button>
                        <button type="button" class="ltp-btn-play" style="width: 150px; background: #ef4444; font-size: 16px; box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);" onclick="window.handleTrueFalseAnswer(false)" ${state.answered ? 'disabled' : ''}>
                            ❌ FALSE
                        </button>
                    </div>

                    ${fbHtml}
                </div>

                <div style="display: flex; justify-content: flex-end; margin-top: 14px;">
                    ${state.answered ? `
                        <button type="button" class="ltp-btn-play ltp-btn-play-mg" style="width: auto; padding: 10px 24px;" onclick="window.nextTrueFalseStep()">
                            ${state.step === total - 1 ? 'See Completion Score 🏆' : 'Next Statement →'}
                        </button>
                    ` : ''}
                </div>
            </div>
        `;
    }

    function handleTrueFalseAnswer(val) {
        const state = LtpState.miniGameState;
        if (!state || state.answered) return;

        state.answered = true;
        state.userChoice = val;
        const item = state.items[state.step];
        if (val === item.answer) {
            state.score++;
            sound.correct();
        } else {
            sound.wrong();
        }
        renderTrueFalse();
    }

    function nextTrueFalseStep() {
        const state = LtpState.miniGameState;
        if (!state) return;
        state.step++;
        state.answered = false;
        state.userChoice = null;
        if (state.step >= state.items.length) {
            finishMiniGame(state.items.length, state.score);
        } else {
            renderTrueFalse();
        }
    }

    /* --- Mini-Game 4: Arrange in Order --- */
    function initArrangeOrder(game) {
        LtpState.miniGameState = {
            roundIdx: 0,
            rounds: game.rounds,
            score: 0,
            placed: [],
            pool: shuffle(game.rounds[0].steps.slice()),
            checked: false,
            isCorrect: false
        };
        renderArrangeOrder();
    }

    function renderArrangeOrder() {
        const state = LtpState.miniGameState;
        const game = LtpState.activeMiniGame;
        const runner = document.getElementById('ltpMiniGameRunner');
        const round = state.rounds[state.roundIdx];
        const totalRounds = state.rounds.length;

        const slotsHtml = round.steps.map((_, idx) => {
            const placedText = state.placed[idx];
            let borderCls = '';
            if (state.checked) {
                borderCls = placedText === round.steps[idx] ? 'border-color: #10b981; background: #ecfdf5;' : 'border-color: #ef4444; background: #fef2f2;';
            }
            return `
                <div class="ltp-order-slot" style="${borderCls}">
                    <div class="ltp-slot-number">${idx + 1}</div>
                    <span style="font-family: var(--font-heading); font-size: 15px; font-weight: 700; color: #1e293b;">
                        ${placedText ? escapeHtml(placedText) : '<span style="color: #94a3b8; font-weight: 500;">Tap a card below to place here</span>'}
                    </span>
                </div>
            `;
        }).join('');

        const poolHtml = state.pool.map((stepText, idx) => {
            const isUsed = state.placed.includes(stepText);
            return `
                <button type="button" class="ltp-order-chip ${isUsed ? 'used' : ''}" onclick="window.placeOrderChip('${escapeHtml(stepText)}')" ${isUsed || state.checked ? 'disabled' : ''}>
                    ${escapeHtml(stepText)}
                </button>
            `;
        }).join('');

        let fbHtml = '';
        if (state.checked) {
            fbHtml = `
                <div class="ltp-feedback-banner ${state.isCorrect ? 'correct' : 'wrong'}">
                    <div style="font-weight: 800; font-size: 15px; margin-bottom: 4px;">
                        ${state.isCorrect ? '✅ Perfect Order!' : '❌ Not in the right sequence.'}
                    </div>
                    <div>Correct sequence: <strong>${round.steps.join(' ➔ ')}</strong></div>
                </div>
            `;
        }

        runner.innerHTML = `
            <div class="ltp-runner-container">
                <div class="ltp-runner-header">
                    <div class="ltp-runner-title-wrap">
                        <span class="badge-mini-game">🏷️ MINI GAME</span>
                        <h3 class="ltp-runner-title">${escapeHtml(game.title)}</h3>
                    </div>
                    <button type="button" class="ltp-btn-close-runner" onclick="window.closeMiniGameRunner()">✕ Quit</button>
                </div>

                <div style="background: #fffbeb; border-left: 4px solid #f59e0b; padding: 10px 16px; border-radius: 8px; font-size: 13.5px; color: #92400e; margin-bottom: 16px;">
                    <strong>Instructions:</strong> ${escapeHtml(game.instructions)}
                </div>

                <div style="font-size: 13px; color: #64748b; font-weight: 700; margin-bottom: 8px;">Round ${state.roundIdx + 1} of ${totalRounds}</div>

                <div class="ltp-question-card">
                    <h4 class="ltp-question-title">${escapeHtml(round.prompt)}</h4>
                    
                    <div class="ltp-order-slots">
                        ${slotsHtml}
                    </div>

                    <div style="margin: 14px 0 8px; font-size: 13px; color: #64748b; font-weight: 700;">Tap cards in chronological / curriculum order:</div>
                    <div class="ltp-order-pool">
                        ${poolHtml}
                    </div>

                    ${fbHtml}
                </div>

                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 14px;">
                    <button type="button" class="ltp-chip-btn" onclick="window.undoOrderChip()" ${state.placed.length === 0 || state.checked ? 'disabled' : ''}>
                        ↩ Undo
                    </button>
                    ${!state.checked ? `
                        <button type="button" class="ltp-btn-play ltp-btn-play-mg" style="width: auto; padding: 10px 24px;" onclick="window.checkOrderSequence()" ${state.placed.length !== round.steps.length ? 'disabled' : ''}>
                            Check Order ✓
                        </button>
                    ` : `
                        <button type="button" class="ltp-btn-play ltp-btn-play-mg" style="width: auto; padding: 10px 24px;" onclick="window.nextOrderRound()">
                            ${state.roundIdx === totalRounds - 1 ? 'See Completion Score 🏆' : 'Next Round →'}
                        </button>
                    `}
                </div>
            </div>
        `;
    }

    function placeOrderChip(text) {
        const state = LtpState.miniGameState;
        if (!state || state.checked) return;
        state.placed.push(text);
        renderArrangeOrder();
    }

    function undoOrderChip() {
        const state = LtpState.miniGameState;
        if (!state || state.checked) return;
        state.placed.pop();
        renderArrangeOrder();
    }

    function checkOrderSequence() {
        const state = LtpState.miniGameState;
        if (!state) return;
        const round = state.rounds[state.roundIdx];
        state.checked = true;
        state.isCorrect = state.placed.every((val, idx) => val === round.steps[idx]);
        if (state.isCorrect) {
            state.score++;
            sound.correct();
        } else {
            sound.wrong();
        }
        renderArrangeOrder();
    }

    function nextOrderRound() {
        const state = LtpState.miniGameState;
        if (!state) return;
        state.roundIdx++;
        if (state.roundIdx >= state.rounds.length) {
            finishMiniGame(state.rounds.length, state.score);
        } else {
            state.placed = [];
            state.pool = shuffle(state.rounds[state.roundIdx].steps.slice());
            state.checked = false;
            state.isCorrect = false;
            renderArrangeOrder();
        }
    }

    /* --- Mini-Game 5: Quick Quiz Challenge --- */
    function initQuickChallenge(game) {
        LtpState.miniGameState = {
            step: 0,
            score: 0,
            timeLeft: game.seconds || 60,
            questions: shuffle(game.questions.slice()),
            answered: false,
            timer: null
        };

        LtpState.miniGameState.timer = setInterval(() => {
            const state = LtpState.miniGameState;
            if (!state) return;
            state.timeLeft--;
            const timerEl = document.getElementById('ltpQuickTimer');
            if (timerEl) timerEl.textContent = `⏱️ ${state.timeLeft}s`;
            if (state.timeLeft <= 0) {
                clearInterval(state.timer);
                finishMiniGame(state.questions.length, state.score, true);
            }
        }, 1000);

        renderQuickChallenge();
    }

    function renderQuickChallenge() {
        const state = LtpState.miniGameState;
        const game = LtpState.activeMiniGame;
        const runner = document.getElementById('ltpMiniGameRunner');
        const q = state.questions[state.step];
        const total = state.questions.length;

        const optionsHtml = q.options.map((opt, idx) => `
            <button type="button" class="ltp-option-btn" onclick="window.handleQuickAnswer(${idx})">
                <span>${escapeHtml(opt)}</span>
            </button>
        `).join('');

        runner.innerHTML = `
            <div class="ltp-runner-container">
                <div class="ltp-runner-header">
                    <div class="ltp-runner-title-wrap">
                        <span class="badge-mini-game">🏷️ MINI GAME</span>
                        <h3 class="ltp-runner-title">${escapeHtml(game.title)}</h3>
                    </div>
                    <div style="display: flex; gap: 8px; align-items: center;">
                        <span id="ltpQuickTimer" style="font-family: var(--font-heading); font-size: 16px; font-weight: 800; color: #dc2626; background: #fee2e2; padding: 4px 12px; border-radius: 999px;">
                            ⏱️ ${state.timeLeft}s
                        </span>
                        <button type="button" class="ltp-btn-close-runner" onclick="window.closeMiniGameRunner()">✕ Quit</button>
                    </div>
                </div>

                <div style="display: flex; justify-content: space-between; font-weight: 700; font-size: 13.5px; color: #475569; margin-bottom: 12px;">
                    <span>Question ${state.step + 1} of ${total}</span>
                    <span>Points: ⭐ ${state.score * 10}</span>
                </div>

                <div class="ltp-question-card">
                    <h4 class="ltp-question-title" style="font-size: 19px;">${escapeHtml(q.q)}</h4>
                    <div class="ltp-options-list">
                        ${optionsHtml}
                    </div>
                </div>
            </div>
        `;
    }

    function handleQuickAnswer(idx) {
        const state = LtpState.miniGameState;
        if (!state) return;
        const q = state.questions[state.step];
        if (idx === q.answer) {
            state.score++;
            sound.correct();
        } else {
            sound.wrong();
        }

        state.step++;
        if (state.step >= state.questions.length) {
            clearInterval(state.timer);
            finishMiniGame(state.questions.length, state.score);
        } else {
            renderQuickChallenge();
        }
    }

    /* --- Mini-Game Finish Screen --- */
    function finishMiniGame(total, score, timeUp = false) {
        const game = LtpState.activeMiniGame;
        const pct = total > 0 ? Math.round((Math.max(0, score) / total) * 100) : 100;
        const stars = pct >= 80 ? 3 : pct >= 50 ? 2 : 1;
        const starStr = '⭐'.repeat(stars) + '☆'.repeat(3 - stars);

        if (pct >= 50) sound.win();

        saveResult({
            id: 'res-' + Date.now(),
            title: game.title,
            type: `Mini Game (${game.format})`,
            subject: game.subject,
            score: Math.max(0, score),
            total: total,
            percentage: pct,
            date: new Date().toLocaleDateString()
        });

        const runner = document.getElementById('ltpMiniGameRunner');
        runner.innerHTML = `
            <div class="ltp-runner-container" style="text-align: center;">
                <span class="badge-mini-game" style="margin-bottom: 12px;">🏷️ MINI GAME</span>
                <div style="font-size: 46px; margin-bottom: 8px;">🎉</div>
                <h3 style="font-family: var(--font-heading); font-size: 26px; font-weight: 800; color: #0f172a; margin: 0 0 4px;">
                    ${timeUp ? "Time's Up!" : "Mini Game Completed!"}
                </h3>
                <div style="font-size: 28px; margin-bottom: 8px;">${starStr}</div>
                <div style="font-family: var(--font-heading); font-size: 32px; font-weight: 800; color: #d97706; margin-bottom: 6px;">
                    ${Math.max(0, score)} / ${total}
                </div>
                <p style="font-size: 15px; color: #475569; max-width: 500px; margin: 0 auto 20px;">
                    ${pct >= 80 ? 'Outstanding performance! You completed the mini-game with high accuracy!' : 'Great job! Play again to sharpen your skills.'}
                </p>

                <div style="display: flex; justify-content: center; gap: 12px; margin-top: 20px; flex-wrap: wrap;">
                    <button type="button" class="ltp-btn-play ltp-btn-play-mg" style="width: auto; padding: 12px 28px;" onclick="window.startLtpMiniGame('${game.id}')">
                        <span>↻</span> Replay Mini Game
                    </button>
                    <button type="button" class="ltp-chip-btn" style="padding: 12px 24px; font-size: 14px; font-weight: 700;" onclick="window.closeMiniGameRunner()">
                        ← Back to Mini Games
                    </button>
                </div>
            </div>
        `;
    }

    // =========================================================================
    // 4. RESULTS & PROGRESS HUB
    // =========================================================================
    function renderResultsView() {
        const container = document.getElementById('ltpResultsContent');
        if (!container) return;

        const results = LtpState.results || [];
        if (results.length === 0) {
            container.innerHTML = `
                <div style="text-align: center; padding: 48px; background: #ffffff; border-radius: 20px; border: 1.5px dashed #cbd5e1;">
                    <div style="font-size: 44px; margin-bottom: 12px;">📊✨</div>
                    <h4 style="font-family: var(--font-heading); font-size: 20px; font-weight: 800; color: #1e1b4b; margin-bottom: 6px;">No activities completed yet</h4>
                    <p style="color: #64748b; font-size: 14.5px; margin-bottom: 20px;">Take a quiz or play a mini-game to view your scores, progress, and performance badges here!</p>
                    <div style="display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;">
                        <button type="button" class="ltp-btn-play" style="width: auto; padding: 10px 22px;" onclick="window.switchLtpTab('quizzes')">Explore Quizzes ✍️</button>
                        <button type="button" class="ltp-btn-play ltp-btn-play-mg" style="width: auto; padding: 10px 22px;" onclick="window.switchLtpTab('minigames')">Play Mini Games 🏷️</button>
                    </div>
                </div>
            `;
            return;
        }

        const totalAttempts = results.length;
        const totalScore = results.reduce((acc, r) => acc + (r.score || 0), 0);
        const totalMax = results.reduce((acc, r) => acc + (r.total || 0), 0);
        const avgPct = totalMax > 0 ? Math.round((totalScore / totalMax) * 100) : 0;

        const rowsHtml = results.map(r => `
            <tr>
                <td><strong>${escapeHtml(r.title)}</strong></td>
                <td><span class="ltp-badge-subject ${r.type.includes('Mini Game') ? 'badge-sub-math' : 'badge-sub-eng'}">${escapeHtml(r.type)}</span></td>
                <td>${escapeHtml(r.subject)}</td>
                <td><strong style="color: #4338ca;">${r.score} / ${r.total}</strong> (${r.percentage}%)</td>
                <td style="color: #64748b; font-size: 13px;">${r.date || 'Recent'}</td>
            </tr>
        `).join('');

        container.innerHTML = `
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 24px;">
                <div class="ltp-stat-pill" style="background: #ffffff; border: 1.5px solid #e2e8f0; padding: 16px;">
                    <div class="ltp-stat-val" style="color: #4338ca;">${totalAttempts}</div>
                    <div class="ltp-stat-lbl" style="color: #64748b;">Activities Completed</div>
                </div>
                <div class="ltp-stat-pill" style="background: #ffffff; border: 1.5px solid #e2e8f0; padding: 16px;">
                    <div class="ltp-stat-val" style="color: #059669;">${avgPct}%</div>
                    <div class="ltp-stat-lbl" style="color: #64748b;">Average Accuracy</div>
                </div>
                <div class="ltp-stat-pill" style="background: #ffffff; border: 1.5px solid #e2e8f0; padding: 16px;">
                    <div class="ltp-stat-val" style="color: #d97706;">⭐ ${totalScore}</div>
                    <div class="ltp-stat-lbl" style="color: #64748b;">Total Stars</div>
                </div>
            </div>

            <div class="ltp-results-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; flex-wrap: wrap; gap: 8px;">
                    <h4 style="font-family: var(--font-heading); font-size: 17px; font-weight: 800; color: #1e1b4b; margin: 0;">Completed Assessments & Games History</h4>
                    <button type="button" class="ltp-chip-btn" onclick="window.clearLtpHistory()">Clear History</button>
                </div>
                <div style="overflow-x: auto;">
                    <table class="ltp-history-table">
                        <thead>
                            <tr>
                                <th>Activity</th>
                                <th>Type</th>
                                <th>Subject</th>
                                <th>Score</th>
                                <th>Date</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${rowsHtml}
                        </tbody>
                    </table>
                </div>
            </div>
        `;
    }

    function clearLtpHistory() {
        if (!confirm('Clear all Learn Through Play score history?')) return;
        LtpState.results = [];
        localStorage.removeItem(STORAGE_KEY);
        updateHeroMetrics();
        renderResultsView();
    }

    // Helper utilities
    function shuffle(arr) {
        const a = arr.slice();
        for (let i = a.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [a[i], a[j]] = [a[j], a[i]];
        }
        return a;
    }

    function escapeHtml(str) {
        if (!str) return '';
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    // Export to global window scope
    window.renderLearnThroughPlay = function () {
        loadResults();
        updateHeroMetrics();
        switchLtpTab(LtpState.activeTab);
    };

    window.switchLtpTab = switchLtpTab;
    window.filterContentBySubject = filterContentBySubject;
    window.filterContentByClass = filterContentByClass;
    window.handleContentSearch = handleContentSearch;
    window.resetLtpContentFilters = resetContentFilters;
    window.jumpToPractice = jumpToPractice;

    window.startLtpQuiz = startLtpQuiz;
    window.closeQuizRunner = closeQuizRunner;
    window.selectQuizAnswer = selectQuizAnswer;
    window.navQuizStep = navQuizStep;

    window.startLtpMiniGame = startLtpMiniGame;
    window.closeMiniGameRunner = closeMiniGameRunner;
    window.handleMatchClick = handleMatchClick;
    window.handleFillAnswer = handleFillAnswer;
    window.nextFillStep = nextFillStep;
    window.handleTrueFalseAnswer = handleTrueFalseAnswer;
    window.nextTrueFalseStep = nextTrueFalseStep;
    window.placeOrderChip = placeOrderChip;
    window.undoOrderChip = undoOrderChip;
    window.checkOrderSequence = checkOrderSequence;
    window.nextOrderRound = nextOrderRound;
    window.handleQuickAnswer = handleQuickAnswer;

    window.clearLtpHistory = clearLtpHistory;

})(window);
