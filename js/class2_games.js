/**
 * ====================================================
 * CLASS 2 INTERACTIVE GAME ENGINES (js/class2_games.js)
 * Tactile, Direct-Manipulation Mini-Games for Ages 6-8
 * High Variety, Procedural Generators & Replayability
 * ====================================================
 */

(function (root) {
  // Web Audio Synthesizer for Class 2 Games
  const AudioEngine = {
    ctx: null,
    getCtx() {
      if (!this.ctx) {
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        if (AudioCtx) this.ctx = new AudioCtx();
      }
      if (this.ctx && this.ctx.state === 'suspended') {
        this.ctx.resume();
      }
      return this.ctx;
    },
    pop() {
      try {
        const ctx = this.getCtx();
        if (!ctx) return;
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(600, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(1400, ctx.currentTime + 0.08);
        gain.gain.setValueAtTime(0.25, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.1);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + 0.11);
      } catch (e) { }
    },
    hop() {
      try {
        const ctx = this.getCtx();
        if (!ctx) return;
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(260, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(540, ctx.currentTime + 0.15);
        gain.gain.setValueAtTime(0.2, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.18);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + 0.19);
      } catch (e) { }
    },
    pour() {
      try {
        const ctx = this.getCtx();
        if (!ctx) return;
        const bufferSize = Math.floor(ctx.sampleRate * 0.22);
        const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
        const data = buffer.getChannelData(0);
        for (let i = 0; i < bufferSize; i++) {
          data[i] = Math.random() * 2 - 1;
        }
        const noise = ctx.createBufferSource();
        noise.buffer = buffer;
        const filter = ctx.createBiquadFilter();
        filter.type = 'bandpass';
        filter.frequency.setValueAtTime(800, ctx.currentTime);
        filter.frequency.linearRampToValueAtTime(1400, ctx.currentTime + 0.2);
        filter.Q.value = 3.5;
        const gain = ctx.createGain();
        gain.gain.setValueAtTime(0.22, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.22);
        noise.connect(filter);
        filter.connect(gain);
        gain.connect(ctx.destination);
        noise.start();
        noise.stop(ctx.currentTime + 0.23);
      } catch (e) { }
    },
    coinClink() {
      try {
        const ctx = this.getCtx();
        if (!ctx) return;
        [1500, 2200].forEach((freq, idx) => {
          const osc = ctx.createOscillator();
          const gain = ctx.createGain();
          osc.type = 'sine';
          osc.frequency.setValueAtTime(freq, ctx.currentTime + idx * 0.04);
          gain.gain.setValueAtTime(0.18, ctx.currentTime + idx * 0.04);
          gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + idx * 0.04 + 0.15);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start(ctx.currentTime + idx * 0.04);
          osc.stop(ctx.currentTime + idx * 0.04 + 0.16);
        });
      } catch (e) { }
    },
    tilt() {
      try {
        const ctx = this.getCtx();
        if (!ctx) return;
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(320, ctx.currentTime);
        osc.frequency.linearRampToValueAtTime(240, ctx.currentTime + 0.14);
        gain.gain.setValueAtTime(0.12, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.15);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + 0.16);
      } catch (e) { }
    },
    success() {
      try {
        const ctx = this.getCtx();
        if (!ctx) return;
        const notes = [523.25, 659.25, 783.99, 1046.5];
        notes.forEach((freq, idx) => {
          const osc = ctx.createOscillator();
          const gain = ctx.createGain();
          osc.type = 'sine';
          osc.frequency.setValueAtTime(freq, ctx.currentTime + idx * 0.1);
          gain.gain.setValueAtTime(0.2, ctx.currentTime + idx * 0.1);
          gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + idx * 0.1 + 0.3);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start(ctx.currentTime + idx * 0.1);
          osc.stop(ctx.currentTime + idx * 0.1 + 0.32);
        });
      } catch (e) { }
    },
    wrong() {
      try {
        const ctx = this.getCtx();
        if (!ctx) return;
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(180, ctx.currentTime);
        osc.frequency.linearRampToValueAtTime(130, ctx.currentTime + 0.2);
        gain.gain.setValueAtTime(0.15, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.22);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + 0.23);
      } catch (e) { }
    }
  };

  // Speech Narration for Class 2 kids
  const SpeechEngine = {
    speak(text) {
      if (!('speechSynthesis' in window)) return;
      window.speechSynthesis.cancel();
      const u = new SpeechSynthesisUtterance(text);
      u.rate = 0.92;
      u.pitch = 1.1;
      const voices = window.speechSynthesis.getVoices();
      const enVoice = voices.find(v => v.lang.startsWith('en-IN')) || voices.find(v => v.lang.startsWith('en'));
      if (enVoice) u.voice = enVoice;
      window.speechSynthesis.speak(u);
    }
  };

  // Helper shuffle
  function pickRandom(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
  }
  function pickMultiple(arr, count) {
    const copy = arr.slice();
    for (let i = copy.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [copy[i], copy[j]] = [copy[j], copy[i]];
    }
    return copy.slice(0, count);
  }

  /* ====================================================
     DYNAMIC PROCEDURAL GENERATORS (MANY POSSIBILITIES)
     Every time a game is launched or replayed, fresh rounds
     with different numbers, items, and targets are generated.
     ==================================================== */
  const Class2Generators = {
    // 1. II-MAT-02: Number Line Hopper (Randomized targets, hops & shapes every play/replay)
    "II-MAT-02": function () {
      const shapePrizes = [
        { icon: "⭐", shape: "star", name: "Golden Star", color: "#f59e0b" },
        { icon: "💎", shape: "gem", name: "Sparkle Gem", color: "#06b6d4" },
        { icon: "🌸", shape: "flower", name: "Water Lily", color: "#ec4899" },
        { icon: "👑", shape: "crown", name: "Royal Crown", color: "#eab308" },
        { icon: "🦋", shape: "butterfly", name: "Blue Butterfly", color: "#3b82f6" },
        { icon: "🐞", shape: "ladybug", name: "Lucky Ladybug", color: "#ef4444" },
        { icon: "🪰", shape: "fly", name: "Dragonfly", color: "#10b981" },
        { icon: "🏆", shape: "trophy", name: "Gold Trophy", color: "#f59e0b" },
        { icon: "🍬", shape: "candy", name: "Sweet Candy", color: "#a855f7" },
        { icon: "🍎", shape: "apple", name: "Red Apple", color: "#f43f5e" }
      ];
      const shuffledPrizes = pickMultiple(shapePrizes, 3);

      // Round 1: Target between 6 and 14 (step 2 or 3)
      const target1 = pickRandom([6, 8, 10, 12, 14]);
      // Round 2: Target between 15 and 25 (step 5 or 4)
      const target2 = pickRandom([15, 18, 20, 21, 24, 25]);
      // Round 3: Offset start (e.g. start at 2, 3 or 4) and target up to 28
      const start3 = pickRandom([2, 3, 4]);
      const target3 = start3 + pickRandom([8, 10, 12, 14, 16]);

      return {
        engine: "number-line-hopper",
        title: "Froggy Number Line Hopper",
        icon: "🐸",
        instruction: "Help Freddie Frog hop along the lilypads to catch the prize shape!",
        speechPrompt: "Choose the jumps to help Freddie Frog land directly on the prize shape!",
        rounds: [
          {
            start: 0,
            target: target1,
            step: 2,
            allowedHops: [1, 2, 5],
            itemAtTarget: shuffledPrizes[0],
            hint: `Try jumps of 2 to hit ${target1}!`
          },
          {
            start: 0,
            target: target2,
            step: 5,
            allowedHops: [2, 5],
            itemAtTarget: shuffledPrizes[1],
            hint: `Big jumps of 5 will get you to ${target2} quickly!`
          },
          {
            start: start3,
            target: target3,
            step: 2,
            allowedHops: [1, 2, 4],
            itemAtTarget: shuffledPrizes[2],
            hint: `Start at ${start3} and hop forward to reach ${target3}!`
          }
        ]
      };
    },

    // 2. II-MAT-06: Fill the Jug Challenge (NEW DEDICATED CAPACITY ENGINE!)
    "II-MAT-06": function () {
      const configs = [
        {
          targetMl: pickRandom([500, 600]),
          targetName: "🥣 500ml Bowl",
          availableCups: [
            { ml: 100, label: "100ml Glass", icon: "🥛" },
            { ml: 250, label: "250ml Cup", icon: "🥤" }
          ]
        },
        {
          targetMl: 1000,
          targetName: "🫗 1000ml (1 Litre) Jug",
          availableCups: [
            { ml: 250, label: "250ml Glass", icon: "🥤" },
            { ml: 500, label: "500ml Bottle", icon: "🫖" }
          ]
        },
        {
          targetMl: pickRandom([750, 800]),
          targetName: "🍶 Measuring Flask",
          availableCups: [
            { ml: 250, label: "250ml Glass", icon: "🥤" },
            { ml: 100, label: "100ml Glass", icon: "🥛" }
          ]
        }
      ];

      return {
        engine: "liquid-pour",
        title: "Fill the Jug Challenge",
        icon: "🫗",
        instruction: "Fill the measuring jug to the exact target capacity by pouring water glasses!",
        speechPrompt: "Pour the glasses of water into the jug until you reach the target line!",
        rounds: configs
      };
    },

    // 3. II-MAT-07: Heavy or Light Balance (DEDICATED PAN BALANCE WEIGHING SCALE!)
    "II-MAT-07": function () {
      const items = [
        { name: "🍉 Watermelon", weight: pickRandom([300, 400, 500]) },
        { name: "🎃 Pumpkin", weight: pickRandom([500, 600, 750]) },
        { name: "🍍 Pineapple", weight: pickRandom([200, 250, 300]) },
        { name: "📚 Books Stack", weight: pickRandom([150, 200, 250]) },
        { name: "🧱 Toy Brick", weight: pickRandom([400, 500, 600]) },
        { name: "🥥 Coconut", weight: pickRandom([250, 300, 350]) }
      ];
      const selected = pickMultiple(items, 3);

      return {
        engine: "pan-balance",
        title: "Heavy or Light Balance Scale",
        icon: "⚖️",
        instruction: "Balance the pans by placing weights until both sides are perfectly level!",
        speechPrompt: "Add the matching weights to make the scale level and balanced.",
        rounds: selected.map(it => ({
          leftItem: it.name,
          targetWeight: it.weight,
          unit: "g",
          availableWeights: [100, 100, 100, 50, 50, 20],
          hint: `Combine weights to reach exactly ${it.weight}g!`
        }))
      };
    },

    // 4. II-MAT-05: Shopkeeper Change Maker (Toy Cash Counter)
    "II-MAT-05": function () {
      const toys = [
        { name: "🧸 Teddy Bear", price: pickRandom([11, 12, 13, 14]) },
        { name: "🚀 Space Rocket", price: pickRandom([16, 17, 18, 19]) },
        { name: "🎨 Color Palette", price: pickRandom([21, 23, 25]) },
        { name: "🏎️ Race Car", price: pickRandom([14, 15, 17]) },
        { name: "🎮 Arcade Game", price: pickRandom([22, 24, 26]) },
        { name: "⚽ Match Football", price: pickRandom([15, 18, 20]) },
        { name: "🚁 Toy Helicopter", price: pickRandom([19, 21, 23]) },
        { name: "🦖 Dino Model", price: pickRandom([12, 16, 18]) }
      ];
      const chosenToys = pickMultiple(toys, 3);

      return {
        engine: "coin-shop",
        title: "Toy Shop Cash Counter",
        icon: "🪙",
        instruction: "Pay for the toy by dragging the exact rupee coins to the counter!",
        speechPrompt: "Check the price tag and count the coins onto the counter.",
        rounds: chosenToys.map(toy => ({
          item: toy.name,
          price: toy.price,
          availableCoins: [20, 10, 10, 5, 5, 2, 2, 1, 1],
          hint: `Count coins to make ₹${toy.price}!`
        }))
      };
    },

    // 5. II-MAT-01: Fair Share Distribution
    "II-MAT-01": function () {
      const treatList = [
        { icon: "🍪", name: "Cookies" },
        { icon: "🍓", name: "Strawberries" },
        { icon: "🧁", name: "Cupcakes" },
        { icon: "🍩", name: "Donuts" },
        { icon: "🍎", name: "Apples" },
        { icon: "🥕", name: "Carrots" }
      ];
      const friendsPool = [
        { id: "bunny", name: "Bunny", avatar: "🐰" },
        { id: "bear", name: "Bear", avatar: "🐻" },
        { id: "fox", name: "Fox", avatar: "🦊" },
        { id: "panda", name: "Panda", avatar: "🐼" }
      ];

      const r1Treat = pickRandom(treatList);
      const r1Total = pickRandom([6, 8, 10]);

      const r2Treat = pickRandom(treatList);
      const r2Total = pickRandom([6, 9, 12]);

      const r3Treat = pickRandom(treatList);
      const r3Total = pickRandom([8, 12, 16]);

      return {
        engine: "fair-share",
        title: "Fair Share Treat Party",
        icon: "🍪",
        instruction: "Share the delicious treats equally among all animal friends!",
        speechPrompt: "Share the treats equally so every friend gets the exact same amount!",
        rounds: [
          {
            treatIcon: r1Treat.icon,
            treatName: r1Treat.name,
            totalTreats: r1Total,
            friends: friendsPool.slice(0, 2),
            hint: `${r1Total} treats shared by 2 friends = ${r1Total / 2} each!`
          },
          {
            treatIcon: r2Treat.icon,
            treatName: r2Treat.name,
            totalTreats: r2Total,
            friends: friendsPool.slice(0, 3),
            hint: `${r2Total} treats shared by 3 friends = ${r2Total / 3} each!`
          },
          {
            treatIcon: r3Treat.icon,
            treatName: r3Treat.name,
            totalTreats: r3Total,
            friends: friendsPool.slice(0, 4),
            hint: `${r3Total} treats shared by 4 friends = ${r3Total / 4} each!`
          }
        ]
      };
    },

    // 6. II-MAT-08: Clock Reader Challenge (Dedicated Clock Face Engine)
    "II-MAT-08": function () {
      const h1 = pickRandom([2, 3, 4, 5]);
      const h2 = pickRandom([6, 7, 8, 9]);
      const h3 = pickRandom([10, 11, 12, 1]);

      return {
        engine: "clock-reader",
        title: "Clock Reading Master",
        icon: "⏰",
        instruction: "Read the clock time and show where the minute hand points!",
        speechPrompt: "Listen to the time and tap the correct minute position on the clock!",
        rounds: [
          {
            targetHour: h1,
            targetMinute: 15,
            prompt: `Set the minute hand for ${h1}:15 (Quarter Past ${h1})! 🕒`
          },
          {
            targetHour: h2,
            targetMinute: 30,
            prompt: `Set the minute hand for ${h2}:30 (Half Past ${h2})! 🕕`
          },
          {
            targetHour: h3,
            targetMinute: pickRandom([0, 45]),
            prompt: `Set the minute hand for ${h3}:00 or Quarter To! 🕘`
          }
        ]
      };
    },

    // 7. II-MAT-04: Shape Sides Sorter
    "II-MAT-04": function () {
      const all3Sided = [
        { text: "Pyramid", icon: "🔺", bucket: "3sides" },
        { text: "Pizza Slice", icon: "🍕", bucket: "3sides" },
        { text: "Traffic Cone", icon: "⚠️", bucket: "3sides" },
        { text: "Mountain Peak", icon: "🏔️", bucket: "3sides" },
        { text: "Yacht Sail", icon: "⛵", bucket: "3sides" },
        { text: "Tortilla Chip", icon: "🧀", bucket: "3sides" }
      ];
      const all4Sided = [
        { text: "Square Box", icon: "🟩", bucket: "4sides" },
        { text: "Door", icon: "🚪", bucket: "4sides" },
        { text: "Book Cover", icon: "📘", bucket: "4sides" },
        { text: "Window", icon: "🪟", bucket: "4sides" },
        { text: "Chess Board", icon: "🏁", bucket: "4sides" },
        { text: "Photo Frame", icon: "🖼️", bucket: "4sides" }
      ];

      return {
        engine: "bucket-sorter",
        title: "Shape Sides Sorter",
        icon: "🔺",
        instruction: "Sort the shapes into 3-Sided Triangles and 4-Sided Shapes!",
        speechPrompt: "Count the sides! Put 3-sided shapes in green, and 4-sided shapes in purple.",
        buckets: [
          { id: "3sides", label: "🔺 3 Sides (Triangles)", color: "#10b981", border: "#059669" },
          { id: "4sides", label: "🟦 4 Sides (Quadrilaterals)", color: "#8b5cf6", border: "#7c3aed" }
        ],
        items: pickMultiple(all3Sided, 3).concat(pickMultiple(all4Sided, 3)).sort(() => Math.random() - 0.5)
      };
    },

    // 8. II-ENG-08: Verb Action Sort
    "II-ENG-08": function () {
      const verbs = [
        { text: "Jump", icon: "🦘", bucket: "verb" },
        { text: "Dance", icon: "💃", bucket: "verb" },
        { text: "Run", icon: "🏃", bucket: "verb" },
        { text: "Swim", icon: "🏊", bucket: "verb" },
        { text: "Sing", icon: "🎤", bucket: "verb" },
        { text: "Clap", icon: "👏", bucket: "verb" },
        { text: "Sleep", icon: "😴", bucket: "verb" },
        { text: "Climb", icon: "🧗", bucket: "verb" }
      ];
      const nouns = [
        { text: "Apple", icon: "🍎", bucket: "noun" },
        { text: "School", icon: "🏫", bucket: "noun" },
        { text: "Tiger", icon: "🐅", bucket: "noun" },
        { text: "Pencil", icon: "✏️", bucket: "noun" },
        { text: "Doctor", icon: "👩‍⚕️", bucket: "noun" },
        { text: "River", icon: "🌊", bucket: "noun" },
        { text: "Sun", icon: "☀️", bucket: "noun" },
        { text: "Ball", icon: "⚽", bucket: "noun" }
      ];

      return {
        engine: "bucket-sorter",
        title: "Action Words vs Naming Words",
        icon: "🏃",
        instruction: "Sort words into Action Words (Verbs) and Naming Words (Nouns)!",
        speechPrompt: "Is it an action verb, or a naming noun? Sort each card.",
        buckets: [
          { id: "noun", label: "🧸 Naming Words (Nouns)", color: "#3b82f6", border: "#2563eb" },
          { id: "verb", label: "🏃 Action Words (Verbs)", color: "#ec4899", border: "#db2777" }
        ],
        items: pickMultiple(verbs, 4).concat(pickMultiple(nouns, 4)).sort(() => Math.random() - 0.5)
      };
    },

    // 9. II-ENG-07: Sentence Scramble (Word Train)
    "II-ENG-07": function () {
      const sentenceBank = [
        ["The", "cat", "drinks", "milk."],
        ["Birds", "sing", "in", "the", "morning."],
        ["I", "love", "playing", "with", "friends."],
        ["The", "frog", "jumps", "in", "pond."],
        ["We", "read", "books", "at", "school."],
        ["A", "rabbit", "hops", "very", "fast."],
        ["The", "sun", "shines", "so", "bright."],
        ["Fish", "swim", "in", "blue", "water."]
      ];
      const selected = pickMultiple(sentenceBank, 3);

      return {
        engine: "word-train",
        title: "Sentence Train Express",
        icon: "🚂",
        instruction: "Assemble the words in the train cars to form a complete sentence!",
        speechPrompt: "Put the words in order to make a good sentence for the train.",
        rounds: selected.map(words => ({
          words: words.slice(),
          correctOrder: words.slice(),
          hint: `Start with '${words[0]}' and end with '${words[words.length - 1]}'`
        }))
      };
    },

    // 10. II-ENG-01: Sound Detective Bubble Pop
    "II-ENG-01": function () {
      const families = [
        {
          prompt: "Pop the words that rhyme with 'CAT'!",
          bubbles: [
            { text: "BAT 🦇", correct: true },
            { text: "DOG 🐶", correct: false },
            { text: "HAT 🎩", correct: true },
            { text: "SUN ☀️", correct: false },
            { text: "MAT 🧘", correct: true },
            { text: "PEN 🖊️", correct: false }
          ]
        },
        {
          prompt: "Pop words starting with the /sh/ sound!",
          bubbles: [
            { text: "SHIP 🚢", correct: true },
            { text: "FISH 🐟", correct: false },
            { text: "SHOE 👟", correct: true },
            { text: "BELL 🔔", correct: false },
            { text: "SHARK 🦈", correct: true },
            { text: "STAR ⭐", correct: false }
          ]
        },
        {
          prompt: "Pop the words that rhyme with 'DOG'!",
          bubbles: [
            { text: "FOG 🌫️", correct: true },
            { text: "CAT 🐱", correct: false },
            { text: "LOG 🪵", correct: true },
            { text: "FROG 🐸", correct: true },
            { text: "CUP 🥤", correct: false },
            { text: "HAT 🎩", correct: false }
          ]
        }
      ];

      return {
        engine: "bubble-pop",
        title: "Sound Detective Bubble Pop",
        icon: "🫧",
        instruction: "Listen carefully and pop the bubbles that match the requested sound!",
        speechPrompt: "Pop the bubbles that match the sound you are looking for!",
        rounds: pickMultiple(families, 2)
      };
    }
  };

  /* ====================================================
     ENGINE DISPATCHER & CORE RUNNER
     ==================================================== */
  const Class2Games = {
    isClass2Interactive(game) {
      if (!game) return false;
      if (game.interactiveConfig) return true;
      if (String(game.id || '').startsWith('II-')) {
        return !!(Class2Generators[game.id]);
      }
      const cls = String(game.class || '').toUpperCase().replace(/^CLASS\s+/, '').trim();
      if (cls === 'II' || cls === '2') {
        return !!(Class2Generators[game.id]);
      }
      return false;
    },

    refreshInteractiveConfig(config) {
      if (!config) return null;
      try {
        const cloned = JSON.parse(JSON.stringify(config));
        if (cloned.engine === 'number-line-hopper') {
          const shapePrizes = [
            { icon: "⭐", shape: "star", name: "Star", color: "#f59e0b" },
            { icon: "💎", shape: "gem", name: "Gem", color: "#06b6d4" },
            { icon: "🌸", shape: "flower", name: "Lotus", color: "#ec4899" },
            { icon: "👑", shape: "crown", name: "Crown", color: "#eab308" },
            { icon: "🦋", shape: "butterfly", name: "Butterfly", color: "#3b82f6" },
            { icon: "🐞", shape: "ladybug", name: "Ladybug", color: "#ef4444" },
            { icon: "🪰", shape: "fly", name: "Dragonfly", color: "#10b981" }
          ];
          const sh = pickMultiple(shapePrizes, 3);
          const t1 = pickRandom([6, 8, 10, 12, 14]);
          const t2 = pickRandom([15, 18, 20, 24, 25]);
          cloned.rounds = [
            { start: 0, target: t1, step: 2, allowedHops: [1, 2, 5], itemAtTarget: sh[0], hint: `Hop by 2s to reach ${t1}!` },
            { start: 0, target: t2, step: 5, allowedHops: [2, 5], itemAtTarget: sh[1], hint: `Hop by 5s to reach ${t2}!` }
          ];
        } else if (cloned.engine === 'liquid-pour') {
          const v1 = pickRandom([400, 500, 600]);
          const v2 = pickRandom([750, 800, 1000]);
          cloned.rounds = [
            { targetMl: v1, targetName: `🥣 ${v1}ml Bowl`, availableCups: [{ ml: 100, label: "100ml Glass", icon: "🥛" }, { ml: 250, label: "250ml Cup", icon: "🥤" }] },
            { targetMl: v2, targetName: `🫗 ${v2}ml Jug`, availableCups: [{ ml: 250, label: "250ml Glass", icon: "🥤" }, { ml: 500, label: "500ml Bottle", icon: "🫖" }] }
          ];
        } else if (cloned.engine === 'pan-balance') {
          const items = [
            { name: "🍉 Watermelon", weight: pickRandom([300, 400, 500]) },
            { name: "🎃 Pumpkin", weight: pickRandom([500, 600, 750]) },
            { name: "🍍 Pineapple", weight: pickRandom([200, 250, 300]) },
            { name: "🥥 Coconut", weight: pickRandom([250, 350]) }
          ];
          const chosen = pickMultiple(items, 2);
          cloned.rounds = chosen.map(it => ({
            leftItem: it.name,
            targetWeight: it.weight,
            unit: "g",
            availableWeights: [100, 100, 100, 50, 50, 20],
            hint: `Reach ${it.weight}g!`
          }));
        } else if (cloned.engine === 'clock-reader') {
          const h1 = pickRandom([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]);
          const h2 = pickRandom([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]);
          cloned.rounds = [
            { targetHour: h1, targetMinute: 0, prompt: `Set the clock for ${h1}:00 (${h1} o'Clock)! ⏰`, speechText: `Set the clock to ${h1} o'clock!` },
            { targetHour: h2, targetMinute: 30, prompt: `Set the minute hand for ${h2}:30 (Half Past ${h2})! 🕧`, speechText: `Set the clock to half past ${h2}!` }
          ];
        }
        return cloned;
      } catch (e) {
        return config;
      }
    },

    getConfig(game) {
      // 1. Procedural generator for curriculum games: ALWAYS generates fresh rounds on every play/replay!
      if (Class2Generators[game.id]) {
        return Class2Generators[game.id]();
      }
      // 2. AI-generated games: refresh and randomize numbers/tasks on replay
      if (game.interactiveConfig) {
        return this.refreshInteractiveConfig(game.interactiveConfig);
      }
      return null;
    },

    render(container, game, onComplete) {
      const config = this.getConfig(game);
      if (!config) {
        container.innerHTML = `<div style="padding:20px;text-align:center;">Interactive game configuration coming soon.</div>`;
        return;
      }

      container.innerHTML = '';
      const stage = document.createElement('div');
      stage.className = 'c2-game-stage';

      // Header Banner
      const banner = document.createElement('div');
      banner.className = 'c2-instruction-banner';
      banner.innerHTML = `
        <div class="c2-instruction-text">
          <span class="c2-instruction-badge">${config.icon || '🎮'}</span>
          <span id="c2InstructionText">${config.instruction}</span>
        </div>
        <button type="button" class="c2-btn-speak" id="c2BtnSpeak">
          <span>🔊</span> Read Aloud
        </button>
      `;
      stage.appendChild(banner);

      // Play Area
      const boardCanvas = document.createElement('div');
      boardCanvas.className = 'c2-board-canvas';
      stage.appendChild(boardCanvas);

      // Footer Bar
      const footer = document.createElement('div');
      footer.className = 'c2-game-footer';
      footer.innerHTML = `
        <span class="c2-progress-pill" id="c2ProgressPill">Round 1 of 3</span>
        <button type="button" class="c2-btn-done" id="c2BtnNext" disabled>Next Round →</button>
      `;
      stage.appendChild(footer);
      container.appendChild(stage);

      // Wire Narration Button
      const speakBtn = banner.querySelector('#c2BtnSpeak');
      const speakPrompt = () => SpeechEngine.speak(config.speechPrompt || config.instruction);
      if (speakBtn) speakBtn.onclick = speakPrompt;
      setTimeout(speakPrompt, 400);

      // Dispatch to specific mini-engine
      switch (config.engine) {
        case 'number-line-hopper':
          this.runNumberLineHopper(boardCanvas, config, footer, onComplete);
          break;
        case 'liquid-pour':
          this.runLiquidJugFiller(boardCanvas, config, footer, onComplete);
          break;
        case 'clock-reader':
          this.runClockChallenge(boardCanvas, config, footer, onComplete);
          break;
        case 'fair-share':
          this.runFairShare(boardCanvas, config, footer, onComplete);
          break;
        case 'coin-shop':
          this.runCoinShop(boardCanvas, config, footer, onComplete);
          break;
        case 'pan-balance':
          this.runPanBalance(boardCanvas, config, footer, onComplete);
          break;
        case 'bucket-sorter':
          this.runBucketSorter(boardCanvas, config, footer, onComplete);
          break;
        case 'word-train':
          this.runWordTrain(boardCanvas, config, footer, onComplete);
          break;
        case 'bubble-pop':
          this.runBubblePop(boardCanvas, config, footer, onComplete);
          break;
        default:
          boardCanvas.innerHTML = `<p>Unknown engine: ${config.engine}</p>`;
      }
    },

    /* ----------------------------------------------------
       1. FROGGY NUMBER LINE HOPPER (FIXED ACCURACY & SHAPE PRIZE)
       ---------------------------------------------------- */
    runNumberLineHopper(canvas, config, footer, onComplete) {
      const rounds = config.rounds;
      let roundIdx = 0;
      let score = 0;

      function renderRound() {
        const R = rounds[roundIdx];
        let currentPos = R.start;
        const targetPos = R.target;
        const hopHistory = [currentPos];

        const progressPill = footer ? footer.querySelector('#c2ProgressPill') : null;
        const nextBtn = footer ? footer.querySelector('#c2BtnNext') : null;
        if (progressPill) progressPill.textContent = `Round ${roundIdx + 1} of ${rounds.length} ⭐`;
        if (nextBtn) {
          nextBtn.disabled = true;
          nextBtn.textContent = roundIdx + 1 < rounds.length ? 'Next Hop →' : 'Finish Challenge! 🏆';
        }

        // Parse prize icon safely - extract shape/icon, never render sprawling text onto lilypad!
        let prizeIcon = '⭐';
        let prizeName = 'Golden Star';
        if (typeof R.itemAtTarget === 'object' && R.itemAtTarget !== null) {
          prizeIcon = R.itemAtTarget.icon || '⭐';
          prizeName = R.itemAtTarget.name || 'Prize Shape';
        } else if (typeof R.itemAtTarget === 'string') {
          const match = R.itemAtTarget.match(/[\p{Emoji_Presentation}\p{Extended_Pictographic}]/u);
          if (match) {
            prizeIcon = match[0];
          }
          prizeName = R.itemAtTarget.replace(/[\p{Emoji_Presentation}\p{Extended_Pictographic}]/u, '').trim() || 'Prize Shape';
        }

        canvas.innerHTML = `
          <div class="c2-pond-container">
            <div class="c2-pond-water-ripples"></div>
            <div class="c2-numberline-track" id="c2Track">
              <div class="c2-numberline-wire"></div>
            </div>
          </div>
          <div class="c2-hopper-controls" id="c2HopControls"></div>
          <div class="c2-hopper-log" id="c2HopLog">
            <span>Path:</span> <b id="c2HopPath">${currentPos}</b>
          </div>
        `;

        const track = canvas.querySelector('#c2Track');
        const maxVal = Math.max(targetPos + 3, 16);
        const nodeEls = {};

        for (let i = 0; i <= maxVal; i++) {
          const node = document.createElement('div');
          node.className = `c2-lilypad-node ${i === targetPos ? 'active-target' : ''}`;
          node.dataset.val = i;

          node.innerHTML = `
            ${i === targetPos ? `
              <div class="c2-target-prize" id="c2TargetPrize">
                <div class="c2-prize-shape-badge" title="${prizeName}">
                  <span>${prizeIcon}</span>
                </div>
                <div class="c2-prize-shape-beacon"></div>
              </div>
            ` : ''}
            <div class="c2-lilypad-graphic">
              <span class="c2-lilypad-number">${i}</span>
            </div>
          `;

          node.onclick = () => {
            const diff = i - currentPos;
            if (diff > 0 && R.allowedHops.includes(diff)) {
              doHop(diff);
            }
          };

          track.appendChild(node);
          nodeEls[i] = node;
        }

        // Add Frog
        const frog = document.createElement('div');
        frog.className = 'c2-frog-avatar';
        frog.textContent = '🐸';
        nodeEls[currentPos].appendChild(frog);

        // Control Buttons
        const controls = canvas.querySelector('#c2HopControls');
        R.allowedHops.forEach(hopVal => {
          const btn = document.createElement('button');
          btn.type = 'button';
          btn.className = 'c2-hop-btn c2-hop-btn-primary';
          btn.innerHTML = `<span>Hop +${hopVal}</span> 🦘`;
          btn.onclick = () => doHop(hopVal);
          controls.appendChild(btn);
        });

        const undoBtn = document.createElement('button');
        undoBtn.type = 'button';
        undoBtn.className = 'c2-hop-btn c2-hop-btn-undo';
        undoBtn.innerHTML = `<span>↩ Undo</span>`;
        undoBtn.onclick = () => {
          if (hopHistory.length > 1) {
            AudioEngine.pop();
            hopHistory.pop();
            currentPos = hopHistory[hopHistory.length - 1];
            updateFrogPos();
          }
        };
        controls.appendChild(undoBtn);

        function updateFrogPos() {
          canvas.querySelectorAll('.c2-lilypad-node').forEach(n => n.classList.remove('visited'));
          hopHistory.forEach(val => {
            if (nodeEls[val]) nodeEls[val].classList.add('visited');
          });

          frog.classList.remove('jumping');
          void frog.offsetWidth; // reflow
          frog.classList.add('jumping');
          if (nodeEls[currentPos]) {
            nodeEls[currentPos].appendChild(frog);
            nodeEls[currentPos].scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
          }

          canvas.querySelector('#c2HopPath').textContent = hopHistory.join(' ➔ ');

          if (currentPos === targetPos) {
            AudioEngine.success();
            score++;
            nextBtn.disabled = false;
            const targetPrizeEl = canvas.querySelector('#c2TargetPrize');
            if (targetPrizeEl) {
              targetPrizeEl.style.transform = 'translateX(-50%) scale(1.35)';
              targetPrizeEl.style.filter = 'drop-shadow(0 0 12px #fbbf24)';
            }
            SpeechEngine.speak(`Hooray! You reached ${targetPos} and caught the ${prizeName}!`);
            controls.querySelectorAll('button').forEach(b => { if (b !== undoBtn) b.disabled = true; });
          } else if (currentPos > targetPos) {
            AudioEngine.wrong();
            SpeechEngine.speak(`Oops, you hopped past ${targetPos}! Tap undo to try again.`);
          }
        }

        function doHop(step) {
          AudioEngine.hop();
          currentPos += step;
          hopHistory.push(currentPos);
          updateFrogPos();
        }

        nextBtn.onclick = () => {
          roundIdx++;
          if (roundIdx < rounds.length) {
            renderRound();
          } else {
            onComplete({ score, total: rounds.length });
          }
        };
      }

      renderRound();
    },

    /* ----------------------------------------------------
       2. LIQUID JUG FILLER (CAPACITY & VOLUME)
       ---------------------------------------------------- */
    runLiquidJugFiller(canvas, config, footer, onComplete) {
      const rounds = config.rounds;
      let roundIdx = 0;
      let score = 0;

      function renderRound() {
        const R = rounds[roundIdx];
        let currentMl = 0;
        const targetMl = R.targetMl;

        const progressPill = footer ? footer.querySelector('#c2ProgressPill') : null;
        const nextBtn = footer ? footer.querySelector('#c2BtnNext') : null;
        if (progressPill) progressPill.textContent = `Round ${roundIdx + 1} of ${rounds.length} ⭐`;
        if (nextBtn) {
          nextBtn.disabled = true;
          nextBtn.textContent = roundIdx + 1 < rounds.length ? 'Next Jug →' : 'Finish Challenge! 🏆';
        }

        canvas.innerHTML = `
          <div class="c2-jug-station">
            <div class="c2-jug-gauge-banner">
              <span>Target: <b>${R.targetName}</b></span>
              <span style="font-size:18px; font-weight:800; color:#0284c7;">Current: <span id="c2CurrentVolume">0</span> / ${targetMl} ml</span>
            </div>

            <div class="c2-jug-stage-bench">
              <div class="c2-measuring-jug-wrap">
                <div class="c2-jug-liquid-fill" id="c2LiquidFill" style="height: 0%;">
                  <div class="c2-liquid-surface-wave"></div>
                </div>
                <div class="c2-jug-tick-marks" id="c2JugTicks"></div>
              </div>
            </div>

            <div style="font-size:13.5px; font-weight:700; color:#475569;">Tap a cup to pour into the jug:</div>
            <div class="c2-cups-dock" id="c2CupsDock"></div>
            <button type="button" class="c2-btn-empty-jug" id="c2BtnEmptyJug">🔄 Empty Jug & Retry</button>
          </div>
        `;

        // Render tick marks
        const ticksContainer = canvas.querySelector('#c2JugTicks');
        [0.25, 0.5, 0.75, 1.0].forEach(pct => {
          const val = Math.round(targetMl * pct);
          const tick = document.createElement('div');
          tick.className = 'c2-jug-tick';
          tick.textContent = `${val}ml`;
          ticksContainer.appendChild(tick);
        });

        const dock = canvas.querySelector('#c2CupsDock');
        R.availableCups.forEach(cup => {
          const btn = document.createElement('button');
          btn.type = 'button';
          btn.className = 'c2-pour-cup-btn';
          btn.innerHTML = `
            <span class="c2-pour-cup-icon">${cup.icon || '🥤'}</span>
            <span class="c2-pour-cup-label">+${cup.ml} ml</span>
          `;
          btn.onclick = () => doPour(cup.ml);
          dock.appendChild(btn);
        });

        const emptyBtn = canvas.querySelector('#c2BtnEmptyJug');
        emptyBtn.onclick = () => {
          AudioEngine.pop();
          currentMl = 0;
          updateJugUI();
        };

        function doPour(ml) {
          AudioEngine.pour();
          currentMl += ml;
          updateJugUI();
        }

        function updateJugUI() {
          const fillEl = canvas.querySelector('#c2LiquidFill');
          const volEl = canvas.querySelector('#c2CurrentVolume');
          volEl.textContent = currentMl;

          const fillPct = Math.min(100, Math.round((currentMl / targetMl) * 100));
          fillEl.style.height = `${fillPct}%`;

          if (currentMl === targetMl) {
            AudioEngine.success();
            score++;
            nextBtn.disabled = false;
            dock.querySelectorAll('button').forEach(b => b.disabled = true);
            emptyBtn.style.display = 'none';
            SpeechEngine.speak(`Splendid! Exactly ${targetMl} millilitres! The jug is filled perfectly!`);
          } else if (currentMl > targetMl) {
            AudioEngine.wrong();
            fillEl.style.background = 'linear-gradient(180deg, #f87171 0%, #dc2626 100%)';
            SpeechEngine.speak(`Oh no, it overflowed! You have ${currentMl} ml. Tap Empty Jug to try again.`);
          } else {
            fillEl.style.background = 'linear-gradient(180deg, #38bdf8 0%, #0284c7 100%)';
          }
        }

        nextBtn.onclick = () => {
          roundIdx++;
          if (roundIdx < rounds.length) {
            renderRound();
          } else {
            onComplete({ score, total: rounds.length });
          }
        };
      }

      renderRound();
    },

    /* ----------------------------------------------------
       3. CLOCK READING MASTER (DEDICATED CLOCK ENGINE)
       ---------------------------------------------------- */
    runClockChallenge(canvas, config, footer, onComplete) {
      const rounds = config.rounds;
      let roundIdx = 0;
      let score = 0;

      function renderRound() {
        const R = rounds[roundIdx];
        const targetHour = R.targetHour;
        const targetMinute = R.targetMinute;

        const progressPill = footer.querySelector('#c2ProgressPill');
        const nextBtn = footer.querySelector('#c2BtnNext');
        progressPill.textContent = `Round ${roundIdx + 1} of ${rounds.length} ⭐`;
        nextBtn.disabled = true;
        nextBtn.textContent = roundIdx + 1 < rounds.length ? 'Next Clock →' : 'Finish Challenge! 🏆';

        canvas.innerHTML = `
          <div class="c2-clock-stage">
            <div style="font-family:var(--font-heading); font-size:18px; font-weight:800; color:#312e81;">
              ${R.prompt}
            </div>

            <div class="c2-clock-face-wrap" id="c2ClockFace">
              <div class="c2-clock-center-pin"></div>
              <div class="c2-clock-hour-hand" id="c2HourHand"></div>
              <div class="c2-clock-minute-hand" id="c2MinuteHand"></div>
            </div>

            <div style="font-size:13.5px; font-weight:700; color:#475569;">Where should the minute hand point?</div>
            <div style="display:flex; gap:10px; flex-wrap:wrap; justify-content:center;" id="c2ClockOptions"></div>
          </div>
        `;

        // Numerals 1 to 12
        const clockFace = canvas.querySelector('#c2ClockFace');
        for (let h = 1; h <= 12; h++) {
          const num = document.createElement('span');
          num.className = 'c2-clock-numeral';
          num.textContent = h;
          const angle = (h * 30 - 90) * (Math.PI / 180);
          const r = 85;
          const x = 110 + r * Math.cos(angle) - 13;
          const y = 110 + r * Math.sin(angle) - 13;
          num.style.left = `${x}px`;
          num.style.top = `${y}px`;
          clockFace.appendChild(num);
        }

        const hourHand = canvas.querySelector('#c2HourHand');
        const minuteHand = canvas.querySelector('#c2MinuteHand');
        const baseHourAngle = (targetHour % 12) * 30;
        hourHand.style.transform = `rotate(${baseHourAngle}deg)`;

        const optionsContainer = canvas.querySelector('#c2ClockOptions');
        const minOptions = [
          { min: 0, label: ":00 (O'clock 🕛)", handAngle: 0 },
          { min: 15, label: ":15 (Quarter Past 🕒)", handAngle: 90 },
          { min: 30, label: ":30 (Half Past 🕕)", handAngle: 180 },
          { min: 45, label: ":45 (Quarter To 🕘)", handAngle: 270 }
        ];

        minOptions.forEach(opt => {
          const btn = document.createElement('button');
          btn.type = 'button';
          btn.className = 'c2-hop-btn c2-hop-btn-primary';
          btn.style.fontSize = '14px';
          btn.textContent = opt.label;
          btn.onclick = () => {
            AudioEngine.hop();
            minuteHand.style.transform = `rotate(${opt.handAngle}deg)`;
            hourHand.style.transform = `rotate(${baseHourAngle + (opt.min / 60) * 30}deg)`;

            if (opt.min === targetMinute) {
              AudioEngine.success();
              score++;
              nextBtn.disabled = false;
              optionsContainer.querySelectorAll('button').forEach(b => b.disabled = true);
              btn.style.background = '#059669';
              SpeechEngine.speak(`That's right! ${targetHour}:${targetMinute < 10 ? '0' + targetMinute : targetMinute}! Excellent clock reading!`);
            } else {
              AudioEngine.wrong();
              SpeechEngine.speak(`That points to ${opt.min} minutes. Try another position.`);
            }
          };
          optionsContainer.appendChild(btn);
        });

        nextBtn.onclick = () => {
          roundIdx++;
          if (roundIdx < rounds.length) {
            renderRound();
          } else {
            onComplete({ score, total: rounds.length });
          }
        };
      }

      renderRound();
    },

    /* ----------------------------------------------------
       4. FAIR SHARE DIVISION
       ---------------------------------------------------- */
    runFairShare(canvas, config, footer, onComplete) {
      const rounds = config.rounds;
      let roundIdx = 0;
      let score = 0;

      function renderRound() {
        const R = rounds[roundIdx];
        const targetPerFriend = R.totalTreats / R.friends.length;
        let pool = Array.from({ length: R.totalTreats }, (_, i) => ({ id: `t_${i}`, icon: R.treatIcon }));
        const plateBuckets = {};
        R.friends.forEach(f => plateBuckets[f.id] = []);

        const progressPill = footer.querySelector('#c2ProgressPill');
        const nextBtn = footer.querySelector('#c2BtnNext');
        progressPill.textContent = `Round ${roundIdx + 1} of ${rounds.length} ⭐`;
        nextBtn.disabled = true;
        nextBtn.textContent = roundIdx + 1 < rounds.length ? 'Next Share →' : 'Finish Challenge! 🏆';

        canvas.innerHTML = `
          <div class="c2-share-wrapper">
            <div class="c2-share-treat-bank">
              <span class="c2-share-treat-label">Treat Basket (${R.treatName}): <b id="c2BankCount">${pool.length}</b> left</span>
              <div class="c2-share-treat-pool" id="c2TreatPool"></div>
            </div>
            <div class="c2-share-plates-row" id="c2PlatesRow"></div>
          </div>
        `;

        const poolEl = canvas.querySelector('#c2TreatPool');
        const platesRow = canvas.querySelector('#c2PlatesRow');
        let selectedTreat = null;

        function renderTreats() {
          poolEl.innerHTML = '';
          canvas.querySelector('#c2BankCount').textContent = pool.length;

          pool.forEach(t => {
            const treat = document.createElement('div');
            treat.className = 'c2-draggable-treat';
            treat.textContent = t.icon;
            treat.dataset.id = t.id;

            treat.onclick = () => {
              AudioEngine.pop();
              if (selectedTreat === t) {
                selectedTreat = null;
                treat.style.transform = '';
              } else {
                canvas.querySelectorAll('.c2-draggable-treat').forEach(el => el.style.transform = '');
                selectedTreat = t;
                treat.style.transform = 'scale(1.3) translateY(-6px)';
              }
            };

            poolEl.appendChild(treat);
          });
        }

        R.friends.forEach(friend => {
          const card = document.createElement('div');
          card.className = 'c2-animal-plate-card';
          card.dataset.friendId = friend.id;

          card.innerHTML = `
            <span class="c2-animal-avatar">${friend.avatar}</span>
            <span class="c2-animal-name">${friend.name}</span>
            <div class="c2-plate-dish" id="dish_${friend.id}"></div>
            <span class="c2-plate-count-badge" id="badge_${friend.id}">0 ${R.treatName}</span>
          `;

          card.onclick = () => {
            if (pool.length > 0) {
              const treatToMove = selectedTreat || pool[0];
              pool = pool.filter(t => t.id !== treatToMove.id);
              plateBuckets[friend.id].push(treatToMove);
              selectedTreat = null;
              AudioEngine.pop();
              updatePlates();
            }
          };

          platesRow.appendChild(card);
        });

        function updatePlates() {
          renderTreats();
          let allEqual = true;
          R.friends.forEach(f => {
            const dish = canvas.querySelector(`#dish_${f.id}`);
            const badge = canvas.querySelector(`#badge_${f.id}`);
            dish.innerHTML = '';
            plateBuckets[f.id].forEach(t => {
              const span = document.createElement('span');
              span.textContent = t.icon;
              span.style.fontSize = '26px';
              dish.appendChild(span);
            });
            const cnt = plateBuckets[f.id].length;
            badge.textContent = `${cnt} ${R.treatName}`;
            if (cnt !== targetPerFriend) allEqual = false;
          });

          if (pool.length === 0 && allEqual) {
            AudioEngine.success();
            score++;
            nextBtn.disabled = false;
            SpeechEngine.speak(`Splendid! Each friend got exactly ${targetPerFriend} ${R.treatName}! Fair share complete!`);
          } else if (pool.length === 0 && !allEqual) {
            AudioEngine.wrong();
            SpeechEngine.speak(`All treats are given, but they are not equal! Tap undo or restart.`);
          }
        }

        renderTreats();

        nextBtn.onclick = () => {
          roundIdx++;
          if (roundIdx < rounds.length) {
            renderRound();
          } else {
            onComplete({ score, total: rounds.length });
          }
        };
      }

      renderRound();
    },

    /* ----------------------------------------------------
       5. COIN SHOPKEEPER (CASH REGISTER)
       ---------------------------------------------------- */
    runCoinShop(canvas, config, footer, onComplete) {
      const rounds = config.rounds;
      let roundIdx = 0;
      let score = 0;

      function renderRound() {
        const R = rounds[roundIdx];
        let placedCoins = [];
        let available = R.availableCoins.slice();

        const progressPill = footer.querySelector('#c2ProgressPill');
        const nextBtn = footer.querySelector('#c2BtnNext');
        progressPill.textContent = `Round ${roundIdx + 1} of ${rounds.length} ⭐`;
        nextBtn.disabled = true;
        nextBtn.textContent = roundIdx + 1 < rounds.length ? 'Next Toy →' : 'Finish Challenge! 🏆';

        canvas.innerHTML = `
          <div class="c2-shop-scene">
            <div class="c2-shop-item-showcase">
              <span class="c2-shop-item-icon">${R.item.split(' ')[0]}</span>
              <div class="c2-shop-price-tag">
                <span style="font-weight:700; color:#334155;">${R.item.split(' ').slice(1).join(' ')}</span>
                <span class="c2-shop-price-amount">₹${R.price}</span>
              </div>
            </div>

            <div class="c2-cash-counter-tray">
              <div style="font-weight:700; color:#475569; margin-bottom:8px;">
                Cash Counter: <b id="c2CounterTotal">₹0</b> / Target: <b>₹${R.price}</b>
              </div>
              <div style="display:flex; gap:8px; flex-wrap:wrap; justify-content:center; min-height:56px;" id="c2PlacedCoinsArea"></div>
            </div>

            <div style="font-size:13px; font-weight:700; color:#64748b; margin-top:6px;">Tap a coin from your wallet to pay:</div>
            <div class="c2-coins-palette" id="c2CoinsPalette"></div>
          </div>
        `;

        const palette = canvas.querySelector('#c2CoinsPalette');
        const counterArea = canvas.querySelector('#c2PlacedCoinsArea');
        const totalEl = canvas.querySelector('#c2CounterTotal');

        function redraw() {
          palette.innerHTML = '';
          available.forEach((val, idx) => {
            const coin = document.createElement('button');
            coin.type = 'button';
            coin.className = `c2-indian-coin coin-${val}`;
            coin.textContent = `₹${val}`;
            coin.onclick = () => {
              AudioEngine.coinClink();
              available.splice(idx, 1);
              placedCoins.push(val);
              redraw();
            };
            palette.appendChild(coin);
          });

          counterArea.innerHTML = '';
          placedCoins.forEach((val, idx) => {
            const coin = document.createElement('button');
            coin.type = 'button';
            coin.className = `c2-indian-coin coin-${val}`;
            coin.textContent = `₹${val}`;
            coin.title = 'Tap to remove';
            coin.onclick = () => {
              AudioEngine.pop();
              placedCoins.splice(idx, 1);
              available.push(val);
              redraw();
            };
            counterArea.appendChild(coin);
          });

          const currentTotal = placedCoins.reduce((s, c) => s + c, 0);
          totalEl.textContent = `₹${currentTotal}`;

          if (currentTotal === R.price) {
            AudioEngine.success();
            score++;
            nextBtn.disabled = false;
            SpeechEngine.speak(`Ka-ching! Exactly ₹${R.price}! Toy purchased!`);
          } else if (currentTotal > R.price) {
            AudioEngine.wrong();
            SpeechEngine.speak(`That is ₹${currentTotal}, which is more than ₹${R.price}. Tap a coin on the counter to remove it.`);
          }
        }

        redraw();

        nextBtn.onclick = () => {
          roundIdx++;
          if (roundIdx < rounds.length) {
            renderRound();
          } else {
            onComplete({ score, total: rounds.length });
          }
        };
      }

      renderRound();
    },

    /* ----------------------------------------------------
       6. PAN BALANCE SCALE (HEAVY OR LIGHT)
       ---------------------------------------------------- */
    runPanBalance(canvas, config, footer, onComplete) {
      const rounds = config.rounds;
      let roundIdx = 0;
      let score = 0;

      function renderRound() {
        const R = rounds[roundIdx];
        let placedWeights = [];
        let available = R.availableWeights.slice();

        const progressPill = footer ? footer.querySelector('#c2ProgressPill') : null;
        const nextBtn = footer ? footer.querySelector('#c2BtnNext') : null;
        if (progressPill) progressPill.textContent = `Round ${roundIdx + 1} of ${rounds.length} ⭐`;
        if (nextBtn) {
          nextBtn.disabled = true;
          nextBtn.textContent = roundIdx + 1 < rounds.length ? 'Next Scale →' : 'Finish Challenge! 🏆';
        }

        canvas.innerHTML = `
          <div class="c2-balance-container">
            <div class="c2-balance-beam-assembly">
              <div class="c2-balance-fulcrum"></div>
              <div class="c2-balance-beam" id="c2Beam">
                <div class="c2-balance-pivot-point"></div>
                <div class="c2-balance-pan left-pan">
                  <div class="c2-pan-strings"></div>
                  <div class="c2-pan-dish">
                    <span>${R.leftItem.split(' ')[0]}</span>
                  </div>
                </div>
                <div class="c2-balance-pan right-pan">
                  <div class="c2-pan-strings"></div>
                  <div class="c2-pan-dish" id="c2RightDish"></div>
                </div>
              </div>
            </div>

            <div style="font-weight:700; color:#334155; margin-top:8px;">
              Item Weight: <b>${R.targetWeight}${R.unit}</b> | Pan Weights: <b id="c2WeightsTotal">0${R.unit}</b>
            </div>

            <div class="c2-balance-weights-tray" id="c2WeightsTray"></div>
          </div>
        `;

        const beam = canvas.querySelector('#c2Beam');
        const rightDish = canvas.querySelector('#c2RightDish');
        const tray = canvas.querySelector('#c2WeightsTray');
        const totalEl = canvas.querySelector('#c2WeightsTotal');

        function updateScale() {
          tray.innerHTML = '';
          available.forEach((w, idx) => {
            const block = document.createElement('button');
            block.type = 'button';
            block.className = 'c2-weight-block';
            block.textContent = `+${w}${R.unit}`;
            block.onclick = () => {
              AudioEngine.tilt();
              available.splice(idx, 1);
              placedWeights.push(w);
              updateScale();
            };
            tray.appendChild(block);
          });

          rightDish.innerHTML = '';
          placedWeights.forEach((w, idx) => {
            const mini = document.createElement('span');
            mini.style.fontSize = '12px';
            mini.style.fontWeight = '800';
            mini.style.background = '#334155';
            mini.style.color = '#fff';
            mini.style.padding = '2px 6px';
            mini.style.borderRadius = '6px';
            mini.style.cursor = 'pointer';
            mini.textContent = `${w}`;
            mini.title = 'Tap to remove';
            mini.onclick = (e) => {
              e.stopPropagation();
              AudioEngine.pop();
              placedWeights.splice(idx, 1);
              available.push(w);
              updateScale();
            };
            rightDish.appendChild(mini);
          });

          const currentTotal = placedWeights.reduce((s, w) => s + w, 0);
          totalEl.textContent = `${currentTotal}${R.unit}`;

          const diff = currentTotal - R.targetWeight;
          let angle = 0;
          if (diff < 0) {
            angle = Math.max(-14, Math.round(diff / 25));
          } else if (diff > 0) {
            angle = Math.min(14, Math.round(diff / 25));
          }
          beam.style.transform = `rotate(${angle}deg)`;

          if (diff === 0) {
            AudioEngine.success();
            score++;
            nextBtn.disabled = false;
            SpeechEngine.speak(`Perfect balance! Both sides weigh ${R.targetWeight}${R.unit}!`);
          }
        }

        updateScale();

        nextBtn.onclick = () => {
          roundIdx++;
          if (roundIdx < rounds.length) {
            renderRound();
          } else {
            onComplete({ score, total: rounds.length });
          }
        };
      }

      renderRound();
    },

    /* ----------------------------------------------------
       7. TACTILE BUCKET SORTER
       ---------------------------------------------------- */
    runBucketSorter(canvas, config, footer, onComplete) {
      let unplaced = config.items.slice();
      let selectedItem = null;
      let mistakes = 0;

      const progressPill = footer.querySelector('#c2ProgressPill');
      const nextBtn = footer.querySelector('#c2BtnNext');
      progressPill.textContent = `${unplaced.length} cards to sort ⭐`;
      nextBtn.disabled = true;
      nextBtn.textContent = 'Finish Sorting! 🏆';

      canvas.innerHTML = `
        <div class="c2-sorter-arena">
          <div class="c2-sorter-cards-dock" id="c2CardsDock"></div>
          <div class="c2-buckets-shelf" id="c2BucketsShelf"></div>
        </div>
      `;

      const dock = canvas.querySelector('#c2CardsDock');
      const shelf = canvas.querySelector('#c2BucketsShelf');

      function renderDock() {
        dock.innerHTML = '';
        unplaced.forEach(it => {
          const card = document.createElement('button');
          card.type = 'button';
          card.className = `c2-tactile-card ${selectedItem === it ? 'selected' : ''}`;
          card.innerHTML = `<span>${it.icon || '🏷️'}</span> <span>${it.text}</span>`;
          card.onclick = () => {
            AudioEngine.pop();
            selectedItem = selectedItem === it ? null : it;
            renderDock();
          };
          dock.appendChild(card);
        });

        progressPill.textContent = `${unplaced.length} cards left to sort ⭐`;
      }

      config.buckets.forEach(b => {
        const bucket = document.createElement('div');
        bucket.className = 'c2-drop-bucket';
        bucket.style.backgroundColor = b.color;
        bucket.style.borderColor = b.border || b.color;
        bucket.dataset.bucketId = b.id;

        bucket.innerHTML = `
          <div class="c2-bucket-title">${b.label}</div>
          <div class="c2-bucket-items-well" id="well_${b.id}"></div>
        `;

        bucket.onclick = () => {
          if (!selectedItem) {
            SpeechEngine.speak('Pick a card first, then tap the bucket!');
            return;
          }

          if (selectedItem.bucket === b.id) {
            AudioEngine.pop();
            const well = bucket.querySelector(`#well_${b.id}`);
            const chip = document.createElement('span');
            chip.style.background = '#ffffff';
            chip.style.color = '#0f172a';
            chip.style.padding = '4px 8px';
            chip.style.borderRadius = '8px';
            chip.style.fontSize = '13px';
            chip.style.fontWeight = '700';
            chip.textContent = `${selectedItem.icon || ''} ${selectedItem.text}`;
            well.appendChild(chip);

            unplaced = unplaced.filter(x => x !== selectedItem);
            selectedItem = null;
            renderDock();

            if (unplaced.length === 0) {
              AudioEngine.success();
              nextBtn.disabled = false;
              SpeechEngine.speak('Awesome sorting! All items placed in the right groups!');
            }
          } else {
            mistakes++;
            AudioEngine.wrong();
            SpeechEngine.speak(`Not quite. Try another bucket for ${selectedItem.text}.`);
          }
        };

        shelf.appendChild(bucket);
      });

      renderDock();

      nextBtn.onclick = () => {
        const score = Math.max(1, config.items.length - mistakes);
        onComplete({ score, total: config.items.length });
      };
    },

    /* ----------------------------------------------------
       8. SENTENCE TRAIN (WORD TRAIN)
       ---------------------------------------------------- */
    runWordTrain(canvas, config, footer, onComplete) {
      const rounds = config.rounds;
      let roundIdx = 0;
      let score = 0;

      function renderRound() {
        const R = rounds[roundIdx];
        let placed = [];
        let pool = R.words.slice().sort(() => Math.random() - 0.5);

        const progressPill = footer.querySelector('#c2ProgressPill');
        const nextBtn = footer.querySelector('#c2BtnNext');
        progressPill.textContent = `Round ${roundIdx + 1} of ${rounds.length} ⭐`;
        nextBtn.disabled = true;
        nextBtn.textContent = roundIdx + 1 < rounds.length ? 'Next Train →' : 'Finish Challenge! 🏆';

        canvas.innerHTML = `
          <div class="c2-train-yard">
            <div class="c2-train-track" id="c2Track">
              <span class="c2-train-locomotive">🚂</span>
            </div>
            <div style="font-size:13px; font-weight:700; color:#64748b; margin-top:8px;">Tap words in sequence to assemble the train:</div>
            <div style="display:flex; gap:10px; flex-wrap:wrap; justify-content:center; min-height:50px;" id="c2WordPool"></div>
          </div>
        `;

        const track = canvas.querySelector('#c2Track');
        const poolEl = canvas.querySelector('#c2WordPool');

        function redraw() {
          track.querySelectorAll('.c2-train-carriage-slot').forEach(e => e.remove());
          R.correctOrder.forEach((_, idx) => {
            const slot = document.createElement('div');
            const word = placed[idx];
            slot.className = `c2-train-carriage-slot ${word ? 'filled' : ''}`;
            slot.textContent = word || `Car ${idx + 1}`;
            if (word) {
              slot.onclick = () => {
                AudioEngine.pop();
                placed.splice(idx, 1);
                pool.push(word);
                redraw();
              };
            }
            track.appendChild(slot);
          });

          poolEl.innerHTML = '';
          pool.forEach((word, idx) => {
            const chip = document.createElement('button');
            chip.type = 'button';
            chip.className = 'c2-tactile-card';
            chip.textContent = word;
            chip.onclick = () => {
              AudioEngine.pop();
              pool.splice(idx, 1);
              placed.push(word);
              redraw();
            };
            poolEl.appendChild(chip);
          });

          if (placed.length === R.correctOrder.length) {
            const isCorrect = placed.every((w, i) => w === R.correctOrder[i]);
            if (isCorrect) {
              AudioEngine.success();
              score++;
              nextBtn.disabled = false;
              SpeechEngine.speak('Choo choo! Perfect sentence! All carriages connected!');
            } else {
              AudioEngine.wrong();
              SpeechEngine.speak('The words are not in the right order yet. Tap a car to change it.');
            }
          }
        }

        redraw();

        nextBtn.onclick = () => {
          roundIdx++;
          if (roundIdx < rounds.length) {
            renderRound();
          } else {
            onComplete({ score, total: rounds.length });
          }
        };
      }

      renderRound();
    },

    /* ----------------------------------------------------
       9. PHONICS BUBBLE POP
       ---------------------------------------------------- */
    runBubblePop(canvas, config, footer, onComplete) {
      const rounds = config.rounds;
      let roundIdx = 0;
      let score = 0;

      function renderRound() {
        const R = rounds[roundIdx];
        const progressPill = footer.querySelector('#c2ProgressPill');
        const nextBtn = footer.querySelector('#c2BtnNext');
        progressPill.textContent = `Round ${roundIdx + 1} of ${rounds.length} ⭐`;
        nextBtn.disabled = true;
        nextBtn.textContent = roundIdx + 1 < rounds.length ? 'Next Bubbles →' : 'Finish Challenge! 🏆';

        canvas.innerHTML = `
          <div style="font-family:var(--font-heading); font-size:17px; font-weight:700; color:#6b21a8; margin-bottom:12px;">
            ${R.prompt}
          </div>
          <div class="c2-bubble-chamber" id="c2Chamber"></div>
        `;

        const chamber = canvas.querySelector('#c2Chamber');
        let remainingTargetCount = R.bubbles.filter(b => b.correct).length;

        R.bubbles.forEach((b, idx) => {
          const bubble = document.createElement('div');
          bubble.className = 'c2-floating-bubble';
          bubble.textContent = b.text;

          const leftPct = 12 + (idx % 3) * 28 + (Math.random() * 8 - 4);
          const topPct = 18 + Math.floor(idx / 3) * 44 + (Math.random() * 8 - 4);
          bubble.style.left = `${leftPct}%`;
          bubble.style.top = `${topPct}%`;
          bubble.style.animationDelay = `${(idx * 0.35).toFixed(2)}s`;

          bubble.onclick = () => {
            if (b.correct) {
              AudioEngine.pop();
              bubble.classList.add('popping');
              b.popped = true;
              remainingTargetCount--;

              setTimeout(() => bubble.remove(), 240);

              if (remainingTargetCount <= 0) {
                AudioEngine.success();
                score++;
                nextBtn.disabled = false;
                SpeechEngine.speak('Splendid! You popped all the target bubbles!');
              }
            } else {
              AudioEngine.wrong();
              bubble.style.transform = 'scale(0.85)';
              setTimeout(() => bubble.style.transform = '', 300);
              SpeechEngine.speak(`That is ${b.text}. Look for words that match the sound!`);
            }
          };

          chamber.appendChild(bubble);
        });

        SpeechEngine.speak(R.speechText || R.prompt);

        nextBtn.onclick = () => {
          roundIdx++;
          if (roundIdx < rounds.length) {
            renderRound();
          } else {
            onComplete({ score, total: rounds.length });
          }
        };
      }

      renderRound();
    }
  };

  root.Class2Games = Class2Games;
})(typeof window !== 'undefined' ? window : this);
