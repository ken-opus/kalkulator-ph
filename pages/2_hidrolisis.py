"""
pages/2_hidrolisis.py
=====================
Halaman kalkulator pH Hidrolisis Garam.
Menampilkan: jenis garam, reaksi hidrolisis, tabel ICE (jika ada),
langkah perhitungan Kh, dan hasil pH.
"""

import streamlit as st
import sys
import os

# ── Pastikan utils/ bisa diimport ──────────────────────────────────────────
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.ph_calculator import (
    hitung_hidrolisis_garam,
    format_angka,
)

# ── Konfigurasi halaman ────────────────────────────────────────────────────
st.set_page_config(
    page_title="Kalkulator pH — Hidrolisis Garam",
    page_icon="🧂",
    layout="centered",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }
    #MainMenu, footer, header {visibility: hidden;}

    .page-title {
        font-size: 2rem;
        font-weight: 700;
        color: #1a1a2e;
        margin-bottom: 0.2rem;
    }
    .page-subtitle {
        font-size: 0.95rem;
        color: #6b7280;
        margin-bottom: 2rem;
    }

    /* Kartu pH */
    .ph-card { border-radius: 16px; padding: 2rem; text-align: center; margin: 1.5rem 0; }
    .ph-card.asam   { background: linear-gradient(135deg,#fff1f2,#ffe4e6); border: 2px solid #fca5a5; }
    .ph-card.basa   { background: linear-gradient(135deg,#eff6ff,#dbeafe); border: 2px solid #93c5fd; }
    .ph-card.netral { background: linear-gradient(135deg,#f0fdf4,#dcfce7); border: 2px solid #86efac; }
    .ph-value { font-size: 3.5rem; font-weight: 700; font-family:'DM Mono',monospace; line-height:1; }
    .ph-value.asam   { color: #dc2626; }
    .ph-value.basa   { color: #2563eb; }
    .ph-value.netral { color: #16a34a; }
    .ph-label { font-size:1rem; font-weight:600; margin-top:0.5rem; letter-spacing:0.05em; text-transform:uppercase; }
    .ph-label.asam   { color:#b91c1c; }
    .ph-label.basa   { color:#1d4ed8; }
    .ph-label.netral { color:#15803d; }

    /* Ion box */
    .ion-box {
        background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px;
        padding:1rem 1.5rem; font-family:'DM Mono',monospace;
        font-size:0.9rem; color:#334155; margin:0.5rem 0;
    }

    /* Tabel ICE */
    .ice-table { width:100%; border-collapse:collapse; font-family:'DM Mono',monospace;
        font-size:0.88rem; margin:1rem 0; border-radius:12px; overflow:hidden; }
    .ice-table th { background:#1a1a2e; color:#f1f5f9; padding:10px 16px; text-align:center; font-weight:600; }
    .ice-table td { padding:9px 16px; text-align:center; border-bottom:1px solid #e5e7eb; color:#374151; }
    .ice-table tr:nth-child(even) td { background:#f8fafc; }
    .ice-table tr:hover td { background:#eff6ff; }
    .ice-table td:first-child { font-weight:600; color:#4f46e5; text-align:left; background:#f5f3ff; }

    /* Info card jenis garam */
    .jenis-card {
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid;
    }
    .jenis-card.ak-bk  { background:#f0fdf4; border-color:#22c55e; }
    .jenis-card.al-bk  { background:#eff6ff; border-color:#3b82f6; }
    .jenis-card.ak-bl  { background:#fff1f2; border-color:#ef4444; }
    .jenis-card.al-bl  { background:#fefce8; border-color:#eab308; }
    .jenis-card h4     { margin:0 0 0.4rem 0; font-size:0.95rem; font-weight:700; }
    .jenis-card p      { margin:0; font-size:0.85rem; color:#4b5563; }

    /* Rumus box */
    .rumus-box {
        background: #1a1a2e; color: #e2e8f0;
        border-radius: 12px; padding: 1.2rem 1.8rem;
        font-family: 'DM Mono', monospace; font-size: 0.9rem;
        margin: 1rem 0; line-height: 1.9;
    }

    .divider { border:none; border-top:1px solid #e5e7eb; margin:1.5rem 0; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# FUNGSI HELPER TAMPILAN
# ═══════════════════════════════════════════════════════

def tampilkan_kartu_ph(pH, pOH, H_plus, OH_minus, label):
    cls = label.lower()
    emoji = "🔴" if cls == "asam" else "🔵" if cls == "basa" else "🟢"
    st.markdown(f"""
    <div class="ph-card {cls}">
        <div class="ph-value {cls}">{pH:.2f}</div>
        <div class="ph-label {cls}">{emoji} Larutan {label}</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="ion-box">pOH = <b>{pOH:.2f}</b></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="ion-box">[H⁺] = <b>{format_angka(H_plus)} M</b></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="ion-box">[OH⁻] = <b>{format_angka(OH_minus)} M</b></div>', unsafe_allow_html=True)


def tampilkan_ice(ice):
    if ice is None:
        return
    header = ice["header"]
    rows = {k: v for k, v in ice.items() if k != "header"}
    header_html = "".join(f"<th>{h}</th>" for h in ["", *header])
    rows_html = ""
    for nama_row, nilai_row in rows.items():
        cells = "".join(f"<td>{v}</td>" for v in nilai_row)
        rows_html += f"<tr><td>{nama_row}</td>{cells}</tr>"
    st.markdown(f"""
    <table class="ice-table">
        <thead><tr>{header_html}</tr></thead>
        <tbody>{rows_html}</tbody>
    </table>
    """, unsafe_allow_html=True)


def tampilkan_steps(steps):
    for step in steps:
        if step.startswith("**"):
            st.markdown(step)
        elif step == "":
            st.write("")
        else:
            st.code(step.strip(), language=None)


# ═══════════════════════════════════════════════════════
# DATA CONTOH GARAM
# ═══════════════════════════════════════════════════════

CONTOH_GARAM = {
    "ak_bk": [
        {"nama": "NaCl (Natrium Klorida)",        "simbol": "NaCl",    "Ka": None, "Kb": None},
        {"nama": "KNO₃ (Kalium Nitrat)",           "simbol": "KNO₃",   "Ka": None, "Kb": None},
        {"nama": "BaSO₄ (Barium Sulfat)",          "simbol": "BaSO₄",  "Ka": None, "Kb": None},
        {"nama": "Lainnya (ketik sendiri)",         "simbol": "",        "Ka": None, "Kb": None},
    ],
    "al_bk": [
        {"nama": "CH₃COONa (Natrium Asetat)  — Ka CH₃COOH = 1.8×10⁻⁵", "simbol": "CH₃COONa", "Ka": 1.8e-5, "Kb": None},
        {"nama": "NaCN (Natrium Sianida)      — Ka HCN = 4.9×10⁻¹⁰",    "simbol": "NaCN",     "Ka": 4.9e-10,"Kb": None},
        {"nama": "NaF (Natrium Fluorida)      — Ka HF = 6.8×10⁻⁴",      "simbol": "NaF",      "Ka": 6.8e-4, "Kb": None},
        {"nama": "HCOOK (Kalium Format)       — Ka HCOOH = 1.8×10⁻⁴",   "simbol": "HCOOK",    "Ka": 1.8e-4, "Kb": None},
        {"nama": "Lainnya (ketik sendiri)",                                "simbol": "",         "Ka": None,   "Kb": None},
    ],
    "ak_bl": [
        {"nama": "NH₄Cl (Amonium Klorida)     — Kb NH₃ = 1.8×10⁻⁵",    "simbol": "NH₄Cl",   "Ka": None, "Kb": 1.8e-5},
        {"nama": "NH₄NO₃ (Amonium Nitrat)     — Kb NH₃ = 1.8×10⁻⁵",    "simbol": "NH₄NO₃",  "Ka": None, "Kb": 1.8e-5},
        {"nama": "C₅H₅NHCl (Piridinuim Kl.)  — Kb C₅H₅N = 1.7×10⁻⁹",  "simbol": "C₅H₅NHCl","Ka": None, "Kb": 1.7e-9},
        {"nama": "Lainnya (ketik sendiri)",                                "simbol": "",        "Ka": None, "Kb": None},
    ],
    "al_bl": [
        {"nama": "CH₃COONH₄ (Amonium Asetat) — Ka=1.8×10⁻⁵, Kb=1.8×10⁻⁵", "simbol": "CH₃COONH₄","Ka": 1.8e-5,"Kb": 1.8e-5},
        {"nama": "NH₄CN (Amonium Sianida)    — Ka=4.9×10⁻¹⁰, Kb=1.8×10⁻⁵", "simbol": "NH₄CN",    "Ka": 4.9e-10,"Kb":1.8e-5},
        {"nama": "Lainnya (ketik sendiri)",                                    "simbol": "",          "Ka": None,   "Kb": None},
    ],
}

# Mapping jenis ke info kartu
INFO_JENIS = {
    "ak_bk": {
        "css": "ak-bk",
        "judul": "⚪ Asam Kuat + Basa Kuat → Netral",
        "penjelasan": "Kedua ion hasil disosiasi tidak bereaksi dengan air. Larutan bersifat netral (pH = 7). Tidak terjadi hidrolisis.",
        "contoh": "NaCl, KNO₃, BaSO₄",
    },
    "al_bk": {
        "css": "al-bk",
        "judul": "🔵 Asam Lemah + Basa Kuat → Basa",
        "penjelasan": "Anion dari asam lemah terhidrolisis menghasilkan OH⁻. Kh = Kw / Ka. Larutan bersifat basa (pH > 7).",
        "contoh": "CH₃COONa, NaCN, NaF",
    },
    "ak_bl": {
        "css": "ak-bl",
        "judul": "🔴 Asam Kuat + Basa Lemah → Asam",
        "penjelasan": "Kation dari basa lemah terhidrolisis menghasilkan H⁺. Kh = Kw / Kb. Larutan bersifat asam (pH < 7).",
        "contoh": "NH₄Cl, NH₄NO₃",
    },
    "al_bl": {
        "css": "al-bl",
        "judul": "🟡 Asam Lemah + Basa Lemah → Bergantung Ka vs Kb",
        "penjelasan": "Kedua ion terhidrolisis. pH = 7 + ½(pKa − pKb). Jika Ka > Kb → asam; Ka < Kb → basa; Ka = Kb → netral.",
        "contoh": "CH₃COONH₄, NH₄CN",
    },
}


# ═══════════════════════════════════════════════════════
# LAYOUT UTAMA
# ═══════════════════════════════════════════════════════

st.markdown('<div class="page-title">🧂 Hidrolisis Garam</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Kalkulator pH berdasarkan jenis garam yang terbentuk</div>', unsafe_allow_html=True)

# ── Panduan singkat ────────────────────────────────────
with st.expander("📖 Panduan Singkat — Cara Menentukan Jenis Garam"):
    st.markdown("""
    | Asam Pembentuk | Basa Pembentuk | Jenis Garam | Sifat Larutan |
    |---|---|---|---|
    | Asam Kuat (HCl, HNO₃...) | Basa Kuat (NaOH, KOH...) | AK + BK | Netral (pH = 7) |
    | Asam Lemah (CH₃COOH...) | Basa Kuat (NaOH, KOH...) | AL + BK | **Basa** (pH > 7) |
    | Asam Kuat (HCl, HNO₃...) | Basa Lemah (NH₃...) | AK + BL | **Asam** (pH < 7) |
    | Asam Lemah (CH₃COOH...) | Basa Lemah (NH₃...) | AL + BL | Tergantung Ka vs Kb |

    **Rumus penting:**
    - AL + BK → `Kh = Kw/Ka` ; `[OH⁻] = √(Kh × C)` ; `pH = 14 − pOH`
    - AK + BL → `Kh = Kw/Kb` ; `[H⁺] = √(Kh × C)` ; `pH = −log[H⁺]`
    - AL + BL → `pH = 7 + ½(pKa − pKb)`
    """)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Pilih jenis garam ──────────────────────────────────
st.markdown("#### Langkah 1 — Pilih Jenis Garam")

jenis_label = {
    "ak_bk": "⚪  Asam Kuat + Basa Kuat (Netral)",
    "al_bk": "🔵  Asam Lemah + Basa Kuat (Basa)",
    "ak_bl": "🔴  Asam Kuat + Basa Lemah (Asam)",
    "al_bl": "🟡  Asam Lemah + Basa Lemah (Bergantung Ka & Kb)",
}

jenis_pilih = st.radio(
    "Jenis garam:",
    options=list(jenis_label.keys()),
    format_func=lambda k: jenis_label[k],
    horizontal=False,
    key="jenis_garam",
)

# Tampilkan info card jenis garam
info = INFO_JENIS[jenis_pilih]
st.markdown(f"""
<div class="jenis-card {info['css']}">
    <h4>{info['judul']}</h4>
    <p>{info['penjelasan']}</p>
    <p style="margin-top:0.4rem"><b>Contoh:</b> {info['contoh']}</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Input zat & konsentrasi ────────────────────────────
st.markdown("#### Langkah 2 — Pilih Garam & Masukkan Data")

daftar_contoh = CONTOH_GARAM[jenis_pilih]
nama_pilihan  = [g["nama"] for g in daftar_contoh]

pilih_garam = st.selectbox("Pilih contoh garam:", nama_pilihan, key="pilih_garam")
data_garam  = next(g for g in daftar_contoh if g["nama"] == pilih_garam)
is_manual   = (data_garam["simbol"] == "")

# Input nama garam
if is_manual:
    nama_garam = st.text_input("Nama / rumus kimia garam:", value="Garam", key="nama_garam_input")
else:
    nama_garam = data_garam["simbol"]
    st.info(f"Garam terpilih: **{nama_garam}**")

# Konsentrasi
konsentrasi = st.number_input(
    "Konsentrasi garam (M):",
    min_value=1e-10, max_value=10.0,
    value=0.1, format="%.6f", key="konsentrasi_garam"
)

# Input Ka / Kb berdasarkan jenis
Ka_input = None
Kb_input = None

if jenis_pilih == "al_bk":
    if is_manual or data_garam["Ka"] is None:
        Ka_input = st.number_input(
            "Nilai Ka asam lemah pembentuk:",
            min_value=1e-14, max_value=1.0,
            value=1.8e-5, format="%.2e", key="ka_manual"
        )
    else:
        Ka_input = data_garam["Ka"]
        st.markdown(f"""
        <div class="rumus-box">
          Ka asam lemah pembentuk  =  {Ka_input:.2e}<br>
          Kh = Kw / Ka  =  1×10⁻¹⁴ / {Ka_input:.2e}  =  {1e-14/Ka_input:.4e}
        </div>
        """, unsafe_allow_html=True)

elif jenis_pilih == "ak_bl":
    if is_manual or data_garam["Kb"] is None:
        Kb_input = st.number_input(
            "Nilai Kb basa lemah pembentuk:",
            min_value=1e-14, max_value=1.0,
            value=1.8e-5, format="%.2e", key="kb_manual"
        )
    else:
        Kb_input = data_garam["Kb"]
        st.markdown(f"""
        <div class="rumus-box">
          Kb basa lemah pembentuk  =  {Kb_input:.2e}<br>
          Kh = Kw / Kb  =  1×10⁻¹⁴ / {Kb_input:.2e}  =  {1e-14/Kb_input:.4e}
        </div>
        """, unsafe_allow_html=True)

elif jenis_pilih == "al_bl":
    col_ka, col_kb = st.columns(2)
    with col_ka:
        if is_manual or data_garam["Ka"] is None:
            Ka_input = st.number_input(
                "Nilai Ka asam lemah:",
                min_value=1e-14, max_value=1.0,
                value=1.8e-5, format="%.2e", key="ka_albl"
            )
        else:
            Ka_input = data_garam["Ka"]
            st.metric("Ka asam lemah", f"{Ka_input:.2e}")
    with col_kb:
        if is_manual or data_garam["Kb"] is None:
            Kb_input = st.number_input(
                "Nilai Kb basa lemah:",
                min_value=1e-14, max_value=1.0,
                value=1.8e-5, format="%.2e", key="kb_albl"
            )
        else:
            Kb_input = data_garam["Kb"]
            st.metric("Kb basa lemah", f"{Kb_input:.2e}")

    # Preview perbandingan Ka vs Kb
    if Ka_input and Kb_input:
        if Ka_input > Kb_input:
            st.warning(f"Ka ({Ka_input:.2e}) > Kb ({Kb_input:.2e}) → Larutan diprediksi **Asam**")
        elif Ka_input < Kb_input:
            st.info(f"Kb ({Kb_input:.2e}) > Ka ({Ka_input:.2e}) → Larutan diprediksi **Basa**")
        else:
            st.success("Ka = Kb → Larutan diprediksi **Netral**")

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Tombol Hitung ──────────────────────────────────────
if st.button("🔬 Hitung pH Hidrolisis", type="primary", use_container_width=True, key="hitung_hidrolisis"):
    try:
        hasil = hitung_hidrolisis_garam(
            nama_garam  = nama_garam,
            konsentrasi = konsentrasi,
            jenis       = jenis_pilih,
            Ka          = Ka_input,
            Kb          = Kb_input,
        )
        r = hasil["result"]

        st.markdown("---")
        st.markdown("#### 📋 Hasil Perhitungan")

        # ── Kartu pH ──────────────────────────────
        tampilkan_kartu_ph(r["pH"], r["pOH"], r["H_plus"], r["OH_minus"], r["label"])

        # ── Kh (jika ada) ─────────────────────────
        if r.get("Kh") is not None:
            st.markdown('<hr class="divider">', unsafe_allow_html=True)
            st.markdown("**⚖️ Konstanta Hidrolisis (Kh)**")
            col_kh1, col_kh2 = st.columns(2)
            with col_kh1:
                st.markdown(
                    f'<div class="ion-box">Kh = <b>{format_angka(r["Kh"])}</b></div>',
                    unsafe_allow_html=True
                )
            with col_kh2:
                rumus_kh = "Kw / Ka" if jenis_pilih == "al_bk" else "Kw / Kb"
                st.markdown(
                    f'<div class="ion-box">Rumus: Kh = <b>{rumus_kh}</b></div>',
                    unsafe_allow_html=True
                )

        # ── pKa & pKb (untuk AL+BL) ───────────────
        if r.get("pKa") is not None:
            st.markdown('<hr class="divider">', unsafe_allow_html=True)
            st.markdown("**📊 Nilai pKa & pKb**")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("pKa", f"{r['pKa']:.4f}")
            with c2:
                st.metric("pKb", f"{r['pKb']:.4f}")
            with c3:
                st.metric("pKa − pKb", f"{r['pKa'] - r['pKb']:.4f}")

        # ── Tabel ICE ─────────────────────────────
        if hasil["ice"] is not None:
            st.markdown('<hr class="divider">', unsafe_allow_html=True)
            st.markdown("**🧊 Tabel ICE (Initial – Change – Equilibrium)**")
            tampilkan_ice(hasil["ice"])

        # ── Langkah perhitungan ───────────────────
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown("**📐 Langkah-langkah Perhitungan**")
        tampilkan_steps(hasil["steps"])

    except ValueError as e:
        st.error(f"❌ Input tidak valid: {e}")
    except Exception as e:
        st.error(f"❌ Terjadi kesalahan: {e}")

# ── Footer ─────────────────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.caption("🧪 Kalkulator pH — Hidrolisis Garam | Suhu referensi 25°C | Kw = 1×10⁻¹⁴")
