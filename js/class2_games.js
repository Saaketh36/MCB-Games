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
          targetMl: 500,
          targetName: "🥣 500ml Measuring Bowl",
          ticks: [100, 200, 300, 400, 500],
          availableCups: [
            { ml: 100, label: "100ml Glass", icon: "🥛" },
            { ml: 250, label: "250ml Cup", icon: "🥤" }
          ]
        },
        {
          targetMl: 750,
          targetName: "🍶 750ml Measuring Flask",
          ticks: [250, 500, 750],
          availableCups: [
            { ml: 250, label: "250ml Glass", icon: "🥤" },
            { ml: 500, label: "500ml Bottle", icon: "🫖" }
          ]
        },
        {
          targetMl: 1000,
          targetName: "🫗 1000ml (1 Litre) Jug",
          ticks: [250, 500, 750, 1000],
          availableCups: [
            { ml: 250, label: "250ml Glass", icon: "🥤" },
            { ml: 500, label: "500ml Bottle", icon: "🫖" }
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
    },

    /* ====================================================
       CLASS 1 PROCEDURAL GENERATORS (AGES 5-6)
       Tactile, Hands-On Mini-Games for Class 1
       ==================================================== */

    // 11. I-MAT-02: Add & Subtract Sprint (Froggy Lilypad Hopper 0-10)
    "I-MAT-02": function () {
      const shapePrizes = [
        { icon: "⭐", shape: "star", name: "Golden Star", color: "#f59e0b" },
        { icon: "💎", shape: "gem", name: "Sparkle Gem", color: "#06b6d4" },
        { icon: "🌸", shape: "flower", name: "Water Lily", color: "#ec4899" },
        { icon: "🍎", shape: "apple", name: "Red Apple", color: "#ef4444" },
        { icon: "🥕", shape: "carrot", name: "Crispy Carrot", color: "#f97316" }
      ];
      const prizes = pickMultiple(shapePrizes, 3);
      const t1 = pickRandom([3, 4, 5]);
      const t2 = pickRandom([6, 7, 8]);
      const t3 = pickRandom([9, 10]);

      return {
        engine: "number-line-hopper",
        title: "Froggy Lilypad Sprint",
        icon: "🐸",
        instruction: "Help Freddie Frog hop along the lilypads to collect the prize!",
        speechPrompt: "Choose your jumps to help Freddie Frog land directly on the prize!",
        rounds: [
          {
            start: 0,
            target: t1,
            step: 1,
            allowedHops: [1, 2],
            itemAtTarget: prizes[0],
            hint: `Start at 0 and take jumps of 1 or 2 to reach ${t1}!`
          },
          {
            start: 1,
            target: t2,
            step: 1,
            allowedHops: [1, 2, 3],
            itemAtTarget: prizes[1],
            hint: `Start at 1 and hop forward to reach ${t2}!`
          },
          {
            start: 2,
            target: t3,
            step: 1,
            allowedHops: [1, 2, 3],
            itemAtTarget: prizes[2],
            hint: `Start at 2 and hop forward to reach ${t3}!`
          }
        ]
      };
    },

    // 12. I-MAT-06: Pattern Train (Word Train Engine for Shapes & Colors)
    "I-MAT-06": function () {
      const patternSets = [
        {
          items: ["🔴 Red", "🟦 Blue", "🔴 Red", "🟦 Blue"],
          hint: "Follow the pattern: Red, Blue, Red, Blue!"
        },
        {
          items: ["⭐ Star", "🌙 Moon", "⭐ Star", "🌙 Moon"],
          hint: "Follow the pattern: Star, Moon, Star, Moon!"
        },
        {
          items: ["🍎 Apple", "🍌 Banana", "🍎 Apple", "🍌 Banana"],
          hint: "Follow the pattern: Apple, Banana, Apple, Banana!"
        },
        {
          items: ["🔺 Triangle", "🟩 Square", "🔺 Triangle", "🟩 Square"],
          hint: "Follow the pattern: Triangle, Square, Triangle, Square!"
        },
        {
          items: ["🟢 Green", "🟡 Yellow", "🟢 Green", "🟡 Yellow"],
          hint: "Follow the pattern: Green, Yellow, Green, Yellow!"
        }
      ];
      const chosen = pickMultiple(patternSets, 3);

      return {
        engine: "word-train",
        title: "Pattern Train Express",
        icon: "🚂",
        instruction: "Tap the items in the right order to complete the repeating pattern train!",
        speechPrompt: "Look at the pattern! Put the cars in order to make the pattern complete.",
        rounds: chosen.map(p => ({
          words: p.items.slice(),
          correctOrder: p.items.slice(),
          hint: p.hint
        }))
      };
    },

    // 13. I-MAT-03: Odd One Out Zoo (4-Legged Animals vs 2-Legged Birds)
    "I-MAT-03": function () {
      const walkers = [
        { text: "Lion", icon: "🦁", bucket: "walker" },
        { text: "Elephant", icon: "🐘", bucket: "walker" },
        { text: "Dog", icon: "🐶", bucket: "walker" },
        { text: "Cat", icon: "🐱", bucket: "walker" },
        { text: "Horse", icon: "🐴", bucket: "walker" },
        { text: "Tiger", icon: "🐯", bucket: "walker" }
      ];
      const birds = [
        { text: "Parrot", icon: "🦜", bucket: "bird" },
        { text: "Duck", icon: "🦆", bucket: "bird" },
        { text: "Peacock", icon: "🦚", bucket: "bird" },
        { text: "Owl", icon: "🦉", bucket: "bird" },
        { text: "Penguin", icon: "🐧", bucket: "bird" },
        { text: "Sparrow", icon: "🐦", bucket: "bird" }
      ];

      return {
        engine: "bucket-sorter",
        title: "Zoo Animal Sorter",
        icon: "🦁",
        instruction: "Sort the animals into 4-Legged Animals and 2-Legged Birds!",
        speechPrompt: "Sort the animals! Put 4-legged animals in green, and 2-legged birds in sky blue.",
        buckets: [
          { id: "walker", label: "🐾 4-Legged Animals", color: "#10b981", border: "#059669" },
          { id: "bird", label: "🪶 2-Legged Birds", color: "#0ea5e9", border: "#0284c7" }
        ],
        items: pickMultiple(walkers, 3).concat(pickMultiple(birds, 3)).sort(() => Math.random() - 0.5)
      };
    },

    // 14. I-MAT-04: Solid Shape Safari (Rolling vs Sliding)
    "I-MAT-04": function () {
      const rolling = [
        { text: "Football", icon: "⚽", bucket: "roll" },
        { text: "Orange", icon: "🍊", bucket: "roll" },
        { text: "Marble", icon: "⚪", bucket: "roll" },
        { text: "Globe", icon: "🌍", bucket: "roll" },
        { text: "Tennis Ball", icon: "🎾", bucket: "roll" },
        { text: "Apple", icon: "🍎", bucket: "roll" }
      ];
      const sliding = [
        { text: "Book", icon: "📕", bucket: "slide" },
        { text: "Dice", icon: "🎲", bucket: "slide" },
        { text: "Eraser", icon: "🧼", bucket: "slide" },
        { text: "Pencil Box", icon: "✏️", bucket: "slide" },
        { text: "Brick", icon: "🧱", bucket: "slide" },
        { text: "Gift Box", icon: "🎁", bucket: "slide" }
      ];

      return {
        engine: "bucket-sorter",
        title: "Roll or Slide Safari",
        icon: "⚽",
        instruction: "Sort objects into things that ROLL and things that SLIDE!",
        speechPrompt: "Can it roll like a ball, or does it slide like a box? Sort each item.",
        buckets: [
          { id: "roll", label: "⚽ Objects that ROLL (Round)", color: "#f59e0b", border: "#d97706" },
          { id: "slide", label: "📦 Objects that SLIDE (Flat)", color: "#8b5cf6", border: "#7c3aed" }
        ],
        items: pickMultiple(rolling, 3).concat(pickMultiple(sliding, 3)).sort(() => Math.random() - 0.5)
      };
    },

    // 15. I-ENG-07: Letter Sound Safari (Phonics Bubble Pop)
    "I-ENG-07": function () {
      const soundGroups = [
        {
          prompt: "Pop all the pictures starting with the /B/ sound!",
          speechText: "Pop bubbles starting with the sound B, like Ball and Bat!",
          bubbles: [
            { text: "BAT 🦇", correct: true },
            { text: "BALL ⚽", correct: true },
            { text: "BIRD 🐦", correct: true },
            { text: "CAT 🐱", correct: false },
            { text: "FISH 🐟", correct: false },
            { text: "SUN ☀️", correct: false }
          ]
        },
        {
          prompt: "Pop all the pictures starting with the /S/ sound!",
          speechText: "Pop bubbles starting with the sound S, like Sun and Star!",
          bubbles: [
            { text: "SUN ☀️", correct: true },
            { text: "STAR ⭐", correct: true },
            { text: "SNAKE 🐍", correct: true },
            { text: "DOG 🐶", correct: false },
            { text: "APPLE 🍎", correct: false },
            { text: "MOON 🌙", correct: false }
          ]
        },
        {
          prompt: "Pop all the pictures starting with the /M/ sound!",
          speechText: "Pop bubbles starting with the sound M, like Monkey and Moon!",
          bubbles: [
            { text: "MONKEY 🐵", correct: true },
            { text: "MOON 🌙", correct: true },
            { text: "MANGO 🥭", correct: true },
            { text: "TREE 🌳", correct: false },
            { text: "BOAT ⛵", correct: false },
            { text: "BELL 🔔", correct: false }
          ]
        },
        {
          prompt: "Pop all the pictures starting with the /P/ sound!",
          speechText: "Pop bubbles starting with the sound P, like Pen and Pig!",
          bubbles: [
            { text: "PEN 🖊️", correct: true },
            { text: "PIG 🐷", correct: true },
            { text: "PAN 🍳", correct: true },
            { text: "COW 🐮", correct: false },
            { text: "HAT 🎩", correct: false },
            { text: "CUP 🥤", correct: false }
          ]
        }
      ];

      return {
        engine: "bubble-pop",
        title: "Letter Sound Safari",
        icon: "🫧",
        instruction: "Listen carefully to the sound and pop the matching bubbles!",
        speechPrompt: "Pop the bubbles that start with the requested letter sound!",
        rounds: pickMultiple(soundGroups, 2)
      };
    },

    // 16. I-ENG-06: Sight Word Memory Match (Bubble Pop)
    "I-ENG-06": function () {
      const sightGroups = [
        {
          prompt: "Find and pop all bubbles with the sight word 'THE'!",
          speechText: "Pop all the bubbles that say THE!",
          bubbles: [
            { text: "THE 🌟", correct: true },
            { text: "THE 🌟", correct: true },
            { text: "THE 🌟", correct: true },
            { text: "AND 🎈", correct: false },
            { text: "YOU 🎈", correct: false },
            { text: "FOR 🎈", correct: false }
          ]
        },
        {
          prompt: "Find and pop all bubbles with the sight word 'SEE'!",
          speechText: "Pop all the bubbles that say SEE!",
          bubbles: [
            { text: "SEE 👀", correct: true },
            { text: "SEE 👀", correct: true },
            { text: "SEE 👀", correct: true },
            { text: "CAN 🥫", correct: false },
            { text: "BIG 🐘", correct: false },
            { text: "RED 🔴", correct: false }
          ]
        },
        {
          prompt: "Find and pop all bubbles with the sight word 'CAN'!",
          speechText: "Pop all the bubbles that say CAN!",
          bubbles: [
            { text: "CAN 🥫", correct: true },
            { text: "CAN 🥫", correct: true },
            { text: "CAN 🥫", correct: true },
            { text: "NOT ❌", correct: false },
            { text: "RUN 🏃", correct: false },
            { text: "ONE 1️⃣", correct: false }
          ]
        },
        {
          prompt: "Find and pop all bubbles with the sight word 'AND'!",
          speechText: "Pop all the bubbles that say AND!",
          bubbles: [
            { text: "AND 🤝", correct: true },
            { text: "AND 🤝", correct: true },
            { text: "AND 🤝", correct: true },
            { text: "SHE 👧", correct: false },
            { text: "HE 👦", correct: false },
            { text: "WE 👫", correct: false }
          ]
        }
      ];

      return {
        engine: "bubble-pop",
        title: "Sight Word Pop Star",
        icon: "🌟",
        instruction: "Spot the target sight word and pop all its bubbles!",
        speechPrompt: "Find and pop all the bubbles with the target sight word!",
        rounds: pickMultiple(sightGroups, 2)
      };
    },

    // 17. I-ENG-09: Word Builder (CVC Phonics Train)
    "I-ENG-09": function () {
      const cvcBank = [
        { word: "CAT", letters: ["C", "A", "T"], hint: "Spell C-A-T (Cat 🐱)" },
        { word: "DOG", letters: ["D", "O", "G"], hint: "Spell D-O-G (Dog 🐶)" },
        { word: "SUN", letters: ["S", "U", "N"], hint: "Spell S-U-N (Sun ☀️)" },
        { word: "PEN", letters: ["P", "E", "N"], hint: "Spell P-E-N (Pen 🖊️)" },
        { word: "BAT", letters: ["B", "A", "T"], hint: "Spell B-A-T (Bat 🦇)" },
        { word: "CUP", letters: ["C", "U", "P"], hint: "Spell C-U-P (Cup 🥤)" },
        { word: "PIG", letters: ["P", "I", "G"], hint: "Spell P-I-G (Pig 🐷)" },
        { word: "BUS", letters: ["B", "U", "S"], hint: "Spell B-U-S (Bus 🚌)" }
      ];
      const selected = pickMultiple(cvcBank, 3);

      return {
        engine: "word-train",
        title: "CVC Word Builder Train",
        icon: "🚂",
        instruction: "Put the letter wagons in the right order to spell the word!",
        speechPrompt: "Tap the letters in the correct order to spell the word for the train.",
        rounds: selected.map(item => ({
          words: item.letters.slice(),
          correctOrder: item.letters.slice(),
          hint: item.hint
        }))
      };
    },

    // 18. I-ENG-11: Noun Basket Sort (Fruits vs Toys)
    "I-ENG-11": function () {
      const fruits = [
        { text: "Apple", icon: "🍎", bucket: "fruit" },
        { text: "Banana", icon: "🍌", bucket: "fruit" },
        { text: "Mango", icon: "🥭", bucket: "fruit" },
        { text: "Grapes", icon: "🍇", bucket: "fruit" },
        { text: "Orange", icon: "🍊", bucket: "fruit" },
        { text: "Strawberry", icon: "🍓", bucket: "fruit" }
      ];
      const toys = [
        { text: "Teddy Bear", icon: "🧸", bucket: "toy" },
        { text: "Toy Train", icon: "🚂", bucket: "toy" },
        { text: "Yo-Yo", icon: "🪀", bucket: "toy" },
        { text: "Spinning Top", icon: "🪀", bucket: "toy" },
        { text: "Doll", icon: "🪆", bucket: "toy" },
        { text: "Robot", icon: "🤖", bucket: "toy" }
      ];

      return {
        engine: "bucket-sorter",
        title: "Noun Basket Sorter",
        icon: "🧺",
        instruction: "Sort the items into the Fruit Basket and Toy Basket!",
        speechPrompt: "Is it a fruit you can eat, or a fun toy to play with? Sort them into the baskets.",
        buckets: [
          { id: "fruit", label: "🍎 Fruit Basket", color: "#ec4899", border: "#db2777" },
          { id: "toy", label: "🧸 Toy Basket", color: "#3b82f6", border: "#2563eb" }
        ],
        items: pickMultiple(fruits, 3).concat(pickMultiple(toys, 3)).sort(() => Math.random() - 0.5)
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
      if (Class2Generators[game.id]) return true;
      if (String(game.id || '').startsWith('II-') || String(game.id || '').startsWith('I-')) {
        return !!(Class2Generators[game.id]);
      }
      const cls = String(game.class || '').toUpperCase().replace(/^CLASS\s+/, '').trim();
      if (cls === 'I' || cls === '1' || cls === 'II' || cls === '2') {
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
          const v1 = pickRandom([400, 500]);
          const v2 = 1000;
          cloned.rounds = [
            {
              targetMl: v1,
              targetName: `🥣 ${v1}ml Measuring Bowl`,
              ticks: v1 === 500 ? [100, 200, 300, 400, 500] : [100, 200, 300, 400],
              availableCups: [
                { ml: 100, label: "100ml Glass", icon: "🥛" },
                { ml: 250, label: "250ml Cup", icon: "🥤" }
              ]
            },
            {
              targetMl: 750,
              targetName: "🍶 750ml Measuring Flask",
              ticks: [250, 500, 750],
              availableCups: [
                { ml: 250, label: "250ml Glass", icon: "🥤" },
                { ml: 500, label: "500ml Bottle", icon: "🫖" }
              ]
            },
            {
              targetMl: v2,
              targetName: `🫗 ${v2}ml (1 Litre) Jug`,
              ticks: [250, 500, 750, 1000],
              availableCups: [
                { ml: 250, label: "250ml Glass", icon: "🥤" },
                { ml: 500, label: "500ml Bottle", icon: "🫖" }
              ]
            }
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

      // Resolve canonical engine name across aliases
      const rawEngine = (config.engine || '').toLowerCase().trim();
      let canonicalEngine = rawEngine;
      if (['bucket-sorter', 'sort-and-group', 'sorting challenge', 'categorization', 'sorter'].includes(rawEngine)) {
        canonicalEngine = 'bucket-sorter';
      } else if (['word-train', 'sequence-order', 'step sequence', 'order & rank', 'timeline', 'train', 'order'].includes(rawEngine)) {
        canonicalEngine = 'word-train';
      } else if (['pair-matcher', 'match-pairs', 'memory match', 'matching', 'pairs', 'matcher'].includes(rawEngine)) {
        canonicalEngine = 'pair-matcher';
      } else if (['word-scramble', 'scramble', 'anagram', 'letter-arrange', 'spelling'].includes(rawEngine)) {
        canonicalEngine = 'word-scramble';
      } else if (['bubble-pop', 'bubble', 'pop'].includes(rawEngine)) {
        canonicalEngine = 'bubble-pop';
      } else if (['number-line-hopper', 'hopper', 'number line', 'math hop'].includes(rawEngine)) {
        canonicalEngine = 'number-line-hopper';
      }

      // Dispatch to specific mini-engine
      switch (canonicalEngine) {
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
        case 'pair-matcher':
          this.runPairMatcher(boardCanvas, config, footer, onComplete);
          break;
        case 'word-scramble':
          this.runWordScramble(boardCanvas, config, footer, onComplete);
          break;
        default:
          boardCanvas.innerHTML = `<div style="padding:24px; text-align:center; color:#64748b; font-weight:700;">Engine <code>${config.engine}</code> ready. Starting challenge...</div>`;
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
                <div class="c2-jug-glass-body">
                  <div class="c2-jug-liquid-fill" id="c2LiquidFill" style="height: 0%;">
                    <div class="c2-liquid-surface-wave"></div>
                  </div>
                  <div class="c2-jug-tick-marks" id="c2JugTicks"></div>
                </div>
              </div>
            </div>

            <div style="font-size:13.5px; font-weight:700; color:#475569;">Tap a cup to pour into the jug:</div>
            <div class="c2-cups-dock" id="c2CupsDock"></div>
            <button type="button" class="c2-btn-empty-jug" id="c2BtnEmptyJug">🔄 Empty Jug & Retry</button>
          </div>
        `;

        // Render tick marks positioned accurately by exact percentage
        const ticksContainer = canvas.querySelector('#c2JugTicks');
        ticksContainer.innerHTML = '';
        const tickValues = R.ticks || [0.25, 0.5, 0.75, 1.0].map(pct => Math.round(targetMl * pct));
        tickValues.forEach(val => {
          const pct = Math.min(100, Math.round((val / targetMl) * 100));
          const tick = document.createElement('div');
          tick.className = 'c2-jug-tick' + (val === targetMl ? ' target-tick' : '');
          tick.style.bottom = `${pct}%`;
          tick.innerHTML = `<span>${val}ml</span>`;
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
          dock.querySelectorAll('button').forEach(b => b.disabled = false);
          emptyBtn.classList.remove('pulse');
          updateJugUI();
        };

        function doPour(ml) {
          if (currentMl >= targetMl) return;
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
            fillEl.style.background = 'linear-gradient(180deg, #34d399 0%, #059669 100%)';
            SpeechEngine.speak(`Splendid! Exactly ${targetMl} millilitres! The jug is filled perfectly!`);
          } else if (currentMl > targetMl) {
            AudioEngine.wrong();
            fillEl.style.background = 'linear-gradient(180deg, #f87171 0%, #dc2626 100%)';
            dock.querySelectorAll('button').forEach(b => b.disabled = true);
            emptyBtn.classList.add('pulse');
            SpeechEngine.speak(`Oh no, it overflowed! You have ${currentMl} ml. Tap Empty Jug to try again.`);
          } else {
            fillEl.style.background = 'linear-gradient(180deg, #38bdf8 0%, #0284c7 100%)';
            dock.querySelectorAll('button').forEach(b => b.disabled = false);
            emptyBtn.classList.remove('pulse');
            emptyBtn.style.display = 'inline-block';
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
          const itemText = it.text || it.label || '';
          const card = document.createElement('button');
          card.type = 'button';
          card.className = `c2-tactile-card ${selectedItem === it ? 'selected' : ''}`;
          card.innerHTML = `<span>${it.icon || '🏷️'}</span> <span>${itemText}</span>`;
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
            const itemText = selectedItem.text || selectedItem.label || '';
            chip.textContent = `${selectedItem.icon || ''} ${itemText}`;
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
            const itName = selectedItem.text || selectedItem.label || 'this item';
            SpeechEngine.speak(`Not quite. Try another bucket for ${itName}.`);
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
    },

    /* ----------------------------------------------------
       10. TACTILE PAIR MATCHER (MATCH PAIRS / CONNECTOR)
       ---------------------------------------------------- */
    runPairMatcher(canvas, config, footer, onComplete) {
      let rawRounds = config.rounds;
      if (!rawRounds || !Array.isArray(rawRounds) || rawRounds.length === 0) {
        const rawPairs = config.pairs || [];
        rawRounds = [{
          prompt: config.instruction || 'Match each item on the left with its partner on the right!',
          pairs: rawPairs
        }];
      }

      let roundIdx = 0;
      let totalRounds = rawRounds.length;
      let totalMatchesMade = 0;
      let totalPossibleMatches = 0;

      function renderRound() {
        const R = rawRounds[roundIdx];
        const rawPairs = R.pairs || [];
        const normalizedPairs = rawPairs.map((p, idx) => {
          let itemA = p.itemA || p.a || p.left || (Array.isArray(p) ? p[0] : `Item ${idx + 1}`);
          let itemB = p.itemB || p.b || p.right || (Array.isArray(p) ? p[1] : `Match ${idx + 1}`);
          return {
            id: String(p.id !== undefined ? p.id : idx),
            a: String(itemA).trim(),
            b: String(itemB).trim()
          };
        });

        totalPossibleMatches += normalizedPairs.length;
        let matchedCount = 0;
        let selectedA = null;

        const progressPill = footer.querySelector('#c2ProgressPill');
        const nextBtn = footer.querySelector('#c2BtnNext');
        if (progressPill) progressPill.textContent = `Round ${roundIdx + 1} of ${totalRounds} · 0 / ${normalizedPairs.length} matched ⭐`;
        if (nextBtn) {
          nextBtn.disabled = true;
          nextBtn.textContent = roundIdx + 1 < totalRounds ? 'Next Match →' : 'Finish Challenge! 🏆';
        }

        // Shuffle sides independently
        const colAItems = normalizedPairs.slice().sort(() => Math.random() - 0.5);
        const colBItems = normalizedPairs.slice().sort(() => Math.random() - 0.5);

        canvas.innerHTML = `
          <div class="c2-pair-arena">
            <div class="c2-pair-prompt-bar">
              <span>🎯</span> <span>${escapeHtml(R.prompt || config.instruction || 'Tap an item on the left, then tap its matching pair on the right!')}</span>
            </div>
            <div class="c2-pair-columns-wrap">
              <div class="c2-pair-column" id="c2ColA"></div>
              <div class="c2-pair-divider">
                <span class="c2-pair-divider-line"></span>
                <span class="c2-pair-connector-icon">⚡</span>
                <span class="c2-pair-divider-line"></span>
              </div>
              <div class="c2-pair-column" id="c2ColB"></div>
            </div>
          </div>
        `;

        const colAEl = canvas.querySelector('#c2ColA');
        const colBEl = canvas.querySelector('#c2ColB');

        function redraw() {
          colAEl.innerHTML = '';
          colBEl.innerHTML = '';

          colAItems.forEach(item => {
            const card = document.createElement('button');
            card.type = 'button';
            card.className = `c2-pair-card c2-pair-card-a ${item.matched ? 'matched' : ''} ${selectedA === item ? 'selected' : ''}`;
            card.dataset.pairId = item.id;
            card.innerHTML = `
              <span class="c2-pair-text">${escapeHtml(item.a)}</span>
              ${item.matched ? '<span class="c2-pair-check">✓</span>' : '<span class="c2-pair-dot">●</span>'}
            `;
            if (!item.matched) {
              card.onclick = () => {
                AudioEngine.pop();
                selectedA = (selectedA === item) ? null : item;
                redraw();
              };
            }
            colAEl.appendChild(card);
          });

          colBItems.forEach(item => {
            const card = document.createElement('button');
            card.type = 'button';
            card.className = `c2-pair-card c2-pair-card-b ${item.matched ? 'matched' : ''}`;
            card.dataset.pairId = item.id;
            card.innerHTML = `
              ${item.matched ? '<span class="c2-pair-check">✓</span>' : '<span class="c2-pair-dot">●</span>'}
              <span class="c2-pair-text">${escapeHtml(item.b)}</span>
            `;
            if (!item.matched) {
              card.onclick = () => {
                if (!selectedA) {
                  SpeechEngine.speak('Pick a card from the left side first!');
                  card.classList.add('c2-pair-hint-wobble');
                  setTimeout(() => card.classList.remove('c2-pair-hint-wobble'), 400);
                  return;
                }

                if (selectedA.id === item.id) {
                  // Correct Match!
                  AudioEngine.success();
                  selectedA.matched = true;
                  item.matched = true;
                  matchedCount++;
                  totalMatchesMade++;
                  selectedA = null;
                  redraw();

                  if (progressPill) progressPill.textContent = `Round ${roundIdx + 1} of ${totalRounds} · ${matchedCount} / ${normalizedPairs.length} matched ⭐`;

                  if (matchedCount === normalizedPairs.length) {
                    AudioEngine.success();
                    if (nextBtn) nextBtn.disabled = false;
                    SpeechEngine.speak('Sensational! All pairs connected perfectly!');
                  } else {
                    SpeechEngine.speak('Great match!');
                  }
                } else {
                  // Mismatch
                  AudioEngine.wrong();
                  card.classList.add('mismatch');
                  const activeCardA = colAEl.querySelector(`.c2-pair-card.selected`);
                  if (activeCardA) activeCardA.classList.add('mismatch');
                  SpeechEngine.speak('Not quite a match. Try another one!');
                  setTimeout(() => {
                    selectedA = null;
                    redraw();
                  }, 500);
                }
              };
            }
            colBEl.appendChild(card);
          });
        }

        redraw();

        if (nextBtn) {
          nextBtn.onclick = () => {
            roundIdx++;
            if (roundIdx < totalRounds) {
              renderRound();
            } else {
              onComplete({ score: totalMatchesMade, total: totalPossibleMatches });
            }
          };
        }
      }

      renderRound();
    },

    /* ----------------------------------------------------
       11. TACTILE WORD SCRAMBLE (SPELLING & LETTER ARRANGE)
       ---------------------------------------------------- */
    runWordScramble(canvas, config, footer, onComplete) {
      let rawRounds = config.rounds;
      if (!rawRounds || !Array.isArray(rawRounds) || rawRounds.length === 0) {
        const words = config.words || [config.word || 'SCIENCE'];
        rawRounds = words.map(w => ({
          word: typeof w === 'string' ? w : (w.word || 'LEARN'),
          clue: typeof w === 'object' ? (w.clue || '') : (config.clue || ''),
          icon: typeof w === 'object' ? (w.icon || '🧩') : (config.icon || '🧩')
        }));
      }

      let roundIdx = 0;
      let totalRounds = rawRounds.length;
      let score = 0;

      function renderRound() {
        const R = rawRounds[roundIdx];
        const rawTarget = String(R.word || 'GAME').toUpperCase().replace(/[^A-Z0-9]/g, '');
        const targetLetters = rawTarget.split('');
        const clueText = R.clue || config.instruction || 'Unscramble the letters to reveal the secret word!';
        const icon = R.icon || '🧩';

        let placed = new Array(targetLetters.length).fill(null);
        let pool = targetLetters.map((char, id) => ({ id, char })).sort(() => Math.random() - 0.5);

        // Ensure scrambled order is not already the answer if length > 2
        if (targetLetters.length > 2 && pool.map(p => p.char).join('') === rawTarget) {
          pool.reverse();
        }

        const progressPill = footer.querySelector('#c2ProgressPill');
        const nextBtn = footer.querySelector('#c2BtnNext');
        if (progressPill) progressPill.textContent = `Word ${roundIdx + 1} of ${totalRounds} ⭐`;
        if (nextBtn) {
          nextBtn.disabled = true;
          nextBtn.textContent = roundIdx + 1 < totalRounds ? 'Next Word →' : 'Finish Challenge! 🏆';
        }

        canvas.innerHTML = `
          <div class="c2-scramble-arena">
            <div class="c2-scramble-clue-card">
              <span class="c2-scramble-icon">${icon}</span>
              <div class="c2-scramble-clue-text">
                <span class="c2-scramble-clue-label">Clue:</span>
                <span class="c2-scramble-clue-body">${escapeHtml(clueText)}</span>
              </div>
            </div>

            <div class="c2-scramble-slots-row" id="c2ScrambleSlots"></div>

            <div class="c2-scramble-controls">
              <button type="button" class="c2-scramble-ctrl-btn" id="c2BtnBackspace" title="Undo last letter">
                <span>⌫</span> Backspace
              </button>
              <button type="button" class="c2-scramble-ctrl-btn" id="c2BtnClearAll" title="Clear all letters">
                <span>🔄</span> Reset
              </button>
            </div>

            <div style="font-size:13px; font-weight:700; color:#64748b; margin-top:14px;">Tap letters to place in order:</div>
            <div class="c2-scramble-pool-row" id="c2ScramblePool"></div>
          </div>
        `;

        const slotsEl = canvas.querySelector('#c2ScrambleSlots');
        const poolEl = canvas.querySelector('#c2ScramblePool');
        const btnBk = canvas.querySelector('#c2BtnBackspace');
        const btnClr = canvas.querySelector('#c2BtnClearAll');

        function redraw() {
          // Render Slots
          slotsEl.innerHTML = '';
          placed.forEach((slotItem, idx) => {
            const slot = document.createElement('button');
            slot.type = 'button';
            slot.className = `c2-scramble-slot ${slotItem ? 'filled' : ''}`;
            slot.textContent = slotItem ? slotItem.char : '';
            if (slotItem) {
              slot.title = 'Tap to remove letter';
              slot.onclick = () => {
                AudioEngine.pop();
                pool.push(slotItem);
                placed[idx] = null;
                redraw();
              };
            }
            slotsEl.appendChild(slot);
          });

          // Render Available Tiles
          poolEl.innerHTML = '';
          pool.forEach((item, idx) => {
            const tile = document.createElement('button');
            tile.type = 'button';
            tile.className = 'c2-scramble-tile';
            tile.textContent = item.char;
            tile.onclick = () => {
              const firstEmpty = placed.indexOf(null);
              if (firstEmpty !== -1) {
                AudioEngine.pop();
                placed[firstEmpty] = item;
                pool.splice(idx, 1);
                redraw();
                checkCompletion();
              }
            };
            poolEl.appendChild(tile);
          });
        }

        function checkCompletion() {
          if (!placed.includes(null)) {
            const assembled = placed.map(p => p.char).join('');
            if (assembled === rawTarget) {
              AudioEngine.success();
              score++;
              slotsEl.querySelectorAll('.c2-scramble-slot').forEach(s => s.classList.add('correct'));
              if (nextBtn) nextBtn.disabled = false;
              SpeechEngine.speak(`Awesome! You spelled ${rawTarget}!`);
            } else {
              AudioEngine.wrong();
              slotsEl.querySelectorAll('.c2-scramble-slot').forEach(s => s.classList.add('wrong'));
              SpeechEngine.speak('Not quite. Tap letters or backspace to try again!');
              setTimeout(() => {
                slotsEl.querySelectorAll('.c2-scramble-slot').forEach(s => s.classList.remove('wrong'));
              }, 600);
            }
          }
        }

        if (btnBk) {
          btnBk.onclick = () => {
            // Find last placed item
            for (let i = placed.length - 1; i >= 0; i--) {
              if (placed[i] !== null) {
                AudioEngine.pop();
                pool.push(placed[i]);
                placed[i] = null;
                redraw();
                break;
              }
            }
          };
        }

        if (btnClr) {
          btnClr.onclick = () => {
            AudioEngine.pop();
            placed.forEach(it => { if (it) pool.push(it); });
            placed = new Array(targetLetters.length).fill(null);
            redraw();
          };
        }

        redraw();

        if (nextBtn) {
          nextBtn.onclick = () => {
            roundIdx++;
            if (roundIdx < totalRounds) {
              renderRound();
            } else {
              onComplete({ score, total: totalRounds });
            }
          };
        }
      }

      renderRound();
    }
  };

  root.Class2Games = Class2Games;
})(typeof window !== 'undefined' ? window : this);
