with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# -------------------------------------------------------------------
# 1. ENHANCE CSS: Quest Runner, Stepper, 3D Choices, Audio, Celebration
# -------------------------------------------------------------------
old_quest_css = """        /* ====================================================
           FULLSCREEN & IMMERSIVE GAME RUNNER ARENA
           ==================================================== */
        .quest-runner-card {
            background: 
                radial-gradient(circle at 10% 12%, rgba(254, 240, 138, 0.3) 0%, transparent 40%),
                radial-gradient(circle at 90% 88%, rgba(199, 210, 254, 0.35) 0%, transparent 45%),
                #ffffff;
            border-radius: var(--radius-xl);
            width: 95vw;
            max-width: 1140px;
            min-height: 82vh;
            max-height: 92vh;
            overflow-y: auto;
            margin: auto;
            padding: 28px 40px;
            box-shadow: 0 25px 70px rgba(15, 23, 42, 0.35);
            animation: modalIn 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
            position: relative;
            border: 3.5px solid #fed7aa;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        }

        /* True Fullscreen Mode when clicked */
        .quest-runner-card.is-fullscreen {
            width: 100vw !important;
            max-width: 100vw !important;
            height: 100vh !important;
            max-height: 100vh !important;
            border-radius: 0 !important;
            border: none !important;
            margin: 0 !important;
            padding: 32px 50px !important;
            position: fixed !important;
            inset: 0 !important;
            z-index: 9999 !important;
            box-shadow: none !important;
        }

        .quest-top-bar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 12px;
            padding-bottom: 14px;
            border-bottom: 2px solid #fef3c7;
            margin-bottom: 16px;
        }

        .quest-game-info {
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
        }

        .quest-game-title {
            font-family: var(--font-heading);
            font-size: 20px;
            font-weight: 700;
            color: #1e1b4b;
        }

        .quest-active-player-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: #ede9fe;
            color: #6d28d9;
            padding: 5px 12px;
            border-radius: 999px;
            font-family: var(--font-heading);
            font-size: 13px;
            font-weight: 700;
            border: 1.5px solid #ddd6fe;
        }

        .quest-top-controls {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .btn-quest-ctrl {
            background: #f8fafc;
            border: 1.5px solid #fed7aa;
            padding: 6px 14px;
            border-radius: 999px;
            font-family: var(--font-heading);
            font-size: 12.5px;
            font-weight: 700;
            color: #78350f;
            cursor: pointer;
            transition: all 0.15s;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }

        .btn-quest-ctrl:hover {
            background: #fef3c7;
            border-color: #f59e0b;
            transform: translateY(-1px);
        }

        /* Progress track */
        .quest-progress-track {
            height: 12px;
            background: #f1f5f9;
            border-radius: 999px;
            overflow: hidden;
            margin-bottom: 20px;
            border: 1.5px solid #e2e8f0;
            position: relative;
        }

        .quest-progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #6366f1, #ec4899, #f59e0b, #10b981);
            border-radius: 999px;
            transition: width 0.35s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 0 10px rgba(99, 102, 241, 0.4);
        }

        /* Question prompt display arena */
        .quest-prompt-card {
            background: linear-gradient(135deg, #fffbeb 0%, #ffffff 50%, #f0fdf4 100%);
            border: 2px solid #fed7aa;
            border-radius: var(--radius-lg);
            padding: 24px 30px;
            margin-bottom: 22px;
            box-shadow: 0 8px 20px rgba(245, 158, 11, 0.06);
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .quest-prompt-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .quest-prompt-title {
            font-family: var(--font-heading);
            font-size: 24px;
            font-weight: 700;
            color: #1e1b4b;
            line-height: 1.4;
            letter-spacing: -0.3px;
        }

        /* 2x2 Question Choice Grid (Bouncy Tactile Blocks) */
        .quest-choices-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 16px;
            margin-bottom: 24px;
        }

        .quest-choice-btn {
            background: #ffffff;
            border: 2.5px solid #e2e8f0;
            border-radius: var(--radius-lg);
            padding: 20px 24px;
            font-family: var(--font-heading);
            font-size: 17.5px;
            font-weight: 700;
            color: #1e293b;
            cursor: pointer;
            transition: all 0.18s cubic-bezier(0.34, 1.56, 0.64, 1);
            display: flex;
            align-items: center;
            gap: 16px;
            text-align: left;
            box-shadow: 0 4px 10px rgba(0,0,0,0.03);
            position: relative;
        }

        .quest-choice-btn:hover {
            border-color: #818cf8;
            background: #faf5ff;
            transform: translateY(-3px) scale(1.01);
            box-shadow: 0 10px 20px rgba(99, 102, 241, 0.15);
        }

        .quest-choice-btn.selected {
            border-color: #4f46e5;
            background: #eef2ff;
            box-shadow: 0 6px 20px rgba(79, 70, 229, 0.25);
            transform: scale(1.02);
        }

        .choice-key-badge {
            width: 40px;
            height: 40px;
            border-radius: 12px;
            background: #f1f5f9;
            color: #475569;
            font-family: var(--font-heading);
            font-weight: 800;
            font-size: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            transition: all 0.15s;
        }

        .quest-choice-btn.selected .choice-key-badge {
            background: #4f46e5;
            color: #ffffff;
        }"""

