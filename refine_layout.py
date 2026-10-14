import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add refined layout CSS
layout_css = """
        /* ====================================================
           UNIFIED & REFINED SIMPLE LAYOUT SYSTEM
           ==================================================== */
        .unified-control-panel {
            background: #ffffff;
            border: 2px solid #fed7aa;
            border-radius: var(--radius-lg);
            padding: 14px 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 16px rgba(245, 158, 11, 0.05);
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .ucp-top-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 12px;
            padding-bottom: 12px;
            border-bottom: 1.5px solid #fef3c7;
        }

        .ucp-bottom-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 12px;
        }

        .teacher-metrics-strip-inline {
            display: flex;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
        }

        .tms-badge {
            font-family: var(--font-heading);
            font-size: 12px;
            font-weight: 700;
            padding: 3px 10px;
            border-radius: 999px;
            display: inline-flex;
            align-items: center;
            gap: 4px;
        }

        .tms-total { background: #f5f3ff; color: #6d28d9; border: 1px solid #ddd6fe; }
        .tms-assigned { background: #fffbeb; color: #b45309; border: 1px solid #fde68a; }
        .tms-done { background: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; }
        .tms-pending { background: #fff7ed; color: #c2410c; border: 1px solid #fed7aa; }

        .tab-toggles-sm .tab-btn {
            padding: 6px 14px;
            font-size: 12px;
        }

        /* Clean Teacher Curriculum Table */
        .teacher-table-container {
            background: #ffffff;
            border: 2px solid #fed7aa;
            border-radius: var(--radius-xl);
            overflow: hidden;
            box-shadow: 0 8px 24px rgba(245, 158, 11, 0.06);
        }

        .curriculum-table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
        }

        .curriculum-table thead th {
            background: #fffbeb;
            padding: 14px 18px;
            font-family: var(--font-heading);
            font-size: 12.5px;
            font-weight: 700;
            color: #78350f;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            border-bottom: 2px solid #fde68a;
        }

        .curriculum-row {
            border-bottom: 1px solid #f1f5f9;
            transition: background 0.15s ease;
        }

        .curriculum-row:hover {
            background: #fffbf5;
        }

        .curriculum-row.is-assigned {
            background: #faf5ff;
        }

        .curriculum-row.is-assigned:hover {
            background: #f5f3ff;
        }

        .curriculum-row td {
            padding: 14px 18px;
            vertical-align: middle;
        }

        .curriculum-title-wrap {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }

        .curriculum-badges {
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
            align-items: center;
        }

        .curriculum-title {
            font-family: var(--font-heading);
            font-size: 15.5px;
            font-weight: 700;
            color: #1e1b4b;
        }

        .curriculum-progress-wrap {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }

        .curriculum-pct {
            font-family: var(--font-heading);
            font-size: 12.5px;
            font-weight: 700;
        }

        .curriculum-pct.done { color: #15803d; }
        .curriculum-pct.in-prog { color: #b45309; }
        .curriculum-pct.none { color: #94a3b8; font-weight: 600; }

        .curriculum-students-cell {
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
            align-items: center;
        }

        .curriculum-empty-dash {
            color: #cbd5e1;
            font-weight: 700;
            font-size: 16px;
        }

        .btn-tac-assign-sm {
            background: linear-gradient(180deg, #6366f1 0%, #4f46e5 100%);
            color: white;
            border: none;
            padding: 6px 14px;
            border-radius: 999px;
            font-family: var(--font-heading);
            font-size: 12px;
            font-weight: 700;
            cursor: pointer;
            box-shadow: 0 2px 0 #3730a3;
            transition: transform 0.15s;
            white-space: nowrap;
        }

        .btn-tac-assign-sm:hover {
            transform: translateY(-1px);
        }

        .btn-tac-play-sm {
            background: #f8fafc;
            border: 1.5px solid #fed7aa;
            color: #78350f;
            padding: 5px 12px;
            border-radius: 999px;
            font-family: var(--font-heading);
            font-size: 11.5px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.15s;
            white-space: nowrap;
        }

        .btn-tac-play-sm:hover {
            background: #fef3c7;
            border-color: #f59e0b;
        }

        /* View Mode Switcher Pills (Table vs Cards) */
        .view-mode-toggle {
            display: inline-flex;
            background: #fef3c7;
            padding: 3px;
            border-radius: 999px;
            border: 1.5px solid #fde68a;
            gap: 2px;
        }

        .view-mode-btn {
            border: none;
            background: transparent;
            padding: 4px 10px;
            border-radius: 999px;
            font-family: var(--font-heading);
            font-size: 11.5px;
            font-weight: 700;
            color: #78350f;
            cursor: pointer;
        }

        .view-mode-btn.active {
            background: #ffffff;
            color: #4f46e5;
            box-shadow: 0 2px 6px rgba(79, 70, 229, 0.15);
        }
"""

