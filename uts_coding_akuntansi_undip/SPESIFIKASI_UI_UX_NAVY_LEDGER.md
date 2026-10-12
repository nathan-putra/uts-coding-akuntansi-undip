# DOKUMEN SPESIFIKASI REKAYASA BALIK (REVERSE SPECIFICATION) UI/UX
## SISTEM BUKU BESAR BIZFLOW LEDGER — DEPARTEMEN AKUNTANSI FEB UNDIP
**Mata Kuliah:** Pemrograman / Coding Akuntansi  
**Dosen Pengampu:** Totok Dewayanto  
**Modul Aplikasi:** Purwarupa Entri Voucher Kas Keluar, Otomasi Mutasi Stok, & Jejak Audit (Soal 3.1)  
**Filosofi Desain:** *Navy Ledger Design System — High-Trust Financial Enterprise*

---

### 1. Filosofi Desain & Dasar Pemikiran (Design Rationale)

Antarmuka **BizFlow Ledger** dirancang berdasarkan prinsip sistem informasi akuntansi korporat modern (setara SAP, Oracle NetSuite, dan Odoo ERP), di mana fungsi estetika tidak boleh mengorbankan **akurasi data, kejelasan hierarki numerik, dan pengendalian internal (*internal control*)**.

Prinsip desain utama:
1. **Zero-Distraction Layout**: Menghindari elemen dekoratif tanpa makna (*anti-slop*), seperti gradien warna neon, bayangan melayang (*excessive shadow*), atau ikon emoji yang mengaburkan data finansial.
2. **Semantic Color Mapping**: Warna hanya digunakan untuk menyampaikan informasi status finansial yang bermakna, bukan sebagai dekorasi semata.
3. **High-Contrast Data Precision**: Memastikan angka desimal dan titik ribuan lurus secara vertikal (*tabular numbers*) untuk memudahkan pembacaan saldo oleh staf dan auditor keuangan.

---

### 2. Design Tokens & Palet Warna (Navy Ledger Palette)

Palet warna *Navy Ledger* dipilih secara khusus untuk mencerminkan stabilitas lembaga keuangan, dengan rasio kontras yang melampaui standar aksesibilitas **WCAG 2.1 Level AAA (7:1)**.

| Token Desain | Kode HEX | Peruntukan Antarmuka | Rasio Kontras (vs Putih) | Makna Akuntansi / Status |
| :--- | :---: | :--- | :---: | :--- |
| `--deep-navy` | `#102A43` | Sidebar utama, judul halaman, teks penekanan tinggi | **12.6 : 1** (AAA) | Kewenangan & fondasi data master |
| `--primary-navy` | `#173B67` | Tombol aksi utama, tab navigasi aktif, header tabel | **9.8 : 1** (AAA) | Aksi finansial terotorisasi |
| `--bg-main` | `#FFFFFF` | Latar belakang kartu (*cards*), form input, tabel jurnal | N/A | Bidang kerja entri data |
| `--bg-soft` | `#F5F7FA` | Latar kanvas aplikasi, striping tabel, panel sekunder | N/A | Pemisah hierarki visual |
| `--border-gray` | `#E2E8F0` | Garis batas (*border*) input, pembatas baris debit/kredit | N/A | Struktur pemisah sel 3NF |
| `--text-muted` | `#526174` | Label input, deskripsi pembantu, stempel waktu | **5.3 : 1** (AA) | Metadata pendukung |
| `--status-success` | `#16805D` | Indikator Seimbang (*Balanced*), badge `POSTED` | **4.8 : 1** (AA) | Asas berpasangan terpenuhi ($D = K$) |
| `--status-success-bg` | `#EBF7F2` | Latar panel saat *Zero Discrepancy* | N/A | Konfirmasi sistem valid |
| `--status-error` | `#C83C45` | Peringatan selisih (*Unbalanced*), eksepsi stok minus | **4.9 : 1** (AA) | Pelanggaran kontrol / data ditolak |
| `--status-error-bg` | `#FDF2F2` | Latar panel saat terjadi selisih debit-kredit | N/A | Penanda tombol submit terkunci |
| `--status-warning` | `#B76E00` | Badge status transaksi `DRAFT` | **4.6 : 1** (AA) | Menunggu verifikasi / belum diposting |

---

### 3. Tipografi Finansial & Skala Teks (Typography Hierarchy)

* **Font Stack**: `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif`.
* **Kepatuhan Numerik Akuntansi**: Seluruh kolom nominal debit, kredit, stok barang, dan persentase diatur menggunakan atribut CSS:
  ```css
  font-variant-numeric: tabular-nums;
  ```
  *Rasional:* Menjamin setiap karakter angka (0–9) memiliki lebar horizontal yang identik (*monospaced digits*), sehingga angka jutaan dan ribuan pada kolom Debit dan Kredit selalu sejajar vertikal dan mudah diverifikasi oleh auditor.