new_quest_css = """        /* ====================================================
           FULLSCREEN & IMMERSIVE GAME RUNNER ARENA (UPGRADED)
           ==================================================== */
        .quest-runner-card {
            background: 
                radial-gradient(circle at 5% 10%, rgba(254, 240, 138, 0.45) 0%, transparent 45%),
                radial-gradient(circle at 95% 90%, rgba(199, 210, 254, 0.5) 0%, transparent 50%),
                radial-gradient(circle at 50% 50%, rgba(255, 237, 213, 0.25) 0%, transparent 60%),
                #ffffff;
            border-radius: 32px;
            width: 95vw;
            max-width: 1120px;
            min-height: 84vh;
            max-height: 92vh;
            overflow-y: auto;
            margin: auto;
            padding: 28px 40px;
            box-shadow: 0 30px 80px rgba(15, 23, 42, 0.38), 0 0 0 1px rgba(255,255,255,0.8) inset;
            animation: modalIn 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
            position: relative;
            border: 3.5px solid #fed7aa;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        }

        /* True Fullscreen Mode */
        .quest-runner-card.is-fullscreen {
            width: 100vw !important;
            max-width: 100vw !important;
            height: 100vh !important;
            max-height: 100vh !important;
            border-radius: 0 !important;
            border: none !important;
            margin: 0 !important;
            padding: 28px 48px !important;
            position: fixed !important;
            inset: 0 !important;
            z-index: 9999 !important;
            box-shadow: none !important;
        }

        .quest-top-bar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 12px;
            padding-bottom: 16px;
            border-bottom: 2px solid #fef3c7;
            margin-bottom: 14px;
        }

        .quest-game-info {
            display: flex;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
        }

        .quest-game-title {
            font-family: var(--font-heading);
            font-size: 21px;
            font-weight: 800;
            color: #1e1b4b;
            letter-spacing: -0.3px;
        }

        .quest-active-player-pill {
            display: inline-flex;
            align-items: center;
            gap: 7px;
            background: linear-gradient(135deg, #ede9fe 0%, #f5f3ff 100%);
            color: #6d28d9;
            padding: 6px 14px;
            border-radius: 999px;
            font-family: var(--font-heading);
            font-size: 13px;
            font-weight: 700;
            border: 1.5px solid #ddd6fe;
            box-shadow: 0 2px 6px rgba(109, 40, 217, 0.1);
        }

        .quest-top-controls {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .btn-quest-ctrl {
            background: #ffffff;
            border: 2px solid #fed7aa;
            padding: 7px 15px;
            border-radius: 999px;
            font-family: var(--font-heading);
            font-size: 12.5px;
            font-weight: 700;
            color: #78350f;
            cursor: pointer;
            transition: all 0.18s cubic-bezier(0.34, 1.56, 0.64, 1);
            display: inline-flex;
            align-items: center;
            gap: 6px;
            box-shadow: 0 2px 5px rgba(245, 158, 11, 0.1);
        }

        .btn-quest-ctrl:hover {
            background: #fef3c7;
            border-color: #f59e0b;
            transform: translateY(-2px);
            box-shadow: 0 5px 12px rgba(245, 158, 11, 0.2);
        }

        .btn-quest-ctrl:active {
            transform: translateY(0);
        }

        /* Interactive Question Stepper Pills (Q1, Q2, Q3...) */
        .quest-stepper-row {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 14px;
            overflow-x: auto;
            padding: 4px 2px;
        }

        .quest-step-pill {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 5px;
            padding: 6px 14px;
            border-radius: 999px;
            font-family: var(--font-heading);
            font-size: 12.5px;
            font-weight: 800;
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
            background: #f1f5f9;
            color: #64748b;
            border: 2px solid #e2e8f0;
        }

        .quest-step-pill:hover {
            border-color: #cbd5e1;
            transform: translateY(-1px);
        }

        .quest-step-pill.active {
            background: #6366f1;
            color: #ffffff;
            border-color: #4f46e5;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.35);
            transform: scale(1.06);
        }

        .quest-step-pill.answered {
            background: #ecfdf5;
            color: #059669;
            border-color: #6ee7b7;
        }

        .quest-step-pill.answered.active {
            background: #10b981;
            color: #ffffff;
            border-color: #047857;
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
        }

        /* Smooth Candy Progress Track */
        .quest-progress-track {
            height: 12px;
            background: #f1f5f9;
            border-radius: 999px;
            overflow: hidden;
            margin-bottom: 20px;
            border: 2px solid #e2e8f0;
            position: relative;
        }

        .quest-progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #6366f1, #8b5cf6, #ec4899, #f59e0b, #10b981);
            background-size: 200% 100%;
            border-radius: 999px;
            transition: width 0.38s cubic-bezier(0.34, 1.56, 0.64, 1);
            box-shadow: 0 0 12px rgba(99, 102, 241, 0.5);
            animation: progressGradient 3s ease infinite;
        }

        @keyframes progressGradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Question prompt display arena (Enhanced & Tactile) */
        .quest-prompt-card {
            background: linear-gradient(135deg, #ffffff 0%, #fffbeb 50%, #f0fdf4 100%);
            border: 2.5px solid #fed7aa;
            border-radius: 24px;
            padding: 26px 32px;
            margin-bottom: 22px;
            box-shadow: 0 10px 25px rgba(245, 158, 11, 0.08);
            display: flex;
            flex-direction: column;
            gap: 14px;
            position: relative;
        }

        .quest-prompt-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 10px;
        }

        .btn-prompt-listen {
            background: #ede9fe;
            color: #6d28d9;
            border: 1.5px solid #ddd6fe;
            padding: 5px 14px;
            border-radius: 999px;
            font-family: var(--font-heading);
            font-size: 12.5px;
            font-weight: 700;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: all 0.15s;
        }

        .btn-prompt-listen:hover {
            background: #ddd6fe;
            transform: translateY(-1px);
        }

        .quest-prompt-title {
            font-family: var(--font-heading);
            font-size: 23px;
            font-weight: 800;
            color: #1e1b4b;
            line-height: 1.45;
            letter-spacing: -0.3px;
        }

        /* 2x2 Question Choice Grid (Bouncy Tactile 3D Blocks) */
        .quest-choices-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 16px;
            margin-bottom: 24px;
        }

        @media (max-width: 680px) {
            .quest-choices-grid {
                grid-template-columns: 1fr;
            }
        }

        .quest-choice-btn {
            background: #ffffff;
            border: 2.5px solid #e2e8f0;
            border-bottom: 4.5px solid #cbd5e1;
            border-radius: 20px;
            padding: 18px 24px;
            font-family: var(--font-heading);
            font-size: 17px;
            font-weight: 700;
            color: #1e293b;
            cursor: pointer;
            transition: all 0.18s cubic-bezier(0.34, 1.56, 0.64, 1);
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 14px;
            text-align: left;
            box-shadow: 0 4px 10px rgba(0,0,0,0.03);
            position: relative;
            outline: none;
        }

        .quest-choice-btn:hover {
            border-color: #a5b4fc;
            border-bottom-color: #818cf8;
            background: #faf5ff;
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(99, 102, 241, 0.15);
        }

        .quest-choice-btn:active {
            transform: translateY(1px);
            border-bottom-width: 2.5px;
        }

        .quest-choice-btn.selected {
            border-color: #6366f1;
            border-bottom: 4.5px solid #4338ca;
            background: linear-gradient(135deg, #eef2ff 0%, #f5f3ff 100%);
            box-shadow: 0 8px 24px rgba(99, 102, 241, 0.28);
            transform: translateY(-2px);
        }

        .choice-main-content {
            display: flex;
            align-items: center;
            gap: 14px;
            flex: 1;
        }

        .choice-key-badge {
            width: 42px;
            height: 42px;
            border-radius: 14px;
            background: #f1f5f9;
            color: #475569;
            font-family: var(--font-heading);
            font-weight: 800;
            font-size: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            transition: all 0.18s;
            border: 2px solid #e2e8f0;
        }

        /* Color-coded keys for engaging visual variety */
        .choice-key-badge.badge-a { background: #ede9fe; color: #6d28d9; border-color: #ddd6fe; }
        .choice-key-badge.badge-b { background: #d1fae5; color: #047857; border-color: #a7f3d0; }
        .choice-key-badge.badge-c { background: #fef3c7; color: #b45309; border-color: #fde68a; }
        .choice-key-badge.badge-d { background: #ffe4e6; color: #be123c; border-color: #fecdd3; }

        .quest-choice-btn.selected .choice-key-badge {
            background: #6366f1 !important;
            color: #ffffff !important;
            border-color: #4f46e5 !important;
            box-shadow: 0 3px 8px rgba(99, 102, 241, 0.4);
        }

        .choice-check-indicator {
            width: 26px;
            height: 26px;
            border-radius: 50%;
            border: 2px solid #cbd5e1;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 13px;
            color: transparent;
            transition: all 0.18s;
            flex-shrink: 0;
        }

        .quest-choice-btn.selected .choice-check-indicator {
            border-color: #6366f1;
            background: #6366f1;
            color: #ffffff;
            box-shadow: 0 2px 6px rgba(99, 102, 241, 0.4);
        }"""

