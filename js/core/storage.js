// Persistent Assignment Storage (Strict user-driven assignments only: NO auto-seeding)
const STORAGE_KEY = 'mcb_assignments_v8';

function loadSavedAssignments() {
    try {
        // Clear any legacy test keys so stale test assignments never linger
        ['mcb_assignments', 'mcb_assignments_v1', 'mcb_assignments_v2', 'mcb_assignments_v3', 'mcb_assignments_v4', 'mcb_assignments_v5', 'mcb_assignments_v6', 'mcb_assignments_v7', 'assignments'].forEach(k => {
            try { localStorage.removeItem(k); } catch (e) { }
        });

        const stored = localStorage.getItem(STORAGE_KEY);
        if (stored) {
            AppState.assignments = JSON.parse(stored);
            if (!Array.isArray(AppState.assignments)) {
                AppState.assignments = [];
            }
        } else {
            AppState.assignments = [];
        }
    } catch (e) {
        AppState.assignments = [];
    }
}

function saveAssignments() {
    try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(AppState.assignments));
    } catch (e) {
        console.error(e);
    }
}

function promptResetAssignments() {
    const modal = document.getElementById('resetConfirmModal');
    if (modal) {
        const classBtnLabel = document.getElementById('resetModalClassBtnLabel');
        if (classBtnLabel) classBtnLabel.textContent = `Class ${AppState.selectedClass}`;
        modal.classList.add('active');
        modal.style.display = 'flex';
    }
}

function closeResetModal() {
    const modal = document.getElementById('resetConfirmModal');
    if (modal) {
        modal.classList.remove('active');
        modal.style.display = 'none';
    }
}

function clearAllAssignments() {
    AppState.assignments = [];
    try {
        ['mcb_assignments', 'mcb_assignments_v1', 'mcb_assignments_v2', 'mcb_assignments_v3', 'mcb_assignments_v4', 'mcb_assignments_v5', 'mcb_assignments_v6', 'mcb_assignments_v7', 'mcb_assignments_v8', 'assignments'].forEach(k => {
            try { localStorage.removeItem(k); } catch (e) { }
        });
    } catch (e) { }
    saveAssignments();
    closeResetModal();
    renderTeacherHub();
    renderKidZone();
    if (AppState.currentView === 'split') {
        renderSplitViews();
    }
    showToastNotification("✨ All assignments for all classes reset to 0!");
}

function clearClassAssignments() {
    const cls = AppState.selectedClass;
    AppState.assignments = AppState.assignments.filter(a => a.class !== cls);
    saveAssignments();
    closeResetModal();
    renderTeacherHub();
    renderKidZone();
    if (AppState.currentView === 'split') {
        renderSplitViews();
    }
    showToastNotification(`✨ All assignments for Class ${cls} reset to 0!`);
}

function unassignActivity(gameId) {
    const cls = AppState.selectedClass;
    AppState.assignments = AppState.assignments.filter(a => !(a.class === cls && a.gameId === gameId));
    saveAssignments();
    renderTeacherHub();
    renderKidZone();
    if (AppState.currentView === 'split') {
        renderSplitViews();
    }
    showToastNotification("Activity unassigned successfully! ✨");
}

function toggleStudentAssignment(gameId, studentName, roll) {
    const cls = AppState.selectedClass;
    const game = GamesCatalog.find(g => g.id === gameId);
    if (!game) return;

    const existingIndex = AppState.assignments.findIndex(a =>
        a.class === cls && a.gameId === gameId && a.student === studentName
    );

    if (existingIndex >= 0) {
        const existing = AppState.assignments[existingIndex];
        if (existing.status === 'completed') {
            showToastNotification(`${studentName} has already completed this activity (Score: ${existing.score || 3}/${existing.maxScore || 3} ⭐)! Progress is preserved. ✨`);
            return;
        }
        AppState.assignments.splice(existingIndex, 1);
        saveAssignments();
        renderTeacherHub();
        renderKidZone();
        if (AppState.currentView === 'split') renderSplitViews();
        showToastNotification(`Unassigned ${studentName} from "${game.title}"`);
    } else {
        AppState.assignments.push({
            id: "asg-" + Date.now() + "-" + Math.random().toString(36).substr(2, 4),
            class: cls,
            subject: game.subject,
            skillArea: game.skillArea || '',
            activity: game.activity || '',
            gameId: game.id,
            gameTitle: game.title,
            student: studentName,
            roll: roll,
            status: 'pending',
            score: null,
            assignedDate: new Date().toISOString()
        });
        saveAssignments();
        renderTeacherHub();
        renderKidZone();
        if (AppState.currentView === 'split') renderSplitViews();
        showToastNotification(`Assigned "${game.title}" to ${studentName}! 🚀`);
    }
}

function assignAllStudentsToGame(gameId) {
    const cls = AppState.selectedClass;
    const game = GamesCatalog.find(g => g.id === gameId);
    if (!game) return;

    const roster = StudentRosters[cls] || [];
    let addedCount = 0;

    roster.forEach(st => {
        const alreadyAssigned = AppState.assignments.some(a =>
            a.class === cls && a.gameId === gameId && a.student === st.name
        );
        if (!alreadyAssigned) {
            AppState.assignments.push({
                id: "asg-" + Date.now() + "-" + Math.random().toString(36).substr(2, 4),
                class: cls,
                subject: game.subject,
                skillArea: game.skillArea || '',
                activity: game.activity || '',
                gameId: game.id,
                gameTitle: game.title,
                student: st.name,
                roll: st.roll,
                status: 'pending',
                score: null,
                assignedDate: new Date().toISOString()
            });
            addedCount++;
        }
    });

    saveAssignments();
    renderTeacherHub();
    renderKidZone();
    if (AppState.currentView === 'split') renderSplitViews();
    showToastNotification(`Assigned "${game.title}" to all ${roster.length} students in Class ${cls}! 👥✨`);
}

function showToastNotification(msg) {
    let toast = document.getElementById('mcbToastNotification');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'mcbToastNotification';
        toast.style.cssText = `
                    position: fixed;
                    bottom: 28px;
                    left: 50%;
                    transform: translateX(-50%) translateY(100px);
                    background: #1e1b4b;
                    color: #ffffff;
                    padding: 12px 24px;
                    border-radius: 999px;
                    font-family: var(--font-heading);
                    font-size: 14px;
                    font-weight: 700;
                    box-shadow: 0 12px 32px rgba(15, 23, 42, 0.4);
                    border: 1px solid #334155;
                    z-index: 99999;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    transition: transform 0.28s cubic-bezier(0.34, 1.56, 0.64, 1), opacity 0.28s;
                    opacity: 0;
                    pointer-events: none;
                `;
        document.body.appendChild(toast);
    }
    toast.textContent = msg;
    toast.style.opacity = '1';
    toast.style.transform = 'translateX(-50%) translateY(0)';
    if (window._mcbToastTimer) clearTimeout(window._mcbToastTimer);
    window._mcbToastTimer = setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(-50%) translateY(100px)';
    }, 3000);
}


Object.assign(window.MCB, {
    STORAGE_KEY,
    loadSavedAssignments, saveAssignments,
    promptResetAssignments, closeResetModal,
    clearAllAssignments, clearClassAssignments,
    unassignActivity, toggleStudentAssignment,
    assignAllStudentsToGame, showToastNotification
});
window.STORAGE_KEY = STORAGE_KEY;
