import os

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

start_marker = 'function renderSplitViews() {'
end_marker = '// Initialize App on DOM ready'

start_idx = c.find(start_marker)
end_idx = c.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print('Markers not found!')
    exit(1)

new_content = """function toggleSplitTeacherFilter(filter) {
            AppState.splitTeacherFilter = filter;
            renderSplitViews();
        }

        function renderSplitViews() {
            const tCol = document.getElementById('splitTeacherContent');
            const kCol = document.getElementById('splitKidContent');
            const cls = AppState.selectedClass;

            const classGames = GamesCatalog.filter(g => g.class === cls);
            const classAsgs = AppState.assignments.filter(a => a.class === cls);
            const assignedGameIds = Array.from(new Set(classAsgs.map(a => a.gameId)));
            const assignedGames = classGames.filter(g => assignedGameIds.includes(g.id));
            const splitFilter = AppState.splitTeacherFilter || 'assigned';

            const gamesToShow = splitFilter === 'assigned' ? assignedGames : classGames;

            // Populate Teacher Side
            tCol.innerHTML = `
                <div style="margin-bottom: 14px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <div>
                            <h3 style="font-family: var(--font-heading); font-size: 18.5px; font-weight: 700; color: #1e1b4b; margin: 0;">🎓 Class ${cls} Teacher Hub</h3>
                            <div style="font-size: 12px; color: var(--text-muted); margin-top: 2px;">Track completion & assign activities</div>
                        </div>
                        <button type="button" class="btn-assign-modal" style="padding: 7px 15px; font-size: 12.5px;" onclick="openAssignModal()">+ Assign</button>
                    </div>

                    <!-- Quick Class Picker in Split View -->
                    <div style="display: flex; gap: 5px; overflow-x: auto; padding-bottom: 6px; margin-bottom: 10px;">
                        ${['I','II','III','IV','V','VI','VII','VIII'].map(c => `
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
                        <div style="text-align: center; padding: 36px 16px; background: #ffffff; border: 2px dashed #fed7aa; border-radius: 16px;">
                            <div style="font-size: 32px; margin-bottom: 6px;">📋✨</div>
                            <h4 style="font-family: var(--font-heading); font-size: 16px; color: #1e1b4b; margin-bottom: 4px;">No activities assigned yet for Class ${cls}</h4>
                            <p style="font-size: 12.5px; color: var(--text-muted); margin-bottom: 12px;">Assign an activity or click 'All Curriculum' above to view all ${classGames.length} activities.</p>
                            <button type="button" class="btn-tac-assign-sm" style="margin: 0 auto;" onclick="openAssignModal()">+ Assign Activity</button>
                        </div>
                    ` : gamesToShow.map(g => {
                        const assigned = classAsgs.filter(a => a.gameId === g.id);
                        const totalAssigned = assigned.length;
                        const completed = assigned.filter(a => a.status === 'completed');
                        const compCount = completed.length;
                        const pct = totalAssigned > 0 ? Math.round((compCount / totalAssigned) * 100) : 0;
                        const isAssigned = totalAssigned > 0;

                        return `
                            <div style="background: #ffffff; border: 1.5px solid ${isAssigned ? '#c7d2fe' : '#fed7aa'}; border-radius: 14px; padding: 12px 14px; box-shadow: 0 2px 8px rgba(0,0,0,0.03);">
                                <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 8px; margin-bottom: 6px;">
                                    <div>
                                        <div style="display: flex; gap: 4px; flex-wrap: wrap; margin-bottom: 4px;">
                                            <span class="tac-badge tac-badge-subject ${g.badgeClass || ''}" style="font-size: 10px; padding: 2px 7px;">${g.subject}</span>
                                            <span class="tac-badge tac-badge-skill" style="font-size: 10px; padding: 2px 7px;">🎯 ${g.skillArea}</span>
                                            <span class="tac-badge tac-badge-act" style="font-size: 10px; padding: 2px 7px;">⚡ ${g.activity}</span>
                                        </div>
                                        <h5 style="font-family: var(--font-heading); font-size: 14.5px; font-weight: 700; color: #0f172a; margin: 0;">${g.title}</h5>
                                    </div>
                                    <div style="display: flex; gap: 4px; align-items: center; flex: none;">
                                        <button type="button" class="btn-tac-assign-sm" style="font-size: 11px; padding: 5px 10px;" onclick="openAssignModalForGame('${g.id}')">+ Assign</button>
                                        <button type="button" class="btn-tac-play-sm" style="font-size: 11px; padding: 4px 8px;" onclick="openWhoIsPlaying('${g.id}')">▶</button>
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

                                <!-- Assigned Students -->
                                <div style="display: flex; flex-wrap: wrap; gap: 4px; align-items: center;">
                                    <span style="font-size: 10.5px; color: #64748b; font-weight: 700;">Students:</span>
                                    ${isAssigned 
                                        ? assigned.map(a => `
                                            <span class="tac-chip ${a.status === 'completed' ? 'completed' : 'pending'}" style="font-size: 10.5px; padding: 2px 7px;">
                                                ${a.status === 'completed' ? `✓ ${a.student}` : `⏳ ${a.student}`}
                                            </span>
                                        `).join('')
                                        : `<span style="font-size: 10.5px; color: #94a3b8; font-style: italic;">None yet</span>`
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
                        <div style="text-align: center; padding: 36px 16px; background: #fffbf5; border: 2px dashed #fed7aa; border-radius: 16px;">
                            <div style="font-size: 36px; margin-bottom: 8px;">🎒✨</div>
                            <h4 style="font-family: var(--font-heading); font-size: 16.5px; color: #1e1b4b; margin-bottom: 4px;">No assigned activities for Class ${cls}</h4>
                            <p style="font-size: 12.5px; color: var(--text-muted); margin-bottom: 12px;">Assign an activity on the Teacher side to see it appear here instantly!</p>
                            <button type="button" class="btn-assign-modal" style="padding: 7px 14px; font-size: 12px; margin: 0 auto;" onclick="openAssignModal()">+ Assign First Activity</button>
                        </div>
                    ` : assignedGames.map(game => {
                        const assignedSts = classAsgs.filter(a => a.gameId === game.id);
                        const isDone = assignedSts.some(a => a.status === 'completed');

                        return `
                            <div class="game-card" style="box-shadow: 0 4px 14px rgba(0,0,0,0.05); border-radius: 16px; overflow: hidden;">
                                <div class="game-thumb-wrap" style="height: 110px;">
                                    <img src="${game.thumb}" alt="${game.title}" class="game-thumb-img">
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

        """

c = c[:start_idx] + new_content + c[end_idx:]
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print('Split Views JS updated successfully!')
