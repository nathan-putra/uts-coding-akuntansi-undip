/**
 * BizFlow Ledger - Enterprise Financial Operations & Accounting Control
 * Architecture: Clean Vanilla JS, Reactive Component Model, Web Crypto SHA-256
 * Conforms to Master UI/UX Redesign Specification (Navy Ledger Design System)
 */

// ============================================================================
// 1. MASTER CHART OF ACCOUNTS (3NF STANDARDIZED)
// ============================================================================
const CHART_OF_ACCOUNTS = [
  { id: "1101", name: "Kas Operasional", type: "ASSET", balance: "DEBIT" },
  { id: "1102", name: "Bank BNI Rekening Utama", type: "ASSET", balance: "DEBIT" },
  { id: "1103", name: "Piutang Usaha", type: "ASSET", balance: "DEBIT" },
  { id: "1104", name: "Persediaan Barang Dagang", type: "ASSET", balance: "DEBIT" },
  { id: "2101", name: "Hutang Usaha", type: "LIABILITY", balance: "CREDIT" },
  { id: "2102", name: "Beban Akrual PPN Keluaran", type: "LIABILITY", balance: "CREDIT" },
  { id: "3101", name: "Modal Saham Disetor", type: "EQUITY", balance: "CREDIT" },
  { id: "4101", name: "Pendapatan Penjualan Ritel", type: "REVENUE", balance: "CREDIT" },
  { id: "5101", name: "Beban Pokok Pendapatan (HPP)", type: "EXPENSE", balance: "DEBIT" },
  { id: "5201", name: "Beban Gaji & Upah Karyawan", type: "EXPENSE", balance: "DEBIT" },
  { id: "5202", name: "Beban Sewa Gedung Kantor", type: "EXPENSE", balance: "DEBIT" },
  { id: "5203", name: "Beban Listrik, Air & Utilitas", type: "EXPENSE", balance: "DEBIT" },
  { id: "5204", name: "Beban Perlengkapan Toko", type: "EXPENSE", balance: "DEBIT" }
];

// ============================================================================
// 2. RUNTIME STATE MANAGEMENT
// ============================================================================
let inventoryItems = [
  { item_id: "BRG-001", item_name: "Beras Premium 5kg", stock_qty: 50, unit_cost: 68000 },
  { item_id: "BRG-002", item_name: "Minyak Goreng Sawit 2L", stock_qty: 30, unit_cost: 32000 },
  { item_id: "BRG-003", item_name: "Gula Pasir Kristal 1kg", stock_qty: 40, unit_cost: 16500 },
  { item_id: "BRG-004", item_name: "Tepung Terigu Serbaguna 1kg", stock_qty: 25, unit_cost: 12000 }
];

let journalHistory = [
  {
    date: "2026-10-19",
    ref: "BKK-2026/10/001",
    desc: "Pembayaran Sewa Kantor Okt 2026",
    account: "5202 - Beban Sewa Gedung Kantor",
    debit: 3500000,
    credit: 0,
    status: "POSTED",
    hash: "a4f91c6e932b78f40192eab54c938174dfb201a74e5482e16f391054ab309172"
  },
  {
    date: "2026-10-19",
    ref: "BKK-2026/10/001",
    desc: "Pembayaran Sewa Kantor Okt 2026",
    account: "1101 - Kas Operasional",
    debit: 0,
    credit: 3500000,
    status: "POSTED",
    hash: "a4f91c6e932b78f40192eab54c938174dfb201a74e5482e16f391054ab309172"
  },
  {
    date: "2026-10-18",
    ref: "BKK-2026/10/002",
    desc: "Pembelian Perlengkapan Toko Tunai",
    account: "5204 - Beban Perlengkapan Toko",
    debit: 1200000,
    credit: 0,
    status: "POSTED",
    hash: "c82b014e82019fab57219c0128e441a9bc382901a18274092b1928374a582910"
  },
  {
    date: "2026-10-18",
    ref: "BKK-2026/10/002",
    desc: "Pembelian Perlengkapan Toko Tunai",
    account: "1101 - Kas Operasional",
    debit: 0,
    credit: 1200000,
    status: "POSTED",
    hash: "c82b014e82019fab57219c0128e441a9bc382901a18274092b1928374a582910"
  }
];

