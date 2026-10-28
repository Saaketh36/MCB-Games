/* ====================================================
   QUEST RUNNER (QUESTION UI ENGINE)
   ==================================================== */
function toggleQuestFullscreen() {
    const card = document.getElementById('questRunnerCard');
    if (!card) return;
    const isFull = card.classList.toggle('is-fullscreen');
    const btn = document.getElementById('btnQuestFullscreen');
    if (btn) {
        btn.innerHTML = isFull ? '<span>🗗</span> Exit Fullscreen' : '<span>⛶</span> Fullscreen';
    }
}

function launchQuestRunner() {
    AppState.missionStep = 0;
    AppState.missionAnswers = {};
    isContextAudioPlaying = false;
    isSequencePracticeOpen = false;
    isContextBodyCollapsed = false;

    const game = AppState.activeMissionGame;
    if (game) {
        const titleEl = document.getElementById('questGameHeaderTitle');
        if (titleEl) titleEl.textContent = game.title;
        const badgeEl = document.getElementById('questGameSubjectBadge');
        if (badgeEl) {
            badgeEl.textContent = `${game.subject} • Class ${game.class || AppState.selectedClass}`;
            badgeEl.className = `tac-badge tac-badge-subject ${game.badgeClass || ''}`;
        }
        const playerEl = document.getElementById('questActivePlayerName');
        if (playerEl && AppState.selectedStudent) {
            if (AppState.selectedStudent.name === "Teacher Preview Mode") {
                playerEl.textContent = "👩‍🏫 Teacher Preview Mode";
            } else {
                playerEl.textContent = `${AppState.selectedStudent.name} (Roll #${AppState.selectedStudent.roll})`;
            }
        }
        const skillTag = document.getElementById('questPromptSkillTag');
        if (skillTag) skillTag.textContent = `🎯 ${game.skillArea || 'Core Skill'}`;
        const actTag = document.getElementById('questPromptActTag');
        if (actTag) actTag.textContent = `⚡ ${game.activity || 'Activity'}`;
    }

    document.getElementById('questActiveRunner').style.display = 'block';
    document.getElementById('questCelebrationRunner').style.display = 'none';

    renderQuestStep();
    document.getElementById('questRunnerModal').classList.add('active');
}

function closeQuestRunner() {
    if ('speechSynthesis' in window) window.speechSynthesis.cancel();
    isContextAudioPlaying = false;
    isSequencePracticeOpen = false;
    const audioBtn = document.getElementById('btnContextAudioPlay');
    if (audioBtn) audioBtn.classList.remove('is-playing');
    if (typeof ReadingStudio !== 'undefined') {
        ReadingStudio.stopSpeech();
        ReadingStudio.hideVocabPopover();
    }
    const card = document.getElementById('questRunnerCard');
    if (card) card.classList.remove('quest-reading-mode');
    const studio = document.getElementById('questReadingStudioContainer');
    if (studio) studio.style.display = 'none';
    const c2 = document.getElementById('c2InteractiveGameContainer');
    if (c2) c2.innerHTML = '';
    document.getElementById('questRunnerModal').classList.remove('active');
    renderKidZone();
    renderTeacherHub();
    if (AppState.currentView === 'split') {
        renderSplitViews();
    }
}

// Web Audio API Sound Synthesizer for Kids Quest
const QuestAudio = {
    enabled: true,
    ctx: null,
    getCtx() {
        if (!this.ctx) {
            const AudioCtx = window.AudioContext || window.webkitAudioContext;
            if (AudioCtx) this.ctx = new AudioCtx();
        }
        if (this.ctx && this.ctx.state === 'suspended') {
            this.ctx.resume();
        }
        return this.ctx;
    },
    playClick() {
        if (!this.enabled) return;
        try {
            const ctx = this.getCtx();
            if (!ctx) return;
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(587.33, ctx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(880, ctx.currentTime + 0.1);
            gain.gain.setValueAtTime(0.18, ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.12);
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start();
            osc.stop(ctx.currentTime + 0.13);
        } catch (e) { }
    },
    playNav() {
        if (!this.enabled) return;
        try {
            const ctx = this.getCtx();
            if (!ctx) return;
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.type = 'triangle';
            osc.frequency.setValueAtTime(440, ctx.currentTime);
            gain.gain.setValueAtTime(0.12, ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.09);
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start();
            osc.stop(ctx.currentTime + 0.1);
        } catch (e) { }
    },
    playFanfare() {
        if (!this.enabled) return;
        try {
            const ctx = this.getCtx();
            if (!ctx) return;
            const notes = [523.25, 659.25, 783.99, 1046.5];
            notes.forEach((freq, idx) => {
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = 'sine';
                osc.frequency.value = freq;
                const start = ctx.currentTime + (idx * 0.12);
                gain.gain.setValueAtTime(0.15, start);
                gain.gain.exponentialRampToValueAtTime(0.001, start + 0.35);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start(start);
                osc.stop(start + 0.36);
            });
        } catch (e) { }
    }
};

function toggleQuestSound() {
    QuestAudio.enabled = !QuestAudio.enabled;
    const icon = document.getElementById('questSoundIcon');
    if (icon) icon.textContent = QuestAudio.enabled ? '🔊' : '🔇';
    showToastNotification(QuestAudio.enabled ? 'Sound effects enabled! 🔊' : 'Sound effects muted 🔇');
}

function launchQuestConfetti() {
    const canvas = document.getElementById('questConfettiCanvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    canvas.width = canvas.parentElement.clientWidth || window.innerWidth;
    canvas.height = canvas.parentElement.clientHeight || window.innerHeight;

    const colors = ['#f59e0b', '#ec4899', '#6366f1', '#10b981', '#3b82f6', '#8b5cf6'];
    const particles = [];
    for (let i = 0; i < 70; i++) {
        particles.push({
            x: canvas.width / 2,
            y: canvas.height / 3,
            vx: (Math.random() - 0.5) * 14,
            vy: (Math.random() - 0.8) * 14,
            size: Math.random() * 8 + 4,
            color: colors[Math.floor(Math.random() * colors.length)],
            rotation: Math.random() * 360,
            vRot: (Math.random() - 0.5) * 10,
            opacity: 1
        });
    }

    let frames = 0;
    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        let alive = false;
        particles.forEach(p => {
            p.x += p.vx;
            p.y += p.vy;
            p.vy += 0.35;
            p.rotation += p.vRot;
            p.opacity -= 0.012;
            if (p.opacity > 0) {
                alive = true;
                ctx.save();
                ctx.translate(p.x, p.y);
                ctx.rotate((p.rotation * Math.PI) / 180);
                ctx.fillStyle = p.color;
                ctx.globalAlpha = Math.max(0, p.opacity);
                ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size * 0.6);
                ctx.restore();
            }
        });
        frames++;
        if (alive && frames < 120) {
            requestAnimationFrame(animate);
        } else {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
        }
    }
    requestAnimationFrame(animate);
}

