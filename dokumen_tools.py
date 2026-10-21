# -*- coding: utf-8 -*-
"""
Alat bantu dokumen untuk LMS STEM Gugus Puspamukti (tanpa Streamlit):
    - ambil LKPD dari Modul Proyek STEM menjadi berkas Word tersendiri
    - petakan bagian LKPD ke pertemuan/tahap pelaksanaan
    - buat berkas Word hasil supervisi kepala sekolah
    - saring presentasi KKG (sembunyikan slide Supervisi KS untuk guru)
    - bungkus banyak berkas menjadi ZIP
"""

import datetime
import io
import re
import zipfile

import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Cm, Pt
from docx.text.paragraph import Paragraph

# ----------------------------------------------------------------------------
# LKPD
# ----------------------------------------------------------------------------
_LKPD_START_RE = re.compile(r"^(\d+)\.\s*(Lembar Kerja Peserta Didik|Lembar Kerja|LKPD)", re.I)
_LKPD_STOP_RE = re.compile(r"^\d+\.\s*(Rubrik|Sumber Referensi|Daftar Pustaka|Glosarium|Lampiran)", re.I)
_SUB_RE = re.compile(r"^([A-H])\.\s+(.+)$")
_TAHAP_DI_JUDUL_RE = re.compile(r"\(Tahap\s+([^)]+)\)", re.I)


def _el_text(el) -> str:
    return "".join(t.text or "" for t in el.iter(qn("w:t"))).strip()


def _lkpd_range(children):
    """Indeks awal & akhir (eksklusif) bagian LKPD di badan dokumen + nomor bab."""
    start = end = no = None
    for i, ch in enumerate(children):
        if not ch.tag.endswith("}p"):
            continue
        t = _el_text(ch)
        if not t:
            continue
        if start is None:
            m = _LKPD_START_RE.match(t)
            if m:
                start, no = i, int(m.group(1))
            continue
        m = re.match(r"^(\d+)\.\s*(.+)$", t)
        if _LKPD_STOP_RE.match(t) or (m and int(m.group(1)) == no + 1 and not t.endswith("?")):
            end = i
            break
    if start is not None and end is None:
        end = len(children)
    # buang paragraf kosong / pemisah halaman di ujung agar tidak ada halaman kosong
    while start is not None and end - 1 > start and children[end - 1].tag.endswith("}p") \
            and not _el_text(children[end - 1]) and not children[end - 1].findall(".//" + qn("w:drawing")):
        end -= 1
    return start, end


def ada_lkpd(path) -> bool:
    d = docx.Document(str(path))
    return _lkpd_range(list(d.element.body.iterchildren()))[0] is not None


def ekstrak_lkpd_docx(path, judul: str = "", kelas=None):
    """Salin Modul Proyek STEM lalu sisakan kop sekolah + bagian LKPD saja.
    Format tabel, gambar, dan gaya asli tetap utuh. Mengembalikan bytes .docx
    atau None bila modul tidak memuat LKPD."""
    d = docx.Document(str(path))
    body = d.element.body
    children = list(body.iterchildren())
    start, end = _lkpd_range(children)
    if start is None:
        return None
    keep = set(range(start, end))
    for i, ch in enumerate(children[:3]):  # kop surat sekolah
        if ch.tag.endswith("}tbl") and "PEMERINTAH" in _el_text(ch).upper():
            keep.add(i)
    for i, ch in enumerate(children):
        if ch.tag == qn("w:sectPr"):
            continue
        if i not in keep:
            body.remove(ch)
    # Judul bab "9. Lembar Kerja ..." -> judul lembar mandiri
    head = Paragraph(children[start], d)
    if head.runs:
        head.runs[0].text = "LEMBAR KERJA PESERTA DIDIK (LKPD)"
        for r in head.runs[1:]:
            r.text = ""
    head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if judul:
        new = d.add_paragraph()  # dibuat lalu dipindah tepat setelah judul
        run = new.add_run(f"{judul}" + (f" • Kelas {kelas}" if kelas else ""))
        run.bold = True
        run.font.size = Pt(11)
        new.alignment = WD_ALIGN_PARAGRAPH.CENTER
        head._p.addnext(new._p)
    buf = io.BytesIO()
    d.save(buf)
    return buf.getvalue()


def bagian_lkpd(path):
    """Daftar sub-bagian LKPD: [(huruf, judul, kata_kunci_tahap|None)]."""
    d = docx.Document(str(path))
    children = list(d.element.body.iterchildren())
    start, end = _lkpd_range(children)
    if start is None:
        return []
    out = []
    for ch in children[start:end]:
        if not ch.tag.endswith("}p"):
            continue
        t = _el_text(ch)
        m = _SUB_RE.match(t)
        if m and len(t) <= 120:
            mt = _TAHAP_DI_JUDUL_RE.search(t)
            out.append((m.group(1), m.group(2).strip(), mt.group(1).strip() if mt else None))
    return out


