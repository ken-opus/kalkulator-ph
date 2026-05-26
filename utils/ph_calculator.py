"""
ph_calculator.py
================
Modul logika perhitungan pH untuk Kalkulator pH Kelas.
Berisi semua fungsi hitung untuk:
  - Asam kuat & asam lemah
  - Basa kuat & basa lemah
  - Hidrolisis garam (4 jenis)

Setiap fungsi mengembalikan dictionary berisi:
  - steps : list of string (langkah-langkah perhitungan)
  - ice   : dict (tabel ICE, jika relevan)
  - result: dict (nilai akhir: H_plus, OH_minus, pH, pOH, label)
"""

import math

# ─────────────────────────────────────────────
# KONSTANTA
# ─────────────────────────────────────────────
Kw = 1e-14          # Konstanta air pada 25°C
pKw = 14.0


# ─────────────────────────────────────────────
# FUNGSI UTILITAS
# ─────────────────────────────────────────────

def hitung_pH(H_plus: float) -> float:
    """Menghitung pH dari konsentrasi ion H⁺."""
    if H_plus <= 0:
        raise ValueError("Konsentrasi H⁺ harus lebih besar dari 0.")
    return -math.log10(H_plus)


def hitung_pOH(OH_minus: float) -> float:
    """Menghitung pOH dari konsentrasi ion OH⁻."""
    if OH_minus <= 0:
        raise ValueError("Konsentrasi OH⁻ harus lebih besar dari 0.")
    return -math.log10(OH_minus)


def label_pH(pH: float) -> str:
    """Mengembalikan label sifat larutan berdasarkan pH."""
    if pH < 7:
        return "Asam"
    elif pH > 7:
        return "Basa"
    else:
        return "Netral"


def format_angka(nilai: float) -> str:
    """Format angka ilmiah yang rapi untuk ditampilkan."""
    if nilai == 0:
        return "0"
    exp = math.floor(math.log10(abs(nilai)))
    mantissa = nilai / (10 ** exp)
    if exp == 0:
        return f"{nilai:.4f}"
    return f"{mantissa:.4f} × 10^{exp}"


# ─────────────────────────────────────────────
# 1. ASAM KUAT
# ─────────────────────────────────────────────

def hitung_asam_kuat(nama: str, konsentrasi: float, volume: float) -> dict:
    """
    Menghitung pH asam kuat (ionisasi sempurna).

    Parameter:
        nama        : nama asam, misal "HCl"
        konsentrasi : konsentrasi dalam M (mol/L)
        volume      : volume dalam mL

    Contoh reaksi: HCl → H⁺ + Cl⁻
    """
    # Hitung mol
    volume_L = volume / 1000
    mol_asam = konsentrasi * volume_L

    # Ionisasi sempurna → [H⁺] = C
    H_plus = konsentrasi
    OH_minus = Kw / H_plus
    pH = hitung_pH(H_plus)
    pOH = pKw - pH

    steps = [
        f"**Reaksi ionisasi:**",
        f"  {nama}  →  H⁺  +  anion⁻  (ionisasi sempurna, α = 1)",
        "",
        f"**Perhitungan mol:**",
        f"  Mol {nama} = C × V = {konsentrasi} M × {volume} mL × (1 L / 1000 mL)",
        f"             = {mol_asam:.6f} mol",
        "",
        f"**Konsentrasi ion H⁺:**",
        f"  Karena ionisasi sempurna:",
        f"  [H⁺] = [Asam] = {format_angka(H_plus)} M",
        "",
        f"**Konsentrasi ion OH⁻:**",
        f"  [OH⁻] = Kw / [H⁺] = 10⁻¹⁴ / {format_angka(H_plus)}",
        f"        = {format_angka(OH_minus)} M",
        "",
        f"**Perhitungan pH:**",
        f"  pH = -log[H⁺]",
        f"     = -log({format_angka(H_plus)})",
        f"     = {pH:.2f}",
        "",
        f"**pOH:**",
        f"  pOH = 14 - pH = 14 - {pH:.2f} = {pOH:.2f}",
    ]

    ice = None  # Asam kuat tidak butuh tabel ICE

    return {
        "steps": steps,
        "ice": ice,
        "mol": {
            "zat": mol_asam,
            "H_plus": mol_asam,
        },
        "result": {
            "H_plus": H_plus,
            "OH_minus": OH_minus,
            "pH": pH,
            "pOH": pOH,
            "label": label_pH(pH),
        }
    }


