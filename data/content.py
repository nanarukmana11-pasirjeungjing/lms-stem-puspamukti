# -*- coding: utf-8 -*-
"""
Konten LMS STEM Gugus Cidugaleun.

Semua teks & data dipisah dari tampilan (app.py) supaya mudah diperbarui.

Sumber dokumen (dibundel di folder docs/ agar aplikasi siap di-deploy):
- docs/kelas1 .. docs/kelas6 -> Daftar Proyek, Daftar Alat & Bahan, 56 Modul Proyek
  STEM, Panduan Guru Pembuatan Produk, dan template Administrasi STEM (00-06).
  Rujukan disusun oleh SD Negeri Panglayungan (anggota Gugus Cidugaleun),
  Tahun Pelajaran 2026/2027, dan dipakai bersama oleh seluruh sekolah gugus.
- docs/umum -> Program Supervisi Kepala Sekolah STEM, contoh Program Pembelajaran
  STEM sekolah, Instrumen Program STEM, Skenario Kegiatan KKG STEM, dan
  Panduan Pembelajaran STEM Kemendikdasmen 2025 (PDF).
"""

APP_NAMA = "LMS STEM Gugus Cidugaleun"

GUGUS = {
    "nama": "Gugus Cidugaleun",
    "wilayah": "Kecamatan Cigalontang, Kabupaten Tasikmalaya",
    "tahun_pelajaran": "2026/2027",
}

# Sekolah anggota gugus (urutan sesuai daftar dari pengurus gugus)
SEKOLAH = [
    "SDN Parentas",
    "SDN Sirnagalih",
    "SDN Karamatjaya",
    "SDN Cidugaleun",
    "SDN Panglayungan",
    "SDN Giriatikan",
]

# Warna aksen kartu tiap sekolah (dipakai di Beranda & Rekap)
SEKOLAH_WARNA = {
    "SDN Parentas": "#2563EB",
    "SDN Sirnagalih": "#16A34A",
    "SDN Karamatjaya": "#F59E0B",
    "SDN Cidugaleun": "#7C3AED",
    "SDN Panglayungan": "#DB2777",
    "SDN Giriatikan": "#0EA5E9",
}

SEKOLAH_PENYUSUN_RUJUKAN = "SDN Panglayungan"

OVERVIEW = {
    "judul": "Pembelajaran STEM Berbasis Proyek",
    "subjudul": "Kelas 1–6 • 6 Sekolah • Tahun Pelajaran 2026/2027",
    "definisi": (
        "Pembelajaran STEM (Sains, Teknologi, Enjinering, Matematika) adalah pembelajaran yang "
        "mengintegrasikan berbagai mata pelajaran — <b>tidak hanya IPA dan Matematika</b> — serta "
        "berfokus pada pemecahan masalah nyata dalam kehidupan sehari-hari. Prosesnya mencakup "
        "penyelidikan ilmiah dan siklus enjinering yang berulang, pemodelan matematis, dan "
        "pemanfaatan teknologi secara tepat guna."
    ),
    "pendekatan": (
        "STEM merupakan salah satu <b>praktik pedagogis pembelajaran mendalam</b>. Praktik saintifik "
        "dan enjinering menjadi wahana pengalaman belajar <b>Memahami → Mengaplikasi → Merefleksi</b> "
        "dengan prinsip <b>Berkesadaran, Bermakna, dan Menggembirakan</b>. Pembelajaran dibuat "
        "<b>mudah</b> (tantangan kontekstual sesuai taraf perkembangan murid) dan <b>murah</b> "
        "(alat-bahan sederhana, termasuk bahan bekas pakai yang aman), serta inklusif bagi seluruh murid."
    ),
    "tujuan_stem": (
        "Meningkatkan kemampuan murid dalam menerapkan pengetahuan yang diperoleh dalam pembelajaran "
        "untuk memecahkan masalah dunia nyata melalui praktik saintifik dan enjinering, sekaligus "
        "menumbuhkan delapan dimensi profil lulusan."
    ),
    "tujuan": [
        "Menyediakan bank modul proyek STEM Kelas 1–6 (56 proyek) yang memuat seluruh komponen Tabel 10 Panduan STEM",
        "Memudahkan guru menjalankan 7 tahap praktik saintifik dan enjinering per pertemuan, lengkap dengan kriteria & batasan proyek",
        "Menyediakan template administrasi dan asesmen autentik pembelajaran STEM",
        "Memantau keterlaksanaan proyek dan supervisi STEM di 6 sekolah dalam satu dasbor gugus",
    ],
    "referensi": "Panduan Pembelajaran STEM, Pusat Kurikulum dan Pembelajaran, Kemendikdasmen 2025",
}