/* ====================================================
   ENGLISH READING COMPREHENSION STUDIO CONTROLLER
   Side-by-side passage reader, audio TTS, vocabulary
   tooltips, and evidence highlighting
   ==================================================== */
function escapeHtml(str) {
    if (!str) return '';
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
}

function isAnswerCorrect(q, userAns) {
    if (!q || userAns === undefined || userAns === null) return false;
    if (q.type === 'typed') {
        const str = String(userAns).trim().toLowerCase();
        if (!str) return false;
        const expected = String(q.answer).trim().toLowerCase();
        if (str === expected || str.includes(expected) || expected.includes(str)) return true;
        if (q.keywords && Array.isArray(q.keywords)) {
            const hits = q.keywords.filter(kw => str.includes(kw.toLowerCase()));
            return hits.length >= 1;
        }
        return false;
    }
    return userAns === q.answer;
}

const ReadingStudio = {
    currentPassage: null,
    fontSize: 17,
    synth: window.speechSynthesis,
    isSpeaking: false,
    popoverEl: null,

    init(passage, containerEl) {
        this.currentPassage = passage;
        this.stopSpeech();
        this.hideVocabPopover();
        this.renderPassage(containerEl);
    },

    stopSpeech() {
        if (this.synth) {
            this.synth.cancel();
        }
        this.isSpeaking = false;
        const btn = document.getElementById('btnReadingTTS');
        if (btn) {
            btn.classList.remove('is-speaking');
            btn.innerHTML = '<span>▶</span> Read Aloud';
        }
        const paras = document.querySelectorAll('.passage-paragraph');
        paras.forEach(p => p.classList.remove('is-speaking-para'));
    },

    toggleSpeech() {
        if (!this.synth || !this.currentPassage) return;
        if (this.isSpeaking) {
            this.stopSpeech();
            return;
        }

        this.stopSpeech();
        const fullText = this.currentPassage.content.join('. ');
        const utter = new SpeechSynthesisUtterance(fullText);
        utter.rate = 0.92;
        utter.pitch = 1.02;

        const btn = document.getElementById('btnReadingTTS');
        if (btn) {
            btn.classList.add('is-speaking');
            btn.innerHTML = '<span>⏹</span> Stop Audio';
        }
        this.isSpeaking = true;

        utter.onend = () => {
            this.stopSpeech();
        };
        utter.onerror = () => {
            this.stopSpeech();
        };

        this.synth.speak(utter);
    },

    adjustFontSize(delta) {
        this.fontSize = Math.min(24, Math.max(14, this.fontSize + delta));
        const txtEl = document.getElementById('passageTextContainer');
        if (txtEl) {
            txtEl.style.fontSize = `${this.fontSize}px`;
        }
    },

    highlightEvidence(paraIdx) {
        const paras = document.querySelectorAll('.passage-paragraph');
        paras.forEach(p => p.classList.remove('is-evidence-target'));

        const target = document.getElementById(`passagePara-${paraIdx}`);
        if (target) {
            target.classList.add('is-evidence-target');
            target.scrollIntoView({ behavior: 'smooth', block: 'center' });
            setTimeout(() => {
                target.classList.remove('is-evidence-target');
            }, 3500);
        }
    },

    showVocabPopover(word, def, example, targetEl) {
        this.hideVocabPopover();
        const pop = document.createElement('div');
        pop.className = 'vocab-popover-card';
        pop.id = 'activeVocabPopover';
        pop.innerHTML = `
                    <div class="vocab-popover-word">
                        <span>📖 ${word}</span>
                        <button type="button" style="background:none; border:none; color:#f8fafc; cursor:pointer; font-size:14px;" onclick="ReadingStudio.hideVocabPopover()">✕</button>
                    </div>
                    <div class="vocab-popover-def">${def}</div>
                    ${example ? `<div class="vocab-popover-example">"${example}"</div>` : ''}
                `;
        document.body.appendChild(pop);

        const rect = targetEl.getBoundingClientRect();
        const top = rect.bottom + window.scrollY + 8;
        const left = Math.min(window.innerWidth - 330, Math.max(10, rect.left + window.scrollX - 20));
        pop.style.top = `${top}px`;
        pop.style.left = `${left}px`;
        this.popoverEl = pop;
    },

    hideVocabPopover() {
        const old = document.getElementById('activeVocabPopover');
        if (old) old.remove();
        this.popoverEl = null;
    },

    renderPassage(container) {
        if (!this.currentPassage) return;
        const p = this.currentPassage;

        const vocabMap = {};
        if (p.vocabulary && Array.isArray(p.vocabulary)) {
            p.vocabulary.forEach(v => {
                vocabMap[v.word.toLowerCase()] = v;
            });
        }

        let parasHtml = '';
        p.content.forEach((paraText, pIdx) => {
            let processed = paraText;
            Object.keys(vocabMap).forEach(w => {
                const regex = new RegExp(`\\b(${w})\\b`, 'gi');
                processed = processed.replace(regex, (match) => {
                    return `<span class="vocab-word-highlight" data-word="${match}" onclick="ReadingStudio.onVocabClick(event, '${w}')">${match}</span>`;
                });
            });

            parasHtml += `
                        <div class="passage-paragraph" id="passagePara-${pIdx}">
                            <span class="passage-para-badge">¶ ${pIdx + 1}</span>
                            ${processed}
                        </div>
                    `;
        });

        container.innerHTML = `
                    <div class="passage-meta-header">
                        <div class="passage-meta-tags">
                            <span class="passage-badge passage-badge-topic">🏷️ ${p.topic || 'Reading'}</span>
                            <span class="passage-badge passage-badge-genre">📚 ${p.genre || 'Story / Essay'}</span>
                            <span class="passage-badge passage-badge-time">⏱️ ${p.estimatedTime || '3 min read'}</span>
                        </div>
                        <h3 class="passage-title">${p.title}</h3>
                    </div>

                    <div class="reading-toolbar">
                        <div class="reading-audio-controls">
                            <button type="button" class="btn-reading-tts" id="btnReadingTTS" onclick="ReadingStudio.toggleSpeech()">
                                <span>▶</span> Read Aloud
                            </button>
                        </div>
                        <div class="reading-font-controls">
                            <span class="font-ctrl-label">Text Size:</span>
                            <button type="button" class="btn-font-size" onclick="ReadingStudio.adjustFontSize(-2)" title="Smaller text">A-</button>
                            <button type="button" class="btn-font-size" onclick="ReadingStudio.adjustFontSize(2)" title="Larger text">A+</button>
                        </div>
                    </div>

                    <div class="passage-text-container" id="passageTextContainer" style="font-size: ${this.fontSize}px;">
                        ${parasHtml}
                    </div>
                `;
    },

    onVocabClick(e, wordKey) {
        e.stopPropagation();
        if (!this.currentPassage || !this.currentPassage.vocabulary) return;
        const item = this.currentPassage.vocabulary.find(v => v.word.toLowerCase() === wordKey.toLowerCase());
        if (item) {
            this.showVocabPopover(item.word, item.definition, item.example || '', e.target);
        }
    }
};

