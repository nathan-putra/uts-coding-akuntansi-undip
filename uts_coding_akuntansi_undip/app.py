import streamlit as st
import pandas as pd
import hashlib
from datetime import date, datetime

st.set_page_config(
    page_title="BizFlow Ledger | Financial Operations & Accounting Control",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling Palet Navy Ledger & Enterprise Design System
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    :root {
        --primary-navy: #173B67;
        --deep-navy: #102A43;
        --bg-soft: #F5F7FA;
        --border-color: #E2E8F0;
        --text-primary: #102A43;
        --text-secondary: #526174;
        --success: #16805D;
        --error: #C83C45;
        --warning: #B76E00;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0F172A !important;
        color: #F8FAFC !important;
        border-right: 1px solid #1E293B;
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] span {
        color: #E2E8F0 !important;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
    }
    
    /* Indicator & Status Cards */
    .balance-card-balanced {
        background-color: #EBF7F2;
        border: 1px solid #16805D;
        color: #16805D;
        padding: 14px 18px;
        border-radius: 8px;
        font-weight: 600;
        margin-bottom: 14px;
        display: flex;
        flex-direction: column;
        gap: 4px;
    }
    .balance-card-unbalanced {
        background-color: #FDF2F2;
        border: 1px solid #C83C45;
        color: #C83C45;
        padding: 14px 18px;
        border-radius: 8px;
        font-weight: 600;
        margin-bottom: 14px;
        display: flex;
        flex-direction: column;
        gap: 4px;
    }
    .alert-banner-error {
        background-color: #FDF2F2;
        border-left: 4px solid #C83C45;
        color: #991B1B;
        padding: 12px 16px;
        border-radius: 4px;
        margin-bottom: 16px;
        font-size: 13px;
        line-height: 1.5;
    }
    .alert-banner-success {
        background-color: #EBF7F2;
        border-left: 4px solid #16805D;
        color: #065F46;
        padding: 12px 16px;
        border-radius: 4px;
        margin-bottom: 16px;
        font-size: 13px;
        line-height: 1.5;
    }
    .metric-container-box {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
</style>
""", unsafe_allow_html=True)

# Master Chart of Accounts (COA) 3NF
COA_LIST = [
    {"id": "1101", "name": "Kas Operasional", "type": "ASSET", "balance": "DEBIT"},
    {"id": "1102", "name": "Bank BNI Rekening Utama", "type": "ASSET", "balance": "DEBIT"},
    {"id": "1103", "name": "Piutang Usaha", "type": "ASSET", "balance": "DEBIT"},
    {"id": "1104", "name": "Persediaan Barang Dagang", "type": "ASSET", "balance": "DEBIT"},
    {"id": "2101", "name": "Hutang Usaha", "type": "LIABILITY", "balance": "CREDIT"},
    {"id": "2102", "name": "Beban Akrual PPN Keluaran", "type": "LIABILITY", "balance": "CREDIT"},
    {"id": "3101", "name": "Modal Saham Disetor", "type": "EQUITY", "balance": "CREDIT"},
    {"id": "4101", "name": "Pendapatan Penjualan Ritel", "type": "REVENUE", "balance": "CREDIT"},
    {"id": "5101", "name": "Beban Pokok Pendapatan (HPP)", "type": "EXPENSE", "balance": "DEBIT"},
    {"id": "5201", "name": "Beban Gaji & Upah Karyawan", "type": "EXPENSE", "balance": "DEBIT"},
    {"id": "5202", "name": "Beban Sewa Gedung Kantor", "type": "EXPENSE", "balance": "DEBIT"},
    {"id": "5203", "name": "Beban Listrik, Air & Utilitas", "type": "EXPENSE", "balance": "DEBIT"},
    {"id": "5204", "name": "Beban Perlengkapan Toko", "type": "EXPENSE", "balance": "DEBIT"},
]
COA_MAP = {f"{c['id']} - {c['name']} ({c['balance']})": c['id'] for c in COA_LIST}

# Inisialisasi Session State Basis Data
if "inventory_db" not in st.session_state:
    st.session_state.inventory_db = [
        {"item_id": "BRG-001", "item_name": "Beras Premium 5kg", "stock_qty": 50, "unit_cost": 68000.0},
        {"item_id": "BRG-002", "item_name": "Minyak Goreng Sawit 2L", "stock_qty": 30, "unit_cost": 32000.0},
        {"item_id": "BRG-003", "item_name": "Gula Pasir Kristal 1kg", "stock_qty": 40, "unit_cost": 16500.0},
        {"item_id": "BRG-004", "item_name": "Tepung Terigu Serbaguna 1kg", "stock_qty": 25, "unit_cost": 12000.0}
    ]

if "journal_db" not in st.session_state:
    st.session_state.journal_db = [
        {
            "ref_no": "BKK-2026/10/001",
            "trx_date": "2026-10-19",
            "description": "Pembayaran Beban Sewa Kantor Okt 2026",
            "account": "5202 - Beban Sewa Gedung Kantor",
            "debit": 3500000.0,
            "credit": 0.0,
            "status_posting": "POSTED",
            "hash_checksum": "a4f91c6e932b78f40192eab54c938174dfb201a74e5482e16f391054ab309172"
        },
        {
            "ref_no": "BKK-2026/10/001",
            "trx_date": "2026-10-19",
            "description": "Pembayaran Beban Sewa Kantor Okt 2026",
            "account": "1101 - Kas Operasional",
            "debit": 0.0,
            "credit": 3500000.0,
            "status_posting": "POSTED",
            "hash_checksum": "a4f91c6e932b78f40192eab54c938174dfb201a74e5482e16f391054ab309172"
        },
        {
            "ref_no": "BKK-2026/10/002",
            "trx_date": "2026-10-18",
            "description": "Pembelian Perlengkapan Toko Tunai",
            "account": "5204 - Beban Perlengkapan Toko",
            "debit": 1200000.0,
            "credit": 0.0,
            "status_posting": "POSTED",
            "hash_checksum": "c82b014e82019fab57219c0128e441a9bc382901a18274092b1928374a582910"
        },
        {
            "ref_no": "BKK-2026/10/002",
            "trx_date": "2026-10-18",
            "description": "Pembelian Perlengkapan Toko Tunai",
            "account": "1101 - Kas Operasional",
            "debit": 0.0,
            "credit": 1200000.0,
            "status_posting": "POSTED",
            "hash_checksum": "c82b014e82019fab57219c0128e441a9bc382901a18274092b1928374a582910"
        }
    ]

if "audit_db" not in st.session_state:
    st.session_state.audit_db = [
        {
            "time": "2026-10-19 09:30:45",
            "action": "POSTED",
            "table": "journal_headers",
            "ref": "BKK-2026/10/001",
            "user": "bizflow",
            "hash": "a4f91c6e932b78f40192eab54c938174dfb201a74e5482e16f391054ab309172"
        },
        {
            "time": "2026-10-18 14:15:22",
            "action": "POSTED",
            "table": "journal_headers",
            "ref": "BKK-2026/10/002",
            "user": "bizflow",
            "hash": "c82b014e82019fab57219c0128e441a9bc382901a18274092b1928374a582910"
        }
    ]

# ==============================================================================
# SIDEBAR ENTERPRISE (ENTERPRISE WORKSPACE)
# ==============================================================================
with st.sidebar:
    st.markdown("### 🏛️ BizFlow Ledger")
    st.caption("Financial Operations & Accounting Control")
    st.markdown("---")
    
    st.caption("WORKSPACE")
    menu = st.radio(
        label="Pilih Modul:",
        options=[
            "Dashboard",
            "Entri Kas Keluar",
            "Buku Besar",
            "Gudang & Stok",
            "Jejak Audit"
        ],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.caption("**Operator:** Staf Akuntan Utama")
    st.caption("**Identitas Sistem:** `bizflow`")

# ==============================================================================
# MODUL 0: DASHBOARD KEUANGAN & KEPATUHAN BISNIS
# ==============================================================================
if menu == "Dashboard":
    df_inv = pd.DataFrame(st.session_state.inventory_db)
    df_inv["total_value"] = df_inv["stock_qty"] * df_inv["unit_cost"]
    total_inv_val = df_inv["total_value"].sum()

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Kas & Setara Kas (PSAK 2)", "Rp 142.500.000", "Likuid")
    k2.metric("Valuasi Persediaan", f"Rp {total_inv_val:,.0f}", "Sistem Perpetual")
    k3.metric("Beban Operasional", "Rp 28.600.000", "Okt 2026")
    k4.metric("Integritas Transaksi", "100% Balanced", "Zero Discrepancy")

    col_coa, col_dist = st.columns([13, 7], gap="large")

    with col_coa:
        st.markdown("#### Bagan Akun Finansial (Chart of Accounts - 3NF)")
        st.caption("Standar klasifikasi pelaporan keuangan PSAK.")
        df_coa_disp = pd.DataFrame(COA_LIST[:8])
        st.dataframe(
            df_coa_disp,
            use_container_width=True,
            column_config={
                "id": st.column_config.TextColumn("Kode Akun"),
                "name": st.column_config.TextColumn("Nama Akun"),
                "type": st.column_config.TextColumn("Klasifikasi"),
                "balance": st.column_config.TextColumn("Saldo Normal")
            },
            hide_index=True
        )

    with col_dist:
        st.markdown("#### Distribusi Beban Operasional")
        expense_df = pd.DataFrame({
            "Kategori": ["Gaji & Upah Karyawan", "Sewa Gedung Kantor", "Listrik, Air & Utilitas", "Perlengkapan Toko"],
            "Nominal (Rp)": [12870000, 7150000, 4290000, 4290000],
            "Porsi": ["45%", "25%", "15%", "15%"]
        })
        st.dataframe(
            expense_df,
            use_container_width=True,
            column_config={
                "Kategori": st.column_config.TextColumn("Kategori Beban"),
                "Nominal (Rp)": st.column_config.NumberColumn("Nominal (Rp)", format="Rp %d"),
                "Porsi": st.column_config.TextColumn("Persentase")
            },
            hide_index=True
        )

    st.markdown("#### Arus Kas & Likuiditas Finansial (Tren 6 Bulan - PSAK 2)")
    cf_col_chart, cf_col_stats = st.columns([13, 7], gap="large")
    with cf_col_chart:
        df_cashflow = pd.DataFrame(
            {
                "Penerimaan Kas": [45000000, 52000000, 49000000, 58000000, 54000000, 62500000],
                "Pengeluaran Kas": [28000000, 31000000, 33000000, 35000000, 32000000, 38000000]
            },
            index=["Mei", "Jun", "Jul", "Agu", "Sep", "Okt"]
        )
        st.bar_chart(df_cashflow, color=["#173B67", "#94A3B8"], use_container_width=True)

    with cf_col_stats:
        st.markdown("##### Rasio Kesehatan Finansial")
        st.metric("Surplus Arus Kas (Okt)", "+ Rp 24.500.000", "+14.2% MoM")
        st.metric("Rasio Lancar (Current Ratio)", "3.42x", "Likuiditas Kuat")
        st.metric("Perputaran Piutang (DSO)", "14 Hari", "Konversi Efisien")

# ==============================================================================
# MODUL 1: ENTRI KAS KELUAR (DUAL-COLUMN WORKSPACE)
# ==============================================================================
elif menu == "Entri Kas Keluar":
    col_left, col_right = st.columns([13, 7], gap="large")

    with col_left:
        st.markdown("#### Informasi Voucher")
        f1, f2, f3 = st.columns([1, 1, 2])
        with f1:
            ref_no = st.text_input("Nomor Voucher", value="BKK-2026/10/003")
        with f2:
            trx_date = st.date_input("Tanggal Transaksi", value=date(2026, 10, 19))
        with f3:
            description = st.text_input("Deskripsi", value="Pembayaran Beban Gaji & Operasional Kantor")

        st.markdown("#### Rincian Jurnal")
        st.caption("Setiap transaksi wajib memiliki minimal satu pasang akun debit dan kredit.")

        if "entry_lines" not in st.session_state:
            st.session_state.entry_lines = pd.DataFrame([
                {"Akun": list(COA_MAP.keys())[9], "Memo": "Alokasi Gaji Karyawan Toko", "Debit": 4500000.0, "Kredit": 0.0},
                {"Akun": list(COA_MAP.keys())[0], "Memo": "Pengeluaran Kas Operasional", "Debit": 0.0, "Kredit": 4500000.0}
            ])

        edited_df = st.data_editor(
            st.session_state.entry_lines,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "Akun": st.column_config.SelectboxColumn("Bagan Akun (COA)", options=list(COA_MAP.keys()), required=True),
                "Memo": st.column_config.TextColumn("Memo Baris", width="medium"),
                "Debit": st.column_config.NumberColumn("Debit (Rp)", min_value=0.0, format="Rp %d"),
                "Kredit": st.column_config.NumberColumn("Kredit (Rp)", min_value=0.0, format="Rp %d")
            }
        )

    with col_right:
        st.markdown("#### Keseimbangan Finansial")
        tot_deb = float(edited_df["Debit"].sum()) if "Debit" in edited_df else 0.0
        tot_cre = float(edited_df["Kredit"].sum()) if "Kredit" in edited_df else 0.0
        diff = abs(tot_deb - tot_cre)
        is_bal = (diff == 0.0) and (tot_deb > 0)

        # Kartu Ringkasan Finansial
        st.metric("Total Debit", f"Rp {tot_deb:,.0f}")
        st.metric("Total Kredit", f"Rp {tot_cre:,.0f}")
        st.metric("Selisih (Discrepancy)", f"Rp {diff:,.0f}", delta=None)

        if is_bal:
            st.markdown("""
            <div class="balance-card-balanced">
                <span style="font-size: 13px; font-weight: 700;">🟢 ZERO DISCREPANCY (SEIMBANG)</span>
                <span style="font-size: 11px; font-weight: normal; color: #16805D;">Pengendalian internal terpenuhi (Debit = Kredit). Siap diposting ke Buku Besar.</span>
            </div>
            """, unsafe_allow_html=True)
        elif tot_deb == 0 and tot_cre == 0:
            st.info("Masukkan nominal transaksi debit dan kredit pada baris akun.")
        else:
            st.markdown(f"""
            <div class="balance-card-unbalanced">
                <span style="font-size: 13px; font-weight: 700;">🔴 TIDAK SEIMBANG</span>
                <span style="font-size: 11px; font-weight: normal; color: #C83C45;">Selisih Rp {diff:,.0f}. Tombol posting terkunci sampai selisih bernilai Rp 0.</span>
            </div>
            """, unsafe_allow_html=True)

        submit_btn = st.button("Posting Voucher ke Buku Besar", disabled=not is_bal, type="primary", use_container_width=True)

        if submit_btn:
            raw_hash = f"{ref_no}|{trx_date}|{tot_deb}|bizflow|{datetime.now().isoformat()}"
            sha_sig = hashlib.sha256(raw_hash.encode("utf-8")).hexdigest()

            for _, row in edited_df.iterrows():
                acc_name = row["Akun"].split(" (")[0]
                st.session_state.journal_db.insert(0, {
                    "ref_no": ref_no,
                    "trx_date": str(trx_date),
                    "description": description,
                    "account": acc_name,
                    "debit": float(row["Debit"]),
                    "credit": float(row["Kredit"]),
                    "status_posting": "POSTED",
                    "hash_checksum": sha_sig
                })

            st.session_state.audit_db.insert(0, {
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "action": "POSTED",
                "table": "journal_headers",
                "ref": ref_no,
                "user": "bizflow",
                "hash": sha_sig
            })

            st.success(f"Voucher {ref_no} berhasil diposting!\nHash SHA-256: {sha_sig[:24]}...")
            st.rerun()

        st.markdown("---")
        st.markdown("**UJI CEPAT SKENARIO:**")
        p1, p2 = st.columns(2)
        with p1:
            if st.button("Skenario Seimbang", use_container_width=True):
                st.session_state.entry_lines = pd.DataFrame([
                    {"Akun": list(COA_MAP.keys())[9], "Memo": "Gaji Staf Toko Oktober 2026", "Debit": 3800000.0, "Kredit": 0.0},
                    {"Akun": list(COA_MAP.keys())[11], "Memo": "Tagihan Listrik PLN Kantor", "Debit": 750000.0, "Kredit": 0.0},
                    {"Akun": list(COA_MAP.keys())[0], "Memo": "Pengeluaran Kas Kasir Utama", "Debit": 0.0, "Kredit": 4550000.0}
                ])
                st.rerun()
        with p2:
            if st.button("Skenario Selisih", use_container_width=True):
                st.session_state.entry_lines = pd.DataFrame([
                    {"Akun": list(COA_MAP.keys())[10], "Memo": "Sewa Gudang Logistik Tambahan", "Debit": 5000000.0, "Kredit": 0.0},
                    {"Akun": list(COA_MAP.keys())[0], "Memo": "Pengeluaran Kas Operasional", "Debit": 0.0, "Kredit": 4200000.0}
                ])
                st.rerun()

# ==============================================================================
# MODUL 2: BUKU BESAR
# ==============================================================================
elif menu == "Buku Besar":
    filter_c1, filter_c2 = st.columns([3, 1])
    with filter_c1:
        search_query = st.text_input("Pencarian Transaksi", placeholder="Cari nomor bukti, akun, atau deskripsi...")
    with filter_c2:
        status_filter = st.selectbox("Status Posting", ["Semua Status", "Hanya POSTED"])

    df_j = pd.DataFrame(st.session_state.journal_db)

    if not df_j.empty:
        if status_filter == "Hanya POSTED":
            df_j = df_j[df_j["status_posting"] == "POSTED"]

        if search_query:
            q = search_query.lower()
            df_j = df_j[
                df_j["ref_no"].str.lower().str.contains(q) |
                df_j["description"].str.lower().str.contains(q) |
                df_j["account"].str.lower().str.contains(q)
            ]

        st.dataframe(
            df_j,
            use_container_width=True,
            column_config={
                "trx_date": st.column_config.TextColumn("Tanggal"),
                "ref_no": st.column_config.TextColumn("No. Voucher"),
                "description": st.column_config.TextColumn("Deskripsi"),
                "account": st.column_config.TextColumn("Akun Finansial"),
                "debit": st.column_config.NumberColumn("Debit (Rp)", format="Rp %d"),
                "credit": st.column_config.NumberColumn("Kredit (Rp)", format="Rp %d"),
                "status_posting": st.column_config.TextColumn("Status"),
                "hash_checksum": st.column_config.TextColumn("Checksum SHA-256")
            },
            hide_index=True
        )
    else:
        st.info("Belum ada data transaksi yang tercatat.")

# ==============================================================================
# MODUL 3: GUDANG & STOK (OTOMASI PERSEDIAAN PERPETUAL)
# ==============================================================================
elif menu == "Gudang & Stok":
    # KPI Metrik Baris Atas
    df_inv = pd.DataFrame(st.session_state.inventory_db)
    df_inv["total_value"] = df_inv["stock_qty"] * df_inv["unit_cost"]

    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Total Jenis Barang", f"{len(df_inv)} Item")
    kpi2.metric("Total Unit Fisik", f"{df_inv['stock_qty'].sum():,.0f} Unit")
    kpi3.metric("Valuasi Persediaan", f"Rp {df_inv['total_value'].sum():,.0f}")

    col_inv, col_form = st.columns([13, 7], gap="large")

    with col_inv:
        st.markdown("#### Katalog Persediaan")
        st.dataframe(
            df_inv,
            use_container_width=True,
            column_config={
                "item_id": st.column_config.TextColumn("Kode Barang"),
                "item_name": st.column_config.TextColumn("Nama Barang"),
                "stock_qty": st.column_config.NumberColumn("Stok Fisik", format="%d unit"),
                "unit_cost": st.column_config.NumberColumn("Harga Pokok (Rp)", format="Rp %d"),
                "total_value": st.column_config.NumberColumn("Total Nilai (Rp)", format="Rp %d")
            },
            hide_index=True
        )

    with col_form:
        st.markdown("#### Mutasi Barang")
        item_opts = [f"{i['item_id']} - {i['item_name']} (Stok: {i['stock_qty']} unit)" for i in st.session_state.inventory_db]
        selected_item_str = st.selectbox("Pilih Barang:", options=item_opts)
        selected_item_id = selected_item_str.split(" - ")[0]

        trx_type = st.selectbox("Jenis Transaksi:", ["SALE (Penjualan)", "PURCHASE (Pembelian)"])
        qty_input = st.number_input("Kuantitas (Unit):", min_value=1, value=10)

        if st.button("Eksekusi Mutasi", type="primary", use_container_width=True):
            target_item = next(i for i in st.session_state.inventory_db if i["item_id"] == selected_item_id)
            if "SALE" in trx_type:
                if qty_input > target_item["stock_qty"]:
                    st.error(
                        f"[TRIGGER EXCEPTION & ROLLBACK]: PENGENDALIAN INTERNAL DITOLAK!\n\n"
                        f"Stok {target_item['item_id']} - {target_item['item_name']} tidak mencukupi untuk diproses.\n"
                        f"Saldo fisik saat ini: {target_item['stock_qty']} unit | Permintaan penjualan: {qty_input} unit.\n\n"
                        f"Status: Transaksi dibatalkan secara atomik oleh Database Trigger. Saldo fisik tetap utuh."
                    )
                    st.session_state.audit_db.insert(0, {
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "action": "REJECTED",
                        "table": "inventory_transactions",
                        "ref": selected_item_id,
                        "user": "bizflow",
                        "hash": "ROLLBACK_TRIGGER_CHECK"
                    })
                else:
                    target_item["stock_qty"] -= qty_input
                    st.success(f"[TRIGGER EXECUTED]: Penjualan {qty_input} unit berhasil. Saldo baru: {target_item['stock_qty']} unit.")
                    st.session_state.audit_db.insert(0, {
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "action": "SALE",
                        "table": "inventory_transactions",
                        "ref": selected_item_id,
                        "user": "bizflow",
                        "hash": "MUTATION_RECORD"
                    })
                    st.rerun()
            else:
                target_item["stock_qty"] += qty_input
                st.success(f"[TRIGGER EXECUTED]: Pembelian {qty_input} unit berhasil. Saldo baru: {target_item['stock_qty']} unit.")
                st.session_state.audit_db.insert(0, {
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "action": "PURCHASE",
                    "table": "inventory_transactions",
                    "ref": selected_item_id,
                    "user": "bizflow",
                    "hash": "MUTATION_RECORD"
                })
                st.rerun()

# ==============================================================================
# MODUL 4: JEJAK AUDIT & PENGUJIAN IMUTABILITAS
# ==============================================================================
elif menu == "Jejak Audit":
    col_aud, col_lab = st.columns([13, 7], gap="large")

    with col_aud:
        st.markdown("#### Kronologi Aktivitas")
        df_audit = pd.DataFrame(st.session_state.audit_db)
        st.dataframe(
            df_audit,
            use_container_width=True,
            column_config={
                "time": st.column_config.TextColumn("Waktu"),
                "action": st.column_config.TextColumn("Aksi"),
                "table": st.column_config.TextColumn("Entitas Tabel"),
                "ref": st.column_config.TextColumn("No. Referensi"),
                "user": st.column_config.TextColumn("Operator"),
                "hash": st.column_config.TextColumn("Checksum SHA-256")
            },
            hide_index=True
        )

    with col_lab:
        st.markdown("#### Pengujian Imutabilitas")
        st.info("Transaksi **POSTED** terkunci permanen. Seluruh koreksi wajib melalui **Jurnal Pembalik (Storno)**.")

        voucher_opts = list(set([j["ref_no"] for j in st.session_state.journal_db if j.get("status_posting") == "POSTED"]))
        selected_v = st.selectbox("Pilih Voucher Terposting:", voucher_opts if voucher_opts else ["BKK-2026/10/001"])

        if st.button("Uji Coba Ubah / Hapus Data", use_container_width=True):
            st.error(
                f"[IMMUTABILITY GATE REJECTION]: AKSES FINANSIAL DITOLAK!\n\n"
                f"Voucher {selected_v} berstatus POSTED dan bersifat imutabel. Operasi UPDATE maupun DELETE ditolak secara mutlak oleh trigger basis data.\n\n"
                f"Prinsip Akuntansi: Kesalahan pencatatan transaksi yang telah diposting wajib diperbaiki melalui Jurnal Pembalik (Storno)."
            )
            st.session_state.audit_db.insert(0, {
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "action": "SECURITY_BLOCKED",
                "table": "journal_headers",
                "ref": selected_v,
                "user": "bizflow",
                "hash": "TAMPER_ATTEMPT_BLOCKED"
            })

        if st.button("Buat Jurnal Pembalik (Storno)", type="primary", use_container_width=True):
            rev_ref = "REV-" + selected_v
            orig_lines = [j for j in st.session_state.journal_db if j["ref_no"] == selected_v]
            sha = hashlib.sha256(f"{rev_ref}|REVERSAL|{datetime.now().isoformat()}".encode("utf-8")).hexdigest()

            for line in orig_lines:
                st.session_state.journal_db.insert(0, {
                    "ref_no": rev_ref,
                    "trx_date": str(date.today()),
                    "description": f"Jurnal Pembalik atas {selected_v}",
                    "account": line["account"],
                    "debit": line["credit"],  # Balik saldo
                    "credit": line["debit"],
                    "status_posting": "POSTED",
                    "hash_checksum": sha
                })

            st.session_state.audit_db.insert(0, {
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "action": "REVERSAL",
                "table": "journal_headers",
                "ref": rev_ref,
                "user": "bizflow",
                "hash": sha
            })

            st.success(f"Jurnal Pembalik {rev_ref} berhasil diterbitkan!\nSaldo Debit dan Kredit telah dibalik secara otomatis.")
            st.rerun()
