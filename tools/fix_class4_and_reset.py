import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# -------------------------------------------------------------------
# 1. Update loadSavedAssignments, saveAssignments, clearAllAssignments, etc.
# -------------------------------------------------------------------
old_storage_block = """        // Load assignments from localStorage (Clean start: NO hardcoded demo assignments)
        function loadSavedAssignments() {
            try {
                // Key bumped to v6 so previous test data is wiped clean
                const stored = localStorage.getItem('mcb_assignments_v6');
                if (stored) {
                    AppState.assignments = JSON.parse(stored);
                } else {
                    AppState.assignments = []; // True empty start
                }
            } catch (e) {
                AppState.assignments = [];
            }
        }

        function saveAssignments() {
            try {
                localStorage.setItem('mcb_assignments_v6', JSON.stringify(AppState.assignments));
            } catch (e) {
                console.error(e);
            }
        }

        function clearAllAssignments() {
            if (confirm("Reset all assignments? This will remove all assigned activities for all classes so you can start from scratch.")) {
                AppState.assignments = [];
                saveAssignments();
                renderTeacherHub();
                renderKidZone();
                if (AppState.currentView === 'split') {
                    renderSplitViews();
                }
            }
        }"""

new_storage_block = """        // Persistent Assignment Storage (Clean start: v7 with NO hardcoded demo assignments)
        const STORAGE_KEY = 'mcb_assignments_v7';

        function loadSavedAssignments() {
            try {
                // Clear any legacy test keys so stale test assignments never linger
                ['mcb_assignments', 'mcb_assignments_v1', 'mcb_assignments_v2', 'mcb_assignments_v3', 'mcb_assignments_v4', 'mcb_assignments_v5', 'mcb_assignments_v6', 'assignments'].forEach(k => {
                    try { localStorage.removeItem(k); } catch(e) {}
                });

                const stored = localStorage.getItem(STORAGE_KEY);
                if (stored) {
                    AppState.assignments = JSON.parse(stored);
                } else {
                    AppState.assignments = []; // True empty start: 0 assignments
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
            const cls = AppState.selectedClass;
            const lbl = document.getElementById('resetModalClassLabel');
            if (lbl) lbl.textContent = cls;
            const modal = document.getElementById('resetConfirmModal');
            if (modal) {
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
                ['mcb_assignments', 'mcb_assignments_v1', 'mcb_assignments_v2', 'mcb_assignments_v3', 'mcb_assignments_v4', 'mcb_assignments_v5', 'mcb_assignments_v6', 'mcb_assignments_v7', 'assignments'].forEach(k => {
                    try { localStorage.removeItem(k); } catch(e) {}
                });
            } catch(e) {}
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
                    border: 2px solid #fed7aa;
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
        }"""

if old_storage_block in html:
    html = html.replace(old_storage_block, new_storage_block)
    print("Replaced storage block successfully!")
else:
    print("Warning: old_storage_block not found!")

# -------------------------------------------------------------------
# 2. Add Reset Confirmation Modal in HTML (after assignModal)
# -------------------------------------------------------------------
old_assign_modal_end = """            <button type="button" class="btn-start-challenge" onclick="submitModalAssignment()">
                <span>✨</span> Assign Game to Selected Students
            </button>
        </div>
    </div>"""

new_assign_modal_end = """            <button type="button" class="btn-start-challenge" onclick="submitModalAssignment()">
                <span>✨</span> Assign Game to Selected Students
            </button>
        </div>
    </div>

    <!-- ====================================================
         RESET ASSIGNMENTS CONFIRMATION MODAL
         ==================================================== -->
    <div class="modal-overlay" id="resetConfirmModal" onclick="if(event.target===this) closeResetModal()">
        <div class="who-modal-card" style="max-width: 480px; text-align: center; border: 3px solid #fecaca; box-shadow: 0 25px 60px rgba(239, 68, 68, 0.2);">
            <div style="font-size: 46px; margin-bottom: 8px;">🗑️✨</div>
            <h3 style="font-family: var(--font-heading); font-size: 22px; color: #1e1b4b; margin-bottom: 8px;">Reset Assignments</h3>
            <p style="color: var(--text-muted); font-size: 14px; line-height: 1.5; margin-bottom: 22px;">
                Choose which assignments you would like to reset. This will remove assigned students and reset completion progress to zero.
            </p>
            <div style="display: flex; flex-direction: column; gap: 10px;">
                <button type="button" class="btn-start-challenge" id="btnResetCurrentClass" style="background: linear-gradient(135deg, #f59e0b, #d97706); justify-content: center;" onclick="clearClassAssignments()">
                    <span>🗑️</span> Reset Class <span id="resetModalClassLabel">IV</span> Only
                </button>
                <button type="button" class="btn-start-challenge" style="background: linear-gradient(135deg, #ef4444, #b91c1c); justify-content: center;" onclick="clearAllAssignments()">
                    <span>⚠️</span> Reset ALL Classes (Wipe to 0)
                </button>
                <button type="button" class="btn-clear-filters" style="margin: 6px auto 0; font-size: 13.5px;" onclick="closeResetModal()">
                    Cancel
                </button>
            </div>
        </div>
    </div>"""

if old_assign_modal_end in html:
    html = html.replace(old_assign_modal_end, new_assign_modal_end)
    print("Added Reset Confirmation Modal!")
else:
    print("Warning: old_assign_modal_end not found!")