# ─────────────────────────────────────────────
# 2. ASAM LEMAH
# ─────────────────────────────────────────────

def hitung_asam_lemah(nama: str, konsentrasi: float, Ka: float) -> dict:
    """
    Menghitung pH asam lemah (ionisasi sebagian).

    Parameter:
        nama        : nama asam, misal "CH₃COOH"
        konsentrasi : konsentrasi dalam M
        Ka          : konstanta ionisasi asam

    Asumsi: x << C sehingga (C - x) ≈ C  (valid jika Ka << C)
    Rumus: [H⁺] = √(Ka × C)
    """
    H_plus = math.sqrt(Ka * konsentrasi)
    OH_minus = Kw / H_plus
    pH = hitung_pH(H_plus)
    pOH = pKw - pH

    # Cek apakah asumsi x << C valid (x/C < 5%)
    persen_ionisasi = (H_plus / konsentrasi) * 100
    catatan_asumsi = (
        f"✅ Asumsi x << C valid ({persen_ionisasi:.2f}% < 5%)"
        if persen_ionisasi < 5
        else f"⚠️ Asumsi x << C kurang tepat ({persen_ionisasi:.2f}% > 5%), gunakan rumus kuadrat untuk akurasi lebih tinggi."
    )

    ice = {
        "header": [nama, "H⁺", "anion⁻"],
        "Initial":  [f"{konsentrasi} M", "0", "0"],
        "Change":   ["-x", "+x", "+x"],
        "Equil.":   [f"{konsentrasi} - x ≈ {konsentrasi} M", "x", "x"],
    }

    steps = [
        f"**Reaksi ionisasi:**",
        f"  {nama}  ⇌  H⁺  +  anion⁻  (ionisasi sebagian)",
        "",
        f"**Tabel ICE:**",
        f"  (lihat tabel di bawah)",
        "",
        f"**Ekspresi Ka:**",
        f"  Ka = [H⁺][anion⁻] / [{nama}]",
        f"     = x² / (C - x)",
        f"     ≈ x² / C  (asumsi x << C)",
        "",
        f"**Hitung [H⁺]:**",
        f"  x = [H⁺] = √(Ka × C)",
        f"            = √({format_angka(Ka)} × {konsentrasi})",
        f"            = √({format_angka(Ka * konsentrasi)})",
        f"            = {format_angka(H_plus)} M",
        "",
        f"  {catatan_asumsi}",
        f"  Derajat ionisasi (α) = {persen_ionisasi:.2f}%",
        "",
        f"**Konsentrasi ion OH⁻:**",
        f"  [OH⁻] = Kw / [H⁺] = {format_angka(OH_minus)} M",
        "",
        f"**Perhitungan pH:**",
        f"  pH = -log[H⁺]",
        f"     = -log({format_angka(H_plus)})",
        f"     = {pH:.2f}",
        "",
        f"**pOH:**",
        f"  pOH = 14 - {pH:.2f} = {pOH:.2f}",
    ]

    return {
        "steps": steps,
        "ice": ice,
        "result": {
            "H_plus": H_plus,
            "OH_minus": OH_minus,
            "pH": pH,
            "pOH": pOH,
            "label": label_pH(pH),
            "persen_ionisasi": persen_ionisasi,
        }
    }


# ─────────────────────────────────────────────
# 3. BASA KUAT
# ─────────────────────────────────────────────

