import os

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

start_marker = 'function renderTeacherHub() {'
end_marker = '/* ====================================================\n           ASSIGN MODAL LOGIC'

start_idx = c.find(start_marker)
end_idx = c.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print('Markers not found!')
    exit(1)

new_content = """function renderTeacherHub() {
            const cls = AppState.selectedClass;
            
            // Update labels
            const lbl = document.getElementById('teacherCurrentClassLabel');
            if (lbl) lbl.textContent = cls;
            const statCls = document.getElementById('teacherStatClassLabel');
            if (statCls) statCls.textContent = cls;

            // Sync class dropdown
            const sel = document.getElementById('teacherClassSelect');
            if (sel) sel.value = cls;

            // Sync class selector pills
            document.querySelectorAll('#teacherClassPills .teacher-class-pill').forEach(btn => {
                const btnText = btn.textContent.trim();
                btn.classList.toggle('active', btnText === `Class ${cls}`);
            });

            // Get all activities for this class
            const classGames = GamesCatalog.filter(g => g.class === cls);
            
            // Get assignments for this class
            const classAsgs = AppState.assignments.filter(a => a.class === cls);
            const assignedGameIds = new Set(classAsgs.map(a => a.gameId));
            const completedAsgs = classAsgs.filter(a => a.status === 'completed');
            const pendingAsgs = classAsgs.filter(a => a.status === 'pending');

            // Update Metrics
            const statTotal = document.getElementById('teacherStatTotalActivities');
            if (statTotal) statTotal.textContent = classGames.length;
            const statAssigned = document.getElementById('teacherStatAssignedActivities');
            if (statAssigned) statAssigned.textContent = assignedGameIds.size;
            const statComp = document.getElementById('teacherStatCompleted');
            if (statComp) statComp.textContent = completedAsgs.length;
            const statPend = document.getElementById('teacherStatPending');
            if (statPend) statPend.textContent = pendingAsgs.length;

            // Filter activities by Subject, Search query, and Status
            let filteredGames = classGames.filter(g => {
                if (AppState.teacherSubjectFilter !== 'all' && g.subject !== AppState.teacherSubjectFilter) return false;
                if (AppState.teacherStatusFilter === 'assigned' && !assignedGameIds.has(g.id)) return false;
                if (AppState.teacherSearchQuery) {
                    const q = AppState.teacherSearchQuery.toLowerCase();
                    const matchTitle = g.title && g.title.toLowerCase().includes(q);
                    const matchSub = g.subject && g.subject.toLowerCase().includes(q);
                    const matchSkill = g.skillArea && g.skillArea.toLowerCase().includes(q);
                    const matchAct = g.activity && g.activity.toLowerCase().includes(q);
                    if (!matchTitle && !matchSub && !matchSkill && !matchAct) return false;
                }
                return true;
            });

            const badgeCount = document.getElementById('teacherBadgeAssignedCount');
            if (badgeCount) badgeCount.textContent = `${filteredGames.length} activities`;

            const mode = AppState.teacherLayoutMode || 'table';
            const tableContainer = document.getElementById('teacherTableContainer');
            const tableBody = document.getElementById('teacherTableBody');
            const grid = document.getElementById('teacherActivitiesGrid');

            if (mode === 'table') {
                if (tableContainer) tableContainer.style.display = 'block';
                if (grid) grid.style.display = 'none';

                if (tableBody) {
                    tableBody.innerHTML = '';
                    if (filteredGames.length === 0) {
                        tableBody.innerHTML = `
                            <tr>
                                <td colspan="4" style="text-align: center; padding: 48px 16px; background: #ffffff;">
                                    <div style="font-size: 38px; margin-bottom: 8px;">📚✨</div>
                                    <h4 style="font-family: var(--font-heading); font-size: 19px; color: #1e1b4b; margin-bottom: 6px;">No activities match this filter</h4>
                                    <p style="color: var(--text-muted); font-size: 13.5px; margin-bottom: 16px;">Try switching to 'All Activities' or selecting a different subject.</p>
                                    <button type="button" class="btn-clear-filters" onclick="resetTeacherFilters()" style="margin: 0 auto;">Reset filters ↺</button>
                                </td>
                            </tr>
                        `;
                    } else {
                        filteredGames.forEach(g => {
                            const assigned = classAsgs.filter(a => a.gameId === g.id);
                            const totalAssigned = assigned.length;
                            const completed = assigned.filter(a => a.status === 'completed');
                            const compCount = completed.length;
                            const pct = totalAssigned > 0 ? Math.round((compCount / totalAssigned) * 100) : 0;
                            const isAssigned = totalAssigned > 0;

                            const tr = document.createElement('tr');
                            tr.className = `curriculum-row ${isAssigned ? 'is-assigned' : ''}`;
                            tr.innerHTML = `
                                <td>
                                    <div class="curriculum-title-wrap">
                                        <div class="curriculum-badges">
                                            <span class="tac-badge tac-badge-subject ${g.badgeClass || ''}">${g.subject}</span>
                                            <span class="tac-badge tac-badge-skill" title="Skill Area: ${g.skillArea || ''}">🎯 ${g.skillArea || 'Skill Area'}</span>
                                            <span class="tac-badge tac-badge-act" title="Activity: ${g.activity || ''}">⚡ ${g.activity || 'Activity'}</span>
                                        </div>
                                        <span class="curriculum-title">${g.title}</span>
                                    </div>
                                </td>
                                <td>
                                    <div class="curriculum-progress-wrap">
                                        <div style="display: flex; justify-content: space-between; align-items: center;">
                                            <span class="curriculum-pct ${pct === 100 ? 'done' : (isAssigned ? 'in-prog' : 'none')}">
                                                ${isAssigned ? `<strong>${compCount}/${totalAssigned}</strong> completed (${pct}%)` : 'Not assigned (0%)'}
                                            </span>
                                        </div>
                                        <div class="tac-progress-bar" style="height: 7px; background: #e2e8f0; border-radius: 999px; overflow: hidden;">
                                            <div class="tac-progress-fill ${pct === 100 ? 'full' : ''}" style="height: 100%; width: ${pct}%; border-radius: 999px; background: ${pct === 100 ? '#10b981' : 'linear-gradient(90deg, #f59e0b, #10b981)'};"></div>
                                        </div>
                                    </div>
                                </td>
                                <td>
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
                                </td>
                                <td style="text-align: right;">
                                    <div style="display: inline-flex; gap: 6px; align-items: center; justify-content: flex-end;">
                                        <button type="button" class="btn-tac-assign-sm" onclick="openAssignModalForGame('${g.id}')">
                                            + Assign
                                        </button>
                                        <button type="button" class="btn-tac-play-sm" onclick="openWhoIsPlaying('${g.id}')">
                                            ▶ Play
                                        </button>
                                    </div>
                                </td>
                            `;
                            tableBody.appendChild(tr);
                        });
                    }
                }
            } else {
                // Grid Mode
                if (tableContainer) tableContainer.style.display = 'none';
                if (grid) {
                    grid.style.display = 'grid';
                    grid.innerHTML = '';

                    if (filteredGames.length === 0) {
                        grid.innerHTML = `
                            <div style="grid-column: 1 / -1; text-align: center; padding: 48px; background: #fff; border-radius: 20px; border: 2.5px dashed #fed7aa;">
                                <div style="font-size: 38px; margin-bottom: 8px;">📚✨</div>
                                <h4 style="font-family: var(--font-heading); font-size: 20px; color: #1e1b4b; margin-bottom: 6px;">No activities match this filter</h4>
                                <p style="color: var(--text-muted); font-size: 14px; margin-bottom: 16px;">Try selecting 'All subjects' or resetting your search query.</p>
                                <button type="button" class="btn-clear-filters" onclick="resetTeacherFilters()" style="margin: 0 auto;">Reset filters ↺</button>
                            </div>
                        `;
                    } else {
                        filteredGames.forEach(g => {
                            const assigned = classAsgs.filter(a => a.gameId === g.id);
                            const totalAssigned = assigned.length;
                            const completed = assigned.filter(a => a.status === 'completed');
                            const compCount = completed.length;
                            const pct = totalAssigned > 0 ? Math.round((compCount / totalAssigned) * 100) : 0;
                            const isAssigned = totalAssigned > 0;

                            const card = document.createElement('div');
                            card.className = `teacher-activity-card ${isAssigned ? 'is-assigned' : ''}`;

                            card.innerHTML = `
                                <div>
                                    <div class="tac-top-row" style="margin-bottom: 6px;">
                                        <div class="tac-badges">
                                            <span class="tac-badge tac-badge-subject ${g.badgeClass || ''}">${g.subject}</span>
                                            <span class="tac-badge tac-badge-skill" title="Skill Area: ${g.skillArea || ''}">🎯 ${g.skillArea || 'Skill Area'}</span>
                                            <span class="tac-badge tac-badge-act" title="Activity: ${g.activity || ''}">⚡ ${g.activity || 'Activity'}</span>
                                        </div>
                                    </div>
                                    <h4 class="tac-title" style="font-size: 16px; margin-bottom: 8px;">${g.title}</h4>
                                </div>

                                <div class="tac-progress-wrap" style="padding: 8px 12px; margin-bottom: 10px;">
                                    <div class="tac-progress-header" style="margin-bottom: 4px; font-size: 11.5px;">
                                        <span class="tac-progress-label">Completion:</span>
                                        <span class="tac-progress-metric ${pct === 100 ? 'completed' : (!isAssigned ? 'unassigned' : '')}">
                                            ${isAssigned 
                                                ? `<strong>${compCount}/${totalAssigned}</strong> (${pct}%)` 
                                                : 'Not assigned (0%)'}
                                        </span>
                                    </div>
                                    <div class="tac-progress-bar" style="height: 7px;">
                                        <div class="tac-progress-fill ${pct === 100 ? 'full' : ''}" style="width: ${pct}%;"></div>
                                    </div>
                                </div>

                                <div class="tac-students-wrap" style="margin-bottom: 10px;">
                                    <div class="tac-students-label" style="font-size: 11px; margin-bottom: 4px;">
                                        <span>Assigned Students (${totalAssigned})</span>
                                        ${isAssigned ? `<span style="font-weight: 700; color: ${pct === 100 ? '#15803d' : '#b45309'};">${pct === 100 ? '✓ Done' : `${compCount}/${totalAssigned} Done`}</span>` : ''}
                                    </div>
                                    <div class="tac-student-chips">
                                        ${isAssigned 
                                            ? assigned.map(a => `
                                                <span class="tac-chip ${a.status === 'completed' ? 'completed' : 'pending'}" style="font-size: 11px; padding: 2px 8px;">
                                                    ${a.status === 'completed' ? `✓ ${a.student}` : `⏳ ${a.student}`}
                                                    ${a.status === 'completed' ? `<span class="tac-chip-stars" style="font-size: 10px;">⭐ ${a.score || 3}/3</span>` : ''}
                                                </span>
                                            `).join('')
                                            : `<span class="tac-no-students-notice" style="font-size: 11px; padding: 3px 8px;">No students assigned</span>`
                                        }
                                    </div>
                                </div>

                                <div class="tac-footer" style="padding-top: 8px;">
                                    <button type="button" class="btn-tac-assign" style="padding: 7px 12px; font-size: 12px;" onclick="openAssignModalForGame('${g.id}')">
                                        <span>+</span> Assign Students
                                    </button>
                                    <button type="button" class="btn-tac-preview" style="padding: 6px 10px; font-size: 11.5px;" onclick="openWhoIsPlaying('${g.id}')">
                                        <span>▶</span> Play
                                    </button>
                                </div>
                            `;

                            grid.appendChild(card);
                        });
                    }
                }
            }
        }

        function handleTeacherClassChange(cls) {
            handleClassFilterChange(cls);
        }

        function filterTeacherSubject(sub, btn) {
            AppState.teacherSubjectFilter = sub;
            document.querySelectorAll('#teacherSubjectChips .chip-btn').forEach(b => b.classList.remove('active'));
            if (btn) btn.classList.add('active');
            renderTeacherHub();
        }

        function filterTeacherActivities(val) {
            AppState.teacherSearchQuery = (val || '').trim();
            renderTeacherHub();
        }

        function filterTeacherStatus(status, btn) {
            AppState.teacherStatusFilter = status;
            const btnAll = document.getElementById('btnTeacherStatusAll');
            const btnAsg = document.getElementById('btnTeacherStatusAssigned');
            if (btnAll) btnAll.classList.toggle('active', status === 'all');
            if (btnAsg) btnAsg.classList.toggle('active', status === 'assigned');
            renderTeacherHub();
        }

        function setTeacherLayoutMode(mode, btn) {
            AppState.teacherLayoutMode = mode;
            document.querySelectorAll('.view-mode-btn').forEach(b => b.classList.remove('active'));
            if (btn) btn.classList.add('active');
            renderTeacherHub();
        }

        function resetTeacherFilters() {
            AppState.teacherSubjectFilter = 'all';
            AppState.teacherSearchQuery = '';
            AppState.teacherStatusFilter = 'all';
            const input = document.getElementById('teacherSearchInput');
            if (input) input.value = '';
            document.querySelectorAll('#teacherSubjectChips .chip-btn').forEach((b, idx) => {
                b.classList.toggle('active', idx === 0);
            });
            const btnAll = document.getElementById('btnTeacherStatusAll');
            const btnAsg = document.getElementById('btnTeacherStatusAssigned');
            if (btnAll) btnAll.classList.add('active');
            if (btnAsg) btnAsg.classList.remove('active');
            renderTeacherHub();
        }

        """

c = c[:start_idx] + new_content + c[end_idx:]
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print('Teacher Hub JS replaced successfully!')