# -------------------------------------------------------------------
# 3. Update Teacher Hub Reset Button: use promptResetAssignments()
# -------------------------------------------------------------------
old_teacher_reset_btn = """                        <button type="button" class="btn-clear-assignments-sm" onclick="clearAllAssignments()" title="Reset all assignments to 0">
                            <span>🗑️</span> Reset
                        </button>"""

new_teacher_reset_btn = """                        <button type="button" class="btn-clear-assignments-sm" onclick="promptResetAssignments()" title="Reset assignments">
                            <span>🗑️</span> Reset
                        </button>"""

if old_teacher_reset_btn in html:
    html = html.replace(old_teacher_reset_btn, new_teacher_reset_btn)
    print("Updated Teacher Hub Reset Button!")
else:
    print("Warning: old_teacher_reset_btn not found!")

# -------------------------------------------------------------------
# 4. Add Reset Button in Kid Zone when in "Assigned activities" tab
# -------------------------------------------------------------------
old_kid_search_row = """                        <input type="text" class="search-box-input" id="gameSearchInput" placeholder="Search activities..." oninput="handleGameSearch(this.value)">
                        <button type="button" class="btn-clear-filters" id="btnClearFilters" onclick="resetAllFilters()" style="display: none;">✕ Clear</button>"""

new_kid_search_row = """                        <input type="text" class="search-box-input" id="gameSearchInput" placeholder="Search activities..." oninput="handleGameSearch(this.value)">
                        <button type="button" class="btn-clear-filters" id="btnClearFilters" onclick="resetAllFilters()" style="display: none;">✕ Clear</button>
                        <button type="button" class="btn-clear-assignments-sm" id="btnKidResetAssignments" onclick="promptResetAssignments()" style="display: none;" title="Reset assigned activities">
                            <span>🗑️</span> Reset
                        </button>"""

if old_kid_search_row in html:
    html = html.replace(old_kid_search_row, new_kid_search_row)
    print("Added Reset Button to Kid Zone search row!")
else:
    print("Warning: old_kid_search_row not found!")

# -------------------------------------------------------------------
# 5. In renderGamesGrid(): Toggle Kid Reset Button
# -------------------------------------------------------------------
old_render_grid_clear = """            const clearBtn = document.getElementById('btnClearFilters');
            if (clearBtn) {
                const hasFilters = AppState.selectedSubject !== 'all' || AppState.selectedSkillArea !== 'all' || AppState.selectedActivity !== 'all' || AppState.searchQuery !== '';
                clearBtn.style.display = hasFilters ? 'inline-flex' : 'none';
            }"""

new_render_grid_clear = """            const clearBtn = document.getElementById('btnClearFilters');
            if (clearBtn) {
                const hasFilters = AppState.selectedSubject !== 'all' || AppState.selectedSkillArea !== 'all' || AppState.selectedActivity !== 'all' || AppState.searchQuery !== '';
                clearBtn.style.display = hasFilters ? 'inline-flex' : 'none';
            }

            const kidResetBtn = document.getElementById('btnKidResetAssignments');
            if (kidResetBtn) {
                const hasAssigned = AppState.assignments.some(a => a.class === AppState.selectedClass);
                kidResetBtn.style.display = (AppState.kidSubTab === 'assigned' && hasAssigned) ? 'inline-flex' : 'none';
            }"""

if old_render_grid_clear in html:
    html = html.replace(old_render_grid_clear, new_render_grid_clear)
    print("Updated renderGamesGrid to show/hide Kid Reset button!")
else:
    print("Warning: old_render_grid_clear not found!")

# -------------------------------------------------------------------
# 6. In Teacher Hub row rendering: Add Unassign Button per activity
# -------------------------------------------------------------------
old_students_cell = """                                <td>
                                    <div class="curriculum-students-cell">
                                        ${isAssigned 
                                            ? assigned.map(a => `
                                                <span class="tac-chip ${a.status === 'completed' ? 'completed' : 'pending'}" style="font-size: 11px; padding: 2px 8px;">
                                                    ${a.status === 'completed' ? `✓ ${a.student}` : `⏳ ${a.student}`}
                                                </span>
                                            `).join('')
                                            : `<span class="curriculum-empty-dash">—</span>`
                                        }
                                    </div>
                                </td>"""

new_students_cell = """                                <td>
                                    <div class="curriculum-students-cell" style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 6px;">
                                        <div style="display: flex; flex-wrap: wrap; gap: 4px; align-items: center;">
                                            ${isAssigned 
                                                ? assigned.map(a => `
                                                    <span class="tac-chip ${a.status === 'completed' ? 'completed' : 'pending'}" style="font-size: 11px; padding: 2px 8px;">
                                                        ${a.status === 'completed' ? `✓ ${a.student}` : `⏳ ${a.student}`}
                                                    </span>
                                                `).join('')
                                                : `<span class="curriculum-empty-dash">—</span>`
                                            }
                                        </div>
                                        ${isAssigned ? `
                                            <button type="button" class="btn-clear-assignments-sm" style="padding: 2px 8px; font-size: 11px; border-radius: 6px;" title="Unassign this activity from Class ${cls}" onclick="unassignActivity('${g.id}')">
                                                ✕ Clear
                                            </button>
                                        ` : ''}
                                    </div>
                                </td>"""

if old_students_cell in html:
    html = html.replace(old_students_cell, new_students_cell)
    print("Added Unassign button per assigned row in Teacher Hub!")
else:
    print("Warning: old_students_cell not found!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html successfully!")
