# utils/sidebar.py
import streamlit as st

def tampilkan_sidebar():
    with st.sidebar:
        st.markdown("### ⚗️ Kalkulator pH")
        st.markdown("---")
        st.markdown("**Navigasi Halaman**")
        st.page_link("app.py",               label="🏠 Beranda")
        st.page_link("pages/1_asam_basa.py", label="🔬 Asam & Basa")
        st.page_link("pages/2_hidrolisis.py",label="🧂 Hidrolisis Garam")
        st.markdown("---")
