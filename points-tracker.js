/**
 * Points Tracker - Displays student points and progress
 */

class PointsTracker {
    constructor() {
        this.currentPoints = 0;
        this.totalQuestions = 5;
        this.correctAnswers = 0;
        this.wrongAnswers = 0;
    }

    /**
     * Create and display points tracker widget
     */
    createTracker() {
        const tracker = document.createElement("div");
        tracker.id = "points-tracker";
        tracker.innerHTML = `
            <div class="tracker-container">
                <div class="tracker-header">📊 STUDENT PROGRESS</div>

                <div class="tracker-content">
                    <div class="tracker-row">
                        <span class="tracker-label">Total Points:</span>
                        <span class="tracker-value" id="totalPoints">0</span>
                    </div>

                    <div class="tracker-row">
                        <span class="tracker-label">Correct Answers:</span>
                        <span class="tracker-value correct" id="correctCount">0</span>
                    </div>

                    <div class="tracker-row">
                        <span class="tracker-label">Wrong Answers:</span>
                        <span class="tracker-value wrong" id="wrongCount">0</span>
                    </div>

                    <div class="tracker-row">
                        <span class="tracker-label">Progress:</span>
                        <span class="tracker-value" id="progressText">0 / 5</span>
                    </div>
                </div>

                <div class="progress-bar-container">
                    <div class="progress-bar" id="progressBar">
                        <div class="progress-fill" id="progressFill"></div>
                    </div>
                </div>
            </div>
        `;

        // Add styles
        this.addStyles();

        // Append to body
        document.body.appendChild(tracker);
    }

    /**
     * Add CSS styles for tracker
     */
    addStyles() {
        const style = document.createElement("style");
        style.innerHTML = `
            #points-tracker {
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 9998;
                background: white;
                border: 3px solid #667eea;
                border-radius: 15px;
                padding: 20px;
                width: 280px;
                box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
            }

            .tracker-container {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }

            .tracker-header {
                font-size: 18px;
                font-weight: bold;
                color: #667eea;
                margin-bottom: 15px;
                text-align: center;
                border-bottom: 2px solid #f0f4ff;
                padding-bottom: 10px;
            }

            .tracker-content {
                margin-bottom: 15px;
            }

            .tracker-row {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 10px 0;
                border-bottom: 1px solid #f0f4ff;
            }

            .tracker-row:last-child {
                border-bottom: none;
            }

            .tracker-label {
                font-size: 14px;
                color: #666;
                font-weight: 600;
            }

            .tracker-value {
                font-size: 20px;
                font-weight: bold;
                color: #667eea;
                background: #f0f4ff;
                padding: 5px 12px;
                border-radius: 8px;
                min-width: 60px;
                text-align: center;
            }

            .tracker-value.correct {
                color: #4caf50;
                background: #e8f5e9;
            }

            .tracker-value.wrong {
                color: #f44336;
                background: #ffebee;
            }

            .progress-bar-container {
                margin-top: 15px;
            }

            .progress-bar {
                width: 100%;
                height: 20px;
                background: #f0f4ff;
                border-radius: 10px;
                overflow: hidden;
                border: 2px solid #667eea;
            }

            .progress-fill {
                height: 100%;
                background: linear-gradient(90deg, #4caf50, #8bc34a);
                width: 0%;
                transition: width 0.3s ease;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 12px;
                font-weight: bold;
            }

            /* Mobile responsive */
            @media (max-width: 768px) {
                #points-tracker {
                    width: 220px;
                    top: 10px;
                    right: 10px;
                }

                .tracker-value {
                    font-size: 16px;
                }

                .tracker-label {
                    font-size: 12px;
                }
            }
        `;
        document.head.appendChild(style);
    }

    /**
     * Add points for correct answer
     */
    addCorrectPoints() {
        this.currentPoints += 10;
        this.correctAnswers++;
        this.updateDisplay();
    }

    /**
     * Add wrong answer (no points)
     */
    addWrongAnswer() {
        this.wrongAnswers++;
        this.updateDisplay();
    }

    /**
     * Update the tracker display
     */
    updateDisplay() {
        const totalQuestions = this.correctAnswers + this.wrongAnswers;
        const percentage = (totalQuestions / this.totalQuestions) * 100;

        // Update values
        document.getElementById("totalPoints").textContent = this.currentPoints;
        document.getElementById("correctCount").textContent = this.correctAnswers;
        document.getElementById("wrongCount").textContent = this.wrongAnswers;
        document.getElementById("progressText").textContent = `${totalQuestions} / ${this.totalQuestions}`;

        // Update progress bar
        const progressFill = document.getElementById("progressFill");
        progressFill.style.width = percentage + "%";

        // Log for debugging
        console.log(`Points: ${this.currentPoints} | Correct: ${this.correctAnswers} | Wrong: ${this.wrongAnswers}`);
    }

    /**
     * Get final score
     */
    getFinalScore() {
        return this.currentPoints;
    }

    /**
     * Reset tracker for new game
     */
    reset() {
        this.currentPoints = 0;
        this.correctAnswers = 0;
        this.wrongAnswers = 0;
        this.updateDisplay();
    }
}

// Create global instance
const pointsTracker = new PointsTracker();