if '/* UNIFIED & REFINED SIMPLE LAYOUT SYSTEM */' not in html:
    html = html.replace('</style>', layout_css + '\n    </style>')

# 2. Replace kidZoneView HTML
new_kid_zone_html = """<!-- ====================================================
             1. KID ZONE VIEW (SIMPLE & UNIFIED LAYOUT)
             ==================================================== -->
        <div id="kidZoneView">
            
            <!-- Single Unified Control Panel -->
            <div class="unified-control-panel">
                <!-- Top Row: Mode Tabs & Class Selector -->
                <div class="ucp-top-row">
                    <div class="tab-toggles">
                        <button type="button" class="tab-btn active" id="tabMyAssignments" onclick="setKidSubTab('assigned')">
                            <span>📖</span> Assigned activities <span class="tab-counter-badge" id="assignedCountBadge">0</span>
                        </button>
                        <button type="button" class="tab-btn" id="tabExploreGames" onclick="setKidSubTab('explore')">
                            <span>🧭</span> Explore all games
                        </button>
                    </div>

                    <div class="teacher-class-selector-wrapper">
                        <span class="teacher-class-label">Class:</span>
                        <div class="teacher-class-pill-group" id="kidClassPills">
                            <button type="button" class="teacher-class-pill" onclick="handleClassFilterChange('I')">Class I</button>
                            <button type="button" class="teacher-class-pill" onclick="handleClassFilterChange('II')">Class II</button>
                            <button type="button" class="teacher-class-pill" onclick="handleClassFilterChange('III')">Class III</button>
                            <button type="button" class="teacher-class-pill active" onclick="handleClassFilterChange('IV')">Class IV</button>
                            <button type="button" class="teacher-class-pill" onclick="handleClassFilterChange('V')">Class V</button>
                            <button type="button" class="teacher-class-pill" onclick="handleClassFilterChange('VI')">Class VI</button>
                            <button type="button" class="teacher-class-pill" onclick="handleClassFilterChange('VII')">Class VII</button>
                            <button type="button" class="teacher-class-pill" onclick="handleClassFilterChange('VIII')">Class VIII</button>
                        </div>
                        <select class="class-dropdown-btn" id="kidClassSelect" style="display: none;" onchange="handleClassFilterChange(this.value)">
                            <option value="I">Class I</option>
                            <option value="II">Class II</option>
                            <option value="III">Class III</option>
                            <option value="IV" selected>Class IV</option>
                            <option value="V">Class V</option>
                            <option value="VI">Class VI</option>
                            <option value="VII">Class VII</option>
                            <option value="VIII">Class VIII</option>
                        </select>
                    </div>
                </div>

                <!-- Bottom Row: Subject Filter Chips, Skill/Activity Dropdowns & Search -->
                <div class="ucp-bottom-row">
                    <div class="subject-filter-chips">
                        <button type="button" class="chip-btn active" onclick="filterBySubject('all', this)">All</button>
                        <button type="button" class="chip-btn" onclick="filterBySubject('Mathematics', this)"><span class="chip-dot chip-dot-math"></span> Math</button>
                        <button type="button" class="chip-btn" onclick="filterBySubject('Science', this)"><span class="chip-dot chip-dot-sci"></span> Science</button>
                        <button type="button" class="chip-btn" onclick="filterBySubject('English', this)"><span class="chip-dot chip-dot-eng"></span> English</button>
                        <button type="button" class="chip-btn" onclick="filterBySubject('EVS', this)"><span class="chip-dot chip-dot-evs"></span> EVS</button>
                        <button type="button" class="chip-btn" onclick="filterBySubject('Social Science', this)"><span class="chip-dot chip-dot-soc"></span> Social</button>
                    </div>

                    <!-- Cascading Skill Area & Activity Dropdowns (inline) -->
                    <div id="kidSkillActivityInline" style="display: none; gap: 8px; align-items: center;">
                        <select class="cascade-filter-select" id="filterSkillAreaSelect" style="width: 170px; padding: 6px 10px; font-size: 12.5px;" onchange="handleSkillAreaFilterChange(this.value)">
                            <option value="all">🎯 All Skills</option>
                        </select>
                        <select class="cascade-filter-select" id="filterActivitySelect" style="width: 170px; padding: 6px 10px; font-size: 12.5px;" onchange="handleActivityFilterChange(this.value)">
                            <option value="all">⚡ All Activities</option>
                        </select>
                    </div>

                    <div style="display: flex; gap: 8px; align-items: center; margin-left: auto;">
                        <input type="text" class="search-box-input" id="gameSearchInput" placeholder="Search activities..." oninput="handleGameSearch(this.value)">
                        <button type="button" class="btn-clear-filters" id="btnClearFilters" onclick="resetAllFilters()" style="display: none;">✕ Clear</button>
                    </div>
                </div>
            </div>

            <!-- Full-Width Clean Games Grid -->
            <div class="games-grid full-width-grid" id="gamesCardsGrid">
                <!-- Populated dynamically via renderGamesGrid() -->
            </div>

        </div>"""

