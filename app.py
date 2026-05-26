"""
app.py
======
Halaman utama Kalkulator pH.
Berisi: landing page, ringkasan fitur, dan navigasi ke halaman lain.
"""

import streamlit as st

# ── Konfigurasi halaman ────────────────────────────────────────────────────
st.set_page_config(
    page_title="Kalkulator pH",
    page_icon="⚗️",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }
    #MainMenu, footer, header { visibility: hidden; }

    /* ── Hero Section ── */
    .hero {
        text-align: center;
        padding: 3rem 1rem 2rem 1rem;
    }
    .hero-icon {
        font-size: 4rem;
        line-height: 1;
        margin-bottom: 1rem;
    }
    .hero-title {
        font-size: 2.8rem;
        font-weight: 700;
        color: #1a1a2e;
        line-height: 1.15;
        margin-bottom: 0.5rem;
    }
    .hero-title span {
        background: linear-gradient(90deg, #6366f1, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: #6b7280;
        margin-bottom: 2rem;
        line-height: 1.6;
    }

    /* ── Kartu Fitur ── */
    .fitur-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin: 2rem 0;
    }
    .fitur-card {
        border-radius: 16px;
        padding: 1.4rem;
        border: 1.5px solid;
        transition: transform 0.15s;
    }
    .fitur-card:hover { transform: translateY(-2px); }

    .fitur-card.merah  { background:#fff1f2; border-color:#fca5a5; }
    .fitur-card.biru   { background:#eff6ff; border-color:#93c5fd; }
    .fitur-card.hijau  { background:#f0fdf4; border-color:#86efac; }
    .fitur-card.ungu   { background:#f5f3ff; border-color:#c4b5fd; }
    .fitur-card.kuning { background:#fefce8; border-color:#fde047; }

    .fitur-card .fc-icon  { font-size: 1.8rem; margin-bottom: 0.5rem; }
    .fitur-card .fc-judul { font-size: 0.95rem; font-weight: 700; color: #1f2937; margin-bottom: 0.3rem; }
    .fitur-card .fc-desc  { font-size: 0.82rem; color: #4b5563; line-height: 1.5; }

    /* ── Rumus Card ── */
    .rumus-section {
        background: #1a1a2e;
        border-radius: 16px;
        padding: 1.8rem 2rem;
        margin: 1.5rem 0;
        color: #e2e8f0;
        font-family: 'DM Mono', monospace;
        font-size: 0.88rem;
        line-height: 2;
    }
    .rumus-section .rs-title {
        font-family: 'DM Sans', sans-serif;
        font-weight: 700;
        font-size: 1rem;
        color: #a5b4fc;
        margin-bottom: 0.8rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    /* ── pH Scale Bar ── */
    .ph-scale {
        width: 100%;
        height: 28px;
        border-radius: 999px;
        background: linear-gradient(to right,
            #ef4444 0%,
            #f97316 14%,
            #eab308 21%,
            #22c55e 42%,
            #22c55e 58%,
            #3b82f6 72%,
            #6366f1 86%,
            #7c3aed 100%
        );
        margin: 1rem 0 0.3rem 0;
        position: relative;
    }
    .ph-scale-labels {
        display: flex;
        justify-content: space-between;
        font-family: 'DM Mono', monospace;
        font-size: 0.75rem;
        color: #6b7280;
        padding: 0 4px;
    }
    .ph-scale-caption {
        display: flex;
        justify-content: space-between;
        font-size: 0.78rem;
        color: #9ca3af;
        margin-bottom: 1rem;
    }

    /* ── Divider ── */
    .divider { border: none; border-top: 1px solid #e5e7eb; margin: 2rem 0; }

    /* ── Sidebar ── */
    .sidebar-header {
        font-weight: 700;
        font-size: 1rem;
        color: #1a1a2e;
        margin-bottom: 0.5rem;
    }
    .sidebar-desc {
        font-size: 0.82rem;
        color: #6b7280;
        line-height: 1.5;
    }

    /* ── Footer ── */
    .footer {
        text-align: center;
        padding: 1.5rem 0 0.5rem 0;
        font-size: 0.8rem;
        color: #9ca3af;
    }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### ⚗️ Kalkulator pH")
    st.markdown("---")
    st.markdown("**Navigasi Halaman**")
    st.page_link("app.py",              label="🏠 Beranda",          icon=None)
    st.page_link("pages/1_asam_basa.py",label="🔬 Asam & Basa",      icon=None)
    st.page_link("pages/2_hidrolisis.py",label="🧂 Hidrolisis Garam", icon=None)
    st.markdown("---")
    st.markdown("**Referensi Cepat**")
    st.markdown("""
    <div class="sidebar-desc">
    • Kw = 1×10⁻¹⁴ (25°C)<br>
    • pH + pOH = 14<br>
    • pH < 7 → Asam<br>
    • pH = 7 → Netral<br>
    • pH > 7 → Basa
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.caption("📚 Untuk keperluan pembelajaran kimia kelas")


# ═══════════════════════════════════════════════════════
# HERO
# ═══════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
    <div class="hero-icon">⚗️</div>
    <div class="hero-title">Kalkulator <span>pH</span> Interaktif</div>
    <div class="hero-subtitle">
        Hitung pH larutan lengkap dengan reaksi ionisasi,<br>
        tabel ICE, dan langkah perhitungan step-by-step.
    </div>
</div>
""", unsafe_allow_html=True)

# ── Skala pH ──────────────────────────────────────────
st.markdown("**Skala pH (0 – 14)**")
st.markdown('<div class="ph-scale"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="ph-scale-labels">
    <span>0</span><span>1</span><span>2</span><span>3</span><span>4</span>
    <span>5</span><span>6</span><span>7</span><span>8</span><span>9</span>
    <span>10</span><span>11</span><span>12</span><span>13</span><span>14</span>
</div>
<div class="ph-scale-caption">
    <span>← Sangat Asam</span>
    <span>Netral</span>
    <span>Sangat Basa →</span>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# KARTU FITUR
# ═══════════════════════════════════════════════════════
st.markdown("#### 🗂️ Fitur yang Tersedia")

st.markdown("""
<div class="fitur-grid">
    <div class="fitur-card merah">
        <div class="fc-icon">🔴</div>
        <div class="fc-judul">Asam Kuat</div>
        <div class="fc-desc">Ionisasi sempurna (α = 1).<br>
        Contoh: HCl, HNO₃, H₂SO₄.<br>
        Rumus: [H⁺] = C</div>
    </div>
    <div class="fitur-card biru">
        <div class="fc-icon">🟠</div>
        <div class="fc-judul">Asam Lemah</div>
        <div class="fc-desc">Ionisasi sebagian + tabel ICE.<br>
        Contoh: CH₃COOH, HF, HCN.<br>
        Rumus: [H⁺] = √(Ka × C)</div>
    </div>
    <div class="fitur-card hijau">
        <div class="fc-icon">🔵</div>
        <div class="fc-judul">Basa Kuat</div>
        <div class="fc-desc">Ionisasi sempurna (α = 1).<br>
        Contoh: NaOH, KOH, Ca(OH)₂.<br>
        Rumus: [OH⁻] = C</div>
    </div>
    <div class="fitur-card ungu">
        <div class="fc-icon">🟣</div>
        <div class="fc-judul">Basa Lemah</div>
        <div class="fc-desc">Ionisasi sebagian + tabel ICE.<br>
        Contoh: NH₃, C₅H₅N.<br>
        Rumus: [OH⁻] = √(Kb × C)</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Kartu hidrolisis (full width)
st.markdown("""
<div class="fitur-card kuning" style="margin-top:0;">
    <div class="fc-icon">🧂</div>
    <div class="fc-judul">Hidrolisis Garam (Fitur Tambahan)</div>
    <div class="fc-desc">
        4 jenis garam: AK+BK (netral) · AL+BK (basa) · AK+BL (asam) · AL+BL (Ka vs Kb).<br>
        Menampilkan Kh, tabel ICE, pKa, pKb, dan langkah perhitungan lengkap.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# RINGKASAN RUMUS
# ═══════════════════════════════════════════════════════
st.markdown("#### 📐 Ringkasan Rumus")

st.markdown("""
<div class="rumus-section">
    <div class="rs-title">Asam & Basa</div>
    Asam Kuat   →  [H⁺] = C                    →  pH = −log[H⁺]<br>
    Asam Lemah  →  [H⁺] = √(Ka × C)            →  pH = −log[H⁺]<br>
    Basa Kuat   →  [OH⁻] = C                   →  pOH = −log[OH⁻]  →  pH = 14 − pOH<br>
    Basa Lemah  →  [OH⁻] = √(Kb × C)           →  pOH = −log[OH⁻]  →  pH = 14 − pOH
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="rumus-section">
    <div class="rs-title">Hidrolisis Garam</div>
    AK + BK  →  pH = 7  (tidak terhidrolisis)<br>
    AL + BK  →  Kh = Kw/Ka  ;  [OH⁻] = √(Kh × C)  ;  pH = 14 − pOH<br>
    AK + BL  →  Kh = Kw/Kb  ;  [H⁺]  = √(Kh × C)  ;  pH = −log[H⁺]<br>
    AL + BL  →  pH = 7 + ½(pKa − pKb)
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# TOMBOL NAVIGASI
# ═══════════════════════════════════════════════════════
st.markdown("#### 🚀 Mulai Hitung")

col1, col2 = st.columns(2)
with col1:
    st.page_link(
        "pages/1_asam_basa.py",
        label="🔬 Buka Kalkulator Asam & Basa",
        use_container_width=True,
    )
with col2:
    st.page_link(
        "pages/2_hidrolisis.py",
        label="🧂 Buka Kalkulator Hidrolisis",
        use_container_width=True,
    )

# ── Footer ─────────────────────────────────────────────
st.markdown("""
<div class="footer">
    ⚗️ Kalkulator pH Interaktif &nbsp;|&nbsp; Suhu referensi 25°C &nbsp;|&nbsp;
    Dibuat dengan Streamlit &nbsp;|&nbsp; Untuk keperluan pembelajaran kimia
</div>
""", unsafe_allow_html=True)