#### Skala Hirarki Tipografi:
* **H1 (Page Title)**: 20px / Bold / `#102A43` (Judul Modul Kerja)
* **H2 (Card Title)**: 15px / Bold / `#102A43` (Nama Dokumen Formulir / Tabel Buku Besar)
* **Body / Label Form**: 12px / Semi-Bold / `#102A43` (Atribut Input Transaksi)
* **Table Data**: 13px / Regular / `#102A43` (Rincian Akun & Memo Jurnal)
* **Status Badge / Caption**: 11px / Bold / `#FFFFFF` atau Warna Semantik (Stempel Posting & Kategori)

---

### 4. Arsitektur Tata Letak & Navigasi (Layout Grid & SPA Architecture)

Antarmuka menggunakan arsitektur **Single Page Application (SPA)** yang terdiri dari dua area utama:
1. **Fixed Sidebar Kiri (Lebar: 240px)**:
   - *Header Brand*: Identitas institusi (*BizFlow - FEB Universitas Diponegoro*).
   - *Navigasi Modul*: 6 Tombol navigasi berbasis SVG icons tanpa emoji (*Dashboard, Entri Kas Keluar, Buku Besar, Gudang & Stok, Jejak Audit, dan Konektor Supabase*).
   - *Footer Operator*: Menampilkan peran pengguna (*Staf Akuntan Utama - Operator: bizflow*).
2. **Dynamic Main Content (Responsif Flex/Grid)**:
   - *Top Bar*: Breadcrumb navigasi hierarkis, kolom pencarian global (Ctrl+K), dan tombol segarkan data.
   - *Workspace Body*: Ruang kerja modular dengan transisi tampilan instan tanpa *page reload*.

---

### 5. Spesifikasi Komponen & Mesin Logika Interaktif

#### A. Komponen Live Balanced Indicator (Zero-Discrepancy Gate - Soal 3.1)
Komponen ini merupakan inti pengendalian internal transaksi kas keluar yang memvalidasi bahwa tidak ada jurnal timpang yang dapat masuk ke buku besar:

* **Logika Kalkulasi**:
  $$\text{Total Debit} = \sum \text{Debit}_i$$
  $$\text{Total Kredit} = \sum \text{Kredit}_i$$
  $$\text{Selisih (Discrepancy)} = |\text{Total Debit} - \text{Total Kredit}|$$

* **Status State Machine**:
  1. **State Netral / Kosong** ($\text{Total Debit} = 0 \land \text{Total Kredit} = 0$):
     - Panel berwarna abu-abu netral (`#F5F7FA`), badge: `"MENUNGGU INPUT BARIS"`.
     - Tombol *Posting Voucher*: **Terkunci (*disabled = true*)**.
  2. **State Tidak Seimbang / Error** ($\text{Selisih} > 0$):
     - Panel berganti latar merah muda (`#FDF2F2`) dengan garis batas merah (`#C83C45`).
     - Badge status: `"TIDAK SEIMBANG (SELISIH: Rp ...)"`.
     - Tombol *Posting Voucher*: **Terkunci mati (*disabled = true*, cursor *not-allowed*)**.
     - Teks bantuan: *"Peringatan Sistem: Asas berpasangan dilanggar. Tombol posting dinonaktifkan sampai selisih bernilai Rp 0."*
  3. **State Seimbang / Sukses** ($\text{Selisih} = 0 \land \text{Total Debit} > 0$):
     - Panel berganti latar hijau muda (`#EBF7F2`) dengan garis batas hijau (`#16805D`).
     - Badge status: `"ZERO DISCREPANCY (SEIMBANG)"`.
     - Tombol *Posting Voucher*: **Aktif penuh (*disabled = false*, warna *Primary Navy*)**.
     - Teks bantuan: *"Pengendalian internal terpenuhi. Transaksi valid untuk diposting ke Buku Besar."*

---

#### B. Komponen Rincian Baris Dinamis (Journal Lines - Normalisasi 3NF)
* Memungkinkan penambahan baris tak terbatas (`+ Tambah Baris Akun`) dan penghapusan baris (`x`).
* Kolom terdiri dari: *Bagan Akun (Dropdown COA), Keterangan Baris (Memo), Input Debit, Input Kredit, dan Aksi Hapus*.
* Otomasi Input: Mengisi nominal Debit otomatis mengosongkan kolom Kredit pada baris yang sama, mencegah kesalahan operator memasukkan dua nominal pada satu baris akun.

---

#### C. Komponen Simulasi Trigger Persediaan & Anti-Stok Minus (Soal 2.1)
* **Katalog Master**: Menampilkan 4 item persediaan fisik (`BRG-001` s.d `BRG-004`) dengan stok awal dan harga pokok perpetual.
* **Mesin Trigger Otomatis**:
  - Transaksi `PURCHASE` menambah kuantitas stok seketika.
  - Transaksi `SALE` dengan kuantitas $\le \text{stok}$ mengurangi saldo stok seketika.
  - Transaksi `SALE` dengan kuantitas $> \text{stok}$ memicu **Eksepsi Pengendalian Internal**:
    Memunculkan kotak error merah dengan pesan resmi trigger database:
    `[TRIGGER EXCEPTION & ROLLBACK]: PENGENDALIAN INTERNAL DITOLAK! Stok barang BRG-002 tidak mencukupi untuk diproses. Saldo saat ini: 30 unit | Permintaan: 45 unit. Transaksi dibatalkan (ROLLBACK) oleh trigger database. Saldo fisik tetap utuh.`

