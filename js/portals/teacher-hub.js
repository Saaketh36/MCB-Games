/* ====================================================
   TEACHER HUB & CLASS-SPECIFIC ACTIVITIES & PROGRESS BOARD
   ==================================================== */
function renderTeacherHub() {
    const cls = AppState.selectedClass;
    const roster = StudentRosters[cls] || [];

    // Update labels
    const lbl = document.getElementById('teacherCurrentClassLabel');
    if (lbl) lbl.textContent = cls;

    // Sync class dropdown
    const sel = document.getElementById('teacherClassSelect');
    if (sel) sel.value = cls;

    // Sync class selector pills
    document.querySelectorAll('#teacherClassPills .teacher-class-pill').forEach(btn => {
        const btnText = btn.textContent.trim();
        btn.classList.toggle('active', btnText === `Class ${cls}`);
    });

    // Update Subject Filter Chips to ONLY show subjects with activities in this class
    updateTeacherSubjectChips();

    // Get all activities for this class
    const classGames = GamesCatalog.filter(g => g.class === cls);

    // Get assignments for this class
    const classAsgs = AppState.assignments.filter(a => a.class === cls);
    const assignedGameIds = new Set(classAsgs.map(a => a.gameId));
    const completedAsgs = classAsgs.filter(a => a.status === 'completed');
    const pendingAsgs = classAsgs.filter(a => a.status === 'pending');

    // Update Metrics
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

    // Extract assignment order (sequence in which games were assigned to this class)
    const assignedOrder = [];
    classAsgs.forEach(a => {
        if (!assignedOrder.includes(a.gameId)) {
            assignedOrder.push(a.gameId);
        }
    });

    // Sort filtered games strictly by assigned order first, then catalog order for unassigned
    filteredGames.sort((a, b) => {
        const aIdx = assignedOrder.indexOf(a.id);
        const bIdx = assignedOrder.indexOf(b.id);
        const aAssigned = aIdx !== -1;
        const bAssigned = bIdx !== -1;

        if (aAssigned && !bAssigned) return -1;
        if (!aAssigned && bAssigned) return 1;
        if (aAssigned && bAssigned) return aIdx - bIdx;
        return 0;
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
                                <td colspan="3" style="text-align: center; padding: 48px 16px; background: #ffffff;">
                                    <div style="font-size: 38px; margin-bottom: 8px;">📚✨</div>
                                    <h4 style="font-family: var(--font-heading); font-size: 19px; color: #1e1b4b; margin-bottom: 6px;">No activities match this filter</h4>
                                    <p style="color: var(--text-muted); font-size: 13.5px; margin-bottom: 16px;">Try switching to 'All Activities' or selecting a different subject.</p>
                                    <button type="button" class="btn-clear-filters" onclick="resetTeacherFilters()" style="margin: 0 auto;">Reset filters ↺</button>
                                </td>
                            </tr>
                        `;
            } else {
                const isSpecificSubject = AppState.teacherSubjectFilter !== 'all';
                const hasAssigned = filteredGames.some(g => assignedGameIds.has(g.id));
                const hasUnassigned = filteredGames.some(g => !assignedGameIds.has(g.id));
                const isMixed = hasAssigned && hasUnassigned;
                let renderedAssignedDivider = false;
                let renderedUnassignedDivider = false;

                filteredGames.forEach(g => {
                    const assigned = classAsgs.filter(a => a.gameId === g.id);
                    const totalAssigned = assigned.length;
                    const isAssigned = totalAssigned > 0;
                    const completed = assigned.filter(a => a.status === 'completed');
                    const compCount = completed.length;
                    const pct = totalAssigned > 0 ? Math.round((compCount / totalAssigned) * 100) : 0;

                    if (isMixed) {
                        if (isAssigned && !renderedAssignedDivider) {
                            renderedAssignedDivider = true;
                            const assignedCount = filteredGames.filter(x => assignedGameIds.has(x.id)).length;
                            const divTr = document.createElement('tr');
                            divTr.className = 'curriculum-skill-header-row';
                            divTr.innerHTML = `
                                <td colspan="3">
                                    <div class="skill-header-content">
                                        <div class="skill-header-left">
                                            <span class="skill-header-icon-badge">📋</span>
                                            <span class="skill-header-title">Assigned Activities (${assignedCount})</span>
                                            <span class="skill-header-count">Sorted by Assigned Order</span>
                                        </div>
                                        <div class="skill-header-right">
                                            <button type="button" class="btn-clear-skill-heading" onclick="promptResetAssignments()" title="Clear all assignments for Class ${cls}">
                                                ✕ Clear All
                                            </button>
                                        </div>
                                    </div>
                                </td>
                            `;
                            tableBody.appendChild(divTr);
                        } else if (!isAssigned && !renderedUnassignedDivider) {
                            renderedUnassignedDivider = true;
                            const unassignedCount = filteredGames.filter(x => !assignedGameIds.has(x.id)).length;
                            const divTr = document.createElement('tr');
                            divTr.className = 'curriculum-skill-header-row';
                            divTr.innerHTML = `
                                <td colspan="3">
                                    <div class="skill-header-content">
                                        <div class="skill-header-left">
                                            <span class="skill-header-icon-badge">📚</span>
                                            <span class="skill-header-title">Other Curriculum Activities (${unassignedCount})</span>
                                            <span class="skill-header-count">Available to Assign</span>
                                        </div>
                                    </div>
                                </td>
                            `;
                            tableBody.appendChild(divTr);
                        }
                    }

                    const tr = document.createElement('tr');
                    tr.className = `curriculum-row ${isAssigned ? 'is-assigned' : ''}`;
                    tr.innerHTML = `
                        <td>
                            <div class="curriculum-title-wrap">
                                ${!isSpecificSubject ? `<span class="tac-badge tac-badge-subject ${g.badgeClass || ''}">${g.subject}</span>` : ''}
                                <span class="tac-badge tac-badge-skill" style="background: #eef2ff; color: #4338ca; border: 1px solid #c7d2fe; font-size: 11px; padding: 2px 7px; border-radius: 6px;">🎯 ${escapeHtml(g.skillArea || 'General')}</span>
                                ${g.isCustom ? '<span class="tac-badge tac-badge-custom">⭐ Custom</span>' : ''}
                                ${(window.Class2Games && window.Class2Games.isClass2Interactive(g)) ? '<span class="tac-badge tac-badge-mini">🎮 Mini-Game</span>' : ''}
                                <span class="curriculum-title" title="${escapeHtml(g.title)}">${g.title}</span>
                                <div style="margin-left: auto; display: flex; align-items: center; gap: 6px; flex-shrink: 0;">
                                    <button type="button" class="btn-tac-preview-sm" onclick="previewActivity('${g.id}')" title="Preview activity before assigning">👁️ Preview</button>
                                    ${isAssigned ? `
                                        <button type="button" class="btn-clear-assignments-sm" style="padding: 4px 10px; font-size: 11px; border-radius: 6px;" onclick="unassignActivity('${g.id}')" title="Unassign this activity from Class ${cls}">✕ Unassign</button>
                                    ` : `
                                        <button type="button" class="btn-tac-preview-sm" style="background: #e0e7ff; color: #3730a3; border-color: #c7d2fe; font-weight: 700;" onclick="openAssignModalForGame('${g.id}')" title="Assign this activity to students">+ Assign</button>
                                    `}
                                </div>
                            </div>
                        </td>
                        <td>
                            <div class="curriculum-progress-wrap">
                                ${isAssigned ? `
                                <div class="curriculum-progress-label">
                                    <span class="curriculum-pct ${pct === 100 ? 'done' : 'in-prog'}">
                                        <strong>${compCount}/${totalAssigned}</strong> completed
                                    </span>
                                    <span class="curriculum-pct-badge ${pct === 100 ? 'done' : ''}">${pct}%</span>
                                </div>
                                <div class="tac-progress-bar">
                                    <div class="tac-progress-fill ${pct === 100 ? 'full' : ''}" style="width: ${pct}%;"></div>
                                </div>
                                ` : `
                                <span class="curriculum-empty-dash">—</span>
                                `}
                            </div>
                        </td>
                        <td>
                            <div class="curriculum-students-cell">
                                ${isAssigned ? `
                                <div class="tac-students-wrap">
                                    ${assigned.map(a => `
                                        <span class="tac-chip ${a.status === 'completed' ? 'completed' : 'pending'}" title="${escapeHtml(a.student)} (Roll #${a.roll}) • ${a.status === 'completed' ? `Score: ${a.score || 3}/${a.maxScore || 3} ⭐` : 'Pending'}">
                                            <span>${a.status === 'completed' ? '✓' : '⏳'}</span>
                                            <span>${escapeHtml(a.student)}</span>
                                            ${a.status === 'completed' && a.score !== undefined && a.score !== null ? `<span class="tac-chip-score">⭐ ${a.score}/${a.maxScore || 3}</span>` : ''}
                                        </span>
                                    `).join('')}
                                </div>
                                ` : `
                                <span class="curriculum-empty-dash" style="color: var(--text-muted); font-size: 12px;">Not Assigned</span>
                                `}
                            </div>
                        </td>
                    `;
                    tableBody.appendChild(tr);
                });
            }
        }
    }

    if (mode === 'grid') {
        if (tableContainer) tableContainer.style.display = 'none';
        if (grid) grid.style.display = 'grid';

        if (grid) {
            grid.innerHTML = '';
            if (filteredGames.length === 0) {
                grid.innerHTML = `
                            <div style="grid-column: 1 / -1; text-align: center; padding: 48px; background: #ffffff; border-radius: 20px; border: 1.5px dashed #cbd5e1;">
                                <div style="font-size: 38px; margin-bottom: 8px;">📚✨</div>
                                <h4 style="font-family: var(--font-heading); font-size: 20px; color: #1e1b4b; margin-bottom: 6px;">No activities match this filter</h4>
                                <p style="color: var(--text-muted); font-size: 14px; margin-bottom: 16px;">Try selecting 'All subjects' or resetting your search query.</p>
                                <button type="button" class="btn-clear-filters" onclick="resetTeacherFilters()" style="margin: 0 auto;">Reset filters ↺</button>
                            </div>
                        `;
            } else {
                const isSpecificSubject = AppState.teacherSubjectFilter !== 'all';
                const hasAssigned = filteredGames.some(g => assignedGameIds.has(g.id));
                const hasUnassigned = filteredGames.some(g => !assignedGameIds.has(g.id));
                const isMixed = hasAssigned && hasUnassigned;
                let renderedAssignedBanner = false;
                let renderedUnassignedBanner = false;

                filteredGames.forEach(g => {
                    const assigned = classAsgs.filter(a => a.gameId === g.id);
                    const totalAssigned = assigned.length;
                    const isAssigned = totalAssigned > 0;
                    const completed = assigned.filter(a => a.status === 'completed');
                    const compCount = completed.length;
                    const pct = totalAssigned > 0 ? Math.round((compCount / totalAssigned) * 100) : 0;

                    if (isMixed) {
                        if (isAssigned && !renderedAssignedBanner) {
                            renderedAssignedBanner = true;
                            const assignedCount = filteredGames.filter(x => assignedGameIds.has(x.id)).length;
                            const banner = document.createElement('div');
                            banner.style.cssText = 'grid-column: 1 / -1; margin-top: 14px; margin-bottom: 6px; padding: 10px 16px; background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 12px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;';
                            banner.innerHTML = `
                                <div style="display: flex; align-items: center; gap: 8px;">
                                    <span style="font-size: 16px;">📋</span>
                                    <span style="font-family: var(--font-heading); font-size: 15px; font-weight: 800; color: #1e1b4b;">Assigned Activities</span>
                                </div>
                                <div style="display: flex; align-items: center; gap: 8px;">
                                    <span style="background: #ede9fe; color: #5b21b6; font-family: var(--font-heading); font-weight: 700; font-size: 11.5px; padding: 2px 10px; border-radius: 999px; border: 1px solid #ddd6fe;">
                                        ${assignedCount} ${assignedCount === 1 ? 'activity' : 'activities'} (Sorted by Assigned Order)
                                    </span>
                                </div>
                            `;
                            grid.appendChild(banner);
                        } else if (!isAssigned && !renderedUnassignedBanner) {
                            renderedUnassignedBanner = true;
                            const unassignedCount = filteredGames.filter(x => !assignedGameIds.has(x.id)).length;
                            const banner = document.createElement('div');
                            banner.style.cssText = 'grid-column: 1 / -1; margin-top: 14px; margin-bottom: 6px; padding: 10px 16px; background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 12px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;';
                            banner.innerHTML = `
                                <div style="display: flex; align-items: center; gap: 8px;">
                                    <span style="font-size: 16px;">📚</span>
                                    <span style="font-family: var(--font-heading); font-size: 15px; font-weight: 800; color: #1e1b4b;">Other Curriculum Activities</span>
                                </div>
                                <div style="display: flex; align-items: center; gap: 8px;">
                                    <span style="background: #f1f5f9; color: #475569; font-family: var(--font-heading); font-weight: 700; font-size: 11.5px; padding: 2px 10px; border-radius: 999px; border: 1px solid #e2e8f0;">
                                        ${unassignedCount} ${unassignedCount === 1 ? 'activity' : 'activities'}
                                    </span>
                                </div>
                            `;
                            grid.appendChild(banner);
                        }
                    }

                    const card = document.createElement('div');
                    card.className = `teacher-activity-card ${isAssigned ? 'is-assigned' : ''}`;
                    card.innerHTML = `
                        <div style="margin-bottom: 10px;">
                            <div class="tac-badges" style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                                ${!isSpecificSubject ? `<span class="tac-badge tac-badge-subject ${g.badgeClass || ''}">${g.subject}</span>` : ''}
                                <span class="tac-badge tac-badge-skill" style="background: #eef2ff; color: #4338ca; border: 1px solid #c7d2fe; font-size: 10.5px; font-weight: 700; border-radius: 6px; padding: 2px 7px;">🎯 ${escapeHtml(g.skillArea || 'General')}</span>
                                ${g.isCustom ? '<span class="tac-badge tac-badge-custom">⭐ Custom</span>' : ''}
                                ${(window.Class2Games && window.Class2Games.isClass2Interactive(g)) ? '<span class="tac-badge" style="background:#fdf2f8; color:#be185d; border:1px solid #fbcfe8; font-size:10.5px; font-weight:800; border-radius:999px; padding:2px 7px;">🎮 Mini-Game</span>' : ''}
                                <h4 class="tac-title" style="font-size: 15.5px; margin: 0; display: inline-block;">${g.title}</h4>
                            </div>
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
                            <div class="tac-students-label" style="font-size: 11px; margin-bottom: 4px; display: flex; justify-content: space-between; align-items: center;">
                                <span>Assigned Students (${totalAssigned})</span>
                                ${isAssigned ? `<span style="font-weight: 700; color: ${pct === 100 ? '#15803d' : '#b45309'};">${pct === 100 ? '✓ Done' : `${compCount}/${totalAssigned} Done`}</span>` : ''}
                            </div>
                            <div class="tac-student-chips" style="display: flex; flex-wrap: wrap; gap: 4px;">
                                ${isAssigned
                            ? assigned.map(a => `
                                        <span class="tac-chip ${a.status === 'completed' ? 'completed' : 'pending'}" style="font-size: 11px; padding: 2px 8px;">
                                            ${a.status === 'completed' ? `✓ ${escapeHtml(a.student)}` : `⏳ ${escapeHtml(a.student)}`}
                                            ${a.status === 'completed' ? `<span class="tac-chip-stars" style="font-size: 10px;">⭐ ${a.score || 3}/3</span>` : ''}
                                        </span>
                                    `).join('')
                            : `<span style="color: #94a3b8; font-size: 12px; font-weight: 500;">—</span>`
                        }
                            </div>
                        </div>

                        <div class="tac-footer" style="padding-top: 8px; display: flex; gap: 6px; justify-content: flex-end;">
                            <button type="button" class="btn-tac-preview" style="padding: 7px 14px; font-size: 12px; flex: 1; justify-content: center; gap: 6px;" onclick="previewActivity('${g.id}')" title="Preview this activity before assigning">
                                <span>👁️</span> Preview
                            </button>
                            ${isAssigned ? `
                                <button type="button" class="btn-clear-assignments-sm" style="padding: 7px 14px; font-size: 12px; border-radius: 8px;" onclick="unassignActivity('${g.id}')" title="Unassign this activity from Class ${cls}">
                                    ✕ Unassign
                                </button>
                            ` : `
                                <button type="button" class="btn-tac-assign" style="padding: 7px 14px; font-size: 12px; border-radius: 8px; background: #6366f1; color: #ffffff; border: none; font-weight: 600; cursor: pointer;" onclick="openAssignModalForGame('${g.id}')" title="Assign this activity">
                                    + Assign
                                </button>
                            `}
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

function updateTeacherSubjectChips() {
    const container = document.getElementById('teacherSubjectChips');
    if (!container) return;

    const cls = AppState.selectedClass;
    const classGames = GamesCatalog.filter(g => g.class === cls);

    // Only subjects that actually have activities in this class
    const presentSubjects = Array.from(new Set(classGames.map(g => g.subject).filter(Boolean)));

    const subjectOrder = ['Mathematics', 'English', 'EVS', 'Science', 'Social Science'];
    presentSubjects.sort((a, b) => {
        const idxA = subjectOrder.indexOf(a);
        const idxB = subjectOrder.indexOf(b);
        return (idxA !== -1 ? idxA : 99) - (idxB !== -1 ? idxB : 99);
    });

    // If selected filter is not present in this class, reset to 'all'
    if (AppState.teacherSubjectFilter !== 'all' && !presentSubjects.includes(AppState.teacherSubjectFilter)) {
        AppState.teacherSubjectFilter = 'all';
    }

    const subjectMeta = {
        'Mathematics': { label: 'Math', dot: 'chip-dot-math' },
        'English': { label: 'English', dot: 'chip-dot-eng' },
        'EVS': { label: 'EVS', dot: 'chip-dot-evs' },
        'Science': { label: 'Science', dot: 'chip-dot-sci' },
        'Social Science': { label: 'Social', dot: 'chip-dot-soc' }
    };

    container.innerHTML = '';

    // 'All' button
    const allBtn = document.createElement('button');
    allBtn.type = 'button';
    allBtn.className = `chip-btn ${AppState.teacherSubjectFilter === 'all' ? 'active' : ''}`;
    allBtn.textContent = 'All';
    allBtn.onclick = function () { filterTeacherSubject('all', this); };
    container.appendChild(allBtn);

    // Dynamically add ONLY subjects that have activities in this class
    presentSubjects.forEach(sub => {
        const meta = subjectMeta[sub] || { label: sub, dot: 'chip-dot-math' };
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = `chip-btn ${AppState.teacherSubjectFilter === sub ? 'active' : ''}`;
        btn.innerHTML = `<span class="chip-dot ${meta.dot}"></span> ${meta.label}`;
        btn.onclick = function () { filterTeacherSubject(sub, this); };
        container.appendChild(btn);
    });
}

function updateKidSubjectChips() {
    const container = document.getElementById('kidSubjectChips');
    if (!container) return;

    const cls = AppState.selectedClass;
    const classGames = GamesCatalog.filter(g => g.class === cls);
    const presentSubjects = Array.from(new Set(classGames.map(g => g.subject).filter(Boolean)));

    const subjectOrder = ['Mathematics', 'English', 'EVS', 'Science', 'Social Science'];
    presentSubjects.sort((a, b) => {
        const idxA = subjectOrder.indexOf(a);
        const idxB = subjectOrder.indexOf(b);
        return (idxA !== -1 ? idxA : 99) - (idxB !== -1 ? idxB : 99);
    });

    if (AppState.selectedSubject !== 'all' && !presentSubjects.includes(AppState.selectedSubject)) {
        AppState.selectedSubject = 'all';
    }

    const subjectMeta = {
        'Mathematics': { label: 'Math', dot: 'chip-dot-math' },
        'English': { label: 'English', dot: 'chip-dot-eng' },
        'EVS': { label: 'EVS', dot: 'chip-dot-evs' },
        'Science': { label: 'Science', dot: 'chip-dot-sci' },
        'Social Science': { label: 'Social', dot: 'chip-dot-soc' }
    };

    container.innerHTML = '';

    const allBtn = document.createElement('button');
    allBtn.type = 'button';
    allBtn.className = `chip-btn ${AppState.selectedSubject === 'all' ? 'active' : ''}`;
    allBtn.textContent = 'All';
    allBtn.onclick = function () { filterBySubject('all', this); };
    container.appendChild(allBtn);

    presentSubjects.forEach(sub => {
        const meta = subjectMeta[sub] || { label: sub, dot: 'chip-dot-math' };
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = `chip-btn ${AppState.selectedSubject === sub ? 'active' : ''}`;
        btn.innerHTML = `<span class="chip-dot ${meta.dot}"></span> ${meta.label}`;
        btn.onclick = function () { filterBySubject(sub, this); };
        container.appendChild(btn);
    });
}

function filterTeacherSubject(sub, btn) {
    AppState.teacherSubjectFilter = sub;
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
    const btnAll = document.getElementById('btnTeacherStatusAll');
    const btnAsg = document.getElementById('btnTeacherStatusAssigned');
    if (btnAll) btnAll.classList.add('active');
    if (btnAsg) btnAsg.classList.remove('active');
    renderTeacherHub();
}

/* ====================================================
   ASSIGN MODAL LOGIC (CASCADING CLASS -> SUBJECT -> SKILL -> ACTIVITY)
   ==================================================== */
/* ====================================================
   ASSIGN MODAL LOGIC (ASSIGN BY SKILL AREA)
   ==================================================== */
function openAssignModal() {
    document.getElementById('modalAssignClass').value = AppState.selectedClass;
    updateModalSubjectOptions(AppState.teacherSubjectFilter !== 'all' ? AppState.teacherSubjectFilter : undefined);
    renderAssignStudentsList();
    document.getElementById('teacherAssignModal').classList.add('active');
}

function openAssignModalForSkill(skillName) {
    document.getElementById('modalAssignClass').value = AppState.selectedClass;
    renderAssignStudentsList();

    const cls = AppState.selectedClass;
    const matchingGame = GamesCatalog.find(g => (g.class === cls || !g.class) && g.skillArea === skillName);
    const sub = matchingGame ? matchingGame.subject : (AppState.teacherSubjectFilter !== 'all' ? AppState.teacherSubjectFilter : undefined);

    updateModalSubjectOptions(sub, skillName);
    document.getElementById('teacherAssignModal').classList.add('active');
}

// Backward compatibility fallback
function openAssignModalForGame(gameId) {
    const game = GamesCatalog.find(g => g.id === gameId);
    if (game && game.skillArea) {
        openAssignModalForSkill(game.skillArea);
    } else {
        openAssignModal();
    }
}

function closeAssignModal() {
    document.getElementById('teacherAssignModal').classList.remove('active');
}

function handleModalClassChange(cls) {
    renderAssignStudentsList();
    updateModalSubjectOptions();
}

function updateModalSubjectOptions(preferredSubject, preferredSkill) {
    const cls = document.getElementById('modalAssignClass').value;
    const subSelect = document.getElementById('modalAssignSubject');
    if (!subSelect) return;

    const classGames = GamesCatalog.filter(g => g.class === cls);
    const presentSubjects = Array.from(new Set(classGames.map(g => g.subject).filter(Boolean)));
    const subjectOrder = ['Mathematics', 'English', 'EVS', 'Science', 'Social Science'];
    presentSubjects.sort((a, b) => {
        const idxA = subjectOrder.indexOf(a);
        const idxB = subjectOrder.indexOf(b);
        return (idxA !== -1 ? idxA : 99) - (idxB !== -1 ? idxB : 99);
    });

    const currentVal = preferredSubject !== undefined ? preferredSubject : subSelect.value;

    subSelect.innerHTML = '';
    presentSubjects.forEach(s => {
        const opt = document.createElement('option');
        opt.value = s;
        opt.textContent = s;
        subSelect.appendChild(opt);
    });

    if (currentVal && currentVal !== 'all' && presentSubjects.includes(currentVal)) {
        subSelect.value = currentVal;
    } else if (presentSubjects.length > 0) {
        subSelect.value = presentSubjects[0];
    } else {
        subSelect.value = '';
    }

    updateModalSkillAreaOptions(preferredSkill);
}

function handleModalSubjectChange(sub) {
    updateModalSkillAreaOptions();
}

function handleModalSkillAreaChange(sa) {
    updateModalSkillActivitiesPreview();
}

function updateModalSkillAreaOptions(preferredSkill) {
    const cls = document.getElementById('modalAssignClass').value;
    const sub = document.getElementById('modalAssignSubject').value;
    const saSelect = document.getElementById('modalAssignSkillArea');
    if (!saSelect) return;

    const games = GamesCatalog.filter(g => {
        if (g.class && g.class !== cls) return false;
        if (sub !== 'all' && g.subject !== sub) return false;
        return true;
    });

    const uniqueSkills = Array.from(new Set(games.map(g => g.skillArea).filter(Boolean))).sort();
    saSelect.innerHTML = '';

    if (uniqueSkills.length === 0) {
        saSelect.innerHTML = '<option value="">No skill areas available</option>';
    } else {
        uniqueSkills.forEach(s => {
            const count = games.filter(g => g.skillArea === s).length;
            const opt = document.createElement('option');
            opt.value = s;
            opt.textContent = `🎯 ${s} (${count} ${count === 1 ? 'activity' : 'activities'})`;
            saSelect.appendChild(opt);
        });
    }

    if (preferredSkill && uniqueSkills.includes(preferredSkill)) {
        saSelect.value = preferredSkill;
    } else if (uniqueSkills.length > 0) {
        saSelect.value = uniqueSkills[0];
    }

    updateModalSkillActivitiesPreview();
}

function updateModalSkillActivitiesPreview() {
    const cls = document.getElementById('modalAssignClass').value;
    const sub = document.getElementById('modalAssignSubject').value;
    const saSelect = document.getElementById('modalAssignSkillArea');
    const sa = saSelect ? saSelect.value : '';
    const previewBox = document.getElementById('modalSkillActivitiesPreview');
    const listEl = document.getElementById('modalSkillActivitiesList');
    const countEl = document.getElementById('modalSkillActivityCount');

    if (!sa || !previewBox || !listEl) {
        if (previewBox) previewBox.style.display = 'none';
        return;
    }

    const gamesInSkill = GamesCatalog.filter(g => {
        if (g.class && g.class !== cls) return false;
        if (sub !== 'all' && g.subject !== sub) return false;
        return g.skillArea === sa;
    });

    if (gamesInSkill.length === 0) {
        previewBox.style.display = 'none';
        return;
    }

    previewBox.style.display = 'block';
    if (countEl) countEl.textContent = gamesInSkill.length;

    listEl.innerHTML = gamesInSkill.map((g, idx) => `
                <label class="student-check-row" style="display: flex; align-items: center; justify-content: space-between; gap: 10px;">
                    <div style="display: flex; align-items: center; gap: 10px; min-width: 0; flex: 1;">
                        <input type="checkbox" name="assignActivityCheck" value="${g.id}" checked>
                        <span style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${escapeHtml(g.title)}</span>
                    </div>
                    <button type="button" class="btn-tac-preview-sm" onclick="event.preventDefault(); event.stopPropagation(); previewActivity('${g.id}')" title="Preview activity before assigning" style="flex: none; display: inline-flex; align-items: center; gap: 4px;">
                        <span>👁️</span> Preview
                    </button>
                </label>
            `).join('');
}

function toggleAssignActivitiesSelectAll() {
    const boxes = document.querySelectorAll('input[name="assignActivityCheck"]');
    const anyUnchecked = Array.from(boxes).some(b => !b.checked);
    boxes.forEach(b => b.checked = anyUnchecked);
}

function renderAssignStudentsList() {
    const cls = document.getElementById('modalAssignClass').value;
    const container = document.getElementById('modalAssignStudentsList');
    container.innerHTML = '';

    const roster = StudentRosters[cls] || [];
    roster.forEach(s => {
        const label = document.createElement('label');
        label.className = 'student-check-row';
        label.innerHTML = `
                    <input type="checkbox" name="assignStudentCheck" value="${s.roll}" data-name="${s.name}" checked>
                    <span>${s.name} (Roll #${s.roll})</span>
                `;
        container.appendChild(label);
    });
}

function toggleAssignSelectAll() {
    const boxes = document.querySelectorAll('input[name="assignStudentCheck"]');
    const anyUnchecked = Array.from(boxes).some(b => !b.checked);
    boxes.forEach(b => b.checked = anyUnchecked);
}

function submitModalAssignment() {
    const cls = document.getElementById('modalAssignClass').value;
    const sub = document.getElementById('modalAssignSubject').value;
    const sa = document.getElementById('modalAssignSkillArea').value;

    if (!sa) {
        alert('Please select a skill area.');
        return;
    }

    const checkedActivityBoxes = Array.from(document.querySelectorAll('input[name="assignActivityCheck"]:checked'));
    if (checkedActivityBoxes.length === 0) {
        alert('Please select at least one activity to assign.');
        return;
    }

    const selectedGameIds = new Set(checkedActivityBoxes.map(b => b.value));
    const selectedGames = GamesCatalog.filter(g => selectedGameIds.has(g.id));

    const checkedStudentBoxes = Array.from(document.querySelectorAll('input[name="assignStudentCheck"]:checked'));
    if (checkedStudentBoxes.length === 0) {
        alert('Please select at least one student to assign.');
        return;
    }

    checkedStudentBoxes.forEach(box => {
        const roll = parseInt(box.value, 10);
        const name = box.dataset.name;

        selectedGames.forEach(game => {
            // Avoid duplicate pending assignment
            const exists = AppState.assignments.some(a => a.class === cls && a.gameId === game.id && a.student === name);
            if (!exists) {
                AppState.assignments.push({
                    id: "asg-" + Date.now() + "-" + roll + "-" + Math.random().toString(36).substr(2, 4),
                    class: cls,
                    subject: game.subject || sub,
                    skillArea: game.skillArea || sa,
                    activity: game.activity || '',
                    gameId: game.id,
                    gameTitle: game.title,
                    student: name,
                    roll: roll,
                    status: 'pending'
                });
            }
        });
    });

    saveAssignments();
    closeAssignModal();
    renderTeacherHub();
    renderKidZone();
    if (AppState.currentView === 'split') {
        renderSplitViews();
    }
}

function unassignSkill(skillName, cls) {
    const targetClass = cls || AppState.selectedClass;
    const gamesInSkill = GamesCatalog.filter(g => (g.class === targetClass || !g.class) && g.skillArea === skillName);
    const gameIds = new Set(gamesInSkill.map(g => g.id));
    AppState.assignments = AppState.assignments.filter(a => !(a.class === targetClass && gameIds.has(a.gameId)));
    saveAssignments();
    renderTeacherHub();
    renderKidZone();
    if (AppState.currentView === 'split') {
        renderSplitViews();
    }
}