if old_quest_css in html:
    html = html.replace(old_quest_css, new_quest_css)
    print("Replaced Quest CSS successfully!")
else:
    print("Warning: old_quest_css not found!")

# -------------------------------------------------------------------
# 2. ENHANCE HTML: Add Confetti Canvas, Sound Toggle, Stepper, etc.
# -------------------------------------------------------------------
old_quest_modal_html = """        <div class="quest-runner-card" id="questRunnerCard">
            <!-- Top Controls Bar -->
            <div class="quest-top-bar">
                <div class="quest-game-info">
                    <span class="tac-badge tac-badge-subject math" id="questGameSubjectBadge">Mathematics</span>
                    <h3 class="quest-game-title" id="questGameHeaderTitle">Multiply Maze</h3>
                    <div class="quest-active-player-pill" id="questActivePlayerPill">
                        <span>👤</span> <span id="questActivePlayerName">Player</span>
                    </div>
                </div>

                <div class="quest-top-controls">
                    <button type="button" class="btn-quest-ctrl" onclick="speakCurrentQuestPrompt()" title="Read prompt aloud">
                        <span>🔊</span> Read Aloud
                    </button>
                    <button type="button" class="btn-quest-ctrl" id="btnQuestFullscreen" onclick="toggleQuestFullscreen()" title="Toggle full screen arena">
                        <span>⛶</span> Fullscreen
                    </button>
                    <button type="button" class="modal-close-btn" onclick="closeQuestRunner()" title="Close Quest">✕</button>
                </div>
            </div>
            
            <!-- ACTIVE QUESTION RUNNER -->
            <div id="questActiveRunner">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <div style="font-family: var(--font-heading); font-size: 13.5px; font-weight: 700; color: #6d28d9;" id="questStepCounter">Question 1 of 3</div>
                    <div style="font-size: 12.5px; font-weight: 700; color: #b45309;" id="questPercentLabel">33% Complete ⭐</div>
                </div>

                <div class="quest-progress-track">
                    <div class="quest-progress-fill" id="questProgressFill" style="width: 33%;"></div>
                </div>

                <!-- Big Interactive Prompt Card -->
                <div class="quest-prompt-card">
                    <div class="quest-prompt-header">
                        <span class="tac-badge tac-badge-skill" id="questPromptSkillTag">🎯 Skill Area</span>
                        <span class="tac-badge tac-badge-act" id="questPromptActTag">⚡ Activity</span>
                    </div>
                    <h2 class="quest-prompt-title" id="questPromptTitle">
                        Loading challenge...
                    </h2>
                </div>"""