// Global dismiss for vocab popover
document.addEventListener('click', (e) => {
    if (!e.target.closest('.vocab-popover-card') && !e.target.closest('.vocab-word-highlight')) {
        ReadingStudio.hideVocabPopover();
    }
});

function cleanQuestionPrompt(text) {
    if (!text || typeof text !== 'string') return text || '';
    // Strip any leading bracketed metadata tags like [IV Science], [Class IV], [Science], [Grade 4 Math]
    return text.replace(/^\s*\[(?:Class\s*|Grade\s*)?[IVXLCDM\d\s\-_:\/|a-zA-Z]+\]\s*/i, '').trim();
}

function cleanVisualHint(hint) {
    if (!hint || typeof hint !== 'string') return '';
    let h = hint.trim();
    for (let i = 0; i < 3; i++) {
        h = h.replace(/^(?:(?:[\uD800-\uDBFF][\uDC00-\uDFFF]|[\u2600-\u27BF]|\uFE0F|\s)*(?:Visual\s*Clue|Clue|Hint)\s*:\s*)+/gi, '').trim();
    }
    return h;
}

function selectReadingMCQAnswer(idx) {
    QuestAudio.playClick();
    AppState.missionAnswers[AppState.missionStep] = idx;
    renderQuestStep();
}

function submitTypedReadingAnswer() {
    const inp = document.getElementById('readingTypedInput');
    if (!inp) return;
    const text = inp.value.trim();
    if (!text) {
        showToastNotification("Please type your response based on the text! ✍️");
        return;
    }
    QuestAudio.playClick();
    AppState.missionAnswers[AppState.missionStep] = text;
    renderQuestStep();
}

function renderReadingStudioStep(game) {
    const pPane = document.getElementById('questReadingPassagePane');
    const qPane = document.getElementById('questReadingQuizPane');
    if (!pPane || !qPane) return;

    if (!pPane.hasChildNodes() || ReadingStudio.currentPassage !== game.passage) {
        ReadingStudio.init(game.passage, pPane);
    }

    const qList = game.questions;
    const total = qList.length;
    const q = qList[AppState.missionStep];
    const userAns = AppState.missionAnswers[AppState.missionStep];
    const isAnswered = userAns !== undefined && userAns !== null && String(userAns).trim().length > 0;

    let stepperHtml = '<div class="quest-stepper-row" style="margin-bottom: 12px;">';
    qList.forEach((_, sIdx) => {
        const isCurrent = sIdx === AppState.missionStep;
        const answered = AppState.missionAnswers[sIdx] !== undefined;
        stepperHtml += `<div class="quest-step-pill ${isCurrent ? 'active' : ''} ${answered ? 'answered' : ''}" onclick="QuestAudio.playNav(); AppState.missionStep = ${sIdx}; renderQuestStep();">Q${sIdx + 1} ${answered ? '✓' : ''}</div>`;
    });
    stepperHtml += '</div>';

    const isTyped = q.type === 'typed';
    const typeLabel = isTyped ? '✍️ Short Answer' : '🎯 Multiple Choice';

    const clueBtn = q.evidenceParagraph !== undefined
        ? `<button type="button" class="btn-show-evidence" onclick="ReadingStudio.highlightEvidence(${q.evidenceParagraph})">🔍 Find in Text (¶ ${q.evidenceParagraph + 1})</button>`
        : '';

    let answerHtml = '';
    if (isTyped) {
        const val = userAns || '';
        let fbHtml = '';
        if (isAnswered) {
            const ok = isAnswerCorrect(q, userAns);
            fbHtml = `<div class="typed-feedback-box ${ok ? 'correct' : 'wrong'}">
                        ${ok ? '✅ Excellent text evidence!' : '💡 Expected answer: ' + q.answer}
                        ${q.explanation ? '<br><span style="font-weight:400; font-size:12.5px;">' + q.explanation + '</span>' : ''}
                    </div>`;
        }

        answerHtml = `
                    <div class="reading-typed-container">
                        <input type="text" id="readingTypedInput" class="reading-typed-input" placeholder="Type your answer based on the passage..." value="${escapeHtml(val)}" ${isAnswered ? '' : 'autofocus'}>
                        <div class="reading-typed-actions">
                            <button type="button" class="btn-typed-submit" id="btnSubmitTyped" onclick="submitTypedReadingAnswer()">
                                ${isAnswered ? 'Update Answer' : 'Check Answer ✓'}
                            </button>
                        </div>
                        ${fbHtml}
                    </div>
                `;
    } else {
        const keys = ['A', 'B', 'C', 'D'];
        const badgeClasses = ['badge-a', 'badge-b', 'badge-c', 'badge-d'];
        answerHtml = '<div class="quest-choices-grid" style="grid-template-columns: 1fr; gap: 10px; margin-top: 14px;">';
        (q.options || []).forEach((optText, optIdx) => {
            const isSelected = userAns === optIdx;
            answerHtml += `
                        <button type="button" class="quest-choice-btn ${isSelected ? 'selected' : ''}" onclick="selectReadingMCQAnswer(${optIdx})">
                            <div class="choice-main-content">
                                <span class="choice-key-badge ${badgeClasses[optIdx % 4]}">${keys[optIdx % 4]}</span>
                                <span style="line-height: 1.4;">${optText}</span>
                            </div>
                            <div class="choice-check-indicator">✓</div>
                        </button>
                    `;
        });
        answerHtml += '</div>';

        if (isAnswered && q.explanation) {
            const ok = userAns === q.answer;
            answerHtml += `
                        <div class="typed-feedback-box ${ok ? 'correct' : 'wrong'}" style="margin-top: 14px;">
                            ${ok ? '✅ Correct!' : '❌ Incorrect.'} <span style="font-weight:400; font-size:12.5px;">${q.explanation}</span>
                        </div>
                    `;
        }
    }

    const answeredCount = Object.keys(AppState.missionAnswers).length;
    const pct = Math.round((answeredCount / total) * 100);

    qPane.innerHTML = `
                <div>
                    ${stepperHtml}

                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <div style="font-family: var(--font-heading); font-size: 13px; font-weight: 800; color: #6d28d9;">
                            Question ${AppState.missionStep + 1} of ${total}
                        </div>
                        <div style="font-size: 12.5px; font-weight: 800; color: #b45309;">
                            ${pct}% Complete ⭐
                        </div>
                    </div>

                    <div class="quest-progress-track" style="margin-bottom: 14px;">
                        <div class="quest-progress-fill" style="width: ${(AppState.missionStep + 1) / total * 100}%;"></div>
                    </div>

                    <div class="reading-question-card">
                        <div class="reading-question-header">
                            <span class="reading-type-badge">${typeLabel}</span>
                            ${clueBtn}
                        </div>
                        <h3 class="reading-question-title">${cleanQuestionPrompt(q.prompt)}</h3>
                        ${answerHtml}
                    </div>
                </div>

                <div class="quest-footer-bar" style="margin-top: 16px;">
                    <button type="button" class="btn-quest-back" onclick="navigateQuest(-1)" style="visibility: ${AppState.missionStep > 0 ? 'visible' : 'hidden'}">
                        <span>←</span> Previous
                    </button>
                    <div class="quest-footer-hint" style="font-size: 12px;">
                        <span>💡</span> Hint: Check the left pane for details!
                    </div>
                    <button type="button" class="btn-quest-next-step" onclick="navigateQuest(1)">
                        ${AppState.missionStep === total - 1 ? 'Submit Challenge 🚀' : 'Next question →'}
                    </button>
                </div>
            `;

    if (isTyped) {
        const inp = document.getElementById('readingTypedInput');
        if (inp) {
            inp.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') submitTypedReadingAnswer();
            });
        }
    }
}