def hitung_basa_kuat(nama: str, konsentrasi: float, volume: float) -> dict:
    """
    Menghitung pH basa kuat (ionisasi sempurna).

    Parameter:
        nama        : nama basa, misal "NaOH"
        konsentrasi : konsentrasi dalam M
        volume      : volume dalam mL

    Contoh reaksi: NaOH → Na⁺ + OH⁻
    """
    volume_L = volume / 1000
    mol_basa = konsentrasi * volume_L

    OH_minus = konsentrasi
    H_plus = Kw / OH_minus
    pOH = hitung_pOH(OH_minus)
    pH = pKw - pOH

    steps = [
        f"**Reaksi ionisasi:**",
        f"  {nama}  →  kation⁺  +  OH⁻  (ionisasi sempurna, α = 1)",
        "",
        f"**Perhitungan mol:**",
        f"  Mol {nama} = C × V = {konsentrasi} M × {volume} mL × (1 L / 1000 mL)",
        f"             = {mol_basa:.6f} mol",
        "",
        f"**Konsentrasi ion OH⁻:**",
        f"  Karena ionisasi sempurna:",
        f"  [OH⁻] = [{nama}] = {format_angka(OH_minus)} M",
        "",
        f"**Konsentrasi ion H⁺:**",
        f"  [H⁺] = Kw / [OH⁻] = 10⁻¹⁴ / {format_angka(OH_minus)}",
        f"        = {format_angka(H_plus)} M",
        "",
        f"**Perhitungan pOH:**",
        f"  pOH = -log[OH⁻]",
        f"      = -log({format_angka(OH_minus)})",
        f"      = {pOH:.2f}",
        "",
        f"**Perhitungan pH:**",
        f"  pH = 14 - pOH = 14 - {pOH:.2f} = {pH:.2f}",
    ]

    return {
        "steps": steps,
        "ice": None,
        "mol": {
            "zat": mol_basa,
            "OH_minus": mol_basa,
        },
        "result": {
            "H_plus": H_plus,
            "OH_minus": OH_minus,
            "pH": pH,
            "pOH": pOH,
            "label": label_pH(pH),
        }
    }


# ─────────────────────────────────────────────
# 4. BASA LEMAH
# ─────────────────────────────────────────────

def hitung_basa_lemah(nama: str, konsentrasi: float, Kb: float) -> dict:
    """
    Menghitung pH basa lemah (ionisasi sebagian).

    Parameter:
        nama        : nama basa, misal "NH₃"
        konsentrasi : konsentrasi dalam M
        Kb          : konstanta ionisasi basa

    Rumus: [OH⁻] = √(Kb × C)
    """
    OH_minus = math.sqrt(Kb * konsentrasi)
    H_plus = Kw / OH_minus
    pOH = hitung_pOH(OH_minus)
    pH = pKw - pOH

    persen_ionisasi = (OH_minus / konsentrasi) * 100
    catatan_asumsi = (
        f"✅ Asumsi x << C valid ({persen_ionisasi:.2f}% < 5%)"
        if persen_ionisasi < 5
        else f"⚠️ Asumsi x << C kurang tepat ({persen_ionisasi:.2f}% > 5%)."
    )

    ice = {
        "header": [nama, "OH⁻", "kation⁺"],
        "Initial":  [f"{konsentrasi} M", "0", "0"],
        "Change":   ["-x", "+x", "+x"],
        "Equil.":   [f"{konsentrasi} - x ≈ {konsentrasi} M", "x", "x"],
    }

    steps = [
        f"**Reaksi ionisasi:**",
        f"  {nama} + H₂O  ⇌  OH⁻  +  kation⁺  (ionisasi sebagian)",
        "",
        f"**Tabel ICE:**",
        f"  (lihat tabel di bawah)",
        "",
        f"**Ekspresi Kb:**",
        f"  Kb = [OH⁻][kation⁺] / [{nama}]",
        f"     = x² / (C - x)",
        f"     ≈ x² / C  (asumsi x << C)",
        "",
        f"**Hitung [OH⁻]:**",
        f"  x = [OH⁻] = √(Kb × C)",
        f"             = √({format_angka(Kb)} × {konsentrasi})",
        f"             = √({format_angka(Kb * konsentrasi)})",
        f"             = {format_angka(OH_minus)} M",
        "",
        f"  {catatan_asumsi}",
        f"  Derajat ionisasi (α) = {persen_ionisasi:.2f}%",
        "",
        f"**Konsentrasi ion H⁺:**",
        f"  [H⁺] = Kw / [OH⁻] = {format_angka(H_plus)} M",
        "",
        f"**Perhitungan pOH:**",
        f"  pOH = -log[OH⁻] = -log({format_angka(OH_minus)}) = {pOH:.2f}",
        "",
        f"**Perhitungan pH:**",
        f"  pH = 14 - pOH = 14 - {pOH:.2f} = {pH:.2f}",
    ]

    return {
        "steps": steps,
        "ice": ice,
        "result": {
            "H_plus": H_plus,
            "OH_minus": OH_minus,
            "pH": pH,
            "pOH": pOH,
            "label": label_pH(pH),
            "persen_ionisasi": persen_ionisasi,
        }
    }


