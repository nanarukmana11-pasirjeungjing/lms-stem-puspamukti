# -*- coding: utf-8 -*-
"""
LMS STEM — Gugus Cidugaleun
(SDN Parentas, SDN Sirnagalih, SDN Karamatjaya, SDN Cidugaleun,
 SDN Panglayungan, SDN Giriatikan)

Struktur proyek:
    lms_stem_cidugaleun/
        app.py               <- titik masuk (halaman ini)
        data/content.py      <- teks & data konten, dipisah dari tampilan
        assets/style.css     <- styling mobile-first
        docs/kelas1..6/      <- Daftar Proyek, Modul, Panduan Guru, Alat & Bahan,
                                template Administrasi STEM per kelas
        docs/umum/           <- dokumen gugus (supervisi, program, panduan)
        storage/             <- dibuat otomatis: progres, unggahan, hasil supervisi
        requirements.txt

Menu:
    🏠 Beranda       — gambaran STEM, karakteristik, 7 tahap praktik, sekolah anggota, KKG
    📖 Panduan       — ringkasan Panduan Pembelajaran STEM Kemendikdasmen 2025
    📚 Modul Kelas   — 56 proyek STEM Kelas 1–6 + uraian per pertemuan
    🗂️ Administrasi  — template administrasi STEM per kelas & dokumen gugus
    📊 Progres Gugus — status proyek tiap sekolah, unggah bukti, galeri
    👨‍💼 Supervisi     — instrumen supervisi STEM (Kepala Sekolah & Pengurus)
"""

import datetime
import io
import json
import re
from pathlib import Path

import streamlit as st

from data.content import (
    APP_NAMA,
    GUGUS,
    SEKOLAH,
    SEKOLAH_WARNA,
    SEKOLAH_PENYUSUN_RUJUKAN,
    OVERVIEW,
    KARAKTERISTIK,
    PERAN_KOMPONEN,
    TAHAP_PRAKTIK,
    TAHAP_CATATAN,
    PENGALAMAN_BELAJAR,
    LANGKAH_PERENCANAAN,
    KOMPONEN_PERENCANAAN,
    MODEL_PEMBELAJARAN,
    IMPLEMENTASI,
    PERAN_PEMANGKU,
    PROFIL_LULUSAN,
    FASE,
    EVENT,
    AGENDA,
    PRINSIP_WARNA,
    PENGALAMAN_WARNA,
    KELOMPOK_KELAS,
    ADMIN_DOCS,
    DOKUMEN_UMUM,
    SUPERVISI_FILE,
    STORYBOOK_LINKS,
    ROLES,
    STATUS_PROYEK,
    STATUS_WARNA,
    LAMPIRAN_TABS,
    KELAS_DATA,
)

try:
    import docx  # python-docx
except ImportError:  # pragma: no cover
    docx = None

st.set_page_config(
    page_title=APP_NAMA,
    page_icon="🧪",
    layout="centered",
    initial_sidebar_state="collapsed",
)

APP_DIR = Path(__file__).resolve().parent
DOCS_DIR = APP_DIR / "docs"
STORAGE_DIR = APP_DIR / "storage"
UPLOAD_DIR = STORAGE_DIR / "uploads"
PROGRESS_FILE = STORAGE_DIR / "progres_proyek.json"
SUPERVISI_LOG = STORAGE_DIR / "hasil_supervisi.json"

ROLE_GURU, ROLE_KS, ROLE_PENGURUS = ROLES
IMG_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif"}


# ============================================================================
# Util umum
# ============================================================================
def load_css():
    css_path = APP_DIR / "assets" / "style.css"
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