function renderQuestStep() {
    const game = AppState.activeMissionGame;
    if (!game) return;

    const c2Container = document.getElementById('c2InteractiveGameContainer');
    const studioContainer = document.getElementById('questReadingStudioContainer');
    const card = document.getElementById('questRunnerCard');
    const standardElements = [
        document.getElementById('questStepperRow'),
        document.getElementById('questStepCounter') ? document.getElementById('questStepCounter').parentElement : null,
        document.querySelector('.quest-progress-track'),
        document.querySelector('.quest-prompt-card'),
        document.getElementById('questChoicesGrid'),
        document.querySelector('.quest-footer-bar')
    ];

    // Direct-manipulation Tactile Mini-Game for Class 2
    if (window.Class2Games && window.Class2Games.isClass2Interactive(game)) {
        if (card) card.classList.remove('quest-reading-mode');
        if (studioContainer) studioContainer.style.display = 'none';
        standardElements.forEach(el => { if (el) el.style.display = 'none'; });
        if (c2Container) {
            c2Container.style.display = 'block';
            window.Class2Games.render(c2Container, game, (result) => {
                AppState.missionAnswers = {};
                const qCount = (game.questions && game.questions.length) || result.total || 3;
                for (let i = 0; i < qCount; i++) {
                    if (i < result.score) {
                        AppState.missionAnswers[i] = (game.questions && game.questions[i]) ? game.questions[i].answer : 0;
                    } else {
                        const cor = (game.questions && game.questions[i]) ? game.questions[i].answer : 0;
                        AppState.missionAnswers[i] = (cor + 1) % 4;
                    }
                }
                finishQuestAndShowReview();
            });
        }
        return;
    }

    // Side-by-Side Reading Comprehension Studio
    const isReadingStudio = !!(game.passage && game.passage.content);
    if (isReadingStudio) {
        if (card) card.classList.add('quest-reading-mode');
        standardElements.forEach(el => { if (el) el.style.display = 'none'; });
        if (c2Container) c2Container.style.display = 'none';
        if (studioContainer) studioContainer.style.display = 'block';

        renderReadingStudioStep(game);
        return;
    } else {
        if (card) card.classList.remove('quest-reading-mode');
        if (studioContainer) studioContainer.style.display = 'none';
    }

    // Standard MCQ / Visual Diagram Quest Runner
    if (c2Container) c2Container.style.display = 'none';
    standardElements.forEach(el => { if (el) el.style.display = ''; });

    // Dedicated Context / Spoken Passage / Lab Procedure & Steps Studio
    renderQuestContext(game);

    const qList = game.questions;
    const total = qList.length;
    const q = qList[AppState.missionStep];

    // Render Stepper Row
    const stepper = document.getElementById('questStepperRow');
    if (stepper) {
        stepper.innerHTML = '';
        qList.forEach((_, sIdx) => {
            const isCurrent = sIdx === AppState.missionStep;
            const isAnswered = AppState.missionAnswers[sIdx] !== undefined;
            const pill = document.createElement('div');
            pill.className = `quest-step-pill ${isCurrent ? 'active' : ''} ${isAnswered ? 'answered' : ''}`;
            pill.innerHTML = `Q${sIdx + 1} ${isAnswered ? '✓' : ''}`;
            pill.onclick = () => {
                QuestAudio.playNav();
                AppState.missionStep = sIdx;
                renderQuestStep();
            };
            stepper.appendChild(pill);
        });
    }

    document.getElementById('questStepCounter').textContent = `Question ${AppState.missionStep + 1} of ${total}`;
    const answeredCount = Object.keys(AppState.missionAnswers).length;
    const pct = Math.round((answeredCount / total) * 100);
    document.getElementById('questProgressFill').style.width = `${pct}%`;
    const pctLabel = document.getElementById('questPercentLabel');
    if (pctLabel) pctLabel.textContent = `${pct}% Complete (${answeredCount}/${total} Answered) ⭐`;

    const tips = [
        "Take your time. Curiosity is your superpower! 🚀",
        "Read carefully and trust your instincts! ⭐",
        "You are doing awesome, keep going! 🌟",
        "Every question makes you smarter! 💡"
    ];
    const tipEl = document.getElementById('questFooterTip');
    if (tipEl) tipEl.innerHTML = `<span>💡</span> ${tips[AppState.missionStep % tips.length]}`;

    // Update Skill Area & Activity Tags
    const skillTag = document.getElementById('questPromptSkillTag');
    const actTag = document.getElementById('questPromptActTag');
    if (skillTag) {
        skillTag.textContent = `🎯 ${game.subject || ''} • ${game.skillArea || ''}`;
    }
    if (actTag) {
        actTag.style.display = 'inline-flex';
        actTag.textContent = `⚡ ${game.gameType || 'Activity'}`;

        // Color-code activity badge based on gameType
        if (game.gameType === 'Sequence Order') {
            actTag.style.cssText = 'background:#ecfdf5; color:#065f46; border:1px solid #a7f3d0; font-size:11px; font-weight:800; border-radius:999px; padding:3px 10px; display:inline-flex;';
        } else if (game.gameType === 'Fill in the Blank') {
            actTag.style.cssText = 'background:#fffbeb; color:#92400e; border:1px solid #fde68a; font-size:11px; font-weight:800; border-radius:999px; padding:3px 10px; display:inline-flex;';
        } else if (game.gameType === 'Match Pairs') {
            actTag.style.cssText = 'background:#eff6ff; color:#1e40af; border:1px solid #bfdbfe; font-size:11px; font-weight:800; border-radius:999px; padding:3px 10px; display:inline-flex;';
        } else if (game.gameType === 'Sort & Group') {
            actTag.style.cssText = 'background:#fdf2f8; color:#9d174d; border:1px solid #fbcfe8; font-size:11px; font-weight:800; border-radius:999px; padding:3px 10px; display:inline-flex;';
        } else if (game.gameType === 'Word Scramble') {
            actTag.style.cssText = 'background:#f5f3ff; color:#5b21b6; border:1px solid #ddd6fe; font-size:11px; font-weight:800; border-radius:999px; padding:3px 10px; display:inline-flex;';
        } else {
            actTag.style.cssText = 'background:#ede9fe; color:#5b21b6; border:1px solid #c4b5fd; font-size:11px; font-weight:800; border-radius:999px; padding:3px 10px; display:inline-flex;';
        }
    }

    // Clean & format question prompt (Highlight blanks for Fill in the Blank)
    let rawPrompt = cleanQuestionPrompt(q.prompt);
    if (game.gameType === 'Fill in the Blank' || rawPrompt.includes('_____')) {
        document.getElementById('questPromptTitle').innerHTML = rawPrompt.replace(/_{3,}/g, '<span class="fitb-blank">[ ________ ]</span>');
    } else {
        document.getElementById('questPromptTitle').textContent = rawPrompt;
    }

    // Multi-Modal Visual Clue & Diagram Rendering
    const visualCont = document.getElementById('questVisualContainer');
    const diagBox = document.getElementById('questDiagramBox');
    const cluePill = document.getElementById('questCluePill');

    if (visualCont && diagBox && cluePill) {
        const hasSvg = q.svg_diagram && q.svg_diagram.includes('<svg');
        const hasClue = q.visual_hint && q.visual_hint.trim().length > 0;

        if (hasSvg || hasClue) {
            visualCont.style.display = 'flex';
            if (hasSvg) {
                diagBox.innerHTML = q.svg_diagram;
                diagBox.style.display = 'flex';
            } else {
                diagBox.innerHTML = '';
                diagBox.style.display = 'none';
            }

            if (hasClue) {
                cluePill.textContent = '💡 Visual Clue: ' + cleanVisualHint(q.visual_hint);
                cluePill.style.display = 'inline-flex';
            } else {
                cluePill.textContent = '';
                cluePill.style.display = 'none';
            }
        } else {
            visualCont.style.display = 'none';
        }
    }

    const grid = document.getElementById('questChoicesGrid');
    grid.innerHTML = '';

    const isTypedInput = q.type === 'typed' || (game.gameType === 'Typing Answer' && (!q.options || q.options.length <= 1));

    if (isTypedInput) {
        const userAns = AppState.missionAnswers[AppState.missionStep] || '';
        const isAnswered = String(userAns).trim().length > 0;
        grid.style.gridTemplateColumns = '1fr';
        grid.innerHTML = `
                    <div style="background: #ffffff; border: 1.5px solid #cbd5e1; border-radius: 14px; padding: 18px 20px;">
                        <label style="display: block; font-family: var(--font-heading); font-size: 13px; font-weight: 700; color: #475569; margin-bottom: 8px;">
                            ✍️ Type your response below:
                        </label>
                        <div style="display: flex; gap: 10px;">
                            <input type="text" id="standardTypedInput" value="${escapeHtml(userAns)}" placeholder="Type your answer here..." style="flex: 1; padding: 12px 16px; border: 2px solid #e2e8f0; border-radius: 10px; font-size: 15px; outline: none; font-family: var(--font-body);" ${isAnswered ? '' : 'autofocus'}>
                            <button type="button" class="btn-typed-submit" id="btnSubmitStandardTyped" onclick="submitStandardTypedAnswer()" style="background: #4f46e5; color: #ffffff; border: none; border-radius: 10px; padding: 12px 20px; font-weight: 700; cursor: pointer;">
                                ${isAnswered ? 'Update ✓' : 'Save Answer ✓'}
                            </button>
                        </div>
                    </div>
                `;
        const inp = document.getElementById('standardTypedInput');
        if (inp) {
            inp.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') submitStandardTypedAnswer();
            });
        }
    } else {
        grid.style.gridTemplateColumns = '';
        const keys = ['A', 'B', 'C', 'D'];
        const badgeClasses = ['badge-a', 'badge-b', 'badge-c', 'badge-d'];

        (q.options || []).forEach((optText, idx) => {
            const isSelected = AppState.missionAnswers[AppState.missionStep] === idx;
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.className = `quest-choice-btn ${isSelected ? 'selected' : ''}`;
            btn.onclick = () => {
                QuestAudio.playClick();
                AppState.missionAnswers[AppState.missionStep] = idx;
                renderQuestStep();
            };

            btn.innerHTML = `
                        <div class="choice-main-content">
                            <span class="choice-key-badge ${badgeClasses[idx % 4]}">${keys[idx % 4]}</span>
                            <span style="line-height: 1.4;">${optText}</span>
                        </div>
                        <div class="choice-check-indicator">✓</div>
                    `;
            grid.appendChild(btn);
        });
    }

    document.getElementById('btnQuestPrev').style.visibility = AppState.missionStep > 0 ? 'visible' : 'hidden';
    document.getElementById('btnQuestNext').innerHTML = AppState.missionStep === total - 1
        ? 'Submit Challenge <span>🚀</span>'
        : 'Next question <span>→</span>';
}