# ─────────────────────────────────────────────
# 5. HIDROLISIS GARAM
# ─────────────────────────────────────────────

def hitung_hidrolisis_garam(
    nama_garam: str,
    konsentrasi: float,
    jenis: str,
    Ka: float = None,
    Kb: float = None
) -> dict:
    """
    Menghitung pH hidrolisis garam.

    Parameter:
        nama_garam  : nama garam, misal "CH₃COONa"
        konsentrasi : konsentrasi garam dalam M
        jenis       : salah satu dari:
                      "ak_bk"  → asam kuat + basa kuat (netral)
                      "al_bk"  → asam lemah + basa kuat (basa)
                      "ak_bl"  → asam kuat + basa lemah (asam)
                      "al_bl"  → asam lemah + basa lemah
        Ka          : Ka asam pembentuk (untuk al_bk dan al_bl)
        Kb          : Kb basa pembentuk (untuk ak_bl dan al_bl)
    """

    if jenis == "ak_bk":
        # Tidak terhidrolisis → pH = 7
        steps = [
            f"**Jenis garam:** Asam Kuat + Basa Kuat",
            f"",
            f"**Analisis ion:**",
            f"  {nama_garam} larut menghasilkan kation dari basa kuat dan anion dari asam kuat.",
            f"  Kation dari basa kuat → tidak terhidrolisis.",
            f"  Anion dari asam kuat → tidak terhidrolisis.",
            f"",
            f"**Kesimpulan:**",
            f"  Garam tidak mengalami hidrolisis.",
            f"  pH = 7 (netral pada 25°C)",
        ]
        return {
            "steps": steps,
            "ice": None,
            "result": {
                "H_plus": 1e-7,
                "OH_minus": 1e-7,
                "pH": 7.0,
                "pOH": 7.0,
                "label": "Netral",
                "Kh": None,
            }
        }

    elif jenis == "al_bk":
        # Anion dari asam lemah terhidrolisis → basa
        # Kh = Kw / Ka
        # [OH⁻] = √(Kh × C)
        if Ka is None:
            raise ValueError("Ka diperlukan untuk garam asam lemah + basa kuat.")
        Kh = Kw / Ka
        OH_minus = math.sqrt(Kh * konsentrasi)
        H_plus = Kw / OH_minus
        pOH = hitung_pOH(OH_minus)
        pH = pKw - pOH

        ice = {
            "header": ["anion⁻ (dari asam lemah)", "OH⁻", "Asam lemah"],
            "Initial":  [f"{konsentrasi} M", "0", "0"],
            "Change":   ["-x", "+x", "+x"],
            "Equil.":   [f"{konsentrasi} - x ≈ {konsentrasi} M", "x", "x"],
        }

        steps = [
            f"**Jenis garam:** Asam Lemah + Basa Kuat → Larutan Basa",
            f"",
            f"**Reaksi hidrolisis (anion terhidrolisis):**",
            f"  anion⁻ + H₂O  ⇌  asam lemah  +  OH⁻",
            f"",
            f"**Konstanta hidrolisis (Kh):**",
            f"  Kh = Kw / Ka",
            f"     = 10⁻¹⁴ / {format_angka(Ka)}",
            f"     = {format_angka(Kh)}",
            f"",
            f"**Tabel ICE:**",
            f"  (lihat tabel di bawah)",
            f"",
            f"**Hitung [OH⁻]:**",
            f"  [OH⁻] = √(Kh × C)",
            f"        = √({format_angka(Kh)} × {konsentrasi})",
            f"        = {format_angka(OH_minus)} M",
            f"",
            f"**Hitung [H⁺]:**",
            f"  [H⁺] = Kw / [OH⁻] = {format_angka(H_plus)} M",
            f"",
            f"**Perhitungan pOH & pH:**",
            f"  pOH = -log[OH⁻] = {pOH:.2f}",
            f"  pH  = 14 - pOH  = 14 - {pOH:.2f} = {pH:.2f}",
        ]

        return {
            "steps": steps,
            "ice": ice,
            "result": {
                "H_plus": H_plus,
                "OH_minus": OH_minus,
                "pH": pH,
                "pOH": pOH,
                "label": label_pH(pH),
                "Kh": Kh,
            }
        }

    elif jenis == "ak_bl":
        # Kation dari basa lemah terhidrolisis → asam
        # Kh = Kw / Kb
        # [H⁺] = √(Kh × C)
        if Kb is None:
            raise ValueError("Kb diperlukan untuk garam asam kuat + basa lemah.")
        Kh = Kw / Kb
        H_plus = math.sqrt(Kh * konsentrasi)
        OH_minus = Kw / H_plus
        pH = hitung_pH(H_plus)
        pOH = pKw - pH

        ice = {
            "header": ["kation⁺ (dari basa lemah)", "H⁺", "Basa lemah"],
            "Initial":  [f"{konsentrasi} M", "0", "0"],
            "Change":   ["-x", "+x", "+x"],
            "Equil.":   [f"{konsentrasi} - x ≈ {konsentrasi} M", "x", "x"],
        }

        steps = [
            f"**Jenis garam:** Asam Kuat + Basa Lemah → Larutan Asam",
            f"",
            f"**Reaksi hidrolisis (kation terhidrolisis):**",
            f"  kation⁺ + H₂O  ⇌  basa lemah  +  H⁺",
            f"",
            f"**Konstanta hidrolisis (Kh):**",
            f"  Kh = Kw / Kb",
            f"     = 10⁻¹⁴ / {format_angka(Kb)}",
            f"     = {format_angka(Kh)}",
            f"",
            f"**Tabel ICE:**",
            f"  (lihat tabel di bawah)",
            f"",
            f"**Hitung [H⁺]:**",
            f"  [H⁺] = √(Kh × C)",
            f"        = √({format_angka(Kh)} × {konsentrasi})",
            f"        = {format_angka(H_plus)} M",
            f"",
            f"**Hitung [OH⁻]:**",
            f"  [OH⁻] = Kw / [H⁺] = {format_angka(OH_minus)} M",
            f"",
            f"**Perhitungan pH:**",
            f"  pH  = -log[H⁺] = {pH:.2f}",
            f"  pOH = 14 - pH  = 14 - {pH:.2f} = {pOH:.2f}",
        ]

        return {
            "steps": steps,
            "ice": ice,
            "result": {
                "H_plus": H_plus,
                "OH_minus": OH_minus,
                "pH": pH,
                "pOH": pOH,
                "label": label_pH(pH),
                "Kh": Kh,
            }
        }

    elif jenis == "al_bl":
        # Keduanya terhidrolisis
        # pH = 7 + ½(pKa - pKb)
        if Ka is None or Kb is None:
            raise ValueError("Ka dan Kb keduanya diperlukan untuk garam asam lemah + basa lemah.")
        pKa = -math.log10(Ka)
        pKb = -math.log10(Kb)
        pH = 7 + 0.5 * (pKa - pKb)
        H_plus = 10 ** (-pH)
        OH_minus = Kw / H_plus
        pOH = pKw - pH

        if Ka > Kb:
            sifat = "Asam (Ka > Kb)"
        elif Ka < Kb:
            sifat = "Basa (Kb > Ka)"
        else:
            sifat = "Netral (Ka = Kb)"

        steps = [
            f"**Jenis garam:** Asam Lemah + Basa Lemah → Sifat tergantung Ka vs Kb",
            f"",
            f"**Reaksi hidrolisis (kedua ion terhidrolisis):**",
            f"  anion⁻  + H₂O  ⇌  asam lemah  +  OH⁻",
            f"  kation⁺ + H₂O  ⇌  basa lemah   +  H⁺",
            f"",
            f"**Rumus pH:**",
            f"  pH = 7 + ½(pKa - pKb)",
            f"",
            f"**Hitung pKa dan pKb:**",
            f"  pKa = -log(Ka) = -log({format_angka(Ka)}) = {pKa:.4f}",
            f"  pKb = -log(Kb) = -log({format_angka(Kb)}) = {pKb:.4f}",
            f"",
            f"**Hitung pH:**",
            f"  pH = 7 + ½({pKa:.4f} - {pKb:.4f})",
            f"     = 7 + ½({pKa - pKb:.4f})",
            f"     = 7 + {0.5*(pKa-pKb):.4f}",
            f"     = {pH:.2f}",
            f"",
            f"**Perbandingan Ka vs Kb:**  {sifat}",
            f"",
            f"**[H⁺]  = {format_angka(H_plus)} M**",
            f"**[OH⁻] = {format_angka(OH_minus)} M**",
            f"**pOH   = {pOH:.2f}**",
        ]

        return {
            "steps": steps,
            "ice": None,
            "result": {
                "H_plus": H_plus,
                "OH_minus": OH_minus,
                "pH": pH,
                "pOH": pOH,
                "label": label_pH(pH),
                "Kh": None,
                "pKa": pKa,
                "pKb": pKb,
            }
        }

    else:
        raise ValueError(f"Jenis garam '{jenis}' tidak dikenal. Gunakan: ak_bk, al_bk, ak_bl, al_bl.")