---

#### D. Komponen Jejak Audit & Laboratorium Imutabilitas (Soal 3.2)
* **Audit Stream**: Mencatat setiap aktivitas mutasi (`INSERT`, `POSTED`, `MUTASI_STOK`, `REVERSAL`, `REJECTED`) dengan stempel waktu detik, operator `bizflow`, dan tanda tangan digital SHA-256.
* **Immutability Gate**:
  - Tombol simulasi pembobolan menguji manipulasi transaksi `POSTED`.
  - Sistem menolak aksi `UPDATE` atau `DELETE` dengan pesan error imutabilitas.
  - Tombol *Buat Jurnal Pembalik (Storno)* menerbitkan voucher berkode `REV-...` yang menukar saldo Debit dan Kredit untuk menetralisasi kesalahan buku besar tanpa merusak riwayat transaksi.

---

### 6. Dokumentasi Prompt Instruksi AI (Gemini Canvas - Soal 3.1a)

Berikut adalah naskah prompt instruksi terstruktur yang digunakan untuk menghasilkan purwarupa UI/UX di atas:

> *"Rancang antarmuka aplikasi web modern kelas enterprise untuk Sistem Buku Besar (General Ledger) Akuntansi dengan nama 'BizFlow Ledger' untuk Departemen Akuntansi FEB Undip. Terapkan palet warna profesional 'Navy Ledger' (Deep Navy #102A43, Primary Navy #173B67, Background #F5F7FA dan #FFFFFF, Status Success Green #16805D, dan Status Error Red #C83C45) dengan kepatuhan kontras tinggi WCAG AAA dan tipografi finansial tabular (font-variant-numeric: tabular-nums).*
>
> *Antarmuka harus mengadopsi arsitektur Single Page Application (SPA) dengan navigasi sidebar interaktif yang mencakup modul: Tableau de bord, Entri Kas Keluar, Buku Jurnal Umum, Gudang & Mutasi Stok Perpetual, dan Jejak Audit.*
>
> *Pada modul Entri Kas Keluar, bangun formulir voucher bukti kas keluar (BKK) dinamis yang memiliki header transaksi dan rincian baris akun debit/kredit yang dapat ditambah atau dihapus. Integrasikan komponen 'Live Balanced Indicator' yang menghitung total debit, total kredit, dan selisih secara realtime. Terapkan aturan bisnis pengendalian internal mutlak: Tombol Submit 'Posting Voucher ke Buku Besar' WAJIB berstatus terkunci (disabled) selama total debit tidak sama dengan total kredit atau bernilai nol (unbalanced), dan hanya boleh aktif saat terjadi keseimbangan sempurna (Zero Discrepancy).*
>
> *Sertakan pula simulasi database trigger persediaan perpetual yang menolak penjualan melebihi stok fisik (anti-negative stock exception) serta mekanisme imutabilitas transaksi POSTED yang dilindungi stempel tanda tangan kriptografis SHA-256 dan prosedur jurnal pembalik (storno)."*

---

### 7. Ringkasan Verifikasi Kepatuhan Standar Akuntansi (NotebookLM - Soal 3.1b)

Berdasarkan pengujian analitis kepatuhan standar akuntansi keuangan:
1. **PSAK 2 (Laporan Arus Kas)**:
   Modul Voucher Kas Keluar memastikan pengeluaran kas operasional secara simultan mencatat pengakuan beban/liabilitas di sisi Debit dan penurunan akun Kas & Setara Kas (Akun `1101`/`1102`) di sisi Kredit secara berpasangan pada periode berjalan.
2. **PSAK 1 (Penyajian Laporan Keuangan)**:
   Penegakan validasi *Zero-Discrepancy Gate* di sisi antarmuka dan *Check Constraint* di sisi database memastikan persamaan dasar akuntansi ($\text{Aset} = \text{Liabilitas} + \text{Ekuitas}$) tidak pernah mengalami ketidakseimbangan (*unbalanced balance sheet*).
3. **Pengendalian Intern (Internal Control COSO Framework)**:
   Penomoran bukti transaksi terstruktur (*pre-numbered voucher* `BKK-2026/10/xxx`), penguncian transaksi berstatus `POSTED` (sifat imutabel), serta pencatatan otomatis identitas operator dan stempel waktu memenuhi asersi audit **Kelengkapan (*Completeness*)**, **Keterjadian (*Occurrence*)**, dan **Pisah Batas (*Cut-Off*)**.