function submitStandardTypedAnswer() {
    const inp = document.getElementById('standardTypedInput');
    if (!inp) return;
    const text = inp.value.trim();
    if (!text) {
        showToastNotification("Please type your answer! ✍️");
        return;
    }
    QuestAudio.playClick();
    AppState.missionAnswers[AppState.missionStep] = text;
    renderQuestStep();
}

/* ====================================================
   QUEST CONTEXT STUDIO & AUDIO PLAYBACK ENGINE
   Handles spoken scripts, lab procedure steps, and
   interactive sequence ordering practice.
   ==================================================== */
let activeContextAudioUtterance = null;
let isContextAudioPlaying = false;
let isContextBodyCollapsed = false;
let isSequencePracticeOpen = false;
let currentShuffledSteps = [];

function renderQuestContext(game) {
    const ctxCard = document.getElementById('questContextCard');
    if (!ctxCard) return;

    const hasInstructions = Array.isArray(game.instructions) && game.instructions.length > 0;
    const hasAudioScript = !!(game.audio_script && game.audio_script.trim().length > 0);
    const hasStory = !!(game.story && game.story.trim().length > 0);
    const hasContext = hasInstructions || hasAudioScript || hasStory || game.skillArea === 'Listening';

    if (!hasContext) {
        ctxCard.style.display = 'none';
        return;
    }

    ctxCard.style.display = 'block';

    const ctxIcon = document.getElementById('questContextIcon');
    const ctxTitle = document.getElementById('questContextTitle');
    const ctxSubtitle = document.getElementById('questContextSubtitle');
    const ctxPill = document.getElementById('questContextPill');
    const stepsList = document.getElementById('questStepsList');
    const narrativeBox = document.getElementById('questNarrativeBox');
    const practiceBtn = document.getElementById('btnContextPracticeSeq');
    const seqInteractiveBox = document.getElementById('questSeqInteractiveBox');

    // Icon & Pill Badges
    if (game.skillArea === 'Listening') {
        ctxIcon.textContent = '🎧';
        ctxPill.textContent = 'Listening Studio';
        ctxPill.style.background = '#ede9fe';
        ctxPill.style.color = '#5b21b6';
    } else if (game.gameType === 'Sequence Order') {
        ctxIcon.textContent = game.subject === 'Science' ? '🔬' : (game.subject === 'Social Science' ? '⏳' : '🔢');
        ctxPill.textContent = 'Sequence Order';
        ctxPill.style.background = '#ecfdf5';
        ctxPill.style.color = '#065f46';
    } else {
        ctxIcon.textContent = '📋';
        ctxPill.textContent = game.gameType || 'Context';
    }

    // Title & Subtitle
    if (hasInstructions) {
        if (game.subject === 'Science') {
            ctxTitle.textContent = '🔬 Laboratory Procedure & Steps';
            ctxSubtitle.textContent = 'Follow the numbered procedure steps to answer this quest accurately';
        } else if (game.subject === 'Social Science') {
            ctxTitle.textContent = '⏳ Historical Timeline & Sequence';
            ctxSubtitle.textContent = 'Follow the chronological sequence of events to solve this challenge';
        } else {
            ctxTitle.textContent = '📋 Step-by-Step Instructions';
            ctxSubtitle.textContent = 'Follow the sequence of instructions below to answer this quest';
        }
    } else {
        ctxTitle.textContent = game.skillArea === 'Listening' ? '🎧 Spoken Audio Script & Passage' : '📖 Story & Background Context';
        ctxSubtitle.textContent = 'Listen carefully to the audio narration or read along below';
    }

    // Steps vs Narrative
    if (hasInstructions) {
        stepsList.style.display = 'flex';
        narrativeBox.style.display = 'none';
        stepsList.innerHTML = '';

        game.instructions.forEach((stepText, idx) => {
            const stepItem = document.createElement('div');
            stepItem.className = 'quest-step-item';

            // Highlight step if current question refers to this step
            const currentQ = (game.questions && game.questions[AppState.missionStep]) ? game.questions[AppState.missionStep] : null;
            const qPrompt = currentQ ? currentQ.prompt.toLowerCase() : '';

            const stepMatch = (idx === 0 && (qPrompt.includes('first') || qPrompt.includes('step 1') || qPrompt.includes('label three'))) ||
                (idx === 1 && (qPrompt.includes('second') || qPrompt.includes('step 2') || qPrompt.includes('distilled water'))) ||
                (idx === 2 && (qPrompt.includes('third') || qPrompt.includes('step 3') || qPrompt.includes('indicator') || qPrompt.includes('tube b'))) ||
                (idx === 3 && (qPrompt.includes('fourth') || qPrompt.includes('step 4') || qPrompt.includes('swirl') || qPrompt.includes('after swirling'))) ||
                (idx === 4 && (qPrompt.includes('fifth') || qPrompt.includes('step 5') || qPrompt.includes('final') || qPrompt.includes('last') || qPrompt.includes('record')));

            if (stepMatch) {
                stepItem.classList.add('is-highlighted');
            }

            const prefix = (game.subject === 'Social Science' && (stepText.startsWith('Era') || stepText.startsWith('Epoch') || stepText.startsWith('Period')))
                ? 'Timeline ' + (idx + 1)
                : 'Step ' + (idx + 1);

            stepItem.innerHTML = `
                        <span class="step-num-pill">${prefix}</span>
                        <span class="step-item-text">${escapeHtml(stepText)}</span>
                    `;
            stepsList.appendChild(stepItem);
        });

        if (practiceBtn) {
            practiceBtn.style.display = (game.gameType === 'Sequence Order') ? 'inline-flex' : 'none';
        }
    } else {
        stepsList.style.display = 'none';
        narrativeBox.style.display = 'block';
        narrativeBox.innerHTML = `
                    <div style="font-style: italic; color: #475569; margin-bottom: 6px; font-size: 12px; font-weight: 700;">
                        ${game.skillArea === 'Listening' ? '🎙️ Spoken Passage:' : '📜 Context:'}
                    </div>
                    <div>${escapeHtml(game.audio_script || game.story)}</div>
                `;
        if (practiceBtn) practiceBtn.style.display = 'none';
    }

    if (seqInteractiveBox && !isSequencePracticeOpen) {
        seqInteractiveBox.style.display = 'none';
    }
}