# ─────────────────────────────────────────────
# CONTOH PENGGUNAAN (untuk testing)
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 50)
    print("TEST: Asam Kuat — HCl 0.01 M, 100 mL")
    hasil = hitung_asam_kuat("HCl", 0.01, 100)
    for s in hasil["steps"]:
        print(s)
    print(f"\n→ pH = {hasil['result']['pH']:.2f} ({hasil['result']['label']})")

    print("\n" + "=" * 50)
    print("TEST: Asam Lemah — CH₃COOH 0.1 M, Ka = 1.8×10⁻⁵")
    hasil = hitung_asam_lemah("CH₃COOH", 0.1, 1.8e-5)
    for s in hasil["steps"]:
        print(s)
    print(f"\n→ pH = {hasil['result']['pH']:.2f} ({hasil['result']['label']})")

    print("\n" + "=" * 50)
    print("TEST: Basa Kuat — NaOH 0.05 M, 200 mL")
    hasil = hitung_basa_kuat("NaOH", 0.05, 200)
    for s in hasil["steps"]:
        print(s)
    print(f"\n→ pH = {hasil['result']['pH']:.2f} ({hasil['result']['label']})")

    print("\n" + "=" * 50)
    print("TEST: Hidrolisis — CH₃COONa (asam lemah + basa kuat), Ka = 1.8×10⁻⁵, C = 0.1 M")
    hasil = hitung_hidrolisis_garam("CH₃COONa", 0.1, "al_bk", Ka=1.8e-5)
    for s in hasil["steps"]:
        print(s)
    print(f"\n→ pH = {hasil['result']['pH']:.2f} ({hasil['result']['label']})")
