 AOS.init({ duration: 700, once: true, offset: 60 });

      /* ── THEME ── */
      function toggleNav() {
        document.getElementById("navLinks").classList.toggle("open");
      }
      function toggleTheme() {
        const body = document.body,
          btn = document.getElementById("themeBtn");
        body.classList.toggle("light");
        const isLight = body.classList.contains("light");
        btn.textContent = isLight ? "🌑" : "🌙";
        localStorage.setItem("theme", isLight ? "light" : "dark");
      }
      if (localStorage.getItem("theme") === "light") {
        document.body.classList.add("light");
        document.getElementById("themeBtn").textContent = "🌑";
      }

      // Fix about image fallback
      document
        .querySelector(".about-img")
        .addEventListener("load", function () {
          document.getElementById("aboutFallback").style.display = "none";
        });

      /* ── GALLERY MODAL ── */
      const galleryItems = [
        { emoji: "🔮", title: "Cosmic Consultation Space" },
        { emoji: "🌙", title: "Night Sky Readings" },
        { emoji: "💎", title: "Gemstone Collection" },
        { emoji: "✨", title: "Vedic Chart Reading" },
        { emoji: "🌿", title: "Sacred Yantra Ceremony" },
        { emoji: "🕯️", title: "Navgrah Pooja Ceremony" },
        { emoji: "⭐", title: "Astrology Class Session" },
        { emoji: "📿", title: "Rudraksha & Sacred Items" },
      ];
      let gCurrent = 0;

      function openGallery(idx) {
        gCurrent = idx;
        updateGalleryModal();
        document.getElementById("galleryModal").classList.add("open");
        document.body.style.overflow = "hidden";
      }
      function closeGallery() {
        document.getElementById("galleryModal").classList.remove("open");
        document.body.style.overflow = "";
      }
      function handleModalClick(e) {
        if (e.target === document.getElementById("galleryModal"))
          closeGallery();
      }
      function galleryNav(dir) {
        gCurrent = (gCurrent + dir + galleryItems.length) % galleryItems.length;
        updateGalleryModal();
      }
      function updateGalleryModal() {
        document.getElementById("mEmoji").textContent =
          galleryItems[gCurrent].emoji;
        document.getElementById("mTitle").textContent =
          galleryItems[gCurrent].title;
        document.getElementById("mCounter").textContent =
          gCurrent + 1 + " / " + galleryItems.length;
      }
      document.addEventListener("keydown", (e) => {
        const modal = document.getElementById("galleryModal");
        if (!modal.classList.contains("open")) return;
        if (e.key === "Escape") closeGallery();
        if (e.key === "ArrowLeft") galleryNav(-1);
        if (e.key === "ArrowRight") galleryNav(1);
      });

      /* ── CAROUSEL ENGINE ── */
      const C = {}; // state store

      function getCardWidth(id) {
        const track = document.getElementById(id + "Track");
        const card = track.children[0];
        if (!card) return 1;
        const mr = parseInt(window.getComputedStyle(card).marginRight) || 0;
        return card.offsetWidth + mr;
      }

      function getVisibleCount(id) {
        const wrap = document.getElementById(id + "Wrap");
        const cw = getCardWidth(id);
        if (!cw) return 1;
        return Math.max(1, Math.floor(wrap.offsetWidth / cw));
      }

      function initCarousel(id, total) {
        const vis = getVisibleCount(id);
        const pages = Math.max(1, Math.ceil(total / vis));
        C[id] = { page: 0, vis, total, pages };

        // Set card widths
        const track = document.getElementById(id + "Track");
        const wrap = document.getElementById(id + "Wrap");
        const gapPx = id === "zod" ? 20 : 22;
        const cardW = (wrap.offsetWidth - gapPx * (vis - 1)) / vis;
        Array.from(track.children).forEach((card) => {
          card.style.width = cardW + "px";
          card.style.flexShrink = "0";
          card.style.marginRight = gapPx + "px";
        });

        // Dots
        const dotsEl = document.getElementById(id + "Dots");
        dotsEl.innerHTML = "";
        for (let i = 0; i < pages; i++) {
          const d = document.createElement("button");
          d.className = "c-dot" + (i === 0 ? " active" : "");
          const pi = i;
          d.onclick = () => goPage(id, pi);
          dotsEl.appendChild(d);
        }
        renderCarousel(id);
      }

      function renderCarousel(id) {
        const { page } = C[id];
        const cw = getCardWidth(id);
        const track = document.getElementById(id + "Track");
        const vis = C[id].vis;
        track.style.transform = `translateX(-${page * vis * cw}px)`;
        const dots = document.getElementById(id + "Dots").children;
        for (let i = 0; i < dots.length; i++)
          dots[i].classList.toggle("active", i === page);
      }

      function slide(id, dir) {
        C[id].page = (C[id].page + dir + C[id].pages) % C[id].pages;
        renderCarousel(id);
      }

      function goPage(id, page) {
        C[id].page = page;
        renderCarousel(id);
      }

      function setupAll() {
        initCarousel("prod", 8);
        initCarousel("zod", 12);
        initCarousel("testi", 6);
      }

      window.addEventListener("load", setupAll);
      let resizeTimer;
      window.addEventListener("resize", () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(setupAll, 200);
      });

      // Auto-play every 4s
      setInterval(() => {
        if (C["prod"]) slide("prod", 1);
        if (C["zod"]) slide("zod", 1);
        if (C["testi"]) slide("testi", 1);
      }, 4000);
