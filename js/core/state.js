/* ====================================================
   CENTRALIZED STATE MANAGEMENT
   ==================================================== */
const AppState = {
    currentView: 'kid', // 'kid' | 'teacher' | 'split'
    selectedClass: 'IV',
    selectedSubject: 'all',
    selectedSkillArea: 'all',
    selectedActivity: 'all',
    searchQuery: '',
    kidSubTab: 'assigned', // Enforce assigned activities only
    teacherSubjectFilter: 'all',
    teacherSearchQuery: '',
    teacherLayoutMode: 'table', // 'table' | 'grid'
    teacherStatusFilter: 'all', // 'all' | 'assigned'
    splitTeacherFilter: 'assigned', // 'assigned' | 'all'
    assignments: [],
    activeMissionGame: null,
    selectedStudent: null,
    missionStep: 0,
    missionAnswers: {}
};


window.MCB.AppState = AppState;
window.AppState = AppState;