# Tiga karakteristik utama pembelajaran STEM (Panduan Bab 1.D, Gambar 6)
KARAKTERISTIK = [
    ("🧩", "Penyelesaian Masalah",
     "Menghadirkan persoalan kontekstual — boleh sederhana namun bermakna — untuk membangun kepedulian "
     "pada isu lokal dan rasa ingin tahu murid."),
    ("🔬", "Praktik Saintifik dan Enjinering",
     "Serangkaian keterampilan ilmuwan dan insinyur untuk memahami fenomena dan menciptakan solusi, "
     "dilaksanakan secara iteratif (berulang) hingga diperoleh solusi paling optimal."),
    ("🔗", "Integrasi Lintas Disiplin Ilmu",
     "Mengintegrasikan konsep lintas mata pelajaran (multidisipliner → interdisipliner → transdisipliner) "
     "untuk menemukan solusi yang utuh."),
]

# Peran tiap komponen STEM (Panduan Gambar 5)
PERAN_KOMPONEN = [
    ("S", "Sains", "Praktik saintifik untuk menanamkan konsep, praktik, dan sikap ilmiah sebagai dasar merencanakan ide solusi."),
    ("T", "Teknologi", "Teknologi yang diperlukan dalam membangun ide solusi, baik teknologi sederhana maupun digital."),
    ("E", "Enjinering", "Tahapan mendesain, membuat, menguji coba, mengevaluasi ide solusi, serta berimprovisasi."),
    ("M", "Matematika", "Berpikir matematis untuk menganalisis, memodelkan, dan mengevaluasi solusi desain secara logis dan terukur."),
]

# Tahapan Praktik Saintifik dan Enjinering (Panduan Gambar 7, Tabel 9 & 11)
# (judul, uraian Panduan, adaptasi Fase A/SD awal, contoh asesmen & instrumen — Tabel 11)
TAHAP_PRAKTIK = [
    ("Bertanya dan Mengidentifikasi Masalah",
     "Murid mengamati lingkungan/situasi sekitar, menemukan masalah nyata, dan mengajukan pertanyaan untuk memperjelas ide.",
     "Mengamati benda/gambar nyata, mendengar cerita guru, lalu menyebutkan masalahnya.",
     "Observasi kemampuan mengidentifikasi masalah & mengajukan pertanyaan — rubrik observasi, catatan anekdotal."),
    ("Bertukar Pikiran dalam Menentukan Solusi",
     "Murid melakukan eksperimen pendahuluan atau studi sederhana untuk mengembangkan ide dan menentukan solusi terbaik.",
     "Menyebutkan/menggambar beberapa ide, lalu memilih satu ide bersama guru.",
     "Penilaian partisipasi dan kontribusi ide dalam diskusi kelompok — lembar observasi."),
    ("Mendesain Solusi",
     "Murid merancang langkah atau skema pembuatan solusi berdasarkan data/informasi yang dimiliki.",
     "Menggambar rancangan sederhana dan menceritakannya (dibantu guru).",
     "Penilaian kelengkapan & kesesuaian desain dengan masalah — rubrik analisis produk (sketsa/rencana kerja)."),
    ("Membuat Solusi",
     "Murid memproduksi atau membangun model solusi berdasarkan rancangan yang telah dibuat.",
     "Membuat karya bersama teman/guru dengan alat yang aman.",
     "Keterampilan menggunakan alat & bahan secara aman dan efektif — rubrik observasi kinerja."),
    ("Menguji dan Mengevaluasi Solusi",
     "Murid menguji apakah solusi bekerja, mencatat data, menganalisis kinerja, dan mengevaluasi efektivitas berdasarkan kriteria keberhasilan.",
     "Mencoba hasil karya, mengamati berhasil atau belum, berdiskusi “apa yang bisa diperbaiki?”.",
     "Kemampuan menganalisis hasil uji berdasarkan kriteria — rubrik penilaian kinerja."),
    ("Mendesain Ulang",
     "Berdasarkan hasil uji coba, murid menganalisis kekurangan lalu mengembangkan versi baru atau menyampaikan revisinya.",
     "Mengubah/menambah bagian karya dan menceritakan perubahannya.",
     "Penilaian perbaikan sesuai temuan uji — rubrik analisis perbaikan produk."),
    ("Mengomunikasikan",
     "Murid menyampaikan hasil pemikiran, mempresentasikan rancangan, pembuatan, dan hasil uji coba solusi dengan berbagai media.",
     "Bercerita di depan kelas, menyebut nama dan fungsi karya.",
     "Kemampuan menyampaikan ide & hasil kerja — rubrik presentasi, rubrik produk (poster, video, portofolio)."),
]
TAHAP_CATATAN = (
    "Tahapan bersifat iteratif (dapat diulang). Alur <i>design thinking</i> dapat diawali tahap "
    "<b>Empati/Memahami</b> kebutuhan pengguna. Pendidik boleh memakai kerangka <i>design process</i> "
    "maupun <i>design thinking</i> yang lebih familiar; untuk Fase A tahapan boleh disederhanakan atau "
    "digabung dalam satu pertemuan tanpa menghilangkan tahapnya."
)