function toggleContextAudio() {
    const game = AppState.activeMissionGame;
    if (!game) return;

    const btn = document.getElementById('btnContextAudioPlay');
    const icon = document.getElementById('contextAudioBtnIcon');
    const label = document.getElementById('contextAudioBtnLabel');

    if (isContextAudioPlaying) {
        if ('speechSynthesis' in window) window.speechSynthesis.cancel();
        isContextAudioPlaying = false;
        if (btn) btn.classList.remove('is-playing');
        if (icon) icon.textContent = '▶';
        if (label) label.textContent = 'Listen to Audio';
        return;
    }

    const textToSpeak = game.audio_script || (game.instructions ? game.instructions.join('. ') : '') || game.story;
    if (!textToSpeak) {
        showToastNotification("No audio narration available for this activity.");
        return;
    }

    if (!('speechSynthesis' in window)) {
        showToastNotification("Speech synthesis is not supported in this browser.");
        return;
    }

    window.speechSynthesis.cancel();
    const utter = new SpeechSynthesisUtterance(textToSpeak);
    utter.rate = 0.90;
    utter.pitch = 1.05;

    const voices = window.speechSynthesis.getVoices();
    const enVoice = voices.find(v => v.lang.startsWith('en-IN')) || voices.find(v => v.lang.startsWith('en'));
    if (enVoice) utter.voice = enVoice;

    utter.onstart = () => {
        isContextAudioPlaying = true;
        if (btn) btn.classList.add('is-playing');
        if (icon) icon.textContent = '⏹';
        if (label) label.textContent = 'Stop Audio';
    };

    utter.onend = () => {
        isContextAudioPlaying = false;
        if (btn) btn.classList.remove('is-playing');
        if (icon) icon.textContent = '▶';
        if (label) label.textContent = 'Listen to Audio';
    };

    utter.onerror = () => {
        isContextAudioPlaying = false;
        if (btn) btn.classList.remove('is-playing');
        if (icon) icon.textContent = '▶';
        if (label) label.textContent = 'Listen to Audio';
    };

    activeContextAudioUtterance = utter;
    window.speechSynthesis.speak(utter);
}