# Replace kidZoneView block
kid_view_regex = r'<!-- ====================================================\s*1\. KID ZONE VIEW.*?</div>\s*<!-- ====================================================\s*2\. TEACHER HUB VIEW'
html = re.sub(kid_view_regex, new_kid_zone_html + '\n\n        <!-- ====================================================\n             2. TEACHER HUB VIEW', html, flags=re.DOTALL)
print('Kid Zone HTML updated!')

# 3. Replace teacherHubView HTML
new_teacher_hub_html = """<!-- ====================================================
             2. TEACHER HUB VIEW (CLEAN CURRICULUM BOARD)
             ==================================================== -->
        <div id="teacherHubView" class="teacher-view-wrap">
            
            <!-- Single Unified Control Panel -->
            <div class="unified-control-panel">
                <!-- Top Row: Title, Inline Metrics & Class Selector -->
                <div class="ucp-top-row">
                    <div style="display: flex; align-items: center; gap: 14px; flex-wrap: wrap;">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <h2 style="font-family: var(--font-heading); font-size: 21px; font-weight: 700; color: #1e1b4b; margin: 0;">🎓 Teacher Hub</h2>
                            <span class="tab-counter-badge" id="teacherBadgeAssignedCount">0 activities</span>
                        </div>
                        <div class="teacher-metrics-strip-inline">
                            <span class="tms-badge tms-total">📚 <strong id="teacherStatTotalActivities">0</strong> in Class <span id="teacherStatClassLabel">IV</span></span>
                            <span class="tms-badge tms-assigned">👥 <strong id="teacherStatAssignedActivities">0</strong> Assigned</span>
                            <span class="tms-badge tms-done">✓ <strong id="teacherStatCompleted">0</strong> Completed</span>
                            <span class="tms-badge tms-pending">⏳ <strong id="teacherStatPending">0</strong> Pending</span>
                        </div>
                    </div>

                    <div class="teacher-class-selector-wrapper">
                        <span class="teacher-class-label">Class:</span>
                        <div class="teacher-class-pill-group" id="teacherClassPills">
                            <button type="button" class="teacher-class-pill" onclick="handleTeacherClassChange('I')">Class I</button>
                            <button type="button" class="teacher-class-pill" onclick="handleTeacherClassChange('II')">Class II</button>
                            <button type="button" class="teacher-class-pill" onclick="handleTeacherClassChange('III')">Class III</button>
                            <button type="button" class="teacher-class-pill active" onclick="handleTeacherClassChange('IV')">Class IV</button>
                            <button type="button" class="teacher-class-pill" onclick="handleTeacherClassChange('V')">Class V</button>
                            <button type="button" class="teacher-class-pill" onclick="handleTeacherClassChange('VI')">Class VI</button>
                            <button type="button" class="teacher-class-pill" onclick="handleTeacherClassChange('VII')">Class VII</button>
                            <button type="button" class="teacher-class-pill" onclick="handleTeacherClassChange('VIII')">Class VIII</button>
                        </div>
                        <select class="class-dropdown-btn" id="teacherClassSelect" style="display: none;" onchange="handleTeacherClassChange(this.value)">
                            <option value="I">Class I</option>
                            <option value="II">Class II</option>
                            <option value="III">Class III</option>
                            <option value="IV" selected>Class IV</option>
                            <option value="V">Class V</option>
                            <option value="VI">Class VI</option>
                            <option value="VII">Class VII</option>
                            <option value="VIII">Class VIII</option>
                        </select>
                    </div>
                </div>

                <!-- Bottom Row: Subject Filter Chips, Status Filter, Search & + Assign Button -->
                <div class="ucp-bottom-row">
                    <div class="subject-filter-chips" id="teacherSubjectChips">
                        <button type="button" class="chip-btn active" onclick="filterTeacherSubject('all', this)">All</button>
                        <button type="button" class="chip-btn" onclick="filterTeacherSubject('Mathematics', this)"><span class="chip-dot chip-dot-math"></span> Math</button>
                        <button type="button" class="chip-btn" onclick="filterTeacherSubject('English', this)"><span class="chip-dot chip-dot-eng"></span> English</button>
                        <button type="button" class="chip-btn" onclick="filterTeacherSubject('EVS', this)"><span class="chip-dot chip-dot-evs"></span> EVS</button>
                        <button type="button" class="chip-btn" onclick="filterTeacherSubject('Science', this)"><span class="chip-dot chip-dot-sci"></span> Science</button>
                        <button type="button" class="chip-btn" onclick="filterTeacherSubject('Social Science', this)"><span class="chip-dot chip-dot-soc"></span> Social</button>
                    </div>

                    <!-- Quick Status Filter (All vs Assigned Only) -->
                    <div class="tab-toggles tab-toggles-sm">
                        <button type="button" class="tab-btn active" id="btnTeacherStatusAll" onclick="filterTeacherStatus('all', this)">All Activities</button>
                        <button type="button" class="tab-btn" id="btnTeacherStatusAssigned" onclick="filterTeacherStatus('assigned', this)">Assigned Only</button>
                    </div>

                    <!-- Layout Mode Switcher (Table vs Cards) -->
                    <div class="view-mode-toggle">
                        <button type="button" class="view-mode-btn active" id="btnModeTable" onclick="setTeacherLayoutMode('table', this)" title="Table view">☰ Table</button>
                        <button type="button" class="view-mode-btn" id="btnModeGrid" onclick="setTeacherLayoutMode('grid', this)" title="Cards grid view">⊞ Cards</button>
                    </div>

                    <div style="display: flex; gap: 10px; align-items: center; margin-left: auto;">
                        <input type="text" class="search-box-input" style="width: 200px;" id="teacherSearchInput" placeholder="Search activities..." oninput="filterTeacherActivities(this.value)">
                        <button type="button" class="btn-assign-modal" onclick="openAssignModal()">
                            <span>+</span> Assign an Activity
                        </button>
                    </div>
                </div>
            </div>

            <!-- Table View Container -->
            <div class="teacher-table-container" id="teacherTableContainer">
                <table class="curriculum-table">
                    <thead>
                        <tr>
                            <th style="width: 38%;">Activity & Categories</th>
                            <th style="width: 24%;">Completion Progress</th>
                            <th style="width: 24%;">Assigned Students</th>
                            <th style="width: 14%; text-align: right;">Action</th>
                        </tr>
                    </thead>
                    <tbody id="teacherTableBody">
                        <!-- Populated dynamically via renderTeacherHub() -->
                    </tbody>
                </table>
            </div>

            <!-- Grid View Container (Hidden by default, can be toggled) -->
            <div id="teacherActivitiesGrid" class="teacher-activities-grid" style="display: none;">
                <!-- Populated dynamically via renderTeacherHub() -->
            </div>

        </div>"""

teacher_view_regex = r'<!-- ====================================================\s*2\. TEACHER HUB VIEW.*?</div>\s*<!-- ====================================================\s*3\. SPLIT VIEW CONTAINER'
html = re.sub(teacher_view_regex, new_teacher_hub_html + '\n\n        <!-- ====================================================\n             3. SPLIT VIEW CONTAINER', html, flags=re.DOTALL)
print('Teacher Hub HTML updated!')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('HTML saved!')
