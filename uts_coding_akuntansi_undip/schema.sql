-- Skema Basis Data Relasional, Kontrol Integritas, dan Audit Trail
-- Departemen Akuntansi FEB Universitas Diponegoro
-- Mata Kuliah: Pemrograman / Coding (S1 Akuntansi)
-- Kasus: PT Diponegoro Niaga Makmur (General Ledger & Perpetual Inventory)

CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- ============================================================================
-- SOAL 1: PERANCANGAN SKEMA BUKU BESAR (GENERAL LEDGER) 3NF
-- ============================================================================

-- Tabel Master Bagan Akun (Chart of Accounts)
CREATE TABLE chart_of_accounts (
    account_id VARCHAR(10) PRIMARY KEY,
    account_name VARCHAR(100) NOT NULL,
    normal_balance VARCHAR(6) NOT NULL CHECK (normal_balance IN ('DEBIT', 'CREDIT')),
    report_class VARCHAR(20) NOT NULL CHECK (report_class IN ('ASSET', 'LIABILITY', 'EQUITY', 'REVENUE', 'EXPENSE')),
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

-- Tabel Transaksi Kepala Jurnal (Journal Headers)
CREATE TABLE journal_headers (
    header_id SERIAL PRIMARY KEY,
    trx_date DATE NOT NULL DEFAULT CURRENT_DATE,
    ref_no VARCHAR(30) NOT NULL UNIQUE,
    description TEXT NOT NULL,
    status_posting VARCHAR(10) NOT NULL DEFAULT 'DRAFT' CHECK (status_posting IN ('DRAFT', 'POSTED', 'VOID')),
    created_by VARCHAR(50) NOT NULL DEFAULT 'bizflow',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    hash_checksum VARCHAR(64)
);

-- Tabel Transaksi Rincian Baris Jurnal (Journal Lines)
CREATE TABLE journal_lines (
    line_id SERIAL PRIMARY KEY,
    header_id INT NOT NULL REFERENCES journal_headers(header_id) ON DELETE RESTRICT,
    account_id VARCHAR(10) NOT NULL REFERENCES chart_of_accounts(account_id) ON DELETE RESTRICT,
    debit NUMERIC(15, 2) NOT NULL DEFAULT 0.00 CHECK (debit >= 0),
    credit NUMERIC(15, 2) NOT NULL DEFAULT 0.00 CHECK (credit >= 0),
    line_memo VARCHAR(200),
    CONSTRAINT chk_not_both_zero CHECK (NOT (debit = 0 AND credit = 0))
);

-- Indeks Performa untuk Relasi Foreign Key
CREATE INDEX idx_journal_lines_header ON journal_lines(header_id);
CREATE INDEX idx_journal_lines_account ON journal_lines(account_id);
CREATE INDEX idx_journal_headers_ref ON journal_headers(ref_no);

-- ============================================================================
-- SOAL 2: OTOMASI PERSEDIAAN PERPETUAL & TRIGGER PENCEGAHAN STOK MINUS
-- ============================================================================

-- Tabel Master Barang Dagang
CREATE TABLE inventory_items (
    item_id VARCHAR(10) PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL,
    stock_qty INT NOT NULL DEFAULT 0 CHECK (stock_qty >= 0),
    unit_cost NUMERIC(15, 2) NOT NULL CHECK (unit_cost >= 0)
);

-- Tabel Mutasi Transaksi Persediaan
CREATE TABLE inventory_transactions (
    trx_id SERIAL PRIMARY KEY,
    item_id VARCHAR(10) NOT NULL REFERENCES inventory_items(item_id) ON DELETE RESTRICT,
    trx_type VARCHAR(10) NOT NULL CHECK (trx_type IN ('PURCHASE', 'SALE', 'ADJUSTMENT')),
    qty INT NOT NULL CHECK (qty > 0),
    trx_date TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Fungsi Trigger Pemutakhiran Stok Perpetual dan Pencegahan Stok Negatif
CREATE OR REPLACE FUNCTION trg_update_stock_and_journal()
RETURNS TRIGGER AS $$
DECLARE
    v_current_stock INT;
    v_unit_cost NUMERIC(15, 2);
BEGIN
    -- Kunci baris master item untuk mengeliminasi race condition (concurrency lock)
    SELECT stock_qty, unit_cost
    INTO v_current_stock, v_unit_cost
    FROM inventory_items
    WHERE item_id = NEW.item_id
    FOR UPDATE;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Item persediaan % tidak ditemukan dalam katalog master.', NEW.item_id;
    END IF;

    -- Mutasi berdasarkan jenis transaksi
    IF NEW.trx_type = 'PURCHASE' THEN
        UPDATE inventory_items
        SET stock_qty = stock_qty + NEW.qty
        WHERE item_id = NEW.item_id;

    ELSIF NEW.trx_type = 'SALE' THEN
        -- Validasi pengendalian internal: cegah defisit kuantitas fisik
        IF v_current_stock < NEW.qty THEN
            RAISE EXCEPTION 'PENGENDALIAN INTERNAL DITOLAK: Stok item % tidak mencukupi! Saldo saat ini: %, Permintaan penjualan: %.',
                NEW.item_id, v_current_stock, NEW.qty;
        END IF;

        UPDATE inventory_items
        SET stock_qty = stock_qty - NEW.qty
        WHERE item_id = NEW.item_id;

    ELSIF NEW.trx_type = 'ADJUSTMENT' THEN
        UPDATE inventory_items
        SET stock_qty = NEW.qty
        WHERE item_id = NEW.item_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_manage_inventory_perpetual
BEFORE INSERT ON inventory_transactions
FOR EACH ROW
EXECUTE FUNCTION trg_update_stock_and_journal();

-- ============================================================================
-- SOAL 3: PENEGAKAN JEJAK AUDIT & SIFAT IMUTABEL (IMMUTABILITY)
-- ============================================================================

-- Tabel Catatan Jejak Audit Terinci
CREATE TABLE audit_log (
    log_id SERIAL PRIMARY KEY,
    table_name VARCHAR(50) NOT NULL,
    record_id INT NOT NULL,
    action VARCHAR(10) NOT NULL CHECK (action IN ('INSERT', 'UPDATE', 'DELETE')),
    old_data JSONB,
    new_data JSONB,
    changed_by VARCHAR(50) NOT NULL DEFAULT 'bizflow',
    changed_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Trigger Audit Trail Otomatis pada Kepala Jurnal
CREATE OR REPLACE FUNCTION trg_audit_journal_headers()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO audit_log (table_name, record_id, action, new_data, changed_by)
        VALUES ('journal_headers', NEW.header_id, 'INSERT', to_jsonb(NEW), NEW.created_by);
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_log (table_name, record_id, action, old_data, new_data, changed_by)
        VALUES ('journal_headers', NEW.header_id, 'UPDATE', to_jsonb(OLD), to_jsonb(NEW), NEW.created_by);
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO audit_log (table_name, record_id, action, old_data, changed_by)
        VALUES ('journal_headers', OLD.header_id, 'DELETE', to_jsonb(OLD), 'bizflow');
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_track_journal_headers
AFTER INSERT OR UPDATE OR DELETE ON journal_headers
FOR EACH ROW
EXECUTE FUNCTION trg_audit_journal_headers();

-- Trigger Penegakan Sifat Imutabel (Immutability Gate)
CREATE OR REPLACE FUNCTION enforce_journal_immutability()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.status_posting = 'POSTED' THEN
        RAISE EXCEPTION 'AKSES FINANSIAL DITOLAK: Jurnal transaksi nomor % (ID: %) telah berstatus POSTED dan bersifat imutabel! Perubahan dilarang secara permanen; gunakan prosedur Jurnal Pembalik (Storno).',
            OLD.ref_no, OLD.header_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_lock_posted_journals
BEFORE UPDATE OR DELETE ON journal_headers
FOR EACH ROW
EXECUTE FUNCTION enforce_journal_immutability();

-- Fungsi Posting Jurnal Finansial & Kalkulasi Hash Checksum SHA-256
CREATE OR REPLACE FUNCTION post_journal_voucher(
    p_header_id INT,
    p_operator VARCHAR(50) DEFAULT 'bizflow'
)
RETURNS JSONB AS $$
DECLARE
    v_total_debit NUMERIC(15, 2);
    v_total_credit NUMERIC(15, 2);
    v_status VARCHAR(10);
    v_ref_no VARCHAR(30);
    v_trx_date DATE;
    v_hash VARCHAR(64);
BEGIN
    SELECT status_posting, ref_no, trx_date
    INTO v_status, v_ref_no, v_trx_date
    FROM journal_headers
    WHERE header_id = p_header_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Voucher jurnal ID % tidak ditemukan.', p_header_id;
    END IF;

    IF v_status = 'POSTED' THEN
        RAISE EXCEPTION 'Voucher jurnal % telah berstatus POSTED sebelumnya.', v_ref_no;
    END IF;

    -- Validasi prinsip zero-discrepancy (Total Debit = Total Kredit)
    SELECT COALESCE(SUM(debit), 0), COALESCE(SUM(credit), 0)
    INTO v_total_debit, v_total_credit
    FROM journal_lines
    WHERE header_id = p_header_id;

    IF v_total_debit = 0 AND v_total_credit = 0 THEN
        RAISE EXCEPTION 'Voucher % tidak memiliki baris rincian transaksi.', v_ref_no;
    END IF;

    IF v_total_debit <> v_total_credit THEN
        RAISE EXCEPTION 'Gagal Posting: Asas berpasangan dilanggar! Total Debit (%) tidak sama dengan Total Kredit (%). Selisih: %',
            v_total_debit, v_total_credit, (v_total_debit - v_total_credit);
    END IF;

    -- Hitung tanda tangan integritas kriptografis SHA-256
    v_hash := encode(
        digest(
            p_header_id::text || '|' || v_ref_no || '|' || v_trx_date::text || '|' || v_total_debit::text || '|' || p_operator,
            'sha256'
        ),
        'hex'
    );

    UPDATE journal_headers
    SET status_posting = 'POSTED',
        hash_checksum = v_hash
    WHERE header_id = p_header_id;

    RETURN jsonb_build_object(
        'success', TRUE,
        'header_id', p_header_id,
        'ref_no', v_ref_no,
        'total_amount', v_total_debit,
        'status', 'POSTED',
        'hash_checksum', v_hash
    );
END;
$$ LANGUAGE plpgsql;

-- Fungsi Pembuatan Jurnal Pembalik Otomatis (Reversing Entry / Storno)
CREATE OR REPLACE FUNCTION create_reversing_entry(
    p_original_header_id INT,
    p_operator VARCHAR(50) DEFAULT 'bizflow',
    p_reversal_reason TEXT DEFAULT 'Koreksi administratif'
)
RETURNS JSONB AS $$
DECLARE
    v_orig_header RECORD;
    v_new_header_id INT;
    v_rev_ref_no VARCHAR(30);
    v_line RECORD;
BEGIN
    SELECT * INTO v_orig_header
    FROM journal_headers
    WHERE header_id = p_original_header_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Jurnal asal ID % tidak ditemukan.', p_original_header_id;
    END IF;

    IF v_orig_header.status_posting <> 'POSTED' THEN
        RAISE EXCEPTION 'Hanya jurnal berstatus POSTED yang memerlukan prosedur jurnal pembalik.';
    END IF;

    v_rev_ref_no := 'REV-' || v_orig_header.ref_no;

    INSERT INTO journal_headers (trx_date, ref_no, description, status_posting, created_by)
    VALUES (
        CURRENT_DATE,
        v_rev_ref_no,
        'Koreksi Pembalik atas voucher ' || v_orig_header.ref_no || '. Alasan: ' || p_reversal_reason,
        'DRAFT',
        p_operator
    )
    RETURNING header_id INTO v_new_header_id;

    -- Pertukaran posisi debit dan kredit
    FOR v_line IN SELECT * FROM journal_lines WHERE header_id = p_original_header_id LOOP
        INSERT INTO journal_lines (header_id, account_id, debit, credit, line_memo)
        VALUES (
            v_new_header_id,
            v_line.account_id,
            v_line.credit,
            v_line.debit,
            'Pembalik baris ID ' || v_line.line_id
        );
    END LOOP;

    RETURN jsonb_build_object(
        'success', TRUE,
        'original_header_id', p_original_header_id,
        'reversal_header_id', v_new_header_id,
        'reversal_ref_no', v_rev_ref_no
    );
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- DATA INISIALISASI PENGUJIAN (SEED DATA)
-- ============================================================================

INSERT INTO chart_of_accounts (account_id, account_name, normal_balance, report_class) VALUES
('1101', 'Kas Operasional', 'DEBIT', 'ASSET'),
('1102', 'Bank BNI Rekening Utama', 'DEBIT', 'ASSET'),
('1103', 'Piutang Usaha', 'DEBIT', 'ASSET'),
('1104', 'Persediaan Barang Dagang', 'DEBIT', 'ASSET'),
('2101', 'Hutang Usaha', 'CREDIT', 'LIABILITY'),
('2102', 'Beban Akrual PPN Keluaran', 'CREDIT', 'LIABILITY'),
('3101', 'Modal Saham Disetor', 'CREDIT', 'EQUITY'),
('4101', 'Pendapatan Penjualan Ritel', 'CREDIT', 'REVENUE'),
('5101', 'Beban Pokok Pendapatan (HPP)', 'DEBIT', 'EXPENSE'),
('5201', 'Beban Gaji & Upah Karyawan', 'DEBIT', 'EXPENSE'),
('5202', 'Beban Sewa Gedung Kantor', 'DEBIT', 'EXPENSE'),
('5203', 'Beban Listrik, Air & Utilitas', 'DEBIT', 'EXPENSE'),
('5204', 'Beban Perlengkapan Toko', 'DEBIT', 'EXPENSE')
ON CONFLICT (account_id) DO NOTHING;

INSERT INTO inventory_items (item_id, item_name, stock_qty, unit_cost) VALUES
('BRG-001', 'Beras Premium 5kg', 50, 68000.00),
('BRG-002', 'Minyak Goreng Sawit 2L', 30, 32000.00),
('BRG-003', 'Gula Pasir Kristal 1kg', 40, 16500.00),
('BRG-004', 'Tepung Terigu Serbaguna 1kg', 25, 12000.00)
ON CONFLICT (item_id) DO NOTHING;