function toggleContextBody() {
    const body = document.getElementById('questContextBody');
    const label = document.getElementById('contextToggleLabel');
    if (!body) return;
    isContextBodyCollapsed = !isContextBodyCollapsed;
    body.style.display = isContextBodyCollapsed ? 'none' : 'block';
    if (label) label.textContent = isContextBodyCollapsed ? 'Show Details' : 'Hide Details';
}

function toggleSequenceOrderPractice() {
    const game = AppState.activeMissionGame;
    if (!game || !game.instructions || game.instructions.length === 0) return;

    const box = document.getElementById('questSeqInteractiveBox');
    if (!box) return;

    isSequencePracticeOpen = !isSequencePracticeOpen;
    if (!isSequencePracticeOpen) {
        box.style.display = 'none';
        return;
    }

    box.style.display = 'block';
    // Shuffle steps
    currentShuffledSteps = game.instructions.map((text, originalIndex) => ({
        text,
        originalIndex
    })).sort(() => Math.random() - 0.5);

    renderSequenceOrderPractice(game);
}

function renderSequenceOrderPractice(game) {
    const box = document.getElementById('questSeqInteractiveBox');
    if (!box) return;

    const isAllCorrect = currentShuffledSteps.every((item, idx) => item.originalIndex === idx);

    let html = `
                <div class="seq-practice-head">
                    <div class="seq-practice-title">🔄 Step Re-ordering Practice: Arrange the steps in the correct order (1 to ${currentShuffledSteps.length})</div>
                    <button type="button" class="btn-context-toggle" onclick="toggleSequenceOrderPractice()">Close ✕</button>
                </div>
                <div class="seq-slots-list">
            `;

    currentShuffledSteps.forEach((item, idx) => {
        const isCorrectSlot = item.originalIndex === idx;
        html += `
                    <div class="seq-draggable-step ${isCorrectSlot ? 'is-correct-slot' : ''}">
                        <div style="display: flex; align-items: center; gap: 10px; flex: 1;">
                            <span class="step-num-pill" style="${isCorrectSlot ? 'background:#10b981;' : ''}">Slot ${idx + 1} ${isCorrectSlot ? '✓' : ''}</span>
                            <span style="font-size: 13.5px; font-weight: 500; color: #1e293b; line-height: 1.4;">${escapeHtml(item.text)}</span>
                        </div>
                        <div class="seq-step-arrows">
                            <button type="button" class="btn-seq-move" onclick="moveSequenceStep(${idx}, -1)" ${idx === 0 ? 'disabled style=\"opacity:0.3; cursor:default;\"' : ''} title=\"Move up\">▲</button>
                            <button type="button" class="btn-seq-move" onclick="moveSequenceStep(${idx}, 1)" ${idx === currentShuffledSteps.length - 1 ? 'disabled style=\"opacity:0.3; cursor:default;\"' : ''} title=\"Move down\">▼</button>
                        </div>
                    </div>
                `;
    });

    html += `</div>`;

    if (isAllCorrect) {
        html += `
                    <div style="margin-top: 12px; background: #ecfdf5; border: 1.5px solid #a7f3d0; border-radius: 10px; padding: 10px 14px; color: #065f46; font-weight: 700; font-size: 13.5px; text-align: center;">
                        🎉 Outstanding! You arranged all steps in perfect order!
                    </div>
                `;
        QuestAudio.playCorrect();
    }

    box.innerHTML = html;
}

function moveSequenceStep(index, direction) {
    const targetIndex = index + direction;
    if (targetIndex < 0 || targetIndex >= currentShuffledSteps.length) return;
    const temp = currentShuffledSteps[index];
    currentShuffledSteps[index] = currentShuffledSteps[targetIndex];
    currentShuffledSteps[targetIndex] = temp;
    QuestAudio.playClick();
    renderSequenceOrderPractice(AppState.activeMissionGame);
}

function navigateQuest(delta) {
    if ('speechSynthesis' in window) window.speechSynthesis.cancel();
    isContextAudioPlaying = false;
    const audioBtn = document.getElementById('btnContextAudioPlay');
    if (audioBtn) audioBtn.classList.remove('is-playing');
    const icon = document.getElementById('contextAudioBtnIcon');
    if (icon) icon.textContent = '▶';
    const label = document.getElementById('contextAudioBtnLabel');
    if (label) label.textContent = 'Listen to Audio';

    const total = AppState.activeMissionGame.questions.length;
    const next = AppState.missionStep + delta;

    if (next >= total) {
        finishQuestAndShowReview();
    } else if (next >= 0) {
        AppState.missionStep = next;
        renderQuestStep();
    }
}

