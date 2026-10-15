/**
 * Audio Generator - Creates sound effects using Web Audio API
 * Generates correct (claps) and wrong (buzzer) sounds
 */

class AudioGenerator {
    constructor() {
        this.audioContext = null;
    }

    initAudio() {
        if (!this.audioContext) {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        }
        return this.audioContext;
    }

    /**
     * Play correct answer sound (3 claps)
     */
    playCorrectSound() {
        try {
            const ctx = this.initAudio();
            const now = ctx.currentTime;

            // 3 CLAPS at different frequencies
            for (let i = 0; i < 3; i++) {
                const osc = ctx.createOscillator();
                const env = ctx.createGain();

                osc.connect(env);
                env.connect(ctx.destination);

                // Frequencies: 800Hz, 900Hz, 1000Hz
                osc.frequency.value = 800 + (i * 100);

                // Envelope: quick attack, quick decay (clap sound)
                env.gain.setValueAtTime(0.4, now + (i * 0.25));
                env.gain.exponentialRampToValueAtTime(0.01, now + (i * 0.25) + 0.12);

                osc.start(now + (i * 0.25));
                osc.stop(now + (i * 0.25) + 0.12);
            }

            console.log("✅ Correct sound played");
        } catch (e) {
            console.error("Error playing correct sound:", e);
        }
    }

    /**
     * Play wrong answer sound (buzzer)
     */
    playWrongSound() {
        try {
            const ctx = this.initAudio();
            const now = ctx.currentTime;

            // BUZZER: Frequency sweep 300Hz -> 200Hz -> 300Hz
            const osc = ctx.createOscillator();
            const env = ctx.createGain();

            osc.connect(env);
            env.connect(ctx.destination);

            // Frequency sweep for "wrong" sound
            osc.frequency.setValueAtTime(400, now);
            osc.frequency.setValueAtTime(250, now + 0.15);
            osc.frequency.setValueAtTime(400, now + 0.3);

            // Volume envelope
            env.gain.setValueAtTime(0.4, now);
            env.gain.exponentialRampToValueAtTime(0.01, now + 0.35);

            osc.start(now);
            osc.stop(now + 0.35);

            console.log("❌ Wrong sound played");
        } catch (e) {
            console.error("Error playing wrong sound:", e);
        }
    }

    /**
     * Play celebration sound (5 ascending notes)
     */
    playCelebrationSound() {
        try {
            const ctx = this.initAudio();
            const now = ctx.currentTime;
            const notes = [523, 659, 784, 1047, 1319]; // C5, E5, G5, C6, E6

            for (let i = 0; i < notes.length; i++) {
                const osc = ctx.createOscillator();
                const env = ctx.createGain();

                osc.connect(env);
                env.connect(ctx.destination);

                osc.frequency.value = notes[i];
                env.gain.setValueAtTime(0.3, now + (i * 0.15));
                env.gain.exponentialRampToValueAtTime(0.01, now + (i * 0.15) + 0.12);

                osc.start(now + (i * 0.15));
                osc.stop(now + (i * 0.15) + 0.12);
            }

            console.log("🎉 Celebration sound played");
        } catch (e) {
            console.error("Error playing celebration sound:", e);
        }
    }
}

// Create global instance
const audioGenerator = new AudioGenerator();
