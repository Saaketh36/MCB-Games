import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ----------------------------------------------------
# 1. FIX CSS: Modals, scrolling, full-screen game arena, custom scrollbars, dropdowns
# ----------------------------------------------------
old_modal_css_start = "/* ====================================================\n           MODALS (WHO'S PLAYING & ASSIGN & QUEST RUNNER)"
old_modal_css_end = "/* ====================================================\n           ASSIGN A GAME MODAL (TEACHER HUB)"

# Check if we can find modal CSS block
print('Modal CSS start found:', old_modal_css_start in html)

refined_css = """        /* ====================================================
           MODALS (WHO'S PLAYING & ASSIGN & QUEST RUNNER)
           Enhanced: Fullscreen Arena, Perfect Scrolling, No Cutoff
           ==================================================== */
        .modal-overlay {
            display: none;
            position: fixed;
            inset: 0;
            background: rgba(15, 23, 42, 0.72);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            z-index: 1000;
            overflow-y: auto;
            overflow-x: hidden;
            padding: 24px 16px;
            box-sizing: border-box;
            -webkit-overflow-scrolling: touch;
        }

        .modal-overlay.active {
            display: flex;
            align-items: flex-start;
            justify-content: center;
            min-height: 100%;
        }

        /* Custom Candy Scrollbars for all scrollable areas */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #fef3c7;
            border-radius: 999px;
        }
        ::-webkit-scrollbar-thumb {
            background: #f59e0b;
            border-radius: 999px;
            border: 2px solid #fef3c7;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #d97706;
        }

        /* Who's Playing Modal Card */
        .who-modal-card {
            background: #ffffff;
            border-radius: var(--radius-xl);
            max-width: 580px;
            width: 100%;
            margin: auto;
            padding: 28px 34px;
            box-shadow: 0 25px 60px rgba(0,0,0,0.25);
            animation: modalIn 0.22s cubic-bezier(0.34, 1.56, 0.64, 1);
            position: relative;
            border: 3px solid #fed7aa;
        }

        @keyframes modalIn {
            from { transform: scale(0.94) translateY(14px); opacity: 0; }
            to { transform: scale(1) translateY(0); opacity: 1; }
        }

        .who-header-top {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            margin-bottom: 16px;
        }

        .who-icon-bubble {
            width: 48px;
            height: 48px;
            border-radius: 16px;
            background: #ede9fe;
            color: var(--primary);
            font-size: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 10px;
            box-shadow: 0 4px 12px rgba(124, 58, 237, 0.15);
        }

        .who-modal-title {
            font-family: var(--font-heading);
            font-size: 23px;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 3px;
        }

        .who-modal-sub {
            font-size: 13.5px;
            color: var(--text-muted);
        }

        .modal-close-btn {
            background: #f1f5f9;
            border: none;
            width: 36px;
            height: 36px;
            border-radius: 50%;
            font-size: 17px;
            color: #64748b;
            cursor: pointer;
            transition: all 0.15s;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .modal-close-btn:hover {
            background: #fee2e2;
            color: #ef4444;
            transform: scale(1.08);
        }

        .who-search-input {
            width: 100%;
            background: #f8fafc;
            border: 2px solid #e2e8f0;
            border-radius: var(--radius-md);
            padding: 11px 16px 11px 42px;
            font-family: var(--font-heading);
            font-size: 13.5px;
            color: #0f172a;
            outline: none;
            margin-bottom: 16px;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='%2394a3b8' viewBox='0 0 256 256'%3E%3Cpath d='M229.66,218.34l-50.07-50.06a88.11,88.11,0,1,0-11.31,11.31l50.06,50.07a8,8,0,0,0,11.32-11.32ZM40,112a72,72,0,1,1,72,72A72.08,72.08,0,0,1,40,112Z'%3E%3C/path%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position: 14px center;
            transition: border-color 0.2s, box-shadow 0.2s;
        }

        .who-search-input:focus {
            border-color: var(--primary);
            background-color: #ffffff;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
        }

        .who-students-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            max-height: 250px;
            overflow-y: auto;
            margin-bottom: 20px;
            padding-right: 4px;
        }

        .who-student-card {
            background: #f8fafc;
            border: 2px solid #e2e8f0;
            border-radius: var(--radius-md);
            padding: 10px 12px;
            display: flex;
            align-items: center;
            gap: 10px;
            cursor: pointer;
            transition: all 0.15s;
        }

        .who-student-card:hover {
            border-color: #c7d2fe;
            background: #f5f3ff;
            transform: translateY(-2px);
        }

        .who-student-card.selected {
            border-color: var(--primary);
            background: #eef2ff;
            box-shadow: 0 4px 14px rgba(79, 70, 229, 0.18);
        }

        .who-avatar-badge {
            width: 36px;
            height: 36px;
            border-radius: 12px;
            font-family: var(--font-heading);
            font-size: 13px;
            font-weight: 700;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }

        .btn-start-challenge {
            width: 100%;
            background: linear-gradient(180deg, #6366f1 0%, #4f46e5 100%);
            color: #ffffff;
            border: none;
            padding: 14px;
            border-radius: var(--radius-md);
            font-family: var(--font-heading);
            font-size: 15.5px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.15s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            box-shadow: 0 4px 0 #3730a3, 0 8px 18px rgba(79, 70, 229, 0.25);
        }

        .btn-start-challenge:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 6px 0 #3730a3, 0 12px 24px rgba(79, 70, 229, 0.35);
        }

        .btn-start-challenge:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            box-shadow: none;
        }

        /* ====================================================
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
        }

        .quest-footer-bar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding-top: 14px;
            border-top: 2px solid #fef3c7;
        }

        .quest-footer-hint {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 13.5px;
            color: #92400e;
            font-weight: 600;
            background: #fffbeb;
            padding: 8px 16px;
            border-radius: 999px;
            border: 1px solid #fde68a;
        }

        .btn-quest-back {
            background: #f8fafc;
            border: 2px solid #e2e8f0;
            border-radius: var(--radius-md);
            padding: 12px 20px;
            font-family: var(--font-heading);
            font-size: 14px;
            font-weight: 700;
            color: #64748b;
            cursor: pointer;
            transition: all 0.15s;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }

        .btn-quest-back:hover {
            background: #f1f5f9;
            color: #0f172a;
        }

        .btn-quest-next-step {
            background: linear-gradient(180deg, #10b981 0%, #059669 100%);
            border: none;
            border-radius: var(--radius-md);
            padding: 13px 28px;
            font-family: var(--font-heading);
            font-size: 15.5px;
            font-weight: 700;
            color: #ffffff;
            cursor: pointer;
            transition: all 0.15s;
            box-shadow: 0 4px 0 #047857, 0 8px 18px rgba(16, 185, 129, 0.3);
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }

        .btn-quest-next-step:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 0 #047857, 0 12px 24px rgba(16, 185, 129, 0.4);
        }

        .btn-quest-next-step:active {
            transform: translateY(2px);
            box-shadow: 0 2px 0 #047857;
        }

        /* Celebration & Answer Review Screen */
        .celebration-view {
            text-align: center;
            padding: 24px 10px;
        }

        .celeb-trophy-icon {
            font-size: 64px;
            margin-bottom: 8px;
            animation: bounce 1.2s infinite;
        }

        .celeb-title {
            font-family: var(--font-heading);
            font-size: 28px;
            font-weight: 700;
            color: #1e1b4b;
            margin-bottom: 6px;
        }

        .celeb-subtitle {
            font-size: 15px;
            color: var(--text-muted);
            margin-bottom: 24px;
        }

        .review-stats-row {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 16px;
            flex-wrap: wrap;
            margin-bottom: 28px;
        }

        .review-stat-item {
            background: #ffffff;
            border: 2px solid #fed7aa;
            border-radius: var(--radius-lg);
            padding: 16px 24px;
            min-width: 130px;
            box-shadow: 0 4px 12px rgba(245, 158, 11, 0.08);
        }

        .review-stat-val {
            font-family: var(--font-heading);
            font-size: 26px;
            font-weight: 700;
            margin-bottom: 2px;
        }

        .review-stat-lbl {
            font-size: 12px;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.6px;
        }

        .review-cards-list {
            display: flex;
            flex-direction: column;
            gap: 14px;
            margin-bottom: 28px;
            text-align: left;
            max-height: 380px;
            overflow-y: auto;
            padding-right: 6px;
        }

        .review-q-card {
            background: #ffffff;
            border: 2px solid #e2e8f0;
            border-radius: var(--radius-md);
            padding: 16px 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.03);
        }

        .review-q-card.is-correct {
            border-color: #86efac;
            border-left: 6px solid #10b981;
            background: linear-gradient(180deg, #ffffff, #f0fdf4);
        }

        .review-q-card.is-wrong {
            border-color: #fca5a5;
            border-left: 6px solid #ef4444;
            background: linear-gradient(180deg, #ffffff, #fef2f2);
        }

        .review-card-head {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 12px;
            margin-bottom: 10px;
        }

        .review-q-prompt-text {
            font-family: var(--font-heading);
            font-size: 15.5px;
            font-weight: 700;
            color: #0f172a;
            line-height: 1.4;
        }

        .review-badge-status {
            font-family: var(--font-heading);
            font-size: 11.5px;
            font-weight: 700;
            padding: 3px 10px;
            border-radius: 999px;
            flex-shrink: 0;
        }

        .badge-ans-correct { background: #dcfce7; color: #15803d; border: 1.5px solid #86efac; }
        .badge-ans-wrong { background: #fee2e2; color: #b91c1c; border: 1.5px solid #fca5a5; }

        .review-pills-row {
            display: flex;
            flex-direction: column;
            gap: 6px;
            font-size: 13px;
            margin-bottom: 8px;
        }

        .ans-pill {
            padding: 7px 12px;
            border-radius: 10px;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-family: var(--font-heading);
            font-size: 13px;
            font-weight: 600;
        }

        .ans-pill-user { background: #fee2e2; color: #991b1b; }
        .ans-pill-user-correct { background: #dcfce7; color: #166534; }
        .ans-pill-solution { background: #ecfdf5; color: #065f46; border: 1.5px solid #a7f3d0; }

        .review-exp-box {
            background: #fffbeb;
            border: 1.5px solid #fde68a;
            border-radius: 10px;
            padding: 8px 12px;
            font-size: 12.5px;
            color: #92400e;
            display: flex;
            align-items: flex-start;
            gap: 6px;
        }

        .review-actions-row {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 16px;
        }

        /* ====================================================
           ASSIGN A GAME MODAL (TEACHER HUB)
           Polished, No Cutoff, Clean Layout
           ==================================================== */
        .assign-modal-card {
            background: #ffffff;
            border-radius: var(--radius-xl);
            max-width: 580px;
            width: 100%;
            margin: auto;
            padding: 26px 32px;
            box-shadow: 0 25px 60px rgba(0,0,0,0.28);
            animation: modalIn 0.22s cubic-bezier(0.34, 1.56, 0.64, 1);
            border: 3px solid #fed7aa;
            position: relative;
        }

        .assign-form-group {
            margin-bottom: 13px;
        }

        .assign-label {
            display: block;
            font-family: var(--font-heading);
            font-size: 13.5px;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 5px;
        }

        .assign-select {
            width: 100%;
            padding: 10px 14px;
            border-radius: var(--radius-md);
            border: 2px solid #e2e8f0;
            font-family: var(--font-heading);
            font-size: 13.5px;
            color: #0f172a;
            outline: none;
            background: #f8fafc;
            transition: all 0.15s;
        }

        .assign-select:focus {
            border-color: #6366f1;
            background: #ffffff;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
        }

        .assign-students-list {
            max-height: 160px;
            overflow-y: auto;
            border: 2px solid #e2e8f0;
            border-radius: var(--radius-md);
            padding: 8px 12px;
            display: flex;
            flex-direction: column;
            gap: 6px;
            background: #f8fafc;
        }

        .student-check-row {
            display: flex;
            align-items: center;
            gap: 10px;
            font-family: var(--font-heading);
            font-size: 13.5px;
            font-weight: 600;
            color: #1e293b;
            cursor: pointer;
            padding: 6px 10px;
            border-radius: 8px;
            background: #ffffff;
            border: 1px solid #f1f5f9;
            transition: all 0.15s;
        }

        .student-check-row:hover {
            background: #eef2ff;
            border-color: #c7d2fe;
        }

        .student-check-row input[type="checkbox"] {
            width: 16px;
            height: 16px;
            accent-color: #6366f1;
            cursor: pointer;
        }

        .btn-clear-assignments-sm {
            background: #fef2f2;
            border: 1.5px solid #fca5a5;
            color: #b91c1c;
            padding: 7px 14px;
            border-radius: 999px;
            font-family: var(--font-heading);
            font-size: 12px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.15s;
            display: inline-flex;
            align-items: center;
            gap: 5px;
        }

        .btn-clear-assignments-sm:hover {
            background: #fee2e2;
            border-color: #ef4444;
            transform: translateY(-1px);
        }
"""

# Replace CSS block from start of modals to end of assign-modal-card
css_pattern = r'/\* ====================================================\s*MODALS \(WHO\'S PLAYING & ASSIGN & QUEST RUNNER\).*?\.assign-modal-card\s*\{[^}]*\}'
match = re.search(css_pattern, html, flags=re.DOTALL)
if match:
    # replace up to end of assign-modal-card
    html = re.sub(css_pattern, refined_css, html, flags=re.DOTALL)
    print('CSS successfully updated!')
else:
    print('Warning: regex match for CSS not found, will search alternatives')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