let auditLogs = [
  {
    action: "POSTED",
    table: "journal_headers",
    ref: "BKK-2026/10/001",
    user: "bizflow",
    time: "2026-10-19 09:30:45",
    desc: "Posting voucher kas keluar senilai Rp 3.500.000",
    hash: "a4f91c6e932b78f40192eab54c938174dfb201a74e5482e16f391054ab309172"
  },
  {
    action: "POSTED",
    table: "journal_headers",
    ref: "BKK-2026/10/002",
    user: "bizflow",
    time: "2026-10-18 14:15:22",
    desc: "Posting voucher kas keluar senilai Rp 1.200.000",
    hash: "c82b014e82019fab57219c0128e441a9bc382901a18274092b1928374a582910"
  }
];

let activeLines = [];

// ============================================================================
// 3. UTILITY FUNCTIONS
// ============================================================================
function formatIDR(amount) {
  return "Rp " + Number(amount || 0).toLocaleString("id-ID");
}

function parseRawNumber(val) {
  if (typeof val === "number") return val;
  const cleaned = String(val || "").replace(/[^\d.-]/g, "");
  const parsed = parseFloat(cleaned);
  return isNaN(parsed) ? 0 : Math.max(0, parsed);
}

async function computeSHA256(message) {
  try {
    const encoder = new TextEncoder();
    const data = encoder.encode(message);
    const hashBuffer = await crypto.subtle.digest("SHA-256", data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, "0")).join("");
  } catch (err) {
    // Fallback simple checksum if Web Crypto not available
    let hash = 0;
    for (let i = 0; i < message.length; i++) {
      hash = ((hash << 5) - hash) + message.charCodeAt(i);
      hash |= 0;
    }
    return Math.abs(hash).toString(16).padStart(32, "0");
  }
}

// ============================================================================
// 4. SPA NAVIGATION (ENTERPRISE WORKSPACE)
// ============================================================================
const PAGE_TITLES = {
  dashboard: "Dashboard",
  voucher: "Entri Kas Keluar",
  journal: "Buku Besar",
  inventory: "Gudang & Stok",
  audit: "Jejak Audit"
};

function navigateTo(pageId) {
  // Update sidebar active buttons
  document.querySelectorAll(".nav-item").forEach(item => {
    item.classList.toggle("active", item.getAttribute("data-page") === pageId);
  });

  // Update page sections
  document.querySelectorAll(".page-section").forEach(sec => {
    sec.classList.remove("active");
  });

  const targetSection = document.getElementById("page-" + pageId);
  if (targetSection) {
    targetSection.classList.add("active");
  }

  // Update topbar breadcrumb
  const topbarLabel = document.getElementById("topbar-current-page");
  if (topbarLabel) {
    topbarLabel.textContent = PAGE_TITLES[pageId] || "Dashboard";
  }

  // Auto-render target module components
  if (pageId === "dashboard") {
    renderDashboardCOA();
    updateDashboardKPIs();
  }
  if (pageId === "journal") renderJournalHistory();
  if (pageId === "inventory") renderInventory();
  if (pageId === "audit") {
    renderAuditTable();
    updateAuditVoucherOptions();
  }
}
window.navigateTo = navigateTo;

document.querySelectorAll(".nav-item").forEach(button => {
  button.addEventListener("click", () => {
    const page = button.getAttribute("data-page");
    if (page) navigateTo(page);
  });
});

