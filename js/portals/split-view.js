/* ====================================================
   SPLIT VIEW RENDERING (SYNCHRONIZED TEACHER HUB & STUDENT ZONE)
   ==================================================== */
function toggleSplitTeacherFilter(filter) {
    AppState.splitTeacherFilter = filter;
    renderSplitViews();
}

function renderSplitViews() {
    const tCol = document.getElementById('splitTeacherContent');
    const kCol = document.getElementById('splitKidContent');
    const cls = AppState.selectedClass;
    const roster = StudentRosters[cls] || [];

    const classGames = GamesCatalog.filter(g => g.class === cls);
    const classAsgs = AppState.assignments.filter(a => a.class === cls);
    const assignedOrder = [];
    classAsgs.forEach(a => {
        if (!assignedOrder.includes(a.gameId)) {
            assignedOrder.push(a.gameId);
        }
    });
    const assignedGames = assignedOrder.map(id => classGames.find(g => g.id === id)).filter(Boolean);
    const splitFilter = AppState.splitTeacherFilter || 'assigned';

    // Sort: Assigned activities first, in assigned order
    const sortedClassGames = [...classGames].sort((a, b) => {
        const aIdx = assignedOrder.indexOf(a.id);
        const bIdx = assignedOrder.indexOf(b.id);
        const aHas = aIdx !== -1;
        const bHas = bIdx !== -1;
        if (aHas && !bHas) return -1;
        if (!aHas && bHas) return 1;
        if (aHas && bHas) return aIdx - bIdx;
        return 0;
    });

    const gamesToShow = splitFilter === 'assigned' ? assignedGames : sortedClassGames;

    // Populate Teacher Side
    tCol.innerHTML = `
                <div style="margin-bottom: 14px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; gap: 10px; flex-wrap: wrap;">
                        <div>
                            <h3 style="font-family: var(--font-heading); font-size: 18.5px; font-weight: 700; color: #1e1b4b; margin: 0;">🎓 Class ${cls} Teacher Hub</h3>
                            <div style="font-size: 12px; color: var(--text-muted); margin-top: 2px;">Track completion & assignments</div>
                        </div>
                        <button type="button" class="btn-teacher-assign-bar" style="padding: 6px 14px; font-size: 12.5px; border-radius: 9px; display: inline-flex; align-items: center; gap: 6px; cursor: pointer; box-shadow: 0 2px 6px rgba(99, 102, 241, 0.25);" onclick="openAssignModal('${cls}')" title="Assign activities to Class ${cls}">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                                <circle cx="8.5" cy="7" r="4"></circle>
                                <line x1="20" y1="8" x2="20" y2="14"></line>
                                <line x1="23" y1="11" x2="17" y2="11"></line>
                            </svg>
                            <span>+ Assign Activities</span>
                        </button>
                    </div>

                    <!-- Quick Class Picker in Split View -->
                    <div style="display: flex; gap: 5px; overflow-x: auto; padding-bottom: 6px; margin-bottom: 10px;">
                        ${['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII'].map(c => `
                            <button type="button" class="teacher-class-pill ${c === cls ? 'active' : ''}" style="padding: 4px 10px; font-size: 11.5px;" onclick="handleClassFilterChange('${c}')">Class ${c}</button>
                        `).join('')}
                    </div>

                    <!-- Filter Toggle (Assigned Only vs All) -->
                    <div class="tab-toggles tab-toggles-sm" style="margin-bottom: 12px;">
                        <button type="button" class="tab-btn ${splitFilter === 'assigned' ? 'active' : ''}" onclick="toggleSplitTeacherFilter('assigned')">
                            📖 Assigned Only (${assignedGames.length})
                        </button>
                        <button type="button" class="tab-btn ${splitFilter === 'all' ? 'active' : ''}" onclick="toggleSplitTeacherFilter('all')">
                            All Curriculum (${classGames.length})
                        </button>
                    </div>
                </div>

                <!-- Teacher Activities List -->
                <div style="display: flex; flex-direction: column; gap: 10px;">
                    ${gamesToShow.length === 0 ? `
                        <div style="text-align: center; padding: 36px 16px; background: #ffffff; border: 1.5px dashed #cbd5e1; border-radius: 16px;">
                            <div style="font-size: 32px; margin-bottom: 6px;">📋✨</div>
                            <h4 style="font-family: var(--font-heading); font-size: 16px; color: #1e1b4b; margin-bottom: 4px;">No activities assigned yet for Class ${cls}</h4>
                            <p style="font-size: 12.5px; color: var(--text-muted); margin-bottom: 14px;">Assign curriculum activities for this class to start tracking real-time student completion.</p>
                            <div style="display: flex; justify-content: center; gap: 8px; flex-wrap: wrap;">
                                <button type="button" class="btn-teacher-assign-bar" style="padding: 7px 16px; font-size: 12.5px; border-radius: 8px; display: inline-flex; align-items: center; gap: 6px; cursor: pointer;" onclick="openAssignModal('${cls}')">
                                    + Assign Activities
                                </button>
                                <button type="button" class="btn-clear-filters" style="margin: 0;" onclick="toggleSplitTeacherFilter('all')">
                                    View All Curriculum
                                </button>
                            </div>
                        </div>
                    ` : gamesToShow.map(g => {
        const assigned = classAsgs.filter(a => a.gameId === g.id);
        const totalAssigned = assigned.length;
        const completed = assigned.filter(a => a.status === 'completed');
        const compCount = completed.length;
        const pct = totalAssigned > 0 ? Math.round((compCount / totalAssigned) * 100) : 0;
        const isAssigned = totalAssigned > 0;

        const isSpecificSubject = AppState.teacherSubjectFilter && AppState.teacherSubjectFilter !== 'all';

        return `
                            <div style="background: #ffffff; border: 1px solid ${isAssigned ? '#818cf8' : '#e2e8f0'}; border-radius: 14px; padding: 12px 14px; box-shadow: 0 2px 8px rgba(0,0,0,0.03);">
                                <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 8px; margin-bottom: 6px;">
                                    <div>
                                        <div style="display: flex; align-items: center; gap: 6px; flex-wrap: wrap; margin-bottom: 4px;">
                                            ${!isSpecificSubject ? `<span class="tac-badge tac-badge-subject ${g.badgeClass || ''}" style="font-size: 10px; padding: 2px 7px;">${g.subject}</span>` : ''}
                                            ${g.isCustom ? '<span class="tac-badge tac-badge-custom" style="font-size: 10px; padding: 2px 7px;">⭐ Custom</span>' : ''}
                                            <span class="tac-badge tac-badge-skill" style="font-size: 10px; padding: 2px 7px;">🎯 ${g.skillArea || 'Skill'}</span>
                                            <h5 class="curriculum-title" style="font-family: var(--font-heading); font-size: 14px; font-weight: 700; color: #0f172a; margin: 0; display: inline; cursor: pointer;" onclick="previewActivity('${g.id}')" title="Click to preview: ${escapeHtml(g.title)}">${g.title}</h5>
                                        </div>
                                    </div>
                                    <div style="display: flex; gap: 6px; align-items: center; flex: none;">
                                        <button type="button" class="btn-tac-preview-sm" style="font-size: 11px; padding: 4px 10px;" onclick="previewActivity('${g.id}')" title="Preview activity">👁️ Preview</button>
                                        ${!isAssigned ? `
                                            <button type="button" class="btn-tac-preview-sm" style="font-size: 11px; padding: 4px 10px; background: #e0e7ff; color: #3730a3; border-color: #c7d2fe; font-weight: 700; cursor: pointer;" onclick="openAssignModalForSkill('${escapeHtml(g.skillArea || '')}', '${cls}')" title="Assign ${escapeHtml(g.skillArea || 'Skill')} to Class ${cls}">+ Assign</button>
                                        ` : `
                                            <button type="button" class="btn-clear-assignments-sm" style="font-size: 10.5px; padding: 3px 8px; border-radius: 6px;" onclick="unassignActivity('${g.id}')" title="Unassign from Class ${cls}">✕ Unassign</button>
                                        `}
                                    </div>
                                </div>

                                <!-- Progress bar -->
                                <div style="margin: 6px 0; background: #f8fafc; padding: 5px 8px; border-radius: 8px; border: 1px solid #e2e8f0;">
                                    <div style="display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 3px;">
                                        <span style="color: #64748b; font-weight: 600;">Completion:</span>
                                        <span style="font-weight: 700; color: ${pct === 100 ? '#15803d' : '#0f172a'};">
                                            ${isAssigned ? `${compCount}/${totalAssigned} (${pct}%)` : 'Not assigned'}
                                        </span>
                                    </div>
                                    <div style="height: 6px; background: #e2e8f0; border-radius: 999px; overflow: hidden;">
                                        <div style="height: 100%; border-radius: 999px; width: ${pct}%; background: ${pct === 100 ? '#10b981' : 'linear-gradient(90deg, #f59e0b, #10b981)'};"></div>
                                    </div>
                                </div>

                                <!-- Student Names & Status -->
                                <div style="display: flex; flex-wrap: wrap; gap: 4px; align-items: center; margin-top: 6px;">
                                    <span style="font-size: 10.5px; color: #64748b; font-weight: 700;">Students:</span>
                                    ${isAssigned
                ? assigned.map(a => `
                                            <span class="tac-chip ${a.status === 'completed' ? 'completed' : 'pending'}" style="font-size: 10px; padding: 2px 7px;">
                                                ${a.status === 'completed' ? `✓ ${a.student}` : `⏳ ${a.student}`}
                                            </span>
                                        `).join('')
                : `<span style="font-size: 11px; color: #94a3b8; font-weight: 500;">—</span>`
            }
                                </div>
                            </div>
                        `;
    }).join('')}
                </div>
            `;

    // Populate Kid Side (Assigned Activities)
    kCol.innerHTML = `
                <div style="margin-bottom: 14px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <div>
                            <h3 style="font-family: var(--font-heading); font-size: 18.5px; font-weight: 700; color: #1e1b4b; margin: 0;">🎒 Class ${cls} Student Zone</h3>
                            <div style="font-size: 12px; color: var(--text-muted); margin-top: 2px;">Assigned quests for your class</div>
                        </div>
                        <span class="tab-counter-badge" style="background: #ede9fe; color: #6d28d9;">${assignedGames.length} active quests</span>
                    </div>
                </div>

                <div style="display: flex; flex-direction: column; gap: 12px;">
                    ${assignedGames.length === 0 ? `
                        <div style="text-align: center; padding: 36px 16px; background: #f8fafc; border: 1.5px dashed #cbd5e1; border-radius: 16px;">
                            <div style="font-size: 36px; margin-bottom: 8px;">🎒✨</div>
                            <h4 style="font-family: var(--font-heading); font-size: 16.5px; color: #1e1b4b; margin-bottom: 4px;">No assigned activities for Class ${cls}</h4>
                            <p style="font-size: 12.5px; color: var(--text-muted); margin-bottom: 6px;">Activities assigned by your teacher in Teacher Hub will appear here!</p>
                        </div>
                    ` : assignedGames.map(game => {
        const assignedSts = classAsgs.filter(a => a.gameId === game.id);
        const isDone = assignedSts.some(a => a.status === 'completed');

        return `
                            <div class="game-card" style="box-shadow: 0 4px 14px rgba(0,0,0,0.05); border-radius: 16px; overflow: hidden;">
                                <div class="game-thumb-wrap" style="height: 110px;">
                                    <img src="${game.thumb}" alt="${game.title}" class="game-thumb-img" onerror="if(!this.src.endsWith('.svg')){this.src='images/thumbnails/${game.id}.svg';}">
                                    <span class="subject-badge-pill ${game.badgeClass}">${game.subject}</span>
                                    ${isDone ? '<span class="game-status-pill"><span>✓</span> Progress Active</span>' : ''}
                                </div>
                                <div class="game-info-body" style="padding: 14px;">
                                    <div class="game-category-tags" style="margin-bottom: 6px;">
                                        <span class="skill-tag-pill" style="font-size: 10px;">🎯 ${game.skillArea}</span>
                                        <span class="activity-tag-pill" style="font-size: 10px;">⚡ ${game.activity}</span>
                                    </div>
                                    <h4 style="font-family: var(--font-heading); font-size: 16px; font-weight: 700; color: #1e1b4b; margin-bottom: 4px;">${game.title}</h4>
                                    <p style="font-size: 12px; color: var(--text-muted); line-height: 1.35; margin-bottom: 8px;">${game.desc}</p>
                                    
                                    <!-- Assigned Students summary -->
                                    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 5px 8px; margin-bottom: 10px; font-size: 11px; color: #4338ca; font-weight: 700;">
                                        👥 Assigned: ${assignedSts.map(a => `${a.student}${a.status === 'completed' ? ' (✓)' : ''}`).join(', ')}
                                    </div>

                                    <button type="button" class="btn-play-action" style="padding: 8px 14px; font-size: 13px;" onclick="openWhoIsPlaying('${game.id}')">
                                        <span>▶</span> Play Activity 🚀
                                    </button>
                                </div>
                            </div>
                        `;
    }).join('')}
                </div>
            `;
}