def _cari_pertemuan(pertemuan, kata):
    kata = kata.lower()
    for p in pertemuan:
        if kata in (p.get("tahap") or "").lower():
            return p
    return None


def peta_lkpd_pertemuan(bagian, pertemuan):
    """Petakan tiap bagian LKPD ke pertemuan pelaksanaan STEM.
    Kembali: [(huruf, judul_bagian, nomor_pertemuan|None, judul_pertemuan, tahap)]."""
    hasil = []
    for huruf, judul, tahap in bagian:
        low = judul.lower()
        p = None
        if tahap:
            kunci = tahap.split(" dan ")[0].split(",")[0].strip()  # "Menguji dan Mengevaluasi" -> "Menguji"
            p = _cari_pertemuan(pertemuan, kunci)
        elif "tantangan" in low:
            p = _cari_pertemuan(pertemuan, "Mengidentifikasi Masalah") or (pertemuan[0] if pertemuan else None)
        elif any(k in low for k in ("perhitungan", "rancangan", "sketsa")):
            p = _cari_pertemuan(pertemuan, "Mendesain Solusi")
        elif any(k in low for k in ("refleksi", "bercerita", "pertanyaan")):
            p = _cari_pertemuan(pertemuan, "Mengomunikasikan") or (pertemuan[-1] if pertemuan else None)
        elif "uji" in low or "data" in low:
            p = _cari_pertemuan(pertemuan, "Menguji")
        hasil.append((huruf, judul, p["nomor"] if p else None, p["judul"] if p else "", p["tahap"] if p else ""))
    return hasil


def pertemuan_pakai_lkpd(document, pertemuan):
    """Nomor pertemuan yang langkahnya menyebut LKPD / lembar kerja secara eksplisit."""
    nomor, in_detail, hits = None, False, set()
    for p in document.paragraphs:
        t = p.text.strip()
        if not t:
            continue
        if re.match(r"^\d+\.\s*Detail Pelaksanaan", t):
            in_detail = True
            continue
        if not in_detail:
            continue
        if _LKPD_START_RE.match(t):
            break
        m = re.match(r"^Pertemuan\s*(\d+)", t)
        if m:
            nomor = int(m.group(1))
            continue
        if nomor and re.search(r"\bLKPD\b|lembar kerja", t, re.I):
            hits.add(nomor)
    return sorted(hits)


# ----------------------------------------------------------------------------
# Hasil supervisi -> Word
# ----------------------------------------------------------------------------
def _set_cell(cell, text, bold=False, size=10):
    cell.text = ""
    run = cell.paragraphs[0].add_run(str(text))
    run.bold = bold
    run.font.size = Pt(size)


def _widths(table, cms):
    table.autofit = False
    grid = table._tbl.tblGrid
    for gc, w in zip(grid.findall(qn("w:gridCol")), cms):
        gc.set(qn("w:w"), str(int(Cm(w).twips)))
    for row in table.rows:
        for cell, w in zip(row.cells, cms):
            cell.width = Cm(w)