new_quest_modal_html = """        <div class="quest-runner-card" id="questRunnerCard">
            <!-- Canvas Confetti Overlay -->
            <canvas id="questConfettiCanvas" style="position: absolute; inset: 0; pointer-events: none; z-index: 50; width: 100%; height: 100%; border-radius: inherit;"></canvas>

            <!-- Top Controls Bar -->
            <div class="quest-top-bar">
                <div class="quest-game-info">
                    <span class="tac-badge tac-badge-subject math" id="questGameSubjectBadge">Mathematics</span>
                    <h3 class="quest-game-title" id="questGameHeaderTitle">Multiply Maze</h3>
                    <div class="quest-active-player-pill" id="questActivePlayerPill">
                        <span>👤</span> <span id="questActivePlayerName">Player</span>
                    </div>
                </div>

                <div class="quest-top-controls">
                    <button type="button" class="btn-quest-ctrl" id="btnQuestSoundToggle" onclick="toggleQuestSound()" title="Toggle sound effects">
                        <span id="questSoundIcon">🔊</span> Sound
                    </button>
                    <button type="button" class="btn-quest-ctrl" onclick="speakCurrentQuestPrompt()" title="Read prompt aloud">
                        <span>🗣️</span> Read Aloud
                    </button>
                    <button type="button" class="btn-quest-ctrl" id="btnQuestFullscreen" onclick="toggleQuestFullscreen()" title="Toggle full screen arena">
                        <span>⛶</span> Fullscreen
                    </button>
                    <button type="button" class="modal-close-btn" onclick="closeQuestRunner()" title="Close Quest">✕</button>
                </div>
            </div>
            
            <!-- ACTIVE QUESTION RUNNER -->
            <div id="questActiveRunner">
                <!-- Stepper Question Pills (Q1, Q2, Q3...) -->
                <div class="quest-stepper-row" id="questStepperRow">
                    <!-- Populated dynamically via renderQuestStep() -->
                </div>

                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <div style="font-family: var(--font-heading); font-size: 13.5px; font-weight: 800; color: #6d28d9;" id="questStepCounter">Question 1 of 3</div>
                    <div style="font-size: 13px; font-weight: 800; color: #b45309;" id="questPercentLabel">33% Complete ⭐</div>
                </div>

                <div class="quest-progress-track">
                    <div class="quest-progress-fill" id="questProgressFill" style="width: 33%;"></div>
                </div>

                <!-- Big Interactive Prompt Card -->
                <div class="quest-prompt-card">
                    <div class="quest-prompt-header">
                        <div style="display: flex; gap: 8px; align-items: center; flex-wrap: wrap;">
                            <span class="tac-badge tac-badge-skill" id="questPromptSkillTag">🎯 Skill Area</span>
                            <span class="tac-badge tac-badge-act" id="questPromptActTag">⚡ Activity</span>
                        </div>
                        <button type="button" class="btn-prompt-listen" onclick="speakCurrentQuestPrompt()" title="Listen to question">
                            <span class="listen-icon">🔊</span> Listen
                        </button>
                    </div>
                    <h2 class="quest-prompt-title" id="questPromptTitle">
                        Loading challenge...
                    </h2>
                </div>"""