# Pengalaman belajar pembelajaran mendalam dalam pelaksanaan STEM (Panduan Bab 4.A.2)
PENGALAMAN_BELAJAR = [
    ("Memahami", "Mengaitkan konsep lintas disiplin dan menjelaskan sebab–akibat."),
    ("Mengaplikasi", "Menerapkan konsep pada situasi autentik, mengambil keputusan desain, dan mengoptimasi solusi."),
    ("Merefleksi", "Jurnal reflektif, log desain, dan diskusi yang menilai kualitas solusi, efektivitas proses, serta rencana perbaikan."),
]

# Langkah merancang pembelajaran STEM intrakurikuler (Panduan Gambar 14)
LANGKAH_PERENCANAAN = [
    ("Menentukan topik proyek STEM", "melalui identifikasi masalah atau potensi di sekitar lingkungan satuan pendidikan, lengkap dengan <b>kriteria</b> (spesifikasi terukur keberhasilan) dan <b>batasan</b> (aturan, bahan, waktu, biaya)."),
    ("Menganalisis capaian pembelajaran", "serta integrasi komponen STEM dan materi mata pelajaran (memakai kalimat CP Kepka BSKAP 046/H/KR/2025)."),
    ("Menentukan strategi pelaksanaan", "proses saintifik dan enjinering (aktivitas murid per tahap)."),
    ("Menyusun perencanaan pembelajaran STEM dan asesmen", "mengikuti komponen Tabel 10."),
]

# Komponen perencanaan pembelajaran STEM (Panduan Tabel 10)
# (kelompok, komponen, kata kunci pencarian di modul, wajib?)
KOMPONEN_PERENCANAAN = [
    ("Identifikasi", "Dimensi Profil Lulusan", "Dimensi Profil Lulusan", True),
    ("Desain Pembelajaran", "Topik Proyek STEM", "Topik Proyek", True),
    ("Desain Pembelajaran", "Konten Masalah", "Konten Masalah", True),
    ("Desain Pembelajaran", "Kriteria", "Kriteria", True),
    ("Desain Pembelajaran", "Batasan", "Batasan", True),
    ("Desain Pembelajaran", "Tujuan Pembelajaran (mapel terkait)", "Tujuan Pembelajaran", True),
    ("Desain Pembelajaran", "Integrasi Komponen STEM", "Integrasi Komponen STEM", True),
    ("Desain Pembelajaran", "Praktik Pedagogis", "Praktik Pedagogis", True),
    ("Desain Pembelajaran", "Kemitraan Pembelajaran (opsional)", "Kemitraan", False),
    ("Desain Pembelajaran", "Lingkungan Pembelajaran", "Lingkungan Pembelajaran", True),
    ("Desain Pembelajaran", "Pemanfaatan Digital (opsional)", "Pemanfaatan Digital", False),
    ("Pengalaman Belajar", "Langkah-langkah pembelajaran", "Pengalaman Belajar", True),
    ("Asesmen", "Asesmen Pembelajaran (formatif & sumatif)", "Asesmen", True),
]

MODEL_PEMBELAJARAN = [
    ("PjBL Lucas (2007)", "Pertanyaan esensial → rencana proyek → jadwal → memantau → menilai hasil → evaluasi pengalaman."),
    ("PjBL STEM Laboy-Rush (2010)", "Merefleksi → meneliti → mengeksplorasi & menemukan → mengaplikasikan → mengomunikasikan."),
    ("Empat Tahap PjBL SEAMEO STEM-ED (2022)", "Memperkenalkan masalah → mengembangkan pemahaman → memecahkan masalah → mengomunikasikan solusi."),
    ("PBL Wurdinger & Carlson (2010)", "Pendefinisian masalah → diagnosis awal → penelitian → pemahaman bersama."),
    ("Siklus Belajar 5E (BSCS)", "Engagement → Exploration → Explanation → Elaboration → Evaluation."),
]

IMPLEMENTASI = [
    ("Intrakurikuler", "Mengintegrasikan berbagai mata pelajaran melalui perencanaan, pelaksanaan, dan asesmen. Proyek dapat dilaksanakan pada jam semua mata pelajaran yang terkait; di SD asesmen dilakukan menyeluruh oleh guru kelas."),
    ("Kokurikuler", "Memperdalam/memperkaya intrakurikuler: analisis kebutuhan → dimensi profil lulusan → tema → bentuk kegiatan → tujuan → alokasi waktu → aktivitas → asesmen."),
    ("Ekstrakurikuler", "Wadah minat dan bakat STEM (klub sains, robotik/koding, lomba) di luar jam intrakurikuler."),
]

PERAN_PEMANGKU = [
    ("Kepala Sekolah", ["Menjadikan pembelajaran STEM salah satu program dalam Kurikulum Satuan Pendidikan",
                        "Menciptakan iklim yang mendukung kolaborasi dan eksplorasi",
                        "Mengatur alokasi waktu dan sumber daya proyek STEM",
                        "Mendorong refleksi pendidik dan murid; menjalin kemitraan dengan komunitas/industri"]),
    ("Guru", ["Membimbing murid menghubungkan konsep STEM dengan masalah nyata",
              "Merencanakan & melaksanakan pembelajaran yang mendorong eksplorasi, eksperimen, dan pemecahan masalah",
              "Melakukan penilaian autentik penerapan pengetahuan STEM"]),
    ("Pengawas / Dinas", ["Mengawasi pelaksanaan & mendorong asesmen autentik",
                          "Mengembangkan komunitas belajar (PLC) antarpendidik — mis. KKG gugus"]),
    ("Orang Tua", ["Memberi dukungan relevan tanpa intervensi yang menurunkan kemandirian murid",
                   "Berkomunikasi dengan pendidik dan berbagi pengalaman bila relevan"]),
]