def hasil_supervisi_docx(rec: dict, gugus_nama: str, tahun: str) -> bytes:
    d = docx.Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(11)
    for txt, size in ((f"HASIL SUPERVISI PEMBELAJARAN STEM — {rec.get('jenis', '').upper()}", 14),
                      (f"{rec.get('sekolah', '')} • {gugus_nama} • TP {tahun}", 11)):
        p = d.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(txt)
        r.bold = True
        r.font.size = Pt(size)

    ident = [("Sekolah", rec.get("sekolah", "")), ("Kelas", rec.get("kelas", "")),
             ("Nama Guru", rec.get("guru", "")), ("Supervisor", rec.get("supervisor", "")),
             ("Jenis Supervisi", rec.get("jenis", "")), ("Hasil", rec.get("nilai", "")),
             ("Disimpan", rec.get("disimpan", ""))]
    if rec.get("predikat"):
        ident.insert(6, ("Predikat", rec["predikat"]))
    for k, v in (rec.get("identitas") or {}).items():
        if v:
            ident.append((k, v))
    d.add_paragraph().add_run("A. Identitas").bold = True
    t = d.add_table(rows=0, cols=2)
    t.style = "Table Grid"
    for k, v in ident:
        row = t.add_row().cells
        _set_cell(row[0], k, bold=True)
        _set_cell(row[1], v)
    _widths(t, [5.5, 11])

    rincian = rec.get("rincian") or []
    if rincian:
        d.add_paragraph()
        d.add_paragraph().add_run("B. Rincian Penilaian").bold = True
        header = rec.get("rincian_header") or ["No", "Aspek / Indikator", "Hasil"]
        t = d.add_table(rows=1, cols=len(header))
        t.style = "Table Grid"
        for c, h in zip(t.rows[0].cells, header):
            _set_cell(c, h, bold=True)
        for r in rincian:
            cells = t.add_row().cells
            for c, v in zip(cells, r):
                _set_cell(c, v)
        _widths(t, [1.2, 12.8, 2.5] if len(header) == 3 else [16.5 / len(header)] * len(header))

    if rec.get("kesimpulan"):
        d.add_paragraph()
        p = d.add_paragraph()
        p.add_run("Kesimpulan: ").bold = True
        p.add_run(str(rec["kesimpulan"]))

    catatan = rec.get("catatan") or {}
    if any(catatan.values()):
        d.add_paragraph()
        d.add_paragraph().add_run("C. Catatan / Tindak Lanjut").bold = True
        t = d.add_table(rows=0, cols=2)
        t.style = "Table Grid"
        for k, v in catatan.items():
            row = t.add_row().cells
            _set_cell(row[0], k, bold=True)
            _set_cell(row[1], v or "-")
        _widths(t, [5.5, 11])

    d.add_paragraph()
    tgl = rec.get("disimpan", "")[:10]
    try:
        tgl = datetime.date.fromisoformat(tgl).strftime("%d-%m-%Y")
    except ValueError:
        pass
    t = d.add_table(rows=4, cols=2)
    _set_cell(t.rows[0].cells[1], f"................, {tgl}")
    _set_cell(t.rows[1].cells[0], "Guru yang disupervisi,")
    _set_cell(t.rows[1].cells[1], "Supervisor,")
    _set_cell(t.rows[3].cells[0], rec.get("guru", ""), bold=True)
    _set_cell(t.rows[3].cells[1], rec.get("supervisor", ""), bold=True)
    t.rows[2].height = Pt(48)
    buf = io.BytesIO()
    d.save(buf)
    return buf.getvalue()


# ----------------------------------------------------------------------------
# Presentasi KKG versi guru (tanpa slide "Supervisi KS")
# ----------------------------------------------------------------------------
_SLIDE_RE = re.compile(r'<section class="slide[^"]*"[^>]*>.*?</section>', re.S)


def html_tanpa_supervisi(html: str, sec_name: str = "Supervisi KS") -> str:
    slides = list(_SLIDE_RE.finditer(html))
    if not slides:
        return html
    keep = [m.group(0) for m in slides if f'data-sec="{sec_name}"' not in m.group(0)]
    if len(keep) == len(slides):
        return html
    total = len(keep)
    baru = []
    for i, s in enumerate(keep, start=1):
        s = re.sub(r'<span class="pg">\d+\s*/\s*\d+</span>', f'<span class="pg">{i} / {total}</span>', s)
        s = re.sub(r'aria-label="Slide \d+:', f'aria-label="Slide {i}:', s)
        baru.append(s)
    head, tail = html[:slides[0].start()], html[slides[-1].end():]
    out = head + "\n".join(baru) + tail

    # daftar isi (bagian & thumbnail) disusun ulang dari slide yang tersisa
    secs, thumbs = [], []
    for i, s in enumerate(keep):
        sec = re.search(r'data-sec="([^"]*)"', s).group(1)
        title = re.search(r'data-title="([^"]*)"', s).group(1)
        if not secs or secs[-1][0] != sec:
            secs.append((sec, i))
        thumbs.append(f'<button data-go="{i}"><b>{i + 1}</b>{title}</button>')
    msec = "".join(f'<button data-go="{i}"><span>{n:02d}</span>{sec}</button>' for n, (sec, i) in enumerate(secs, 1))
    out = re.sub(r'<div class="msec">.*?</div>', f'<div class="msec">{msec}</div>', out, count=1, flags=re.S)
    out = re.sub(r'<div class="mthumbs">.*?</div>', f'<div class="mthumbs">{"".join(thumbs)}</div>', out,
                 count=1, flags=re.S)
    out = re.sub(r'<span id="counter">1 / \d+</span>', f'<span id="counter">1 / {total}</span>', out)
    return out


# ----------------------------------------------------------------------------
# ZIP
# ----------------------------------------------------------------------------
def buat_zip(items) -> bytes:
    """items: iterable (nama_dalam_zip, bytes)."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in items:
            if data:
                z.writestr(name, data)
    return buf.getvalue()