if old_quest_modal_html in html:
    html = html.replace(old_quest_modal_html, new_quest_modal_html)
    print("Replaced Quest Modal HTML successfully!")
else:
    print("Warning: old_quest_modal_html not found!")

# -------------------------------------------------------------------
# 3. ENHANCE JS: Web Audio API sound generator, stepper renderer, confetti
# -------------------------------------------------------------------
old_render_quest_js = """        function renderQuestStep() {
            const game = AppState.activeMissionGame;
            const qList = game.questions;
            const total = qList.length;
            const q = qList[AppState.missionStep];

            document.getElementById('questStepCounter').textContent = `Question ${AppState.missionStep + 1} of ${total}`;
            const pct = Math.round(((AppState.missionStep + 1) / total) * 100);
            document.getElementById('questProgressFill').style.width = `${pct}%`;
            const pctLabel = document.getElementById('questPercentLabel');
            if (pctLabel) pctLabel.textContent = `${pct}% Complete ⭐`;

            const tips = [
                "Take your time. Curiosity is your superpower! 🚀",
                "Read carefully and trust your instincts! ⭐",
                "You are doing awesome, keep going! 🌟",
                "Every question makes you smarter! 💡"
            ];
            const tipEl = document.getElementById('questFooterTip');
            if (tipEl) tipEl.innerHTML = `<span>💡</span> ${tips[AppState.missionStep % tips.length]}`;

            document.getElementById('questPromptTitle').textContent = q.prompt;

            const grid = document.getElementById('questChoicesGrid');
            grid.innerHTML = '';
            const keys = ['A', 'B', 'C', 'D'];

            q.options.forEach((optText, idx) => {
                const isSelected = AppState.missionAnswers[AppState.missionStep] === idx;
                const btn = document.createElement('button');
                btn.type = 'button';
                btn.className = `quest-choice-btn ${isSelected ? 'selected' : ''}`;
                btn.onclick = () => {
                    AppState.missionAnswers[AppState.missionStep] = idx;
                    renderQuestStep();
                };

                btn.innerHTML = `
                    <span class="choice-key-badge">${keys[idx]}</span>
                    <span>${optText}</span>
                `;
                grid.appendChild(btn);
            });

            document.getElementById('btnQuestPrev').style.visibility = AppState.missionStep > 0 ? 'visible' : 'hidden';
            document.getElementById('btnQuestNext').innerHTML = AppState.missionStep === total - 1 
                ? 'Submit Challenge <span>🚀</span>' 
                : 'Next question <span>→</span>';
        }"""

