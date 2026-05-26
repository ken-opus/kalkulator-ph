"""
pages/1_asam_basa.py
====================
Halaman kalkulator pH untuk Asam Kuat, Asam Lemah, Basa Kuat, Basa Lemah.
Menampilkan: reaksi ionisasi, tabel ICE, langkah perhitungan, dan hasil pH.
"""

import streamlit as st
import sys
import os

# ── Pastikan utils/ bisa diimport ──────────────────────────────────────────
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.ph_calculator import (
    hitung_asam_kuat,
    hitung_asam_lemah,
    hitung_basa_kuat,
    hitung_basa_lemah,
    format_angka,
)

# ── Konfigurasi halaman ────────────────────────────────────────────────────
st.set_page_config(
    page_title="Kalkulator pH — Asam & Basa",
    page_icon="⚗️",
    layout="centered",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Import font */
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    /* Sembunyikan default header streamlit */
    #MainMenu, footer, header {visibility: hidden;}

    /* Judul halaman */
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

    /* Kartu hasil pH besar */
    .ph-card {
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        margin: 1.5rem 0;
    }
    .ph-card.asam {
        background: linear-gradient(135deg, #fff1f2, #ffe4e6);
        border: 2px solid #fca5a5;
    }
    .ph-card.basa {
        background: linear-gradient(135deg, #eff6ff, #dbeafe);
        border: 2px solid #93c5fd;
    }
    .ph-card.netral {
        background: linear-gradient(135deg, #f0fdf4, #dcfce7);
        border: 2px solid #86efac;
    }
    .ph-value {
        font-size: 3.5rem;
        font-weight: 700;
        font-family: 'DM Mono', monospace;
        line-height: 1;
    }
    .ph-value.asam  { color: #dc2626; }
    .ph-value.basa  { color: #2563eb; }
    .ph-value.netral { color: #16a34a; }
    .ph-label {
        font-size: 1rem;
        font-weight: 600;
        margin-top: 0.5rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    .ph-label.asam   { color: #b91c1c; }
    .ph-label.basa   { color: #1d4ed8; }
    .ph-label.netral { color: #15803d; }

    /* Info box ion */
    .ion-box {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        font-family: 'DM Mono', monospace;
        font-size: 0.9rem;
        color: #334155;
        margin: 0.5rem 0;
    }

    /* Kotak reaksi */
    .reaksi-box {
        background: #1a1a2e;
        color: #e2e8f0;
        border-radius: 12px;
        padding: 1.2rem 1.8rem;
        font-family: 'DM Mono', monospace;
        font-size: 1rem;
        margin: 1rem 0;
        letter-spacing: 0.03em;
    }

    /* Step perhitungan */
    .step-box {
        background: #fafafa;
        border-left: 4px solid #6366f1;
        border-radius: 0 12px 12px 0;
        padding: 1.2rem 1.5rem;
        font-family: 'DM Mono', monospace;
        font-size: 0.85rem;
        color: #374151;
        line-height: 1.8;
        white-space: pre-wrap;
        margin: 1rem 0;
    }

    /* Tabel ICE */
    .ice-table {
        width: 100%;
        border-collapse: collapse;
        font-family: 'DM Mono', monospace;
        font-size: 0.88rem;
        margin: 1rem 0;
        border-radius: 12px;
        overflow: hidden;
    }
    .ice-table th {
        background: #1a1a2e;
        color: #f1f5f9;
        padding: 10px 16px;
        text-align: center;
        font-weight: 600;
    }
    .ice-table td {
        padding: 9px 16px;
        text-align: center;
        border-bottom: 1px solid #e5e7eb;
        color: #374151;
    }
    .ice-table tr:nth-child(even) td { background: #f8fafc; }
    .ice-table tr:hover td { background: #eff6ff; }
    .ice-table td:first-child {
        font-weight: 600;
        color: #4f46e5;
        text-align: left;
        background: #f5f3ff;
    }

    /* Badge jenis */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }
    .badge-asam   { background: #fee2e2; color: #b91c1c; }
    .badge-basa   { background: #dbeafe; color: #1d4ed8; }

    /* Divider */
    .divider {
        border: none;
        border-top: 1px solid #e5e7eb;
        margin: 1.5rem 0;
    }

    /* Catatan persen ionisasi */
    .catatan-valid   { color: #15803d; font-size: 0.85rem; }
    .catatan-invalid { color: #b45309; font-size: 0.85rem; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# FUNGSI HELPER TAMPILAN
# ═══════════════════════════════════════════════════════

def tampilkan_kartu_ph(pH: float, pOH: float, H_plus: float, OH_minus: float, label: str):
    """Tampilkan kartu besar hasil pH."""
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


def tampilkan_ice(ice: dict):
    """Render tabel ICE sebagai HTML table."""
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


def tampilkan_steps(steps: list):
    """Tampilkan langkah-langkah perhitungan."""
    teks = "\n".join(steps)
    # Render markdown bold (**teks**) tetap bekerja di dalam st.markdown
    st.markdown(f'<div class="step-box">{teks}</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# DAFTAR CONTOH ZAT (untuk dropdown)
# ═══════════════════════════════════════════════════════

ASAM_KUAT_LIST = {
    "HCl (Asam Klorida)":     {"simbol": "HCl"},
    "HBr (Asam Bromida)":     {"simbol": "HBr"},
    "HI (Asam Iodida)":       {"simbol": "HI"},
    "HNO₃ (Asam Nitrat)":     {"simbol": "HNO₃"},
    "H₂SO₄ (Asam Sulfat)":    {"simbol": "H₂SO₄"},
    "HClO₄ (Asam Perklorat)": {"simbol": "HClO₄"},
    "Lainnya (ketik sendiri)": {"simbol": ""},
}

ASAM_LEMAH_LIST = {
    "CH₃COOH (Asam Asetat)  — Ka = 1.8×10⁻⁵":  {"simbol": "CH₃COOH", "Ka": 1.8e-5},
    "HF (Asam Fluorida)     — Ka = 6.8×10⁻⁴":   {"simbol": "HF",       "Ka": 6.8e-4},
    "HCN (Asam Sianida)     — Ka = 4.9×10⁻¹⁰":  {"simbol": "HCN",      "Ka": 4.9e-10},
    "H₂CO₃ (Asam Karbonat)  — Ka = 4.3×10⁻⁷":   {"simbol": "H₂CO₃",   "Ka": 4.3e-7},
    "HCOOH (Asam Format)    — Ka = 1.8×10⁻⁴":   {"simbol": "HCOOH",    "Ka": 1.8e-4},
    "Lainnya (ketik sendiri)":                     {"simbol": "",          "Ka": None},
}

BASA_KUAT_LIST = {
    "NaOH (Natrium Hidroksida)":  {"simbol": "NaOH"},
    "KOH (Kalium Hidroksida)":    {"simbol": "KOH"},
    "Ca(OH)₂ (Kalsium Hidroksida)": {"simbol": "Ca(OH)₂"},
    "LiOH (Litium Hidroksida)":   {"simbol": "LiOH"},
    "Ba(OH)₂ (Barium Hidroksida)": {"simbol": "Ba(OH)₂"},
    "Lainnya (ketik sendiri)":    {"simbol": ""},
}

BASA_LEMAH_LIST = {
    "NH₃ (Amonia)           — Kb = 1.8×10⁻⁵":   {"simbol": "NH₃",     "Kb": 1.8e-5},
    "C₅H₅N (Piridin)        — Kb = 1.7×10⁻⁹":   {"simbol": "C₅H₅N",  "Kb": 1.7e-9},
    "C₆H₅NH₂ (Anilin)       — Kb = 4.3×10⁻¹⁰":  {"simbol": "C₆H₅NH₂","Kb": 4.3e-10},
    "N₂H₄ (Hidrazin)        — Kb = 9.6×10⁻⁷":   {"simbol": "N₂H₄",   "Kb": 9.6e-7},
    "Lainnya (ketik sendiri)":                     {"simbol": "",         "Kb": None},
}


# ═══════════════════════════════════════════════════════
# LAYOUT UTAMA
# ═══════════════════════════════════════════════════════

st.markdown('<div class="page-title">⚗️ Kalkulator pH</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Asam Kuat · Asam Lemah · Basa Kuat · Basa Lemah</div>', unsafe_allow_html=True)

# ── Pilih kategori ─────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["🔴 Asam Kuat", "🟠 Asam Lemah", "🔵 Basa Kuat", "🟣 Basa Lemah"])


# ════════════════════════════════════════
# TAB 1 — ASAM KUAT
# ════════════════════════════════════════
with tab1:
    st.markdown("##### Asam Kuat — Ionisasi Sempurna (α = 1)")
    st.caption("Contoh: HCl, HBr, HNO₃, H₂SO₄, HClO₄")
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    pilihan_ak = st.selectbox("Pilih asam kuat:", list(ASAM_KUAT_LIST.keys()), key="ak_pilih")
    info_ak = ASAM_KUAT_LIST[pilihan_ak]

    if pilihan_ak == "Lainnya (ketik sendiri)":
        nama_ak = st.text_input("Nama / rumus kimia asam:", value="HA", key="ak_nama")
    else:
        nama_ak = info_ak["simbol"]
        st.info(f"Zat terpilih: **{nama_ak}**")

    col1, col2 = st.columns(2)
    with col1:
        konsentrasi_ak = st.number_input(
            "Konsentrasi (M):", min_value=1e-14, max_value=10.0,
            value=0.01, format="%.6f", key="ak_konsentrasi"
        )
    with col2:
        volume_ak = st.number_input(
            "Volume (mL):", min_value=0.1, max_value=10000.0,
            value=100.0, format="%.1f", key="ak_volume"
        )

    if st.button("🔬 Hitung pH", key="hitung_ak", type="primary", use_container_width=True):
        if not nama_ak.strip():
            st.error("Nama zat tidak boleh kosong.")
        else:
            try:
                hasil = hitung_asam_kuat(nama_ak, konsentrasi_ak, volume_ak)
                r = hasil["result"]

                st.markdown('<hr class="divider">', unsafe_allow_html=True)
                st.markdown("#### 📋 Hasil Perhitungan")

                # Kartu pH
                tampilkan_kartu_ph(r["pH"], r["pOH"], r["H_plus"], r["OH_minus"], r["label"])

                # Mol
                st.markdown('<hr class="divider">', unsafe_allow_html=True)
                st.markdown("**🧪 Mol yang Terbentuk**")
                mol_data = hasil.get("mol", {})
                c1, c2 = st.columns(2)
                with c1:
                    st.metric(f"Mol {nama_ak}", f"{mol_data.get('zat', 0):.6f} mol")
                with c2:
                    st.metric("Mol H⁺ yang dihasilkan", f"{mol_data.get('H_plus', 0):.6f} mol")

                # Langkah perhitungan
                st.markdown('<hr class="divider">', unsafe_allow_html=True)
                st.markdown("**📐 Langkah-langkah Perhitungan**")
                for step in hasil["steps"]:
                    if step.startswith("**"):
                        st.markdown(step)
                    elif step == "":
                        st.write("")
                    else:
                        st.code(step.strip(), language=None)

            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")


# ════════════════════════════════════════
# TAB 2 — ASAM LEMAH
# ════════════════════════════════════════
with tab2:
    st.markdown("##### Asam Lemah — Ionisasi Sebagian (α < 1)")
    st.caption("Contoh: CH₃COOH, HF, HCN, H₂CO₃, HCOOH")
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    pilihan_al = st.selectbox("Pilih asam lemah:", list(ASAM_LEMAH_LIST.keys()), key="al_pilih")
    info_al = ASAM_LEMAH_LIST[pilihan_al]

    if pilihan_al == "Lainnya (ketik sendiri)":
        nama_al = st.text_input("Nama / rumus kimia asam:", value="HA", key="al_nama")
        Ka_al = st.number_input("Nilai Ka:", min_value=1e-14, max_value=1.0, value=1.8e-5, format="%.2e", key="al_ka_input")
    else:
        nama_al = info_al["simbol"]
        Ka_al = info_al["Ka"]
        st.info(f"Zat terpilih: **{nama_al}** | Ka = {Ka_al:.2e}")

    konsentrasi_al = st.number_input(
        "Konsentrasi (M):", min_value=1e-14, max_value=10.0,
        value=0.1, format="%.6f", key="al_konsentrasi"
    )

    if st.button("🔬 Hitung pH", key="hitung_al", type="primary", use_container_width=True):
        if not nama_al.strip():
            st.error("Nama zat tidak boleh kosong.")
        elif Ka_al is None:
            st.error("Nilai Ka harus diisi.")
        else:
            try:
                hasil = hitung_asam_lemah(nama_al, konsentrasi_al, Ka_al)
                r = hasil["result"]

                st.markdown('<hr class="divider">', unsafe_allow_html=True)
                st.markdown("#### 📋 Hasil Perhitungan")

                tampilkan_kartu_ph(r["pH"], r["pOH"], r["H_plus"], r["OH_minus"], r["label"])

                # Derajat ionisasi
                alpha = r.get("persen_ionisasi", 0)
                warna = "normal" if alpha < 5 else "inverse"
                st.metric("Derajat Ionisasi (α)", f"{alpha:.2f}%",
                          delta="Asumsi x<<C valid ✅" if alpha < 5 else "Asumsi x<<C kurang tepat ⚠️",
                          delta_color=warna)

                # Tabel ICE
                st.markdown('<hr class="divider">', unsafe_allow_html=True)
                st.markdown("**🧊 Tabel ICE (Initial – Change – Equilibrium)**")
                tampilkan_ice(hasil["ice"])

                # Langkah
                st.markdown('<hr class="divider">', unsafe_allow_html=True)
                st.markdown("**📐 Langkah-langkah Perhitungan**")
                for step in hasil["steps"]:
                    if step.startswith("**"):
                        st.markdown(step)
                    elif step == "":
                        st.write("")
                    else:
                        st.code(step.strip(), language=None)

            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")


# ════════════════════════════════════════
# TAB 3 — BASA KUAT
# ════════════════════════════════════════
with tab3:
    st.markdown("##### Basa Kuat — Ionisasi Sempurna (α = 1)")
    st.caption("Contoh: NaOH, KOH, Ca(OH)₂, Ba(OH)₂")
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    pilihan_bk = st.selectbox("Pilih basa kuat:", list(BASA_KUAT_LIST.keys()), key="bk_pilih")
    info_bk = BASA_KUAT_LIST[pilihan_bk]

    if pilihan_bk == "Lainnya (ketik sendiri)":
        nama_bk = st.text_input("Nama / rumus kimia basa:", value="BOH", key="bk_nama")
    else:
        nama_bk = info_bk["simbol"]
        st.info(f"Zat terpilih: **{nama_bk}**")

    col1, col2 = st.columns(2)
    with col1:
        konsentrasi_bk = st.number_input(
            "Konsentrasi (M):", min_value=1e-14, max_value=10.0,
            value=0.05, format="%.6f", key="bk_konsentrasi"
        )
    with col2:
        volume_bk = st.number_input(
            "Volume (mL):", min_value=0.1, max_value=10000.0,
            value=200.0, format="%.1f", key="bk_volume"
        )

    if st.button("🔬 Hitung pH", key="hitung_bk", type="primary", use_container_width=True):
        if not nama_bk.strip():
            st.error("Nama zat tidak boleh kosong.")
        else:
            try:
                hasil = hitung_basa_kuat(nama_bk, konsentrasi_bk, volume_bk)
                r = hasil["result"]

                st.markdown('<hr class="divider">', unsafe_allow_html=True)
                st.markdown("#### 📋 Hasil Perhitungan")

                tampilkan_kartu_ph(r["pH"], r["pOH"], r["H_plus"], r["OH_minus"], r["label"])

                # Mol
                st.markdown('<hr class="divider">', unsafe_allow_html=True)
                st.markdown("**🧪 Mol yang Terbentuk**")
                mol_data = hasil.get("mol", {})
                c1, c2 = st.columns(2)
                with c1:
                    st.metric(f"Mol {nama_bk}", f"{mol_data.get('zat', 0):.6f} mol")
                with c2:
                    st.metric("Mol OH⁻ yang dihasilkan", f"{mol_data.get('OH_minus', 0):.6f} mol")

                # Langkah
                st.markdown('<hr class="divider">', unsafe_allow_html=True)
                st.markdown("**📐 Langkah-langkah Perhitungan**")
                for step in hasil["steps"]:
                    if step.startswith("**"):
                        st.markdown(step)
                    elif step == "":
                        st.write("")
                    else:
                        st.code(step.strip(), language=None)

            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")


# ════════════════════════════════════════
# TAB 4 — BASA LEMAH
# ════════════════════════════════════════
with tab4:
    st.markdown("##### Basa Lemah — Ionisasi Sebagian (α < 1)")
    st.caption("Contoh: NH₃, C₅H₅N, C₆H₅NH₂")
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    pilihan_bl = st.selectbox("Pilih basa lemah:", list(BASA_LEMAH_LIST.keys()), key="bl_pilih")
    info_bl = BASA_LEMAH_LIST[pilihan_bl]

    if pilihan_bl == "Lainnya (ketik sendiri)":
        nama_bl = st.text_input("Nama / rumus kimia basa:", value="B", key="bl_nama")
        Kb_bl = st.number_input("Nilai Kb:", min_value=1e-14, max_value=1.0, value=1.8e-5, format="%.2e", key="bl_kb_input")
    else:
        nama_bl = info_bl["simbol"]
        Kb_bl = info_bl["Kb"]
        st.info(f"Zat terpilih: **{nama_bl}** | Kb = {Kb_bl:.2e}")

    konsentrasi_bl = st.number_input(
        "Konsentrasi (M):", min_value=1e-14, max_value=10.0,
        value=0.1, format="%.6f", key="bl_konsentrasi"
    )

    if st.button("🔬 Hitung pH", key="hitung_bl", type="primary", use_container_width=True):
        if not nama_bl.strip():
            st.error("Nama zat tidak boleh kosong.")
        elif Kb_bl is None:
            st.error("Nilai Kb harus diisi.")
        else:
            try:
                hasil = hitung_basa_lemah(nama_bl, konsentrasi_bl, Kb_bl)
                r = hasil["result"]

                st.markdown('<hr class="divider">', unsafe_allow_html=True)
                st.markdown("#### 📋 Hasil Perhitungan")

                tampilkan_kartu_ph(r["pH"], r["pOH"], r["H_plus"], r["OH_minus"], r["label"])

                # Derajat ionisasi
                alpha = r.get("persen_ionisasi", 0)
                st.metric("Derajat Ionisasi (α)", f"{alpha:.2f}%",
                          delta="Asumsi x<<C valid ✅" if alpha < 5 else "Asumsi x<<C kurang tepat ⚠️",
                          delta_color="normal" if alpha < 5 else "inverse")

                # Tabel ICE
                st.markdown('<hr class="divider">', unsafe_allow_html=True)
                st.markdown("**🧊 Tabel ICE (Initial – Change – Equilibrium)**")
                tampilkan_ice(hasil["ice"])

                # Langkah
                st.markdown('<hr class="divider">', unsafe_allow_html=True)
                st.markdown("**📐 Langkah-langkah Perhitungan**")
                for step in hasil["steps"]:
                    if step.startswith("**"):
                        st.markdown(step)
                    elif step == "":
                        st.write("")
                    else:
                        st.code(step.strip(), language=None)

            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")