# Penguatan 8 dimensi profil lulusan melalui STEM (Panduan Tabel 2, diringkas)
PROFIL_LULUSAN = [
    ("Keimanan & Ketakwaan terhadap Tuhan YME", "Rasa syukur melalui pemahaman keteraturan dan keindahan alam serta teknologi yang bermanfaat bagi manusia dan lingkungan."),
    ("Kewargaan", "Kesadaran dan kepedulian pada isu lokal/global (lingkungan, sumber daya) serta aksi nyata bagi masyarakat."),
    ("Penalaran Kritis", "Merancang solusi berbasis data, menganalisis, dan mengevaluasinya untuk memecahkan masalah nyata."),
    ("Kreativitas", "Menemukan solusi inovatif dan menghasilkan karya orisinal melalui praktik saintifik dan enjinering."),
    ("Kolaborasi", "Bekerja sama secara gotong royong melalui pembagian peran dan tanggung jawab."),
    ("Kemandirian", "Bertanggung jawab atas proses dan hasil belajar, berinisiatif, dan gigih mengatasi hambatan."),
    ("Kesehatan", "Menjalankan kebiasaan hidup sehat dan aman serta menjaga keseimbangan fisik dan mental."),
    ("Komunikasi", "Menyampaikan ide, gagasan, dan informasi dengan jelas serta berinteraksi efektif."),
]

FASE = {1: "Fase A", 2: "Fase A", 3: "Fase B", 4: "Fase B", 5: "Fase C", 6: "Fase C"}

# Skenario pertemuan KKG STEM (rujukan rundown — tanggal ditetapkan pengurus gugus)
EVENT = {
    "nama": "Pertemuan KKG STEM Gugus Cidugaleun",
    "tema": "Penerapan Modul Proyek STEM Kelas 1–6: Praktik Saintifik–Enjinering, Pengalaman Belajar (Memahami–Mengaplikasi–Merefleksi), dan Prinsip Pembelajaran Mendalam",
    "waktu": "07.30 – 12.10 WIB (tanggal ditetapkan pengurus KKG gugus)",
    "sasaran": "Guru Kelas 1–6 dan Kepala Sekolah dari 6 SD anggota Gugus Cidugaleun",
    "kelompok": "6 kelompok kelas lintas sekolah (Kelas 1 s.d. Kelas 6)",
    "referensi": "Skenario Kegiatan KKG STEM (docs/umum/Skenario_Kegiatan_KKG_STEM_Rujukan.docx)",
}

PRINSIP_WARNA = {
    "Berkesadaran": "#2563EB",
    "Bermakna": "#16A34A",
    "Menggembirakan": "#F59E0B",
    "3M Lengkap": "#7C3AED",
    "—": "#9CA3AF",
}

PENGALAMAN_WARNA = {
    "Memahami": "#0EA5E9",
    "Mengaplikasi": "#7C3AED",
    "Merefleksi": "#DB2777",
}

AGENDA = [
    {"waktu": "07.30–08.00", "kegiatan": "Registrasi & Pembukaan",
     "bentuk": "Pleno", "penanggung_jawab": "Ketua KKG Gugus", "prinsip": "Berkesadaran"},
    {"waktu": "08.00–08.20", "kegiatan": "Paparan Umum: STEM PjBL, Kalender Pendidikan, Daftar Alat & Bahan",
     "bentuk": "Pleno", "penanggung_jawab": "Ketua KKG / Narasumber", "prinsip": "Bermakna"},
    {"waktu": "08.20–08.30", "kegiatan": "Pembentukan Kelompok Kelas Lintas Sekolah",
     "bentuk": "Transisi", "penanggung_jawab": "Panitia", "prinsip": "—"},
    {"waktu": "08.30–11.15", "kegiatan": "Sesi Kelompok Kelas — Memahami, Mengaplikasi, Merefleksi (6 kelas paralel)",
     "bentuk": "Kelompok (6 kelas)", "penanggung_jawab": "Fasilitator per kelas", "prinsip": "3M Lengkap"},
    {"waktu": "11.15–11.45", "kegiatan": "Berbagi Hasil Antarkelompok (Gallery Walk)",
     "bentuk": "Pleno", "penanggung_jawab": "Perwakilan tiap kelompok", "prinsip": "Bermakna"},
    {"waktu": "11.45–12.00", "kegiatan": "Refleksi Bersama & Rencana Tindak Lanjut (RTL) per Sekolah",
     "bentuk": "Pleno", "penanggung_jawab": "Ketua KKG Gugus", "prinsip": "Berkesadaran"},
    {"waktu": "12.00–12.10", "kegiatan": "Penutup",
     "bentuk": "Pleno", "penanggung_jawab": "Ketua KKG Gugus", "prinsip": "Menggembirakan"},
]