new_render_quest_js = """        // Web Audio API Sound Synthesizer for Kids Quest
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
                } catch(e) {}
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
                } catch(e) {}
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
                } catch(e) {}
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

        function renderQuestStep() {
            const game = AppState.activeMissionGame;
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

            document.getElementById('questPromptTitle').textContent = q.prompt;

            const grid = document.getElementById('questChoicesGrid');
            grid.innerHTML = '';
            const keys = ['A', 'B', 'C', 'D'];
            const badgeClasses = ['badge-a', 'badge-b', 'badge-c', 'badge-d'];

            q.options.forEach((optText, idx) => {
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
                        <span class="choice-key-badge ${badgeClasses[idx]}">${keys[idx]}</span>
                        <span style="line-height: 1.4;">${optText}</span>
                    </div>
                    <div class="choice-check-indicator">✓</div>
                `;
                grid.appendChild(btn);
            });

            document.getElementById('btnQuestPrev').style.visibility = AppState.missionStep > 0 ? 'visible' : 'hidden';
            document.getElementById('btnQuestNext').innerHTML = AppState.missionStep === total - 1 
                ? 'Submit Challenge <span>🚀</span>' 
                : 'Next question <span>→</span>';
        }"""

if old_render_quest_js in html:
    html = html.replace(old_render_quest_js, new_quest_js := new_render_quest_js)
    print("Replaced Quest Step JS successfully!")
else:
    print("Warning: old_render_quest_js not found!")

# -------------------------------------------------------------------
# 4. In finishQuestAndShowReview(): Play fanfare and launch confetti!
# -------------------------------------------------------------------
old_finish_start = """        function finishQuestAndShowReview() {
            if ('speechSynthesis' in window) window.speechSynthesis.cancel();"""

new_finish_start = """        function finishQuestAndShowReview() {
            if ('speechSynthesis' in window) window.speechSynthesis.cancel();
            QuestAudio.playFanfare();
            launchQuestConfetti();"""

if old_finish_start in html:
    html = html.replace(old_finish_start, new_finish_start)
    print("Added fanfare and confetti to finishQuestAndShowReview!")
else:
    print("Warning: old_finish_start not found!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html with new Question Screen enhancements!")
