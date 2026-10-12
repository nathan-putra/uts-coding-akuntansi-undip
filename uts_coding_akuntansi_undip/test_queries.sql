-- ============================================================================
-- PANDUAN PENGUJIAN KONTROL INTEGRITAS & PENGAMBILAN TANGKAPAN LAYAR (SUPABASE)
-- Departemen Akuntansi FEB Universitas Diponegoro
-- ============================================================================

-- ----------------------------------------------------------------------------
-- UJI 1: INSERT DATA NORMAL TRANSAKSI KAS KELUAR (BERHASIL)
-- ----------------------------------------------------------------------------
INSERT INTO journal_headers (ref_no, trx_date, description, created_by)
VALUES ('BKK-2026/10/001', CURRENT_DATE, 'Pembayaran Beban Sewa Kantor Bulan Oktober 2026', 'bizflow');

INSERT INTO journal_lines (header_id, account_id, debit, credit, line_memo)
VALUES 
(1, '5202', 3500000.00, 0.00, 'Alokasi Beban Sewa Ruang'),
(1, '1101', 0.00, 3500000.00, 'Pengeluaran Kas Operasional');

-- Verifikasi data
SELECT h.ref_no, h.trx_date, h.status_posting, l.account_id, a.account_name, l.debit, l.credit
FROM journal_headers h
JOIN journal_lines l ON h.header_id = l.header_id
JOIN chart_of_accounts a ON l.account_id = a.account_id
WHERE h.ref_no = 'BKK-2026/10/001';

-- ----------------------------------------------------------------------------
-- UJI 2 (NEGATIF): CEGAH BARIS DENGAN DEBIT DAN KREDIT NOL BERSAMAAN
-- Ekspektasi: Gagal dengan pesan error 'chk_not_both_zero'
-- ----------------------------------------------------------------------------
INSERT INTO journal_lines (header_id, account_id, debit, credit)
VALUES (1, '1101', 0.00, 0.00);

-- ----------------------------------------------------------------------------
-- UJI 3 (NEGATIF): CEGAH NOMINAL DEBIT ATAU KREDIT BERNILAI MINUS
-- Ekspektasi: Gagal dengan pesan error constraint debit >= 0
-- ----------------------------------------------------------------------------
INSERT INTO journal_lines (header_id, account_id, debit, credit)
VALUES (1, '1101', -500000.00, 0.00);

-- ----------------------------------------------------------------------------
-- UJI 4 (NEGATIF): CEGAH PENGHAPUSAN AKUN ATAU HEADER YANG MASIH DIGUNAKAN
-- Ekspektasi: Gagal dengan pesan error 'violates foreign key constraint' (ON DELETE RESTRICT)
-- ----------------------------------------------------------------------------
DELETE FROM chart_of_accounts WHERE account_id = '1101';
DELETE FROM journal_headers WHERE header_id = 1;

-- ----------------------------------------------------------------------------
-- UJI 5: UJI MUTASI PERSEDIAAN OTOMATIS (PEMBELIAN BERHASIL)
-- Cek stok awal BRG-001 (50 unit), lalu lakukan pembelian 20 unit
-- ----------------------------------------------------------------------------
INSERT INTO inventory_transactions (item_id, trx_type, qty)
VALUES ('BRG-001', 'PURCHASE', 20);

-- Verifikasi: stock_qty otomatis bertambah menjadi 70
SELECT item_id, item_name, stock_qty FROM inventory_items WHERE item_id = 'BRG-001';

-- ----------------------------------------------------------------------------
-- UJI 6 (NEGATIF): UJI TRIGGER ANTI-NEGATIVE INVENTORY (PENJUALAN MELEBIHI STOK)
-- Ekspektasi: Gagal dan memicu RAISE EXCEPTION 'PENGENDALIAN INTERNAL DITOLAK'
-- ----------------------------------------------------------------------------
-- Stok BRG-002 saat ini 30 unit, coba jual 35 unit:
INSERT INTO inventory_transactions (item_id, trx_type, qty)
VALUES ('BRG-002', 'SALE', 35);

-- Bukti Rollback: Cek saldo stok tetap utuh di angka 30 unit
SELECT item_id, item_name, stock_qty FROM inventory_items WHERE item_id = 'BRG-002';

-- ----------------------------------------------------------------------------
-- UJI 7: POSTING VOUCHER JURNAL & PENETAPAN HASH KRIPTOGRAFIS SHA-256
-- ----------------------------------------------------------------------------
SELECT post_journal_voucher(1, 'bizflow');

-- Verifikasi status_posting menjadi 'POSTED' dan kolom hash_checksum terisi
SELECT header_id, ref_no, status_posting, hash_checksum FROM journal_headers WHERE header_id = 1;

-- ----------------------------------------------------------------------------
-- UJI 8 (NEGATIF): PENEGAKAN SIFAT IMUTABEL (IMMUTABILITY) PADA DATA POSTED
-- Ekspektasi: Gagal dan memicu error penolakan manipulasi finansial
-- ----------------------------------------------------------------------------
UPDATE journal_headers SET description = 'Manipulasi deskripsi ilegal' WHERE header_id = 1;
DELETE FROM journal_headers WHERE header_id = 1;

-- ----------------------------------------------------------------------------
-- UJI 9: KOREKSI DATA MELALUI JURNAL PEMBALIK (STORNO / REVERSING ENTRY)
-- ----------------------------------------------------------------------------
SELECT create_reversing_entry(1, 'bizflow', 'Salah pembebanan periode akuntansi');

-- Verifikasi kemunculan voucher jurnal pembalik REV-BKK-2026/10/001
SELECT h.ref_no, h.description, l.account_id, l.debit, l.credit
FROM journal_headers h
JOIN journal_lines l ON h.header_id = l.header_id
WHERE h.ref_no LIKE 'REV-%';

-- ----------------------------------------------------------------------------
-- UJI 10: INSPEKSI CATATAN JEJAK AUDIT (AUDIT LOG HISTORI LENGKAP)
-- ----------------------------------------------------------------------------
SELECT log_id, table_name, record_id, action, changed_by, changed_at, new_data
FROM audit_log
ORDER BY log_id DESC;
