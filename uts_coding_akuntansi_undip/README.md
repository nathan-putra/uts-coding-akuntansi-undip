# Repositori Proyek UTS Pemrograman / Coding Akuntansi FEB Undip
**Dosen Pengampu:** Totok Dewayanto  
**Program Studi:** S1 Reguler Akuntansi, Fakultas Ekonomika dan Bisnis, Universitas Diponegoro  
**Kasus Entitas:** PT Diponegoro Niaga Makmur (General Ledger & Perpetual Inventory Automation)

---

## 1. Struktur Berkas Repositori

Semua berkas proyek disusun secara rapi dan modular dalam satu folder:

| Nama Berkas | Peruntukan Soal | Deskripsi Teknis |
| :--- | :--- | :--- |
| `schema.sql` | Soal 1.2, 2.1, 3.2 | Skrip DDL PostgreSQL/Supabase: skema relasional 3NF, check constraints, trigger mutasi stok perpetual dengan anti-stok negatif, trigger penguncian data imutabel, tabel audit log, serta fungsi posting dan jurnal pembalik. |
| `test_queries.sql` | Soal 1, 2, 3 (Uji) | Kumpulan skenario pengujian positif (data normal) dan negatif (pelanggaran batasan sistem) untuk keperluan dokumentasi tangkapan layar di Supabase. |
| `index.html` | Soal 3.1 | Antarmuka purwarupa web interaktif dengan desain korporat *BizFlow* dan palet *Navy Ledger*. |
| `styles.css` | Soal 3.1 | Penataan visual berbasis palet *Navy Ledger*, kontras tinggi WCAG AAA, dan tipografi finansial tabular. |
| `app.js` | Soal 3.1, 3.2 | Logika JavaScript mandiri untuk kalkulasi otomatis debit-kredit realtime (*Live Balanced Indicator*), validasi gerbang *zero-discrepancy*, dan pencatatan jejak audit dengan hash SHA-256. |
| `app.py` | Soal 3.1 (Alternatif) | Implementasi purwarupa web alternatif menggunakan Python Streamlit. |
| `README.md` | Dokumentasi | Panduan instalasi, cara eksekusi sistem, dan ringkasan teori akuntansi komputasional. |

---

## 2. Cara Menjalankan Aplikasi Web

Anda memiliki dua pilihan antarmuka yang keduanya 100% berfungsi secara nyata:

### Opsi A: Antarmuka Web Dashboard BizFlow (Direkomendasikan)
Antarmuka ini dibangun menggunakan HTML5, CSS3 (*Navy Ledger*), dan JavaScript modern.
1. Cukup klik ganda (*double click*) berkas `index.html` untuk langsung membukanya di browser apa saja (Google Chrome, Microsoft Edge, atau Mozilla Firefox).
2. Atau, jalankan server lokal sederhana melalui terminal PowerShell di dalam folder ini:
   ```powershell
   python -m http.server 8080
   ```
   Lalu buka tautan: `http://localhost:8080` pada browser Anda.

### Opsi B: Antarmuka Web Python Streamlit
1. Buka PowerShell di dalam folder ini, kemudian jalankan:
   ```powershell
   streamlit run app.py
   ```
2. Aplikasi akan otomatis terbuka pada peramban web di alamat: `http://localhost:8501`.

---

## 3. Fitur Utama Pengendalian Finansial

1. **Live Balanced Indicator (Zero Discrepancy Gate)**:
   - Sistem secara *realtime* menghitung total debit, total kredit, dan selisih (*discrepancy*).
   - Tombol **Posting Voucher** otomatis terkunci (*disabled*) jika terjadi selisih, dan baru aktif ketika Total Debit = Total Kredit serta bernilai > 0.
2. **Otomasi Persediaan Perpetual & Pencegahan Stok Negatif**:
   - Transaksi penjualan (*SALE*) yang melebihi ketersediaan fisik gudang otomatis dibatalkan (*rollback*) dengan eksepsi `RAISE EXCEPTION`.
   - Menggunakan klausa `SELECT ... FOR UPDATE` untuk mencegah fenomena *race condition / overselling* antar-kasir.
3. **Imutabilitas Transaksi & Jejak Audit (Audit Trail)**:
   - Transaksi berstatus `POSTED` terkunci permanen di tingkat database; modifikasi (`UPDATE`) dan penghapusan (`DELETE`) akan ditolak secara mutlak.
   - Perbaikan transaksi salah wajib menggunakan mekanisme **Jurnal Pembalik (Reversing Entry / Storno)**.
   - Dilengkapi stempel integritas digital **SHA-256 Checksum** untuk mendeteksi manipulasi database secara ilegal.

---

## 4. Panduan Eksekusi di Supabase

1. Buka proyek Supabase Anda di `https://supabase.com`.
2. Masuk ke menu **SQL Editor**.
3. Salin dan jalankan seluruh isi berkas `schema.sql` (klik **Run**).
4. Untuk mendokumentasikan bukti uji pengujian:
   - Salin blok-blok kueri dari berkas `test_queries.sql`.
   - Jalankan satu per satu untuk mendapatkan tangkapan layar bukti eksekusi sukses maupun tangkapan layar pesan error merah (validasi batasan) untuk dilampirkan pada laporan tugas akhir.
