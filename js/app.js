// Initialize App on DOM ready
window.addEventListener('DOMContentLoaded', () => {
    loadSavedAssignments();
    loadCustomTasksIntoCatalog();
    updateSkillAreaOptions();

    // Sync class dropdowns with AppState default
    const kidSel = document.getElementById('kidClassSelect');
    const teachSel = document.getElementById('teacherClassSelect');
    if (kidSel) kidSel.value = AppState.selectedClass;
    if (teachSel) teachSel.value = AppState.selectedClass;

    renderKidZone();
    renderTeacherHub();
    checkAiStatus();

    // Direct deep-link via URL hash or view parameter
    const viewQuery = new URLSearchParams(window.location.search).get('view');
    if (viewQuery === 'teacher' || viewQuery === 'split') {
        switchMainView(viewQuery);
    }

    // Direct deep-link via URL hash (e.g., #quest=II-ENG-05 or ?quest=II-ENG-05)
    const hashMatch = window.location.hash.match(/quest=([^&]+)/);
    const queryMatch = new URLSearchParams(window.location.search).get('quest');
    const targetQuestId = queryMatch || (hashMatch ? hashMatch[1] : null);
    if (targetQuestId) {
        const targetGame = GamesCatalog.find(g => g.id === targetQuestId);
        if (targetGame) {
            AppState.selectedClass = targetGame.class;
            openStudentSelectionModal(targetGame);
        }
    }

    // Keyboard shortcuts for Question Screen
    window.addEventListener('keydown', (e) => {
        const questModal = document.getElementById('questRunnerModal');
        if (!questModal || !questModal.classList.contains('active')) return;

        // Don't intercept typing when typing into text boxes
        if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA')) {
            if (e.key === 'Escape') closeQuestRunner();
            return;
        }

        const activeRunner = document.getElementById('questActiveRunner');
        if (!activeRunner || activeRunner.style.display === 'none') return;

        const game = AppState.activeMissionGame;
        if (!game || !game.questions) return;
        const q = game.questions[AppState.missionStep];
        if (!q) return;

        const key = e.key.toUpperCase();
        let choiceIdx = -1;
        if (key === '1' || key === 'A') choiceIdx = 0;
        else if (key === '2' || key === 'B') choiceIdx = 1;
        else if (key === '3' || key === 'C') choiceIdx = 2;
        else if (key === '4' || key === 'D') choiceIdx = 3;

        if (choiceIdx !== -1 && q.options && choiceIdx < q.options.length) {
            e.preventDefault();
            QuestAudio.playClick();
            AppState.missionAnswers[AppState.missionStep] = choiceIdx;
            renderQuestStep();
        } else if (e.key === 'Enter' || e.key === 'ArrowRight') {
            e.preventDefault();
            navigateQuest(1);
        } else if (e.key === 'ArrowLeft') {
            e.preventDefault();
            navigateQuest(-1);
        } else if (e.key === 'Escape') {
            closeQuestRunner();
        }
    });
});