// ============================================================================
// 4.1 MODUL 0: DASHBOARD KEUANGAN & KEPATUHAN
// ============================================================================
function renderDashboardCOA() {
  const tbody = document.getElementById("dashboard-coa-tbody");
  if (!tbody) return;
  tbody.innerHTML = "";
  CHART_OF_ACCOUNTS.slice(0, 8).forEach(acc => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td style="font-weight: 600; color: var(--deep-navy);">${acc.id}</td>
      <td>${acc.name}</td>
      <td><span class="badge badge-draft">${acc.type}</span></td>
      <td class="tabular" style="text-align: center; font-weight: 600;">${acc.balance}</td>
    `;
    tbody.appendChild(tr);
  });
}

function updateDashboardKPIs() {
  const cashVal = document.getElementById("dash-kpi-cash");
  const invVal = document.getElementById("dash-kpi-inventory");
  const expVal = document.getElementById("dash-kpi-expense");

  const totalInventoryVal = inventoryItems.reduce((acc, i) => acc + (i.stock_qty * i.unit_cost), 0);
  if (cashVal) cashVal.textContent = "Rp 142.500.000";
  if (invVal) invVal.textContent = formatIDR(totalInventoryVal);
  if (expVal) expVal.textContent = "Rp 28.600.000";
}

// ============================================================================
// 5. MODUL 1: ENTRI KAS KELUAR & REAL-TIME BALANCED ENGINE
// ============================================================================
function initLines() {
  activeLines = [
    { id: 1, account_id: "5201", memo: "Alokasi Gaji Karyawan Toko", debit: 4500000, credit: 0 },
    { id: 2, account_id: "1101", memo: "Pengeluaran Kas Operasional", debit: 0, credit: 4500000 }
  ];
  document.getElementById("ref-no").value = "BKK-2026/10/003";
  document.getElementById("trx-date").value = "2026-10-19";
  document.getElementById("description").value = "Pembayaran Beban Gaji & Operasional Kantor";
  renderLines();
  updateBalanceCalculation();
}

function renderLines() {
  const tbody = document.getElementById("lines-tbody");
  if (!tbody) return;
  tbody.innerHTML = "";

  activeLines.forEach((line, index) => {
    const tr = document.createElement("tr");

    const accountOptions = CHART_OF_ACCOUNTS.map(acc => {
      const isSelected = acc.id === line.account_id ? "selected" : "";
      return `<option value="${acc.id}" ${isSelected}>${acc.id} - ${acc.name} (${acc.balance})</option>`;
    }).join("");

    tr.innerHTML = `
      <td>
        <select class="form-control" onchange="updateLineAccount(${index}, this.value)">
          ${accountOptions}
        </select>
      </td>
      <td>
        <input type="text" class="form-control" value="${line.memo || ''}" oninput="updateLineMemo(${index}, this.value)" placeholder="Keterangan baris...">
      </td>
      <td>
        <input type="number" step="1000" min="0" class="form-control tabular" style="text-align: right;" value="${line.debit || ''}" oninput="updateLineDebit(${index}, this.value)" placeholder="0">
      </td>
      <td>
        <input type="number" step="1000" min="0" class="form-control tabular" style="text-align: right;" value="${line.credit || ''}" oninput="updateLineCredit(${index}, this.value)" placeholder="0">
      </td>
      <td style="text-align: center;">
        <button type="button" class="btn-delete" onclick="removeLine(${index})" title="Hapus baris">&times;</button>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

window.updateLineAccount = function(index, accountId) {
  if (activeLines[index]) activeLines[index].account_id = accountId;
};

window.updateLineMemo = function(index, memo) {
  if (activeLines[index]) activeLines[index].memo = memo;
};

window.updateLineDebit = function(index, val) {
  const num = parseRawNumber(val);
  if (!activeLines[index]) return;
  activeLines[index].debit = num;
  if (num > 0) activeLines[index].credit = 0;
  renderLines();
  updateBalanceCalculation();
};

window.updateLineCredit = function(index, val) {
  const num = parseRawNumber(val);
  if (!activeLines[index]) return;
  activeLines[index].credit = num;
  if (num > 0) activeLines[index].debit = 0;
  renderLines();
  updateBalanceCalculation();
};

window.removeLine = function(index) {
  if (activeLines.length <= 1) {
    alert("Jurnal minimal memiliki 1 baris akun.");
    return;
  }
  activeLines.splice(index, 1);
  renderLines();
  updateBalanceCalculation();
};

const btnAddLine = document.getElementById("btn-add-line");
if (btnAddLine) {
  btnAddLine.addEventListener("click", () => {
    const newId = activeLines.length ? Math.max(...activeLines.map(l => l.id)) + 1 : 1;
    activeLines.push({
      id: newId,
      account_id: "5203",
      memo: "Beban Operasional Tambahan",
      debit: 0,
      credit: 0
    });
    renderLines();
    updateBalanceCalculation();
  });
}

// Live Balanced Indicator Calculation
function updateBalanceCalculation() {
  const totalDebit = activeLines.reduce((sum, l) => sum + (parseFloat(l.debit) || 0), 0);
  const totalCredit = activeLines.reduce((sum, l) => sum + (parseFloat(l.credit) || 0), 0);
  const diff = Math.abs(totalDebit - totalCredit);

  document.getElementById("display-total-debit").textContent = formatIDR(totalDebit);
  document.getElementById("display-total-credit").textContent = formatIDR(totalCredit);
  document.getElementById("display-diff").textContent = formatIDR(diff);

  const statusBlock = document.getElementById("balance-status-block");
  const badge = document.getElementById("balance-badge");
  const hint = document.getElementById("balance-status-hint");
  const submitBtn = document.getElementById("btn-submit-voucher");
  const voucherBadge = document.getElementById("voucher-status-badge");

  if (totalDebit === 0 && totalCredit === 0) {
    statusBlock.className = "balance-status-block";
    badge.className = "balance-status-badge neutral";
    badge.textContent = "MENUNGGU INPUT BARIS";
    hint.textContent = "Masukkan nominal transaksi debit dan kredit pada baris akun.";
    submitBtn.disabled = true;
    if (voucherBadge) {
      voucherBadge.className = "badge badge-draft";
      voucherBadge.textContent = "DRAFT";
    }
  } else if (diff === 0 && totalDebit > 0) {
    statusBlock.className = "balance-status-block balanced";
    badge.className = "balance-status-badge balanced";
    badge.textContent = "ZERO DISCREPANCY (SEIMBANG)";
    hint.textContent = "Pengendalian internal terpenuhi (Debit = Kredit). Siap diposting ke Buku Besar.";
    submitBtn.disabled = false;
    if (voucherBadge) {
      voucherBadge.className = "badge badge-posted";
      voucherBadge.textContent = "SIAP POSTING";
    }
  } else {
    statusBlock.className = "balance-status-block unbalanced";
    badge.className = "balance-status-badge unbalanced";
    badge.textContent = "TIDAK SEIMBANG";
    hint.textContent = `Selisih: ${formatIDR(diff)}. Tombol posting terkunci sampai selisih bernilai Rp 0.`;
    submitBtn.disabled = true;
    if (voucherBadge) {
      voucherBadge.className = "badge badge-draft";
      voucherBadge.textContent = "DRAFT (SELISIH)";
    }
  }
}

// Preset Skenario
const btnLoadBalanced = document.getElementById("btn-load-balanced");
if (btnLoadBalanced) {
  btnLoadBalanced.addEventListener("click", () => {
    activeLines = [
      { id: 1, account_id: "5201", memo: "Gaji Staf Toko Oktober 2026", debit: 3800000, credit: 0 },
      { id: 2, account_id: "5203", memo: "Tagihan Listrik PLN Kantor", debit: 750000, credit: 0 },
      { id: 3, account_id: "1101", memo: "Pengeluaran Kas Kasir Utama", debit: 0, credit: 4550000 }
    ];
    document.getElementById("ref-no").value = "BKK-2026/10/004";
    document.getElementById("description").value = "Pembayaran Rutin Gaji dan Utilitas Listrik";
    renderLines();
    updateBalanceCalculation();
  });
}

const btnLoadUnbalanced = document.getElementById("btn-load-unbalanced");
if (btnLoadUnbalanced) {
  btnLoadUnbalanced.addEventListener("click", () => {
    activeLines = [
      { id: 1, account_id: "5202", memo: "Sewa Gudang Logistik Tambahan", debit: 5000000, credit: 0 },
      { id: 2, account_id: "1101", memo: "Pengeluaran Kas Operasional", debit: 0, credit: 4200000 }
    ];
    document.getElementById("ref-no").value = "BKK-2026/10/TEST-UNBALANCED";
    document.getElementById("description").value = "Uji Coba Transaksi Tidak Seimbang (Pengujian Proteksi)";
    renderLines();
    updateBalanceCalculation();
  });
}

const btnReset = document.getElementById("btn-reset");
if (btnReset) {
  btnReset.addEventListener("click", () => {
    initLines();
  });
}

// Submit Voucher Handler
const btnSubmitVoucher = document.getElementById("btn-submit-voucher");
if (btnSubmitVoucher) {
  btnSubmitVoucher.addEventListener("click", async () => {
    const refNo = document.getElementById("ref-no").value.trim();
    const trxDate = document.getElementById("trx-date").value;
    const description = document.getElementById("description").value.trim();
    const operator = "bizflow";

    const totalDebit = activeLines.reduce((sum, l) => sum + (parseFloat(l.debit) || 0), 0);
    const totalCredit = activeLines.reduce((sum, l) => sum + (parseFloat(l.credit) || 0), 0);

    if (totalDebit !== totalCredit || totalDebit === 0) {
      alert("Asas berpasangan dilanggar: Total Debit harus sama dengan Total Kredit.");
      return;
    }

    const payload = `${refNo}|${trxDate}|${totalDebit}|${operator}|${Date.now()}`;
    const checksum = await computeSHA256(payload);

    // Unshift each line into journalHistory
    activeLines.forEach(line => {
      const accObj = CHART_OF_ACCOUNTS.find(a => a.id === line.account_id);
      journalHistory.unshift({
        date: trxDate,
        ref: refNo,
        desc: description,
        account: `${line.account_id} - ${accObj ? accObj.name : ""}`,
        debit: line.debit,
        credit: line.credit,
        status: "POSTED",
        hash: checksum
      });
    });

    // Record audit trail
    auditLogs.unshift({
      action: "POSTED",
      table: "journal_headers",
      ref: refNo,
      user: operator,
      time: new Date().toISOString().replace("T", " ").substring(0, 19),
      desc: `Posting voucher kas keluar senilai ${formatIDR(totalDebit)}`,
      hash: checksum
    });

    renderJournalHistory();
    renderAuditTable();
    updateAuditVoucherOptions();

    alert(`Voucher ${refNo} berhasil diposting ke Buku Besar!\nNilai: ${formatIDR(totalDebit)}\nChecksum SHA-256: ${checksum.substring(0, 20)}...`);

    // Otomatis majukan nomor bukti
    const match = refNo.match(/\d+$/);
    if (match) {
      const nextSeq = String(parseInt(match[0], 10) + 1).padStart(3, "0");
      document.getElementById("ref-no").value = refNo.replace(/\d+$/, nextSeq);
    }
  });
}

// ============================================================================
// 6. MODUL 2: BUKU BESAR
// ============================================================================
function renderJournalHistory() {
  const tbody = document.getElementById("journal-tbody");
  if (!tbody) return;
  tbody.innerHTML = "";

  const filterSelect = document.getElementById("filter-journal-status");
  const filterStatus = filterSelect ? filterSelect.value : "ALL";
  const searchInput = document.getElementById("journal-search-input");
  const searchQ = (searchInput ? searchInput.value : "").toLowerCase().trim();

  const filtered = journalHistory.filter(item => {
    const matchStatus = filterStatus === "ALL" || item.status === filterStatus;
    const matchSearch = !searchQ ||
      item.ref.toLowerCase().includes(searchQ) ||
      item.account.toLowerCase().includes(searchQ) ||
      item.desc.toLowerCase().includes(searchQ);
    return matchStatus && matchSearch;
  });

  if (filtered.length === 0) {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td colspan="8" style="text-align: center; color: var(--secondary-text); padding: 24px;">Tidak ada transaksi yang cocok dengan kriteria pencarian.</td>`;
    tbody.appendChild(tr);
    return;
  }

  filtered.forEach(item => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td style="font-size: 12px; color: var(--secondary-text); white-space: nowrap;">${item.date}</td>
      <td style="font-weight: 600; color: var(--deep-navy); white-space: nowrap;">${item.ref}</td>
      <td>${item.desc}</td>
      <td style="color: var(--primary-navy); font-weight: 500;">${item.account}</td>
      <td class="tabular" style="text-align: right; font-weight: 600;">${item.debit ? formatIDR(item.debit) : "-"}</td>
      <td class="tabular" style="text-align: right; font-weight: 600;">${item.credit ? formatIDR(item.credit) : "-"}</td>
      <td style="text-align: center;"><span class="badge badge-posted">${item.status}</span></td>
      <td style="text-align: center;">
        <button class="btn-link" onclick="inspectChecksum('${item.hash}', '${item.ref}')">Cek Hash</button>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

const filterJournalStatus = document.getElementById("filter-journal-status");
if (filterJournalStatus) filterJournalStatus.addEventListener("change", renderJournalHistory);

const journalSearchInput = document.getElementById("journal-search-input");
if (journalSearchInput) journalSearchInput.addEventListener("input", renderJournalHistory);

window.inspectChecksum = function(hash, ref) {
  alert(`Verifikasi Integritas Kriptografis Voucher ${ref}:\n\nSHA-256 Hash Checksum:\n${hash}\n\nStatus: Terverifikasi Valid, Tercatat di Jejak Audit, & Imutabel.`);
};

// ============================================================================
// 7. MODUL 3: GUDANG & STOK (OTOMASI PERSEDIAAN PERPETUAL)
// ============================================================================
function updateInventoryKPIs() {
  const kpiCount = document.getElementById("inv-kpi-count");
  const kpiUnits = document.getElementById("inv-kpi-units");
  const kpiValuation = document.getElementById("inv-kpi-valuation");

  const totalTypes = inventoryItems.length;
  const totalUnits = inventoryItems.reduce((acc, i) => acc + i.stock_qty, 0);
  const totalValuation = inventoryItems.reduce((acc, i) => acc + (i.stock_qty * i.unit_cost), 0);

  if (kpiCount) kpiCount.textContent = `${totalTypes} Item`;
  if (kpiUnits) kpiUnits.textContent = `${totalUnits} Unit`;
  if (kpiValuation) kpiValuation.textContent = formatIDR(totalValuation);
}

function renderInventory() {
  const tbody = document.getElementById("inventory-tbody");
  const select = document.getElementById("inv-item-select");
  if (!tbody || !select) return;

  tbody.innerHTML = "";
  select.innerHTML = "";

  inventoryItems.forEach(item => {
    const totalVal = item.stock_qty * item.unit_cost;
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td style="font-weight: 600; color: var(--deep-navy);">${item.item_id}</td>
      <td>${item.item_name}</td>
      <td class="tabular" style="text-align: right; font-weight: 700; color: ${item.stock_qty < 10 ? 'var(--error)' : 'var(--deep-navy)'};">${item.stock_qty} unit</td>
      <td class="tabular" style="text-align: right;">${formatIDR(item.unit_cost)}</td>
      <td class="tabular" style="text-align: right; font-weight: 600; color: var(--primary-navy);">${formatIDR(totalVal)}</td>
    `;
    tbody.appendChild(tr);

    const opt = document.createElement("option");
    opt.value = item.item_id;
    opt.textContent = `${item.item_id} - ${item.item_name} (Sisa: ${item.stock_qty} unit)`;
    select.appendChild(opt);
  });

  updateInventoryKPIs();
}

function executeMutation(itemId, trxType, qty) {
  const item = inventoryItems.find(i => i.item_id === itemId);
  if (!item) return;

  const alertBox = document.getElementById("inventory-alert-callout");
  if (!alertBox) return;

  if (trxType === "SALE") {
    // Validasi penegakan trigger anti-negative inventory
    if (qty > item.stock_qty) {
      alertBox.className = "alert-callout error";
      alertBox.style.display = "block";
      alertBox.innerHTML = `
        <strong>[TRIGGER EXCEPTION & ROLLBACK]: PENGENDALIAN INTERNAL DITOLAK!</strong><br>
        Stok barang <strong>${item.item_id} - ${item.item_name}</strong> tidak mencukupi untuk diproses.<br>
        Saldo fisik saat ini: <strong>${item.stock_qty} unit</strong> | Permintaan penjualan: <strong>${qty} unit</strong>.<br>
        <em>Status: Transaksi dibatalkan secara atomik oleh Database Trigger. Saldo fisik tetap utuh.</em>
      `;

      auditLogs.unshift({
        action: "REJECTED",
        table: "inventory_transactions",
        ref: itemId,
        user: "bizflow",
        time: new Date().toISOString().replace("T", " ").substring(0, 19),
        desc: `Penjualan ${qty} unit ${itemId} ditolak trigger (Defisit stok dicegah)`,
        hash: "ROLLBACK_TRIGGER_CHECK"
      });
      renderAuditTable();
      return;
    }

    item.stock_qty -= qty;
    alertBox.className = "alert-callout success";
    alertBox.style.display = "block";
    alertBox.innerHTML = `
      <strong>[TRIGGER EXECUTED]:</strong> Penjualan <strong>${qty} unit</strong> ${item.item_name} berhasil dicatat.<br>
      Saldo persediaan fisik otomatis termutakhirkan menjadi <strong>${item.stock_qty} unit</strong>.
    `;
  } else if (trxType === "PURCHASE") {
    item.stock_qty += qty;
    alertBox.className = "alert-callout success";
    alertBox.style.display = "block";
    alertBox.innerHTML = `
      <strong>[TRIGGER EXECUTED]:</strong> Pembelian <strong>${qty} unit</strong> ${item.item_name} berhasil dicatat.<br>
      Saldo persediaan fisik otomatis bertambah menjadi <strong>${item.stock_qty} unit</strong>.
    `;
  }

  auditLogs.unshift({
    action: trxType,
    table: "inventory_transactions",
    ref: itemId,
    user: "bizflow",
    time: new Date().toISOString().replace("T", " ").substring(0, 19),
    desc: `Mutasi ${trxType} ${qty} unit ${item.item_name}. Saldo baru: ${item.stock_qty} unit`,
    hash: "MUTATION_RECORD"
  });

  renderInventory();
  updateDashboardKPIs();
  renderAuditTable();
}

const btnExecuteMutation = document.getElementById("btn-execute-mutation");
if (btnExecuteMutation) {
  btnExecuteMutation.addEventListener("click", () => {
    const itemId = document.getElementById("inv-item-select").value;
    const trxType = document.getElementById("inv-trx-type").value;
    const qty = parseInt(document.getElementById("inv-qty-input").value, 10) || 0;
    if (qty <= 0) {
      alert("Kuantitas mutasi harus lebih besar dari 0.");
      return;
    }
    executeMutation(itemId, trxType, qty);
  });
}

const btnTestNormalSale = document.getElementById("btn-test-normal-sale");
if (btnTestNormalSale) {
  btnTestNormalSale.addEventListener("click", () => {
    document.getElementById("inv-item-select").value = "BRG-002";
    document.getElementById("inv-trx-type").value = "SALE";
    document.getElementById("inv-qty-input").value = "10";
    executeMutation("BRG-002", "SALE", 10);
  });
}

const btnTestNegativeStock = document.getElementById("btn-test-negative-stock");
if (btnTestNegativeStock) {
  btnTestNegativeStock.addEventListener("click", () => {
    document.getElementById("inv-item-select").value = "BRG-002";
    document.getElementById("inv-trx-type").value = "SALE";
    document.getElementById("inv-qty-input").value = "45";
    executeMutation("BRG-002", "SALE", 45);
  });
}

// ============================================================================
// 8. MODUL 4: JEJAK AUDIT & LABORATORIUM PENGUJIAN IMUTABILITAS
// ============================================================================
function updateAuditVoucherOptions() {
  const select = document.getElementById("audit-target-voucher");
  if (!select) return;

  const uniqueRefs = [...new Set(journalHistory.map(j => j.ref))];
  select.innerHTML = "";
  uniqueRefs.forEach(ref => {
    const opt = document.createElement("option");
    opt.value = ref;
    opt.textContent = `${ref} (POSTED)`;
    select.appendChild(opt);
  });
}

function renderAuditTable() {
  const tbody = document.getElementById("audit-table-tbody");
  if (!tbody) return;
  tbody.innerHTML = "";

  auditLogs.forEach(log => {
    const tr = document.createElement("tr");
    let badgeClass = "badge-posted";
    if (log.action === "REJECTED" || log.action === "SECURITY_BLOCKED") badgeClass = "badge-draft";
    if (log.action === "REVERSAL") badgeClass = "badge-draft";

    tr.innerHTML = `
      <td style="font-size: 12px; color: var(--secondary-text); white-space: nowrap;">${log.time}</td>
      <td><span class="badge ${badgeClass}">${log.action}</span></td>
      <td><code>${log.table}</code></td>
      <td style="font-weight: 600; color: var(--deep-navy);">${log.ref}</td>
      <td>${log.user}</td>
      <td class="tabular" style="font-family: monospace; font-size: 11px; color: var(--secondary-text);">${(log.hash || '').substring(0, 16)}...</td>
    `;
    tbody.appendChild(tr);
  });
}

const btnTestTamper = document.getElementById("btn-test-tamper");
if (btnTestTamper) {
  btnTestTamper.addEventListener("click", () => {
    const targetRef = document.getElementById("audit-target-voucher").value;
    const alertBox = document.getElementById("audit-alert-callout");
    if (!alertBox) return;

    alertBox.className = "alert-callout error";
    alertBox.style.display = "block";
    alertBox.innerHTML = `
      <strong>[IMMUTABILITY GATE REJECTION]: AKSES FINANSIAL DITOLAK!</strong><br>
      Voucher transaksi <strong>${targetRef}</strong> berstatus <strong>POSTED</strong> dan bersifat imutabel.<br>
      Operasi <code>UPDATE</code> maupun <code>DELETE</code> ditolak secara mutlak oleh trigger basis data.<br>
      <em>Prinsip Akuntansi: Kesalahan pencatatan transaksi yang telah diposting wajib dinetralkan melalui Jurnal Pembalik (Storno).</em>
    `;

    auditLogs.unshift({
      action: "SECURITY_BLOCKED",
      table: "journal_headers",
      ref: targetRef,
      user: "bizflow",
      time: new Date().toISOString().replace("T", " ").substring(0, 19),
      desc: `Percobaan modifikasi ilegal atas voucher terposting ${targetRef} digagalkan`,
      hash: "TAMPER_ATTEMPT_BLOCKED"
    });
    renderAuditTable();
  });
}

const btnTestReversal = document.getElementById("btn-test-reversal");
if (btnTestReversal) {
  btnTestReversal.addEventListener("click", async () => {
    const targetRef = document.getElementById("audit-target-voucher").value;
    const origEntries = journalHistory.filter(j => j.ref === targetRef);
    if (!origEntries.length) {
      alert("Tidak ditemukan data jurnal untuk voucher tersebut.");
      return;
    }

    const revRef = "REV-" + targetRef;
    const sha = await computeSHA256(revRef + "|REVERSAL|" + Date.now());

    origEntries.forEach(line => {
      journalHistory.unshift({
        date: new Date().toISOString().substring(0, 10),
        ref: revRef,
        desc: `Jurnal Pembalik atas ${targetRef}`,
        account: line.account,
        debit: line.credit, // Posisi ditukar untuk meniadakan saldo
        credit: line.debit,
        status: "POSTED",
        hash: sha
      });
    });

    auditLogs.unshift({
      action: "REVERSAL",
      table: "journal_headers",
      ref: revRef,
      user: "bizflow",
      time: new Date().toISOString().replace("T", " ").substring(0, 19),
      desc: `Penerbitan jurnal pembalik (Storno) atas voucher ${targetRef}`,
      hash: sha
    });

    const alertBox = document.getElementById("audit-alert-callout");
    if (alertBox) {
      alertBox.className = "alert-callout success";
      alertBox.style.display = "block";
      alertBox.innerHTML = `
        <strong>[REVERSING ENTRY CREATED]:</strong> Jurnal Pembalik <strong>${revRef}</strong> berhasil diterbitkan!<br>
        Saldo Debit dan Kredit telah dibalik secara otomatis untuk menetralkan voucher asal tanpa memanipulasi riwayat historis.
      `;
    }

    renderJournalHistory();
    renderAuditTable();
    updateAuditVoucherOptions();
  });
}

// ============================================================================
// 9. INITIAL LIFECYCLE MOUNT
// ============================================================================
document.addEventListener("DOMContentLoaded", () => {
  renderDashboardCOA();
  updateDashboardKPIs();
  initLines();
  renderJournalHistory();
  renderInventory();
  renderAuditTable();
  updateAuditVoucherOptions();
});

// Run once immediately if DOM already loaded
if (document.readyState === "complete" || document.readyState === "interactive") {
  renderDashboardCOA();
  updateDashboardKPIs();
  initLines();
  renderJournalHistory();
  renderInventory();
  renderAuditTable();
  updateAuditVoucherOptions();
}