# Proyek yang dipraktikkan pada sesi kelompok KKG (sesuai Skenario rujukan)
KELOMPOK_KELAS = [
    {"kelas": "Kelas 1", "modul": "Berhitung Asyik dengan Benda Kesayangan", "fase": "Fase A"},
    {"kelas": "Kelas 2", "modul": "Menara Bentuk: Membangun dari Bangun Ruang", "fase": "Fase A"},
    {"kelas": "Kelas 3", "modul": "Es Krim Kantong Ajaib: Mengamati Perubahan Wujud", "fase": "Fase B"},
    {"kelas": "Kelas 4", "modul": "Zat Ajaib: Mengamati Perubahan Wujud di Sekitar Kita", "fase": "Fase B"},
    {"kelas": "Kelas 5", "modul": "Detektif Zat: Memisahkan Campuran di Sekitar Kita", "fase": "Fase C"},
    {"kelas": "Kelas 6", "modul": "Kompas dan Peta Harta Karun", "fase": "Fase C"},
]

# Template administrasi pembelajaran STEM per kelas (berkas berawalan 00_..06_)
ADMIN_DOCS = [
    ("00", "Daftar Isi Administrasi STEM", "00_Daftar_Isi_Administrasi_STEM_Kelas{k}.docx"),
    ("01", "Program Tahunan STEM", "01_Program_Tahunan_STEM_Kelas{k}.docx"),
    ("02", "Program Semester STEM", "02_Program_Semester_STEM_Kelas{k}.docx"),
    ("03", "Jurnal Pelaksanaan STEM", "03_Jurnal_Pelaksanaan_STEM_Kelas{k}.docx"),
    ("04", "Daftar Nilai Proyek STEM", "04_Daftar_Nilai_Proyek_STEM_Kelas{k}.docx"),
    ("05", "Observasi Profil Lulusan & Refleksi", "05_Observasi_Profil_dan_Refleksi_STEM_Kelas{k}.docx"),
    ("06", "Laporan Pelaksanaan STEM", "06_Laporan_Pelaksanaan_STEM_Kelas{k}.docx"),
]

# Dokumen tingkat gugus/sekolah (folder docs/umum)
DOKUMEN_UMUM = [
    ("📕", "Panduan Pembelajaran STEM — Kemendikdasmen 2025", "Panduan_Pembelajaran_STEM_Kemendikdasmen_2025.pdf",
     "Acuan resmi: karakteristik STEM, 7 tahap praktik saintifik & enjinering, komponen perencanaan (Tabel 10), dan asesmen."),
    ("🏫", "Contoh Program Pembelajaran STEM Sekolah 2026/2027", "Contoh_Program_Pembelajaran_STEM_Sekolah_2026-2027.docx",
     "Program STEM tingkat sekolah (disusun SDN Panglayungan) — dapat diadaptasi tiap sekolah gugus."),
    ("🧾", "Instrumen Program STEM 2026/2027", "Instrumen_Program_STEM_2026-2027.docx",
     "Instrumen pemantauan & evaluasi keterlaksanaan program STEM sekolah."),
    ("👨‍💼", "Program Supervisi Kepala Sekolah — STEM", "Program_Supervisi_Kepala_Sekolah_STEM.docx",
     "Instrumen observasi kelas, telaah modul, tindak lanjut, dan rekap supervisi (dipakai di Portal Supervisi)."),
    ("🤝", "Skenario Kegiatan KKG STEM (Rujukan)", "Skenario_Kegiatan_KKG_STEM_Rujukan.docx",
     "Rundown & skenario sesi kelompok kelas (Memahami–Mengaplikasi–Merefleksi) untuk pertemuan KKG gugus."),
]

SUPERVISI_FILE = "Program_Supervisi_Kepala_Sekolah_STEM.docx"

# Tautan Storybook (Gemini) yang sudah dibuat untuk sebagian proyek
STORYBOOK_LINKS = {
    "Berhitung Asyik dengan Benda Kesayangan": "https://share.gemini.google/T2e15Gte53iK",
    "Menara Bentuk: Membangun dari Bangun Ruang": "https://share.gemini.google/b0sCaR82gtjJ",
    "Es Krim Kantong Ajaib: Mengamati Perubahan Wujud": "https://share.gemini.google/79eEvCuaqqtw",
    "Lampu Senter Sederhana: Mengenal Sumber Energi": "https://share.gemini.google/r8SrPUz0hDNJ",
    "Zat Ajaib: Mengamati Perubahan Wujud di Sekitar Kita": "https://share.gemini.google/IwsdiuBQLZQg",
    "Detektif Zat: Memisahkan Campuran di Sekitar Kita": "https://share.gemini.google/QIM2CUdqJePh",
    "Rumah Panas atau Dingin? Eksplorasi Perpindahan Panas": "https://share.gemini.google/5pvLAM4PZhxw",
    "Kompas dan Peta Harta Karun": "https://share.gemini.google/z6pUVKpI40z6",
}

