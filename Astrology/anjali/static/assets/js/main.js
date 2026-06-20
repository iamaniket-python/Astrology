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

// FIX: About image fallback — only run if element exists
const aboutImg = document.querySelector(".about-img");
if (aboutImg) {
  aboutImg.addEventListener("load", function () {
    const fallback = document.getElementById("aboutFallback");
    if (fallback) fallback.style.display = "none";
  });
}

/* ── GALLERY MODAL ── */
// FIX: Use GALLERY_DATA from Django (injected in HTML), fallback to empty array
const galleryItems = (typeof GALLERY_DATA !== "undefined" && GALLERY_DATA.length)
  ? GALLERY_DATA
  : [];

let gCurrent = 0;

function openGallery(idx) {
  if (!galleryItems.length) return;
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
  if (e.target === document.getElementById("galleryModal")) closeGallery();
}
function galleryNav(dir) {
  if (!galleryItems.length) return;
  gCurrent = (gCurrent + dir + galleryItems.length) % galleryItems.length;
  updateGalleryModal();
}
function updateGalleryModal() {
  const item = galleryItems[gCurrent];
  if (!item) return;

  // Show/hide image vs emoji
  const mEmoji = document.getElementById("mEmoji");
  const mImg   = document.getElementById("mImg");
  const mImgEl = document.getElementById("mImgEl");

  if (item.image) {
    mEmoji.textContent = "";
    mImgEl.src = item.image;
    mImgEl.alt = item.title;
    mImg.style.display = "block";
  } else {
    mImg.style.display = "none";
    mEmoji.textContent = item.emoji || "🔮";
  }

  document.getElementById("mTitle").textContent = item.title || "";
  document.getElementById("mCounter").textContent =
    (gCurrent + 1) + " / " + galleryItems.length;
}
document.addEventListener("keydown", (e) => {
  const modal = document.getElementById("galleryModal");
  if (!modal.classList.contains("open")) return;
  if (e.key === "Escape")      closeGallery();
  if (e.key === "ArrowLeft")   galleryNav(-1);
  if (e.key === "ArrowRight")  galleryNav(1);
});

/* ── CAROUSEL ENGINE ── */
const C = {};

function getCardWidth(id) {
  const track = document.getElementById(id + "Track");
  if (!track || !track.children[0]) return 1;
  const card = track.children[0];
  const mr = parseInt(window.getComputedStyle(card).marginRight) || 0;
  return card.offsetWidth + mr;
}

function getVisibleCount(id) {
  const wrap = document.getElementById(id + "Wrap");
  if (!wrap) return 1;
  const cw = getCardWidth(id);
  if (!cw) return 1;
  return Math.max(1, Math.floor(wrap.offsetWidth / cw));
}

function initCarousel(id) {
  const track = document.getElementById(id + "Track");
  const wrap  = document.getElementById(id + "Wrap");
  if (!track || !wrap) return;

  // FIX: count actual children, not hardcoded numbers
  const total = track.children.length;
  if (total === 0) return;

  const vis    = getVisibleCount(id);
  const pages  = Math.max(1, Math.ceil(total / vis));
  const gapPx  = id === "zod" ? 20 : 22;
  const cardW  = (wrap.offsetWidth - gapPx * (vis - 1)) / vis;

  C[id] = { page: 0, vis, total, pages };

  Array.from(track.children).forEach((card) => {
    card.style.width      = cardW + "px";
    card.style.flexShrink = "0";
    card.style.marginRight = gapPx + "px";
  });

  const dotsEl = document.getElementById(id + "Dots");
  if (dotsEl) {
    dotsEl.innerHTML = "";
    for (let i = 0; i < pages; i++) {
      const d = document.createElement("button");
      d.className = "c-dot" + (i === 0 ? " active" : "");
      const pi = i;
      d.onclick = () => goPage(id, pi);
      dotsEl.appendChild(d);
    }
  }
  renderCarousel(id);
}

function renderCarousel(id) {
  if (!C[id]) return;
  const { page, vis } = C[id];
  const cw    = getCardWidth(id);
  const track = document.getElementById(id + "Track");
  if (track) track.style.transform = `translateX(-${page * vis * cw}px)`;

  const dotsEl = document.getElementById(id + "Dots");
  if (dotsEl) {
    Array.from(dotsEl.children).forEach((d, i) =>
      d.classList.toggle("active", i === page)
    );
  }
}

function slide(id, dir) {
  if (!C[id]) return;
  C[id].page = (C[id].page + dir + C[id].pages) % C[id].pages;
  renderCarousel(id);
}

function goPage(id, page) {
  if (!C[id]) return;
  C[id].page = page;
  renderCarousel(id);
}

function setupAll() {
  // FIX: no hardcoded totals — initCarousel counts automatically
  initCarousel("prod");
  initCarousel("zod");
  initCarousel("testi");
}

window.addEventListener("load", setupAll);
let resizeTimer;
window.addEventListener("resize", () => {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(setupAll, 200);
});

// Auto-play every 4s
setInterval(() => {
  if (C["prod"])  slide("prod",  1);
  if (C["zod"])   slide("zod",   1);
  if (C["testi"]) slide("testi", 1);
}, 4000);