def init_state():
    defaults = {
        "auth": None,
        "page": "landing",
        "kelas_terpilih": 1,
        "lampiran_tab": "lampiran1",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def _slug(text: str) -> str:
    return re.sub(r"\W+", "_", text.lower()).strip("_")[:40]


def _esc(text: str) -> str:
    return (text or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def section(icon: str, title: str):
    st.markdown(f'<div class="section-title"><span class="icon">{icon}</span> {title}</div>', unsafe_allow_html=True)


def card(html: str):
    st.markdown(f'<div class="card">{html}</div>', unsafe_allow_html=True)


def _goto(page_key: str):
    st.session_state.page = page_key
    st.rerun()


def kelas_dir(kelas: int) -> Path:
    return DOCS_DIR / f"kelas{kelas}"


def umum_path(filename: str) -> Path:
    return DOCS_DIR / "umum" / filename


def _mtime(path: Path) -> float:
    return path.stat().st_mtime if path.exists() else 0


_HARI_ID = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
_BULAN_ID = ["Januari", "Februari", "Maret", "April", "Mei", "Juni",
             "Juli", "Agustus", "September", "Oktober", "November", "Desember"]


def _format_tanggal_id(d) -> str:
    return f"{_HARI_ID[d.weekday()]}, {d.day} {_BULAN_ID[d.month - 1]} {d.year}"


# ============================================================================
# Penyimpanan sederhana berbasis berkas JSON (folder storage/)
# Catatan: di Streamlit Community Cloud penyimpanan ini bersifat sementara
# (hilang saat aplikasi di-reboot). Saat dijalankan di laptop/PC sekolah,
# data tersimpan permanen di folder storage/.
# ============================================================================
def _read_json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def _write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(path)


def load_progress() -> dict:
    return _read_json(PROGRESS_FILE, {})


def get_status(progress: dict, sekolah: str, kelas: int, judul: str) -> dict:
    return progress.get(sekolah, {}).get(str(kelas), {}).get(judul, {})


def set_status(sekolah: str, kelas: int, judul: str, **fields):
    progress = load_progress()
    rec = progress.setdefault(sekolah, {}).setdefault(str(kelas), {}).setdefault(judul, {})
    rec.update(fields)
    rec["diperbarui"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    _write_json(PROGRESS_FILE, progress)


def save_upload(sekolah: str, kelas: int, judul: str, uploaded, pengunggah: str) -> str:
    folder = UPLOAD_DIR / _slug(sekolah) / f"kelas{kelas}"
    folder.mkdir(parents=True, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = re.sub(r"[^\w.\-]+", "_", uploaded.name)
    target = folder / f"{stamp}_{safe_name}"
    target.write_bytes(uploaded.getbuffer())
    progress = load_progress()
    rec = progress.setdefault(sekolah, {}).setdefault(str(kelas), {}).setdefault(judul, {})
    rec.setdefault("bukti", []).append({
        "berkas": str(target.relative_to(STORAGE_DIR)).replace("\\", "/"),
        "nama_asli": uploaded.name,
        "pengunggah": pengunggah,
        "waktu": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
    })
    rec.setdefault("status", "Sedang berjalan")
    rec["diperbarui"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    _write_json(PROGRESS_FILE, progress)
    return target.name


def school_summary(progress: dict, sekolah: str):
    """Kembalikan {kelas: (terlaksana, berjalan, total)} untuk satu sekolah."""
    out = {}
    for k, kd in KELAS_DATA.items():
        total = len(kd["proyek"])
        done = run = 0
        for judul in kd["proyek"]:
            s = get_status(progress, sekolah, k, judul).get("status")
            if s == "Terlaksana":
                done += 1
            elif s == "Sedang berjalan":
                run += 1
        out[k] = (done, run, total)
    return out


# ============================================================================
# Pembacaan dokumen .docx
# ============================================================================
def _cell_text(cell) -> str:
    return " ".join(p.text for p in cell.paragraphs).strip()


def _iter_block_items(document):
    from docx.table import Table
    from docx.text.paragraph import Paragraph

    for child in document.element.body.iterchildren():
        if child.tag.endswith("}p"):
            yield Paragraph(child, document)
        elif child.tag.endswith("}tbl"):
            yield Table(child, document)


@st.cache_resource(show_spinner="Membuka dokumen...")
def load_docx_document(path_str: str, _mtime_val: float):
    path = Path(path_str)
    if not path.exists():
        return None, f"Berkas '{path.name}' tidak ditemukan di folder docs/."
    try:
        return docx.Document(str(path)), None
    except Exception as exc:  # pragma: no cover
        return None, f"Gagal membaca '{path.name}': {exc}"


def open_doc(path: Path):
    return load_docx_document(str(path), _mtime(path))


def _get_identitas_dict(document) -> dict:
    if not document.tables:
        return {}
    return {
        _cell_text(r.cells[0]): _cell_text(r.cells[1])
        for r in document.tables[0].rows
        if len(r.cells) >= 2 and _cell_text(r.cells[0])
    }


_BULLET_RE = re.compile(r"^[•\-–▪●◦]\s*")
_PERT_RE = re.compile(r"^Pertemuan\s*(\d+)\s*[–-]\s*(.+)$")
_DETAIL_START_RE = re.compile(r"^\d+\.\s*Detail Pelaksanaan")
_DETAIL_END_RE = re.compile(r"^\d+\.\s*(Lembar Kerja|LKPD)")
_TAHAP_RE = re.compile(r"^Tahap Praktik Saintifik dan Enjinering\s*\([^)]*\):\s*(.+)$")
_PENGALAMAN_RE = re.compile(r"^Pengalaman Belajar:\s*(.+?)\s*\|\s*Prinsip Pembelajaran Mendalam:\s*(.+)$")
_JUDUL_TGL_RE = re.compile(
    r"^(?P<tgl>[A-Za-z]+,\s*\d{1,2}\s+\w+\s+\d{4})\s*:\s*(?P<judul>.+?)\s*\((?P<jp>[^)]+)\)\s*$"
)
_JUDUL_PERIODE_RE = re.compile(
    r"^(?:Pertemuan|Minggu) ke-\d+\s*[—–-]\s*(?P<tgl>.+?\d{4}(?:\s*\([^)]*\))?)\s*:\s*(?P<judul>.+?)\s*\((?P<jp>[^)]+)\)\s*$"
)
_JUDUL_TANPA_TGL_RE = re.compile(r"^(?P<judul>.+?)\s*\((?P<jp>[^)]+)\)\s*$")
_SECTION_MAP = [
    (re.compile(r"^Tujuan Spesifik Pertemuan"), "tujuan"),
    (re.compile(r"^Langkah Kegiatan Guru"), "langkah_guru"),
    (re.compile(r"^Langkah Kegiatan Siswa"), "langkah_siswa"),
    (re.compile(r"^Pertanyaan Pemantik"), "pertanyaan"),
    (re.compile(r"^Alat dan Bahan"), "alat_bahan"),
]


def parse_pertemuan(document):
    """Pecah bagian 'Detail Pelaksanaan' Modul Proyek STEM menjadi daftar
    pertemuan: tanggal, tahap praktik saintifik-enjinering, pengalaman
    belajar (3M), prinsip, tujuan, langkah guru/siswa, pemantik, alat-bahan."""
    hasil, current, section_key, in_detail = [], None, None, False
    for item in _iter_block_items(document):
        if item.__class__.__name__ != "Paragraph":
            continue
        txt = item.text.strip()
        if not txt:
            continue
        if _DETAIL_START_RE.match(txt):
            in_detail = True
            continue
        if not in_detail:
            continue
        if _DETAIL_END_RE.match(txt):
            break

        m = _PERT_RE.match(txt)
        if m:
            if current:
                hasil.append(current)
            rest = m.group(2).strip()
            mm = _JUDUL_TGL_RE.match(rest) or _JUDUL_PERIODE_RE.match(rest)
            if mm:
                tgl, judul, jp = mm.group("tgl"), mm.group("judul").strip(), mm.group("jp").strip()
            else:
                mm2 = _JUDUL_TANPA_TGL_RE.match(rest)
                tgl = None
                judul = mm2.group("judul").strip() if mm2 else rest
                jp = mm2.group("jp").strip() if mm2 else ""
            current = {"nomor": int(m.group(1)), "hari_tanggal": tgl, "judul": judul, "jp": jp,
                       "tahap": "", "pengalaman": [], "prinsip": [], "tujuan": [], "langkah_guru": [],
                       "langkah_siswa": [], "pertanyaan": [], "alat_bahan": []}
            section_key = None
            continue
        if current is None:
            continue
        mt = _TAHAP_RE.match(txt)
        if mt:
            current["tahap"] = mt.group(1).strip()
            section_key = None
            continue
        mp = _PENGALAMAN_RE.match(txt)
        if mp:
            current["pengalaman"] = [s.strip() for s in mp.group(1).split(",")]
            current["prinsip"] = [s.strip() for s in mp.group(2).split(",")]
            section_key = None
            continue
        matched = False
        for pat, key in _SECTION_MAP:
            if pat.match(txt):
                section_key, matched = key, True
                break
        if matched:
            continue
        is_list = (item.style is not None and item.style.name == "List Paragraph") or bool(_BULLET_RE.match(txt))
        if section_key and is_list:
            current[section_key].append(_BULLET_RE.sub("", txt))
    if current:
        hasil.append(current)
    return hasil


def _paragraph_image_blob(document, paragraph):
    m = re.search(r'r:embed="(rId\d+)"', paragraph._p.xml)
    if not m:
        return None
    try:
        return document.part.related_parts[m.group(1)].blob
    except Exception:
        return None


def _table_is_blank(table) -> bool:
    for row in table.rows:
        for cell in row.cells:
            if _cell_text(cell).strip():
                return False
    return True


def _dedupe_cells(cells):
    """Sel gabungan (merged) di python-docx berulang — rapikan untuk tampilan."""
    out = []
    for c in cells:
        t = _cell_text(c)
        out.append(t)
    return out


def render_docx_generic(document, key_prefix: str = "doc", skip_kop: bool = True):
    """Tampilkan isi dokumen .docx berurutan: judul, teks, daftar, gambar,
    kotak tips, dan tabel. Tabel kop surat (1 baris, berisi logo) dilewati."""
    idx = 0
    for item in _iter_block_items(document):
        idx += 1
        if item.__class__.__name__ == "Paragraph":
            blob = _paragraph_image_blob(document, item)
            if blob:
                try:
                    st.image(blob, width="stretch")
                except Exception:
                    pass
                continue
            txt = item.text.strip()
            if not txt:
                continue
            if _BULLET_RE.match(txt):
                st.markdown(f'<div class="doc-bullet">• {_esc(_BULLET_RE.sub("", txt))}</div>', unsafe_allow_html=True)
                continue
            is_bold = bool(item.runs) and all((r.bold or not r.text.strip()) for r in item.runs)
            heading_like = bool(re.match(r"^(\d+(\.\d+)?\.?\s|[A-Z]\.\s|BAB\s)", txt)) and len(txt) <= 110
            if heading_like or (is_bold and len(txt) <= 90):
                st.markdown(f'<div class="doc-heading">{_esc(txt)}</div>', unsafe_allow_html=True)
            elif re.match(r"^Gambar \d+\.", txt):
                st.markdown(f'<div class="doc-caption">{_esc(txt)}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="doc-text">{_esc(txt)}</div>', unsafe_allow_html=True)
            continue

        table = item
        if len(table.rows) == 0:
            continue
        ncols = len(table.columns)
        first_txt = " ".join(_cell_text(c) for c in table.rows[0].cells)
        if skip_kop and idx <= 3 and len(table.rows) == 1 and ("PEMERINTAH" in first_txt.upper() or not first_txt.strip()):
            continue  # kop surat sekolah
        if ncols == 1 and len(table.rows) <= 2:
            text = " ".join(_cell_text(c) for r in table.rows for c in r.cells).strip()
            if text:
                st.markdown(f'<div class="tip-box">💡 {_esc(text)}</div>', unsafe_allow_html=True)
            continue
        if _table_is_blank(table):
            st.markdown('<div class="worksheet-note">📄 Lembar isian (diisi saat kegiatan berlangsung).</div>',
                        unsafe_allow_html=True)
            continue
        if ncols == 2:
            rows_html = "".join(
                f'<div class="doc-kv"><div class="doc-k">{_esc(_cell_text(r.cells[0]))}</div>'
                f'<div class="doc-v">{_esc(_cell_text(r.cells[1]))}</div></div>'
                for r in table.rows if _cell_text(r.cells[0]) or _cell_text(r.cells[1])
            )
            if rows_html:
                st.markdown(f'<div class="doc-table-card">{rows_html}</div>', unsafe_allow_html=True)
            continue
        headers = _dedupe_cells(table.rows[0].cells)
        # buat header unik (kolom kalender promes berulang: Juli, Juli, ...)
        seen, uniq = {}, []
        for h in headers:
            h = h or "-"
            seen[h] = seen.get(h, 0) + 1
            uniq.append(h if seen[h] == 1 else f"{h} ({seen[h]})")
        rows = []
        for r in table.rows[1:]:
            vals = _dedupe_cells(r.cells)
            if any(vals):
                rows.append(dict(zip(uniq, vals)))
        if rows:
            st.dataframe(rows, width="stretch", hide_index=True, key=f"{key_prefix}_tbl_{idx}")


@st.cache_data(show_spinner="Membaca daftar proyek...")
def load_class_projects(kelas: int, _mtime_val: float):
    kd = KELAS_DATA[kelas]
    path = kelas_dir(kelas) / kd["daftar"]
    if docx is None:
        return None, "Modul python-docx belum terpasang."
    if not path.exists():
        return None, f"Berkas '{kd['daftar']}' tidak ditemukan."
    document = docx.Document(str(path))
    table = document.tables[0]
    headers = [_cell_text(c) for c in table.rows[0].cells]
    projects = []
    for row in table.rows[1:]:
        values = [_cell_text(c) for c in row.cells]
        if len(values) < 3 or not values[2].strip():
            continue
        projects.append({
            "smt": values[1],
            "judul": values[2],
            "rincian": [(headers[i], values[i]) for i in range(3, min(7, len(values))) if values[i]],
            "produk": values[7] if len(values) > 7 else "",
        })
    return {"headers": headers, "projects": projects}, None


def get_projects(kelas: int):
    path = kelas_dir(kelas) / KELAS_DATA[kelas]["daftar"]
    return load_class_projects(kelas, _mtime(path))


def download_btn(label: str, path: Path, key: str):
    if path.exists():
        mime = ("application/pdf" if path.suffix.lower() == ".pdf"
                else "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        st.download_button(label, data=path.read_bytes(), file_name=path.name, mime=mime,
                           width="stretch", key=key)


# ============================================================================
# Halaman: Login
# ============================================================================
def render_login():
    st.markdown(
        f"""
        <div class="hero-banner">
            <div class="hero-eyebrow">🧪 LMS STEM • {GUGUS['nama']}</div>
            <div class="hero-title">Masuk ke Aplikasi</div>
            <div class="hero-subtitle">{GUGUS['wilayah']} • TP {GUGUS['tahun_pelajaran']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    chips = "".join(
        f'<span class="school-chip" style="border-color:{SEKOLAH_WARNA[s]};color:{SEKOLAH_WARNA[s]}">{s}</span>'
        for s in SEKOLAH
    )
    card(f"<p>Sekolah anggota gugus:</p><div class='school-chip-row'>{chips}</div>")

    role = st.radio("Masuk sebagai", ROLES, horizontal=True, key="login_role")
    with st.form("form_login"):
        sekolah = None
        if role != ROLE_PENGURUS:
            sekolah = st.selectbox("Asal Sekolah", SEKOLAH, key="login_sekolah")
        nama = st.text_input("Nama Lengkap", placeholder="Contoh: Ibu Siti Nurhaliza, S.Pd.")
        kelas = None
        if role == ROLE_GURU:
            kelas = st.selectbox("Kelas yang Diampu", list(range(1, 7)), format_func=lambda i: f"Kelas {i}")
        submitted = st.form_submit_button("Masuk →", width="stretch")

    st.markdown(
        '<div class="footer-note">Login sederhana tanpa kata sandi. Peran menentukan menu: '
        'Portal Supervisi untuk Kepala Sekolah & Pengurus KKG/Pengawas.</div>',
        unsafe_allow_html=True,
    )

    if submitted:
        if not nama.strip():
            st.error("Nama tidak boleh kosong.")
            return
        st.session_state.auth = {"role": role, "name": nama.strip(), "sekolah": sekolah, "kelas": kelas}
        if kelas:
            st.session_state.kelas_terpilih = kelas
        st.session_state.page = "landing"
        st.rerun()


# ============================================================================
# Navigasi atas
# ============================================================================
NAV_ALL = {
    "🏠 Beranda": "landing",
    "📚 Modul": "modul_kelas",
    "📖 Panduan": "panduan",
    "🗂️ Administrasi": "administrasi",
    "📊 Progres": "progres",
    "👨‍💼 Supervisi": "supervisi",
}


def render_top_nav():
    auth = st.session_state.auth
    pages = dict(NAV_ALL)
    if auth["role"] == ROLE_GURU:
        pages.pop("👨‍💼 Supervisi")
    labels = list(pages.keys())
    key_to_label = {v: k for k, v in pages.items()}
    current = key_to_label.get(st.session_state.page, labels[0])

    icon = {"Guru Kelas": "🧑‍🏫", "Kepala Sekolah": "👨‍💼"}.get(auth["role"], "🧭")
    sub = auth["sekolah"] or "Pengurus Gugus"
    if auth.get("kelas"):
        sub += f" • Kelas {auth['kelas']}"
    c1, c2 = st.columns([4, 1.3])
    with c1:
        st.markdown(f'<div class="user-chip">{icon} {_esc(auth["name"])} — {_esc(sub)}</div>', unsafe_allow_html=True)
    with c2:
        if st.button("Keluar", key="btn_logout", width="stretch"):
            st.session_state.auth = None
            st.session_state.page = "landing"
            st.rerun()

    with st.container(key="top-nav"):
        choice = st.radio("Menu", labels, index=labels.index(current), horizontal=True,
                          label_visibility="collapsed", key=f"nav_radio_{st.session_state.page}")
    if pages[choice] != st.session_state.page:
        st.session_state.page = pages[choice]
        st.rerun()


# ============================================================================
# Halaman: Beranda
# ============================================================================
def render_landing():
    auth = st.session_state.auth
    total_proyek = sum(len(v["proyek"]) for v in KELAS_DATA.values())
    total_panduan = sum(1 for v in KELAS_DATA.values() for p in v["proyek"].values() if p["panduan"])

    st.markdown(
        f"""
        <div class="hero-banner">
            <div class="hero-eyebrow">🧪 LMS STEM • {GUGUS['nama']}</div>
            <div class="hero-title">{OVERVIEW['judul']}</div>
            <div class="hero-subtitle">{OVERVIEW['subjudul']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div class="stat-grid">
            <div class="stat"><div class="stat-num">{len(SEKOLAH)}</div><div class="stat-lbl">Sekolah</div></div>
            <div class="stat"><div class="stat-num">6</div><div class="stat-lbl">Kelas</div></div>
            <div class="stat"><div class="stat-num">{total_proyek}</div><div class="stat-lbl">Modul Proyek</div></div>
            <div class="stat"><div class="stat-num">{total_panduan}</div><div class="stat-lbl">Panduan Produk</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    section("📘", "Gambaran Umum")
    card(f"<p>{OVERVIEW['definisi']}</p><p>{OVERVIEW['pendekatan']}</p>")
    goals = "".join(
        f'<div class="goal-item"><span class="goal-bullet">{i+1}</span><span>{g}</span></div>'
        for i, g in enumerate(OVERVIEW["tujuan"])
    )
    card(goals)

    section("🧭", "Tiga Karakteristik Utama STEM")
    st.markdown('<div class="siklus-grid">' + "".join(
        f'<div class="siklus-tile"><div class="siklus-head">{ic} {t}</div><div class="siklus-body">{d}</div></div>'
        for ic, t, d in KARAKTERISTIK) + '</div>', unsafe_allow_html=True)

    section("⚙️", "Praktik Saintifik dan Enjinering")
    st.markdown('<div class="tahap-flow">' + "".join(
        f'<div class="tahap-step"><span class="tahap-no">{i+1}</span>{t[0]}</div>'
        for i, t in enumerate(TAHAP_PRAKTIK)) + '<div class="tahap-loop">↻ iteratif: uji → desain ulang → uji</div></div>',
        unsafe_allow_html=True)
    st.markdown(f'<div class="footer-note">{TAHAP_CATATAN}</div>', unsafe_allow_html=True)
    if st.button("📖 Pelajari Panduan STEM selengkapnya", width="stretch", key="cta_panduan"):
        _goto("panduan")
    with st.expander("🌱 Penguatan 8 Dimensi Profil Lulusan melalui Proyek STEM"):
        for nama, isi in PROFIL_LULUSAN:
            st.markdown(f"**{nama}** — {isi}")

    section("🏫", "Sekolah Anggota Gugus")
    progress = load_progress()
    rows = []
    for s in SEKOLAH:
        summ = school_summary(progress, s)
        done = sum(v[0] for v in summ.values())
        tot = sum(v[2] for v in summ.values())
        pct = int(round(100 * done / tot)) if tot else 0
        mine = " • sekolah Anda" if auth.get("sekolah") == s else ""
        rujukan = " • penyusun modul rujukan" if s == SEKOLAH_PENYUSUN_RUJUKAN else ""
        rows.append(
            f'<div class="school-card" style="border-left-color:{SEKOLAH_WARNA[s]}">'
            f'<div class="school-name">{s}<span class="school-tag">{mine}{rujukan}</span></div>'
            f'<div class="bar"><div class="bar-fill" style="width:{pct}%;background:{SEKOLAH_WARNA[s]}"></div></div>'
            f'<div class="school-meta">{done} dari {tot} proyek terlaksana ({pct}%)</div></div>'
        )
    st.markdown("".join(rows), unsafe_allow_html=True)

    section("🤝", "Pertemuan KKG STEM Gugus")
    card(
        f"""<div class="info-grid">
            <div class="label">Tema</div><div class="value">{EVENT['tema']}</div>
            <div class="label">Waktu</div><div class="value">{EVENT['waktu']}</div>
            <div class="label">Sasaran</div><div class="value">{EVENT['sasaran']}</div>
            <div class="label">Kelompok</div><div class="value">{EVENT['kelompok']}</div>
        </div>"""
    )
    with st.expander("🕒 Lini masa (rundown) kegiatan"):
        for item in AGENDA:
            color = PRINSIP_WARNA.get(item["prinsip"], "#9CA3AF")
            badge = f'<span class="badge" style="background:{color}">{item["prinsip"]}</span>' if item["prinsip"] != "—" else ""
            st.markdown(
                f"""<div class="timeline-item" style="border-left-color:{color}">
                    <div class="timeline-time">{item['waktu']}</div>
                    <div class="timeline-activity">{item['kegiatan']}</div>
                    <div class="timeline-meta">{item['bentuk']} • PJ: {item['penanggung_jawab']}</div>{badge}
                </div>""",
                unsafe_allow_html=True,
            )
    with st.expander("👥 Proyek yang dipraktikkan tiap kelompok kelas"):
        for kk in KELOMPOK_KELAS:
            st.markdown(f"**{kk['kelas']}** ({kk['fase']}) — {kk['modul']}")
    st.markdown(f'<div class="footer-note">Sumber: {EVENT["referensi"]} • {OVERVIEW["referensi"]}</div>',
                unsafe_allow_html=True)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("📚 Buka Modul Kelas", width="stretch", key="cta_modul"):
            _goto("modul_kelas")
    with c2:
        if st.button("📊 Lihat Progres Gugus", width="stretch", key="cta_progres"):
            _goto("progres")


# ============================================================================
# Halaman: Modul Kelas
# ============================================================================
def kelas_picker(prefix: str):
    with st.container(key=f"kelas-menu-{prefix}"):
        cols = st.columns(6, gap="small")
        for i, col in enumerate(cols, start=1):
            with col:
                if st.button(str(i), key=f"{prefix}_kelas_{i}", width="stretch",
                             type="primary" if st.session_state.kelas_terpilih == i else "secondary"):
                    st.session_state.kelas_terpilih = i
                    st.rerun()
    return st.session_state.kelas_terpilih


def _pert_section(title: str, icon: str, items: list):
    if items:
        st.markdown(f'<div class="pert-section-label">{icon} {title}</div>', unsafe_allow_html=True)
        st.markdown('<ul class="pert-list">' + "".join(f"<li>{_esc(x)}</li>" for x in items) + "</ul>",
                    unsafe_allow_html=True)


def render_pertemuan_detail(p: dict, total: int):
    tgl = p["hari_tanggal"] or "Tanggal menyesuaikan kalender sekolah"
    st.markdown(
        f"""<div class="pert-detail-card">
            <div class="pert-detail-header">🗓️ Pertemuan {p['nomor']} dari {total} — {tgl}</div>
            <div class="pert-detail-title">{_esc(p['judul'])}</div>
            {f'<div class="pert-detail-jp">⏱️ {p["jp"]}</div>' if p.get("jp") else ''}
        </div>""",
        unsafe_allow_html=True,
    )
    badges = []
    if p.get("tahap"):
        badges.append(f'<span class="pert-badge pert-badge-tahap">🧭 {_esc(p["tahap"])}</span>')
        low = p["tahap"].lower()
        nomor = [str(i + 1) for i, t in enumerate(TAHAP_PRAKTIK) if t[0].lower() in low]
        if nomor:
            badges.append(f'<span class="pert-badge pert-badge-tahap">⚙️ Tahap praktik ke-{", ".join(nomor)} dari 7</span>')
    for x in p.get("pengalaman", []):
        c = PENGALAMAN_WARNA.get(x, "#0EA5E9")
        badges.append(f'<span class="pert-badge" style="background:{c}1F;color:{c};border-color:{c}66">💡 {x}</span>')
    for x in p.get("prinsip", []):
        c = PRINSIP_WARNA.get(x, "#9CA3AF")
        badges.append(f'<span class="pert-badge" style="background:{c}1F;color:{c};border-color:{c}66">🌱 {x}</span>')
    if badges:
        st.markdown(f'<div class="pert-badge-row">{"".join(badges)}</div>', unsafe_allow_html=True)
    _pert_section("Tujuan Spesifik Pertemuan", "🎯", p["tujuan"])
    _pert_section("Langkah Kegiatan Guru", "👩‍🏫", p["langkah_guru"])
    _pert_section("Langkah Kegiatan Murid", "🧒", p["langkah_siswa"])
    _pert_section("Pertanyaan Pemantik", "❓", p["pertanyaan"])
    _pert_section("Alat dan Bahan", "🧰", p["alat_bahan"])



# ----------------------------------------------------------------------------
# Kesesuaian modul dengan Panduan STEM (Tabel 10 & 7 tahap praktik)
# ----------------------------------------------------------------------------
_TANTANGAN_HEAD = {"b": "konten", "c": "kriteria", "d": "batasan"}


def extract_tantangan(document) -> dict:
    """Ambil Konten Masalah, Kriteria, dan Batasan dari bagian 3.1 modul."""
    out = {"konten": [], "kriteria": [], "batasan": []}
    cur = None
    for p in document.paragraphs:
        t = p.text.strip()
        if not t:
            continue
        m = re.match(r"^([a-j])\.\s", t)
        if m:
            cur = _TANTANGAN_HEAD.get(m.group(1))
            if m.group(1) > "d":
                if out["batasan"]:
                    break
            continue
        if re.match(r"^\d+(\.\d+)?\.?\s", t) and cur:
            break
        if cur:
            out[cur].append(_BULLET_RE.sub("", t))
    return out


def cek_kesesuaian(document, pertemuan) -> dict:
    paras = [p.text.strip() for p in document.paragraphs if p.text.strip()]
    ident = _get_identitas_dict(document)
    komponen = []
    for grup, nama, kunci, wajib in KOMPONEN_PERENCANAAN:
        if kunci == "Dimensi Profil Lulusan":
            ada = bool(ident.get("Dimensi Profil Lulusan"))
        else:
            ada = any((kunci in x and len(x) < 70) or x.lower().startswith(kunci.lower()) for x in paras) \
                or any(re.match(rf"^[a-j]\.\s*{re.escape(kunci)}", x) for x in paras)
        komponen.append((grup, nama, ada, wajib))
    gabung = " ".join(p["tahap"].lower() for p in pertemuan)
    tahap = [(t[0], t[0].lower() in gabung) for t in TAHAP_PRAKTIK]
    peng = {g for p in pertemuan for g in p["pengalaman"]}
    pengalaman = [(n, n in peng) for n, _ in PENGALAMAN_BELAJAR]
    return {"komponen": komponen, "tahap": tahap, "pengalaman": pengalaman,
            "rubrik": any("Rubrik" in x for x in paras)}


def render_kesesuaian(hasil: dict):
    ok = lambda b: "✅" if b else "⚠️"
    wajib_ok = all(a for _, _, a, w in hasil["komponen"] if w)
    tahap_ok = all(a for _, a in hasil["tahap"])
    peng_ok = all(a for _, a in hasil["pengalaman"])
    skor = sum([wajib_ok, tahap_ok, peng_ok, hasil["rubrik"]])
    warna = "#16A34A" if skor == 4 else "#F59E0B"
    st.markdown(f'<div class="status-pill" style="border-color:{warna};color:{warna};background:{warna}14">'
                f'{"Sesuai Panduan STEM 2025" if skor == 4 else "Perlu dilengkapi"} — {skor}/4 aspek terpenuhi</div>',
                unsafe_allow_html=True)
    st.markdown("**Komponen Perencanaan (Tabel 10)**")
    st.markdown("".join(f'<div class="cek-row">{ok(a)} <b>{g}</b> — {n}</div>' for g, n, a, _ in hasil["komponen"]),
                unsafe_allow_html=True)
    st.markdown("**7 Tahap Praktik Saintifik dan Enjinering (seluruh pertemuan)**")
    st.markdown("".join(f'<div class="cek-row">{ok(a)} {i+1}. {n}</div>' for i, (n, a) in enumerate(hasil["tahap"])),
                unsafe_allow_html=True)
    st.markdown("**Pengalaman Belajar & Asesmen**")
    st.markdown("".join(f'<div class="cek-row">{ok(a)} {n}</div>' for n, a in hasil["pengalaman"])
                + f'<div class="cek-row">{ok(hasil["rubrik"])} Rubrik penilaian (asesmen autentik)</div>',
                unsafe_allow_html=True)


def render_tantangan(t: dict):
    if not any(t.values()):
        return
    html = '<div class="tantangan-card"><div class="tantangan-title">🎯 Tantangan Proyek (Panduan STEM: konten masalah, kriteria, batasan)</div>'
    if t["konten"]:
        html += f'<div class="tantangan-sub">Konten Masalah</div><div class="tantangan-text">{_esc(" ".join(t["konten"]))}</div>'
    if t["kriteria"]:
        html += '<div class="tantangan-sub">✔️ Kriteria keberhasilan</div><ul>' + "".join(f"<li>{_esc(x)}</li>" for x in t["kriteria"]) + "</ul>"
    if t["batasan"]:
        html += '<div class="tantangan-sub">⛔ Batasan</div><ul>' + "".join(f"<li>{_esc(x)}</li>" for x in t["batasan"]) + "</ul>"
    st.markdown(html + "</div>", unsafe_allow_html=True)


def render_project_detail(kelas: int, proj: dict):
    auth = st.session_state.auth
    judul = proj["judul"]
    docs_info = KELAS_DATA[kelas]["proyek"].get(judul, {})
    modul_path = kelas_dir(kelas) / docs_info["modul"] if docs_info.get("modul") else None
    panduan_path = kelas_dir(kelas) / docs_info["panduan"] if docs_info.get("panduan") else None
    key = f"k{kelas}_{_slug(judul)}"

    document, err = open_doc(modul_path) if modul_path else (None, "Modul belum tersedia.")
    identitas = _get_identitas_dict(document) if document else {}
    pertemuan = parse_pertemuan(document) if document else []

    st.markdown(
        f"""<div class="project-card project-card-active">
            <span class="project-chip">Kelas {kelas} • {FASE[kelas]} • Semester {proj['smt']}</span>
            <div class="project-title">{_esc(identitas.get('Judul Proyek', judul))}</div>
            {f'<div class="project-produk">🎯 <b>Produk akhir:</b> {_esc(proj["produk"])}</div>' if proj["produk"] else ''}
            {f'<div class="project-produk">⏱️ {_esc(identitas.get("Alokasi Waktu",""))}</div>' if identitas.get("Alokasi Waktu") else ''}
            {f'<div class="project-produk">🌱 {_esc(identitas.get("Dimensi Profil Lulusan",""))}</div>' if identitas.get("Dimensi Profil Lulusan") else ''}
        </div>""",
        unsafe_allow_html=True,
    )

    if auth.get("sekolah"):
        s = get_status(load_progress(), auth["sekolah"], kelas, judul).get("status", "Belum dimulai")
        st.markdown(
            f'<div class="status-pill" style="background:{STATUS_WARNA[s]}22;color:{STATUS_WARNA[s]};'
            f'border-color:{STATUS_WARNA[s]}">Status di {auth["sekolah"]}: <b>{s}</b></div>',
            unsafe_allow_html=True,
        )

    if document:
        render_tantangan(extract_tantangan(document))

    sb = STORYBOOK_LINKS.get(judul)
    if sb:
        st.link_button("📖 Baca Buku Cerita (Storybook) →", sb, width="stretch", key=f"sb_{key}")

    tab_names = ["🗓️ Per Pertemuan", "📘 Modul Lengkap"]
    if panduan_path:
        tab_names.append("🛠️ Panduan Produk")
    tab_names += ["📌 CP & Integrasi", "✅ Kesesuaian Panduan"]
    tabs = st.tabs(tab_names)

    with tabs[0]:
        if err:
            st.error(err)
        elif not pertemuan:
            st.info("Rincian per pertemuan tidak ditemukan pada modul ini — lihat tab Modul Lengkap.")
        else:
            if identitas.get("Waktu Pelaksanaan"):
                st.caption(f"📅 Waktu pelaksanaan rujukan: {identitas['Waktu Pelaksanaan']} — "
                           "sesuaikan dengan kalender pendidikan sekolah Anda.")
            sel_key = f"pert_sel_{key}"
            if sel_key not in st.session_state:
                st.session_state[sel_key] = pertemuan[0]["nomor"]
            with st.container(key=f"pert-menu-{key}"):
                cols = st.columns(len(pertemuan), gap="small")
                for col, p in zip(cols, pertemuan):
                    with col:
                        if st.button(f"P{p['nomor']}", key=f"btnp_{key}_{p['nomor']}", width="stretch",
                                     type="primary" if st.session_state[sel_key] == p["nomor"] else "secondary"):
                            st.session_state[sel_key] = p["nomor"]
                            st.rerun()
            chosen = next((p for p in pertemuan if p["nomor"] == st.session_state[sel_key]), pertemuan[0])
            render_pertemuan_detail(chosen, len(pertemuan))

    with tabs[1]:
        if err:
            st.error(err)
        else:
            if modul_path:
                download_btn("⬇️ Unduh Modul (Word)", modul_path, f"dl_modul_{key}")
            st.markdown(
                f'<div class="footer-note">Modul rujukan gugus disusun oleh {SEKOLAH_PENYUSUN_RUJUKAN}. '
                'Sekolah lain cukup menyesuaikan identitas sekolah, nama guru, dan tanggal.</div>',
                unsafe_allow_html=True,
            )
            if st.toggle("Tampilkan isi modul di sini", key=f"tg_modul_{key}"):
                render_docx_generic(document, key_prefix=f"{key}_modul")

    ti = 2
    if panduan_path:
        with tabs[ti]:
            download_btn("⬇️ Unduh Panduan Guru (Word)", panduan_path, f"dl_pan_{key}")
            pdoc, perr = open_doc(panduan_path)
            if perr:
                st.error(perr)
            else:
                render_docx_generic(pdoc, key_prefix=f"{key}_panduan")
        ti += 1

    with tabs[ti]:
        for h, v in proj["rincian"]:
            st.markdown(f"**{h}**")
            st.caption(v)

    with tabs[ti + 1]:
        if document:
            render_kesesuaian(cek_kesesuaian(document, pertemuan))
            st.caption("Pemeriksaan otomatis terhadap Panduan Pembelajaran STEM Kemendikdasmen 2025 "
                       "(Tabel 10 Komponen Perencanaan, Gambar 7 Praktik Saintifik dan Enjinering).")


def render_modul_kelas():
    auth = st.session_state.auth
    section("📚", "Modul Proyek STEM per Kelas")
    if auth["role"] == ROLE_GURU:
        card(f"<p>Default menampilkan kelas yang Anda ampu (<b>Kelas {auth['kelas']}</b>). "
             "Anda tetap dapat melihat proyek kelas lain untuk berbagi praktik.</p>")
    kelas = kelas_picker("mk")

    data, err = get_projects(kelas)
    if err:
        st.error(err)
        return
    projects = data["projects"]

    c1, c2 = st.columns([1, 2])
    with c1:
        smt = st.selectbox("Semester", ["Semua", "1", "2"], key=f"smt_{kelas}")
    with c2:
        q = st.text_input("Cari proyek", placeholder="mis. energi, pecahan, peta…", key=f"q_{kelas}")
    filtered = [p for p in projects if (smt == "Semua" or p["smt"] == smt)
                and (not q or q.lower() in (p["judul"] + " " + p["produk"]).lower())]

    progress = load_progress()
    sekolah = auth.get("sekolah")
    st.caption(f"{len(filtered)} dari {len(projects)} proyek • Kelas {kelas} ({FASE[kelas]})")

    rows = []
    for i, p in enumerate(filtered):
        s = get_status(progress, sekolah, kelas, p["judul"]).get("status", "Belum dimulai") if sekolah else None
        dot = f'<span class="dot" style="background:{STATUS_WARNA[s]}" title="{s}"></span>' if s else ""
        extra = " 🛠️" if KELAS_DATA[kelas]["proyek"][p["judul"]]["panduan"] else ""
        extra += " 📖" if p["judul"] in STORYBOOK_LINKS else ""
        rows.append(f'<div class="proj-row">{dot}<span class="proj-smt">S{p["smt"]}</span>'
                    f'<span class="proj-name">{_esc(p["judul"])}{extra}</span></div>')
    if rows:
        st.markdown(f'<div class="proj-list">{"".join(rows)}</div>', unsafe_allow_html=True)
        st.markdown('<div class="footer-note">🛠️ ada panduan pembuatan produk • 📖 ada storybook'
                    + (' • titik warna = status di sekolah Anda' if sekolah else '') + '</div>',
                    unsafe_allow_html=True)
    else:
        st.info("Tidak ada proyek yang cocok dengan filter.")
        return

    section("🔎", "Detail Proyek")
    titles = [p["judul"] for p in filtered]
    pilih = st.selectbox("Pilih proyek", titles, key=f"pilih_{kelas}_{smt}_{q}", label_visibility="collapsed")
    proj = next(p for p in filtered if p["judul"] == pilih)
    render_project_detail(kelas, proj)



# ============================================================================
# Halaman: Panduan STEM (ringkasan Panduan Pembelajaran STEM 2025)
# ============================================================================
def render_panduan():
    section("📖", "Ringkasan Panduan Pembelajaran STEM 2025")
    card(f"<p>{OVERVIEW['definisi']}</p><p><b>Tujuan:</b> {OVERVIEW['tujuan_stem']}</p>")
    download_btn("⬇️ Unduh Panduan Lengkap (PDF)", umum_path("Panduan_Pembelajaran_STEM_Kemendikdasmen_2025.pdf"), "dl_panduan_pdf")
    t1, t2, t3, t4, t5 = st.tabs(["💡 Konsep", "⚙️ Praktik S–E", "📝 Perencanaan", "📊 Asesmen", "👥 Peran"])
    with t1:
        st.markdown("**Tiga karakteristik utama**")
        for ic, t, d in KARAKTERISTIK:
            card(f"<p><b>{ic} {t}</b></p><p class='muted'>{d}</p>")
        st.markdown("**Peran setiap komponen STEM**")
        st.markdown('<div class="siklus-grid">' + "".join(
            f'<div class="siklus-tile"><div class="siklus-head">{h} — {n}</div><div class="siklus-body">{d}</div></div>'
            for h, n, d in PERAN_KOMPONEN) + "</div>", unsafe_allow_html=True)
        st.markdown("**Pengalaman belajar pembelajaran mendalam dalam STEM**")
        for n, d in PENGALAMAN_BELAJAR:
            st.markdown(f"- **{n}** — {d}")
        st.markdown("Prinsip: **Berkesadaran, Bermakna, Menggembirakan**.")
        st.markdown("**Implementasi**")
        for n, d in IMPLEMENTASI:
            st.markdown(f"- **{n}** — {d}")
        with st.expander("🌱 Penguatan 8 Dimensi Profil Lulusan (Tabel 2)"):
            for nama, isi in PROFIL_LULUSAN:
                st.markdown(f"**{nama}** — {isi}")
    with t2:
        st.markdown(f'<div class="footer-note" style="text-align:left">{TAHAP_CATATAN}</div>', unsafe_allow_html=True)
        for i, (n, d, fa, _) in enumerate(TAHAP_PRAKTIK):
            card(f"<p><b>{i+1}. {n}</b></p><p>{d}</p><p class='muted'>Fase A / SD awal: {fa}</p>")
        with st.expander("Contoh model pembelajaran yang mengakomodasi praktik S–E"):
            for n, d in MODEL_PEMBELAJARAN:
                st.markdown(f"- **{n}**: {d}")
    with t3:
        st.markdown("**Langkah merancang pembelajaran STEM**")
        for i, (n, d) in enumerate(LANGKAH_PERENCANAAN):
            st.markdown(f"{i+1}. **{n}** {d}", unsafe_allow_html=True)
        st.markdown("**Komponen Perencanaan Pembelajaran STEM (Tabel 10)**")
        st.dataframe([{"Kelompok": g, "Komponen": n, "Keterangan": "wajib" if w else "opsional"}
                      for g, n, _, w in KOMPONEN_PERENCANAAN], width="stretch", hide_index=True, key="tbl10")
        st.caption("Bila perencanaan STEM sudah disusun, guru tidak perlu membuat perencanaan terpisah "
                   "untuk mata pelajaran yang telah terintegrasi.")
    with t4:
        st.markdown("**Contoh rancangan asesmen per tahap (Tabel 11)**")
        st.dataframe([{"Tahap": n, "Asesmen & instrumen": a} for n, _, _, a in TAHAP_PRAKTIK],
                     width="stretch", hide_index=True, key="tbl11")
        st.caption("Asesmen formatif dan sumatif dengan penekanan autentik & holistik. "
                   "Untuk SD, asesmen pembelajaran STEM dilakukan menyeluruh oleh guru kelas.")
    with t5:
        for n, items in PERAN_PEMANGKU:
            card(f"<p><b>{n}</b></p><ul>" + "".join(f"<li>{x}</li>" for x in items) + "</ul>")
    st.markdown(f'<div class="footer-note">Sumber: {OVERVIEW["referensi"]}</div>', unsafe_allow_html=True)

# ============================================================================
# Halaman: Administrasi
# ============================================================================
def render_administrasi():
    section("🗂️", "Administrasi & Dokumen STEM")
    tab_kelas, tab_umum = st.tabs(["📁 Per Kelas", "🏛️ Dokumen Gugus"])

    with tab_kelas:
        card("<p>Template administrasi pembelajaran proyek STEM per kelas: program tahunan, program semester, "
             f"jurnal, daftar nilai, observasi profil & refleksi, dan laporan. Contoh terisi dari "
             f"{SEKOLAH_PENYUSUN_RUJUKAN} — unduh lalu sesuaikan identitas sekolah dan guru.</p>")
        kelas = kelas_picker("adm")
        items = [(kode, nama, pat.format(k=kelas)) for kode, nama, pat in ADMIN_DOCS]
        items.append(("AB", "Daftar Alat dan Bahan STEM", KELAS_DATA[kelas]["alat"]))
        items.append(("DP", "Daftar Proyek STEM", KELAS_DATA[kelas]["daftar"]))
        for kode, nama, fname in items:
            path = kelas_dir(kelas) / fname
            c1, c2 = st.columns([3, 1.4])
            with c1:
                st.markdown(f'<div class="doc-row"><span class="doc-code">{kode}</span>{nama}</div>',
                            unsafe_allow_html=True)
            with c2:
                download_btn("⬇️ Unduh", path, f"dl_adm_{kelas}_{kode}")
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        lihat = st.selectbox("👁️ Pratinjau dokumen", ["—"] + [n for _, n, _ in items], key=f"prev_adm_{kelas}")
        if lihat != "—":
            fname = next(f for _, n, f in items if n == lihat)
            document, err = open_doc(kelas_dir(kelas) / fname)
            if err:
                st.error(err)
            else:
                render_docx_generic(document, key_prefix=f"adm_{kelas}_{_slug(lihat)}")

    with tab_umum:
        for icon, nama, fname, ket in DOKUMEN_UMUM:
            card(f"<p><b>{icon} {nama}</b></p><p class='muted'>{ket}</p>")
            download_btn(f"⬇️ Unduh {fname.rsplit('.', 1)[1].upper()}", umum_path(fname), f"dl_umum_{_slug(fname)}")
        docx_umum = [(n, f) for _, n, f, _ in DOKUMEN_UMUM if f.endswith(".docx")]
        lihat = st.selectbox("👁️ Pratinjau dokumen", ["—"] + [n for n, _ in docx_umum], key="prev_umum")
        if lihat != "—":
            fname = dict(docx_umum)[lihat]
            document, err = open_doc(umum_path(fname))
            if err:
                st.error(err)
            else:
                render_docx_generic(document, key_prefix=f"umum_{_slug(fname)}")


# ============================================================================
# Halaman: Progres Gugus
# ============================================================================
def render_rekap_gugus(progress: dict):
    rows = []
    for s in SEKOLAH:
        summ = school_summary(progress, s)
        row = {"Sekolah": s}
        done_all = tot_all = 0
        for k in range(1, 7):
            d, r, t = summ[k]
            row[f"K{k}"] = f"{d}/{t}" + (f" (+{r})" if r else "")
            done_all += d
            tot_all += t
        row["Terlaksana"] = f"{round(100 * done_all / tot_all)}%"
        rows.append(row)
    st.dataframe(rows, width="stretch", hide_index=True, key="rekap_gugus")
    st.caption("Format: terlaksana/jumlah proyek; (+n) = sedang berjalan.")


def render_update_form(sekolah: str, kelas: int, editor: str):
    data, err = get_projects(kelas)
    if err:
        st.error(err)
        return
    progress = load_progress()
    if st.session_state.pop("flash_prog", None):
        st.success("✅ Progres proyek tersimpan.")
    with st.form(f"form_prog_{_slug(sekolah)}_{kelas}"):
        st.markdown(f"**{sekolah} — Kelas {kelas}**")
        vals = {}
        for p in data["projects"]:
            cur = get_status(progress, sekolah, kelas, p["judul"])
            st.markdown(f'<div class="indikator-text"><b>S{p["smt"]}</b> • {_esc(p["judul"])}</div>',
                        unsafe_allow_html=True)
            c1, c2 = st.columns([1.3, 1])
            k = f"{_slug(sekolah)}_{kelas}_{_slug(p['judul'])}"
            with c1:
                status = st.selectbox("Status", STATUS_PROYEK, label_visibility="collapsed", key=f"st_{k}",
                                      index=STATUS_PROYEK.index(cur.get("status", "Belum dimulai")))
            with c2:
                tgl_def = None
                if cur.get("tanggal"):
                    try:
                        tgl_def = datetime.date.fromisoformat(cur["tanggal"])
                    except ValueError:
                        tgl_def = None
                tgl = st.date_input("Tanggal", value=tgl_def, label_visibility="collapsed", key=f"tg_{k}",
                                    format="DD/MM/YYYY")
            catatan = st.text_input("Catatan", value=cur.get("catatan", ""), key=f"ct_{k}",
                                    placeholder="Catatan singkat (opsional)", label_visibility="collapsed")
            vals[p["judul"]] = (status, tgl, catatan)
        ok = st.form_submit_button("💾 Simpan Progres", width="stretch")
    if ok:
        for judul, (status, tgl, catatan) in vals.items():
            cur = get_status(load_progress(), sekolah, kelas, judul)
            new_tgl = tgl.isoformat() if tgl else ""
            if (cur.get("status", "Belum dimulai"), cur.get("tanggal", ""), cur.get("catatan", "")) != (status, new_tgl, catatan):
                set_status(sekolah, kelas, judul, status=status, tanggal=new_tgl, catatan=catatan, oleh=editor)
        st.session_state["flash_prog"] = "✅ Progres proyek tersimpan."
        st.rerun()


def render_upload(sekolah: str, kelas: int, editor: str):
    data, err = get_projects(kelas)
    if err:
        return
    judul = st.selectbox("Proyek", [p["judul"] for p in data["projects"]], key=f"up_proj_{_slug(sekolah)}_{kelas}")
    files = st.file_uploader("Foto kegiatan / produk / laporan (boleh lebih dari satu)",
                             type=["png", "jpg", "jpeg", "webp", "pdf", "docx"], accept_multiple_files=True,
                             key=f"uploader_{_slug(sekolah)}_{kelas}")
    if st.button("📤 Unggah Bukti", width="stretch", key=f"btn_up_{_slug(sekolah)}_{kelas}", disabled=not files):
        names = [save_upload(sekolah, kelas, judul, f, editor) for f in files]
        st.success(f"✅ {len(names)} berkas tersimpan untuk proyek '{judul}'.")


def render_galeri(sekolah: str, kelas: int):
    progress = load_progress()
    kelas_rec = progress.get(sekolah, {}).get(str(kelas), {})
    bukti = [(j, b) for j, rec in kelas_rec.items() for b in rec.get("bukti", [])]
    if not bukti:
        st.info("Belum ada bukti yang diunggah untuk kelas ini.")
        return
    imgs = [(j, b) for j, b in bukti if Path(b["berkas"]).suffix.lower() in IMG_EXT]
    others = [(j, b) for j, b in bukti if Path(b["berkas"]).suffix.lower() not in IMG_EXT]
    if imgs:
        cols = st.columns(3)
        for i, (j, b) in enumerate(imgs):
            p = STORAGE_DIR / b["berkas"]
            if p.exists():
                with cols[i % 3]:
                    st.image(str(p), caption=f"{j[:40]} • {b['waktu']}", width="stretch")
    for i, (j, b) in enumerate(others):
        p = STORAGE_DIR / b["berkas"]
        if p.exists():
            st.download_button(f"📄 {b['nama_asli']} — {j[:40]}", data=p.read_bytes(), file_name=b["nama_asli"],
                               width="stretch", key=f"dl_bukti_{_slug(sekolah)}_{kelas}_{i}")


def render_progres():
    auth = st.session_state.auth
    progress = load_progress()
    section("📊", "Rekap Keterlaksanaan Proyek STEM Gugus")
    render_rekap_gugus(progress)

    # Tentukan cakupan sekolah & kelas yang boleh diperbarui
    if auth["role"] == ROLE_PENGURUS:
        sekolah = st.selectbox("Sekolah", SEKOLAH, key="prog_sekolah")
    else:
        sekolah = auth["sekolah"]

    if auth["role"] == ROLE_GURU:
        kelas = auth["kelas"]
        st.markdown(f'<div class="kelas-chip">🧑‍🏫 {sekolah} • Kelas {kelas}</div>', unsafe_allow_html=True)
    else:
        kelas = st.selectbox("Kelas", list(range(1, 7)), format_func=lambda i: f"Kelas {i}", key="prog_kelas")

    t1, t2, t3 = st.tabs(["✏️ Perbarui Status", "📤 Unggah Bukti", "🖼️ Galeri"])
    with t1:
        render_update_form(sekolah, kelas, auth["name"])
    with t2:
        render_upload(sekolah, kelas, auth["name"])
    with t3:
        render_galeri(sekolah, kelas)
    st.markdown('<div class="footer-note">Data progres & unggahan tersimpan di folder <code>storage/</code> '
                'aplikasi. Jika aplikasi dijalankan online (Streamlit Cloud), data dapat terhapus saat aplikasi '
                'di-reboot — unduh/arsipkan bukti penting secara berkala.</div>', unsafe_allow_html=True)


# ============================================================================
# Portal Supervisi (dibaca dari Program_Supervisi_Kepala_Sekolah_STEM.docx)
# ============================================================================
@st.cache_data(show_spinner="Membaca program supervisi...")
def load_supervisi_full(_mtime_val: float):
    path = umum_path(SUPERVISI_FILE)
    if not path.exists():
        return None, f"Berkas '{SUPERVISI_FILE}' tidak ditemukan."
    document = docx.Document(str(path))
    tujuan, capture_tujuan = [], False
    current_lamp, last_heading = None, None
    capturing_kes, kes_buf = False, []
    state = {
        1: {"identitas": [], "skala": "", "kategori": [], "catatan_aspek": []},
        2: {"identitas": [], "checklist": [], "kesimpulan_opsi": [], "catatan_aspek": []},
        3: {"identitas": [], "aspek": []},
        4: {"rekap_header": [], "rekap": []},
    }
    for item in _iter_block_items(document):
        if item.__class__.__name__ == "Paragraph":
            txt = item.text.strip()
            if not txt:
                continue
            if txt.startswith("D. TUJUAN SUPERVISI"):
                capture_tujuan = True
                continue
            if txt.startswith("E. SASARAN SUPERVISI"):
                capture_tujuan = False
            if capture_tujuan and not txt.rstrip().endswith("bertujuan untuk:"):
                tujuan.append(txt)
            m = re.match(r"^Lampiran (\d)\.", txt)
            if m:
                current_lamp, last_heading = int(m.group(1)), None
                continue
            if txt == "Kesimpulan Telaah":
                capturing_kes, kes_buf = True, []
                continue
            if capturing_kes:
                if re.match(r"^[A-H]\.\s", txt) or txt.startswith("Lampiran"):
                    state[2]["kesimpulan_opsi"] = kes_buf
                    capturing_kes = False
                else:
                    kes_buf.append(txt)
                    continue
            if current_lamp == 1 and re.match(r"^[A-H]\.\s", txt):
                last_heading = txt
        else:
            headers = [_cell_text(c) for c in item.rows[0].cells]
            if capturing_kes:
                state[2]["kesimpulan_opsi"] = kes_buf
                capturing_kes = False
            if current_lamp == 1:
                if headers and headers[0].startswith("Skala Penilaian"):
                    state[1]["skala"] = headers[0]
                elif headers[:1] == ["Indikator"]:
                    inds = [_cell_text(r.cells[0]) for r in item.rows[1:] if _cell_text(r.cells[0])]
                    if inds:
                        state[1]["kategori"].append({"kategori": last_heading or "", "indikator": inds})
                elif headers and headers[0] == "Kolom Isian":
                    state[1]["identitas"] = [_cell_text(r.cells[0]) for r in item.rows[1:]]
                elif headers == ["Aspek", "Uraian"]:
                    state[1]["catatan_aspek"] = [_cell_text(r.cells[0]) for r in item.rows[1:]]
            elif current_lamp == 2:
                if headers and headers[0] == "Kolom Isian":
                    state[2]["identitas"] = [_cell_text(r.cells[0]) for r in item.rows[1:]]
                elif len(headers) > 1 and headers[0] == "No" and "Komponen" in headers[1]:
                    state[2]["checklist"] = [[_cell_text(c) for c in r.cells] for r in item.rows[1:]]
                elif headers == ["Aspek", "Uraian"]:
                    state[2]["catatan_aspek"] = [_cell_text(r.cells[0]) for r in item.rows[1:]]
            elif current_lamp == 3:
                if headers and headers[0] == "Kolom Isian":
                    state[3]["identitas"] = [_cell_text(r.cells[0]) for r in item.rows[1:]]
                elif headers == ["Aspek", "Uraian"]:
                    state[3]["aspek"] = [_cell_text(r.cells[0]) for r in item.rows[1:]]
            elif current_lamp == 4:
                if headers and headers[0] == "No" and "Kelas" in headers:
                    state[4]["rekap_header"] = headers
                    state[4]["rekap"] = [[_cell_text(c) for c in r.cells] for r in item.rows[1:]]
    if not state[1]["kategori"]:
        return None, f"Instrumen Lampiran 1 tidak ditemukan di '{SUPERVISI_FILE}'."
    return {"tujuan": tujuan, "lampiran": state}, None


def _sup_target(prefix: str):
    """Sekolah, guru, kelas yang disupervisi (disimpan ke log hasil supervisi)."""
    auth = st.session_state.auth
    c1, c2 = st.columns(2)
    with c1:
        if auth["role"] == ROLE_PENGURUS:
            sekolah = st.selectbox("Sekolah", SEKOLAH, key=f"{prefix}_sekolah")
        else:
            sekolah = auth["sekolah"]
            st.text_input("Sekolah", value=sekolah, disabled=True, key=f"{prefix}_sekolah_ro")
    with c2:
        kelas = st.selectbox("Kelas", list(range(1, 7)), format_func=lambda i: f"Kelas {i}", key=f"{prefix}_kelas")
    guru = st.text_input("Nama guru yang disupervisi", key=f"{prefix}_guru")
    return sekolah, kelas, guru


def render_identity_field(label: str, key_prefix: str, prefill: str = ""):
    low = label.lower()
    key = f"{key_prefix}_{_slug(label)}"
    if ("sekolah" in low and "kepala" not in low) or ("kelas" in low and "semester" in low) or "nama guru" in low:
        return None  # sudah diisi lewat _sup_target
    if "tanggal" in low:
        return str(st.date_input(label, key=key, format="DD/MM/YYYY"))
    if "tahap 3m" in low or "pertemuan ke-" in low:
        return st.selectbox(label, ["Memahami", "Mengaplikasi", "Merefleksi"], key=key)
    if "jenis supervisi" in low:
        return st.selectbox(label, ["Dokumen", "Kelas/Akademik"], key=key)
    if "judul proyek" in low or "modul" in low and "judul" in low:
        return st.text_input(label, key=key)
    return st.text_input(label, value=prefill, key=key)


def log_supervisi(record: dict):
    logs = _read_json(SUPERVISI_LOG, [])
    record["disimpan"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    logs.append(record)
    _write_json(SUPERVISI_LOG, logs)


def render_lampiran1(data):
    lamp = data["lampiran"][1]
    auth = st.session_state.auth
    section("📋", "Identitas Observasi")
    sekolah, kelas, guru = _sup_target("l1")
    with st.expander("Isian identitas lainnya"):
        for label in lamp["identitas"]:
            render_identity_field(label, "l1", auth["name"] if "kepala sekolah" in label.lower() else "")
    if lamp["skala"]:
        st.markdown(f'<div class="skala-note">📏 {lamp["skala"]}</div>', unsafe_allow_html=True)
    section("✍️", "Penilaian per Indikator")
    skor = []
    for kat in lamp["kategori"]:
        with st.expander(kat["kategori"]):
            for i, ind in enumerate(kat["indikator"]):
                st.markdown(f'<div class="indikator-text">{_esc(ind)}</div>', unsafe_allow_html=True)
                skor.append(st.select_slider("Skor", options=[1, 2, 3, 4], value=3, label_visibility="collapsed",
                                             key=f"l1_skor_{_slug(kat['kategori'])}_{i}"))
    section("📝", "Catatan Hasil Observasi")
    catatan = {label: st.text_area(label, key=f"l1_cat_{_slug(label)}") for label in lamp["catatan_aspek"]}
    if st.button("💾 Simpan Instrumen Observasi Kelas", width="stretch", key="btn_simpan_l1"):
        if not guru.strip():
            st.error("Isi nama guru yang disupervisi.")
            return
        rata = sum(skor) / len(skor) if skor else 0
        log_supervisi({"jenis": "Observasi Kelas", "sekolah": sekolah, "kelas": kelas, "guru": guru.strip(),
                       "supervisor": auth["name"], "nilai": f"{rata:.2f} / 4", "catatan": catatan})
        st.success(f"✅ Observasi tersimpan. Rata-rata skor: **{rata:.2f} / 4**.")
        st.balloons()


def render_lampiran2(data):
    lamp = data["lampiran"][2]
    auth = st.session_state.auth
    section("📋", "Identitas Telaah")
    sekolah, kelas, guru = _sup_target("l2")
    with st.expander("Isian identitas lainnya"):
        for label in lamp["identitas"]:
            render_identity_field(label, "l2", auth["name"] if "penelaah" in label.lower() else "")
    section("✅", f"Checklist Komponen Tabel 10 Panduan STEM ({len(lamp['checklist'])} butir)")
    hasil = []
    for row in lamp["checklist"]:
        st.markdown(f'<div class="indikator-text"><b>{row[0]}.</b> {_esc(row[1])}</div>', unsafe_allow_html=True)
        hasil.append(st.radio("Sesuai?", ["Ya", "Tidak"], horizontal=True, label_visibility="collapsed",
                              key=f"l2_sesuai_{row[0]}"))
    kes = None
    if lamp["kesimpulan_opsi"]:
        section("🏁", "Kesimpulan Telaah")
        kes = st.selectbox("Kesimpulan", lamp["kesimpulan_opsi"], key="l2_kes", label_visibility="collapsed")
    section("📝", "Catatan Penelaah")
    catatan = {label: st.text_area(label, key=f"l2_cat_{_slug(label)}") for label in lamp["catatan_aspek"]}
    if st.button("💾 Simpan Checklist Telaah", width="stretch", key="btn_simpan_l2"):
        if not guru.strip():
            st.error("Isi nama guru yang disupervisi.")
            return
        ya = hasil.count("Ya")
        log_supervisi({"jenis": "Telaah Modul", "sekolah": sekolah, "kelas": kelas, "guru": guru.strip(),
                       "supervisor": auth["name"], "nilai": f"{ya}/{len(hasil)} sesuai", "kesimpulan": kes,
                       "catatan": catatan})
        st.success(f"✅ Telaah tersimpan: {ya}/{len(hasil)} komponen sesuai.")
        st.balloons()


def render_lampiran3(data):
    lamp = data["lampiran"][3]
    auth = st.session_state.auth
    section("📋", "Identitas Supervisi")
    sekolah, kelas, guru = _sup_target("l3")
    with st.expander("Isian identitas lainnya"):
        for label in lamp["identitas"]:
            render_identity_field(label, "l3")
    section("🤝", "Tindak Lanjut / Coaching")
    isian = {label: st.text_area(label, key=f"l3_{_slug(label)}") for label in lamp["aspek"]}
    if st.button("💾 Simpan Lembar Tindak Lanjut", width="stretch", key="btn_simpan_l3"):
        if not guru.strip():
            st.error("Isi nama guru yang disupervisi.")
            return
        log_supervisi({"jenis": "Tindak Lanjut", "sekolah": sekolah, "kelas": kelas, "guru": guru.strip(),
                       "supervisor": auth["name"], "nilai": "-", "catatan": isian})
        st.success("✅ Lembar tindak lanjut tersimpan.")
        st.balloons()


def render_lampiran4(data):
    auth = st.session_state.auth
    section("🗃️", "Hasil Supervisi Tersimpan")
    logs = _read_json(SUPERVISI_LOG, [])
    if auth["role"] == ROLE_KS:
        logs = [x for x in logs if x.get("sekolah") == auth["sekolah"]]
    if logs:
        rows = [{"Waktu": x["disimpan"], "Sekolah": x["sekolah"], "Kelas": x["kelas"], "Guru": x["guru"],
                 "Jenis": x["jenis"], "Hasil": x["nilai"], "Supervisor": x["supervisor"]} for x in reversed(logs)]
        st.dataframe(rows, width="stretch", hide_index=True, key="log_sup")
        csv = io.StringIO()
        csv.write("Waktu;Sekolah;Kelas;Guru;Jenis;Hasil;Supervisor\n")
        for r in rows:
            csv.write(";".join(str(v) for v in r.values()) + "\n")
        st.download_button("⬇️ Unduh Rekap (CSV)", csv.getvalue().encode("utf-8-sig"),
                           file_name="rekap_supervisi_stem_cidugaleun.csv", mime="text/csv", width="stretch")
    else:
        st.info("Belum ada hasil supervisi yang disimpan.")

    lamp = data["lampiran"][4]
    if lamp["rekap"]:
        section("📅", "Jadwal Supervisi Satu Tahun (dari dokumen)")
        st.dataframe([dict(zip(lamp["rekap_header"], r)) for r in lamp["rekap"]], width="stretch",
                     hide_index=True, key="rekap_dok")


def render_supervisi():
    auth = st.session_state.auth
    section("👨‍💼", "Portal Supervisi STEM")
    lingkup = "seluruh sekolah Gugus Cidugaleun" if auth["role"] == ROLE_PENGURUS else auth["sekolah"]
    card(f"<p>Instrumen supervisi pembelajaran STEM berbasis proyek Kelas 1–6 untuk <b>{lingkup}</b>, "
         "dibaca langsung dari dokumen Program Supervisi Kepala Sekolah — STEM.</p>")
    if docx is None:
        st.error("Modul python-docx belum terpasang.")
        return
    data, err = load_supervisi_full(_mtime(umum_path(SUPERVISI_FILE)))
    if err:
        st.error(err)
        return
    if data["tujuan"]:
        with st.expander("🎯 Tujuan Supervisi"):
            for i, g in enumerate(data["tujuan"]):
                st.markdown(f"{i+1}. {g}")
    labels = list(LAMPIRAN_TABS.keys())
    with st.container(key="lampiran-menu"):
        cols = st.columns(4, gap="small")
        for col, label in zip(cols, labels):
            with col:
                if st.button(label, key=f"btn_tab_{LAMPIRAN_TABS[label]}", width="stretch",
                             type="primary" if st.session_state.lampiran_tab == LAMPIRAN_TABS[label] else "secondary"):
                    st.session_state.lampiran_tab = LAMPIRAN_TABS[label]
                    st.rerun()
    {"lampiran1": render_lampiran1, "lampiran2": render_lampiran2,
     "lampiran3": render_lampiran3, "lampiran4": render_lampiran4}[st.session_state.lampiran_tab](data)
    st.markdown(f'<div class="footer-note">Sumber: {SUPERVISI_FILE}</div>', unsafe_allow_html=True)


# ============================================================================
# Router
# ============================================================================
def main():
    load_css()
    init_state()
    if not st.session_state.auth:
        render_login()
        return
    render_top_nav()
    page = st.session_state.page
    if page == "supervisi" and st.session_state.auth["role"] == ROLE_GURU:
        page = "landing"
    {
        "landing": render_landing,
        "modul_kelas": render_modul_kelas,
        "panduan": render_panduan,
        "administrasi": render_administrasi,
        "progres": render_progres,
        "supervisi": render_supervisi,
    }.get(page, render_landing)()


if __name__ == "__main__":
    main()