ROLES = ["Guru Kelas", "Kepala Sekolah", "Pengurus KKG / Pengawas"]

STATUS_PROYEK = ["Belum dimulai", "Sedang berjalan", "Terlaksana"]
STATUS_WARNA = {"Belum dimulai": "#9CA3AF", "Sedang berjalan": "#F59E0B", "Terlaksana": "#16A34A"}

LAMPIRAN_TABS = {
    "📋 Observasi": "lampiran1",
    "✅ Telaah": "lampiran2",
    "🤝 Tindak Lanjut": "lampiran3",
    "📊 Rekap": "lampiran4",
}

# Peta kelas -> berkas Daftar Proyek, Daftar Alat & Bahan, dan pasangan
# Judul Proyek (persis seperti di kolom "Judul Proyek" Daftar Proyek) ->
# Modul Proyek STEM lengkap + Panduan Guru Pembuatan Produk (bila ada).
# Seluruh 56 proyek sudah memiliki modul lengkap.
KELAS_DATA = {
    1: {
        "daftar": "Daftar_Proyek_STEM_Kelas1.docx",
        "alat": "Daftar_Alat_dan_Bahan_STEM_Kelas1.docx",
        "proyek": {
            "Bentuk-Bentuk di Sekitarku: Mengenal Bangun Datar dan Bangun Ruang": {"modul": "Modul_Proyek_STEM_Bentuk_Bentuk_di_Sekitarku_Kelas1.docx", "panduan": None},
            "Berhitung Asyik dengan Benda Kesayangan": {"modul": "Modul_Proyek_STEM_Berhitung_Asyik.docx", "panduan": None},
            "Pola Warna dan Bunyi di Sekelilingku": {"modul": "Modul_Proyek_STEM_Pola_Warna_dan_Bunyi_Kelas1.docx", "panduan": "Modul_Proyek_STEM_Pola_Warna_dan_Bunyi_Kelas1_Panduan_Guru.docx"},
            "Ayo Mengukur Tanpa Penggaris!": {"modul": "Modul_Proyek_STEM_Ayo_Mengukur_Tanpa_Penggaris_Kelas1.docx", "panduan": None},
            "Piktogram Kesukaanku: Data Warna dan Buah Favorit": {"modul": "Modul_Proyek_STEM_Piktogram_Kesukaanku_Kelas1.docx", "panduan": None},
            "Kiri-Kanan, Depan-Belakang: Petualangan Posisi Benda": {"modul": "Modul_Proyek_STEM_Kiri_Kanan_Depan_Belakang_Kelas1.docx", "panduan": None},
            "Cerita Pecahan: Berbagi Sama Banyak": {"modul": "Modul_Proyek_STEM_Cerita_Pecahan_Kelas1.docx", "panduan": None},
            "Sama dengan Berapa? Bermain dengan Simbol \"=\"": {"modul": "Modul_Proyek_STEM_Sama_dengan_Berapa_Bermain_dengan_Simbol_Kelas1.docx", "panduan": None},
        },
    },
    2: {
        "daftar": "Daftar_Proyek_STEM_Kelas2.docx",
        "alat": "Daftar_Alat_dan_Bahan_STEM_Kelas2.docx",
        "proyek": {
            "Toko-Tokoan Angka: Berhitung dengan Uang Mainan": {"modul": "Modul_Proyek_STEM_Toko_Tokoan_Angka_Kelas2.docx", "panduan": None},
            "Menara Bentuk: Membangun dari Bangun Ruang": {"modul": "Modul_Proyek_STEM_Menara_Bentuk.docx", "panduan": "Panduan_Guru_Pembuatan_Produk_Menara_Bentuk.docx"},
            "Timbangan Sederhana: Membandingkan Berat Benda": {"modul": "Modul_Proyek_STEM_Timbangan_Sederhana_Kelas2.docx", "panduan": "Modul_Proyek_STEM_Timbangan_Sederhana_Kelas2_Panduan_Guru.docx"},
            "Rumah Pola: Motif Berulang pada Dinding Rumah Mainan": {"modul": "Modul_Proyek_STEM_Rumah_Pola_Kelas2.docx", "panduan": None},
            "Piktogram Cuaca: Mencatat Cuaca Harian": {"modul": "Modul_Proyek_STEM_Piktogram_Cuaca_Kelas2.docx", "panduan": None},
            "Peta Harta Karun Kelasku: Mengenal Posisi dan Arah": {"modul": "Modul_Proyek_STEM_Peta_Harta_Karun_Kelasku_Kelas2.docx", "panduan": None},
            "Pasar Buah Pecahanku: Berbagi Buah Sama Banyak": {"modul": "Modul_Proyek_STEM_Pasar_Buah_Pecahanku_Kelas2.docx", "panduan": None},
            "Kartu Setara: Bermain dengan Simbol \"=\"": {"modul": "Modul_Proyek_STEM_Kartu_Setara_Kelas2.docx", "panduan": None},
        },
    },
    3: {
        "daftar": "Daftar_Proyek_STEM_Kelas3.docx",
        "alat": "Daftar_Alat_dan_Bahan_STEM_Kelas3.docx",
        "proyek": {
            "Tebak Benda Pancaindraku": {"modul": "Modul_Proyek_STEM_Tebak_Benda_Pancaindraku.docx", "panduan": None},
            "Es Krim Kantong Ajaib: Mengamati Perubahan Wujud": {"modul": "Modul_Proyek_STEM_Es_Krim_Kantong_Ajaib.docx", "panduan": "Panduan_Guru_Pembuatan_Produk_Es_Krim_Kantong_Ajaib.docx"},
            "Lampu Senter Sederhana: Mengenal Sumber Energi": {"modul": "Modul_Proyek_STEM_Lampu_Senter_Sederhana_Kelas3.docx", "panduan": "Panduan_Guru_Pembuatan_Produk_Lampu_Senter_Sederhana_Kelas3.docx"},
            "Bola Gaya: Bermain sambil Mengenal Dorong dan Tarik": {"modul": "Modul_Proyek_STEM_Bola_Gaya.docx", "panduan": None},
            "Kotak Cerita Kampungku: Mengenal Sejarah Lingkungan Tempat Tinggal": {"modul": "Modul_Proyek_STEM_Kotak_Cerita_Kampungku.docx", "panduan": None},
            "Wayang Kertas Budayaku: Mengenal Ragam Budaya Nusantara": {"modul": "Modul_Proyek_STEM_Wayang_Kertas_Budayaku_Kelas3.docx", "panduan": None},
            "Pahlawan Sampah: Solusi Sederhana Menjaga Bumi": {"modul": "Modul_Proyek_STEM_Pahlawan_Sampah_Kelas3.docx", "panduan": None},
            "Toko Kelontong Mini: Mengenal Nilai Uang": {"modul": "Modul_Proyek_STEM_Toko_Kelontong_Mini_Kelas3.docx", "panduan": None},
            "Kebun Kecil Siklus Hidup: Menanam dan Mengamati Tanaman": {"modul": "Modul_Proyek_STEM_Kebun_Kecil_Siklus_Hidup_Kelas3.docx", "panduan": None},
            "Drama Mini Peran Warga: Interaksi Sosial di Sekitarku": {"modul": "Modul_Proyek_STEM_Drama_Mini_Peran_Warga_Kelas3.docx", "panduan": None},
        },
    },
    4: {
        "daftar": "Daftar_Proyek_STEM_Kelas4.docx",
        "alat": "Daftar_Alat_dan_Bahan_STEM_Kelas4.docx",
        "proyek": {
            "Pancaindraku Hebat: Alat Peraga Fungsi Panca Indra": {"modul": "Modul_Proyek_STEM_Pancaindraku_Hebat_Kelas4.docx", "panduan": None},
            "Zat Ajaib: Mengamati Perubahan Wujud di Sekitar Kita": {"modul": "Modul_Proyek_STEM_Zat_Ajaib.docx", "panduan": "Panduan_Guru_Pembuatan_Produk_Zat_Ajaib.docx"},
            "Kincir Angin Mini: Sumber dan Perubahan Energi": {"modul": "Modul_Proyek_STEM_Kincir_Angin_Mini_Kelas4.docx", "panduan": None},
            "Mainan Dorong-Tarik: Mengenal Gaya dan Pengaruhnya": {"modul": "Modul_Proyek_STEM_Mainan_Dorong_Tarik_Kelas4.docx", "panduan": "Modul_Proyek_STEM_Mainan_Dorong_Tarik_Kelas4_Panduan_Guru.docx"},
            "Peta Kampungku: Mengenal Letak Wilayah Tempat Tinggal": {"modul": "Modul_Proyek_STEM_Peta_Kampungku_Kelas4.docx", "panduan": None},
            "Grafik Panenku: Piktogram Bentang Alam dan Hasil Bumi Daerahku": {"modul": "Modul_Proyek_STEM_Grafik_Panenku_Kelas4.docx", "panduan": None},
            "Motif Nusantara: Menemukan Pola pada Kain Adat": {"modul": "Modul_Proyek_STEM_Motif_Nusantara_Kelas4.docx", "panduan": None},
            "Kios Kejujuran Sekolah: Mengenal Nilai Uang dan Pengelolaan Keuangan": {"modul": "Modul_Proyek_STEM_Kios_Kejujuran_Sekolah_Kelas4.docx", "panduan": None},
            "Taman Kupu-Kupu Sekolah: Siklus Hidup dan Pelestarian Makhluk Hidup": {"modul": "Modul_Proyek_STEM_Taman_Kupu_Kupu_Sekolah_Kelas4.docx", "panduan": None},
            "Panggung Boneka Peran Warga: Interaksi Sosial di Lingkunganku": {"modul": "Modul_Proyek_STEM_Panggung_Boneka_Peran_Warga_Kelas4.docx", "panduan": None},
        },
    },
    5: {
        "daftar": "Daftar_Proyek_STEM_Kelas5.docx",
        "alat": "Daftar_Alat_dan_Bahan_STEM_Kelas5.docx",
        "proyek": {
            "Menjelajah Tubuhku: Model Sistem Pencernaan Manusia": {"modul": "Modul_Proyek_STEM_Menjelajah_Tubuhku_Kelas5.docx", "panduan": None},
            "Detektif Zat: Memisahkan Campuran di Sekitar Kita": {"modul": "Modul_Proyek_STEM_Detektif_Zat.docx", "panduan": "Panduan_Guru_Pembuatan_Produk_Detektif_Zat.docx"},
            "Rumah Panas atau Dingin? Eksplorasi Perpindahan Panas": {"modul": "Modul_Proyek_STEM_Rumah_Panas_atau_Dingin_Kelas5.docx", "panduan": "Panduan_Guru_Pembuatan_Produk_Rumah_Panas_atau_Dingin_Kelas5.docx"},
            "Roda Berputar: Pesawat Sederhana untuk Memindahkan Beban": {"modul": "Modul_Proyek_STEM_Roda_Berputar_Kelas5.docx", "panduan": "Modul_Proyek_STEM_Roda_Berputar_Kelas5_Panduan_Guru.docx"},
            "Sahabat Bumi: Siklus Air dan Konservasi Lingkungan": {"modul": "Modul_Proyek_STEM_Sahabat_Bumi_Kelas5.docx", "panduan": None},
            "Pulau-Pulau Nusantara: Menjelajah Keunikan Geografis Indonesia": {"modul": "Modul_Proyek_STEM_Pulau_Pulau_Nusantara_Kelas5.docx", "panduan": None},
            "Kenali Budayaku: Pameran Keragaman Suku dan Adat Nusantara": {"modul": "Modul_Proyek_STEM_Kenali_Budayaku_Kelas5.docx", "panduan": None},
            "Kantin Kejujuran Mini: Belajar Jual-Beli dan Kejujuran": {"modul": "Modul_Proyek_STEM_Kantin_Kejujuran_Mini_Kelas5.docx", "panduan": None},
            "Getaran dan Gelombang: Membuat Telepon Kaleng": {"modul": "Modul_Proyek_STEM_Getaran_dan_Gelombang_Kelas5.docx", "panduan": None},
            "Lampu Kunang-Kunang Malam: Mengenal Cahaya dan Bayangan": {"modul": "Modul_Proyek_STEM_Lampu_Kunang_Kunang_Malam_Kelas5.docx", "panduan": None},
        },
    },
    6: {
        "daftar": "Daftar_Proyek_STEM_Kelas6_Lintas_Mapel_v2.docx",
        "alat": "Daftar_Alat_dan_Bahan_STEM_Kelas6.docx",
        "proyek": {
            "Rumah Cerdas Hemat Energi": {"modul": "Modul_Proyek_STEM_Rumah_Cerdas_Kelas6_v2.docx", "panduan": "Panduan_Guru_Pembuatan_Produk_Rumah_Cerdas.docx"},
            "Kompas dan Peta Harta Karun": {"modul": "Modul_Proyek_STEM_Kompas_Peta_Harta_Karun_v2.docx", "panduan": "Panduan_Guru_Pembuatan_Produk_Kompas_Peta.docx"},
            "Ekosistem Mini dalam Botol (Ekobotol)": {"modul": "Modul_Proyek_STEM_Ekobotol.docx", "panduan": None},
            "Alat Penjernih Air Sederhana": {"modul": "Modul_Proyek_STEM_Alat_Penjernih_Air_Sederhana_Kelas6.docx", "panduan": None},
            "Peta Timbul Wilayah Indonesia": {"modul": "Modul_Proyek_STEM_Peta_Timbul_Wilayah_Indonesia_Kelas6.docx", "panduan": None},
            "Model Tata Surya Berskala": {"modul": "Modul_Proyek_STEM_Model_Tata_Surya_Berskala_Kelas6.docx", "panduan": None},
            "Alat Musik dari Barang Bekas: Eksplorasi Bunyi": {"modul": "Modul_Proyek_STEM_Alat_Musik_dari_Barang_Bekas_Kelas6.docx", "panduan": None},
            "Periskop dan Kamera Lubang Jarum": {"modul": "Modul_Proyek_STEM_Periskop_dan_Kamera_Lubang_Jarum_Kelas6.docx", "panduan": None},
            "Pasar Rakyat Mini: Simulasi Kegiatan Ekonomi": {"modul": "Modul_Proyek_STEM_Pasar_Rakyat_Mini_Kelas6.docx", "panduan": None},
            "Garis Waktu Perjuangan dan Keragaman Budaya Nusantara": {"modul": "Modul_Proyek_STEM_Garis_Waktu_Perjuangan_dan_Keragaman_Budaya_Nusantara_Kelas6.docx", "panduan": None},
        },
    },
}