function speakCurrentQuestPrompt() {
    if (!('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();
    const game = AppState.activeMissionGame;
    const q = game && game.questions ? game.questions[AppState.missionStep] : null;
    if (!q) return;

    let textToSpeak = cleanQuestionPrompt(q.prompt);
    textToSpeak = textToSpeak.replace(/_{2,}/g, 'blank');

    if (q.options && q.options.length > 0) {
        textToSpeak += '. Option A: ' + q.options[0] + '. Option B: ' + q.options[1];
        if (q.options[2]) textToSpeak += '. Option C: ' + q.options[2];
        if (q.options[3]) textToSpeak += '. Option D: ' + q.options[3];
    }

    const utter = new SpeechSynthesisUtterance(textToSpeak);
    utter.rate = 0.95;
    utter.pitch = 1.05;
    window.speechSynthesis.speak(utter);
}

function retakeCurrentQuest() {
    showToastNotification("Activity completed! You do not need to do this task again. 🎉");
    closeQuestRunner();
}

/* ====================================================
   FINISH QUEST & POST-TEST ANSWER REVIEW
   ==================================================== */
function finishQuestAndShowReview() {
    if ('speechSynthesis' in window) window.speechSynthesis.cancel();
    QuestAudio.playFanfare();
    launchQuestConfetti();

    const game = AppState.activeMissionGame;
    const qList = game.questions;
    const total = qList.length;

    let correct = 0;
    qList.forEach((q, idx) => {
        if (isAnswerCorrect(q, AppState.missionAnswers[idx])) correct++;
    });

    const wrong = total - correct;
    const pct = Math.round((correct / total) * 100);

    // Save completed state to assignments (only if not in Teacher Preview Mode)
    if (AppState.selectedStudent && AppState.selectedStudent.name !== "Teacher Preview Mode") {
        let existing = AppState.assignments.find(a =>
            a.class === AppState.selectedClass &&
            a.gameId === game.id &&
            a.student === AppState.selectedStudent.name
        );

        if (existing) {
            existing.status = 'completed';
            existing.score = correct;
            existing.maxScore = total;
        } else {
            AppState.assignments.push({
                id: "asg-" + Date.now(),
                class: AppState.selectedClass,
                subject: game.subject,
                skillArea: game.skillArea || '',
                activity: game.activity || '',
                gameId: game.id,
                gameTitle: game.title,
                student: AppState.selectedStudent.name,
                roll: AppState.selectedStudent.roll,
                status: 'completed',
                score: correct,
                maxScore: total
            });
        }
        saveAssignments();
    }
    renderKidZone();
    renderTeacherHub();
    if (AppState.currentView === 'split') {
        renderSplitViews();
    }

    // Populate Review Header
    const trophyEl = document.getElementById('celebTrophyEmoji');
    const titleEl = document.getElementById('celebMainTitle');
    const subEl = document.getElementById('celebSubTitle');
    const isTeacherPreview = AppState.selectedStudent && AppState.selectedStudent.name === "Teacher Preview Mode";
    const celebNotice = document.getElementById('celebCompletedNotice');
    if (celebNotice) {
        celebNotice.style.display = isTeacherPreview ? 'none' : 'inline-flex';
    }

    if (isTeacherPreview) {
        trophyEl.textContent = '👁️';
        titleEl.textContent = 'PREVIEW COMPLETED';
        subEl.textContent = `Teacher Preview for ${game.title}. Questions and answers evaluated successfully!`;
    } else if (pct === 100) {
        trophyEl.textContent = '🌟';
        titleEl.textContent = 'PERFECT SCORE! 🏆';
        subEl.textContent = `Amazing work, ${AppState.selectedStudent.name}! You scored 100% on ${game.title}!`;
    } else if (pct >= 65) {
        trophyEl.textContent = '🎉';
        titleEl.textContent = 'GREAT JOB! ⭐';
        subEl.textContent = `Well done, ${AppState.selectedStudent.name}! Here is your answer review:`;
    } else {
        trophyEl.textContent = '💪';
        titleEl.textContent = 'NICE EFFORT! 🚀';
        subEl.textContent = `Good try, ${AppState.selectedStudent.name}! Check the explanations below to learn more!`;
    }

    document.getElementById('reviewScoreText').textContent = `${correct} / ${total}`;
    document.getElementById('reviewAccuracyText').textContent = `${pct}%`;
    document.getElementById('reviewCorrectText').textContent = `${correct}`;
    document.getElementById('reviewWrongText').textContent = `${wrong}`;

    // Populate Detailed Question Review Cards
    const reviewList = document.getElementById('reviewAnswersList');
    reviewList.innerHTML = '';

    qList.forEach((q, idx) => {
        const userChoice = AppState.missionAnswers[idx];
        const isAnswered = userChoice !== undefined && userChoice !== null && String(userChoice).trim().length > 0;
        const isCorrect = isAnswered && isAnswerCorrect(q, userChoice);
        const userText = isAnswered
            ? (q.type === 'typed' ? escapeHtml(String(userChoice)) : (q.options ? q.options[userChoice] : String(userChoice)))
            : 'Not answered';
        const correctText = q.type === 'typed' ? q.answer : (q.options ? q.options[q.answer] : q.answer);

        const card = document.createElement('div');
        card.className = `review-q-card ${isCorrect ? 'is-correct' : 'is-wrong'}`;

        card.innerHTML = `
                    <div class="review-card-head">
                        <div style="flex: 1;">
                            <span style="font-size: 11px; font-weight: 800; color: var(--text-muted); text-transform: uppercase;">Question ${idx + 1}</span>
                            <div class="review-q-prompt-text">${cleanQuestionPrompt(q.prompt)}</div>
                        </div>
                        <span class="review-badge-status ${isCorrect ? 'badge-ans-correct' : 'badge-ans-wrong'}">
                            ${isCorrect ? '✓ Correct (+1 ⭐)' : (isAnswered ? '✗ Incorrect' : '⚠️ Unanswered')}
                        </span>
                    </div>

                    <div class="review-pills-row">
                        <div class="ans-pill ${isCorrect ? 'ans-pill-user-correct' : 'ans-pill-user'}">
                            <strong>Your Answer:</strong> ${userText}
                        </div>
                        ${!isCorrect ? `
                        <div class="ans-pill ans-pill-solution">
                            <strong>Correct Solution:</strong> ${correctText}
                        </div>
                        ` : ''}
                    </div>

                    ${q.explanation ? `
                    <div class="review-exp-box">
                        <span>💡</span>
                        <div><strong>Why?</strong> ${q.explanation}</div>
                    </div>
                    ` : ''}

                    ${q.visual_hint ? `
                    <div style="font-size: 12.5px; color: #4338ca; background: #eef2ff; border-radius: 8px; padding: 6px 12px; margin-top: 8px; font-weight: 600; display: inline-flex; align-items: center; gap: 6px;">
                        <span>🎨 Visual Clue:</span> ${escapeHtml(cleanVisualHint(q.visual_hint))}
                    </div>
                    ` : ''}
                `;
        reviewList.appendChild(card);
    });

    document.getElementById('questActiveRunner').style.display = 'none';
    document.getElementById('questCelebrationRunner').style.display = 'block';
}

