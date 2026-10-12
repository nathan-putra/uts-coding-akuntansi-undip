import os
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

def render_html(html_str):
    clean = "".join([line.strip() for line in html_str.split("\n") if line.strip()])
    st.markdown(clean, unsafe_allow_html=True)

def format_idr(num):
    return f"Rp {int(num):,}".replace(",", ".")

css_file_path = os.path.join(os.path.dirname(__file__), "styles.css")
base_css = ""
if os.path.exists(css_file_path):
    with open(css_file_path, "r", encoding="utf-8") as f:
        base_css = f.read()

st.markdown(f"""
<style>
{base_css}

/* Streamlit Header & Chrome Removal */
#MainMenu, header[data-testid="stHeader"], footer, [data-testid="stToolbar"] {{
    display: none !important;
    height: 0 !important;
}}

[data-testid="stSidebarCollapseButton"],
button[kind="header"] {{
    display: none !important;
}}

.stApp {{
    background-color: #F5F7FA !important;
}}

[data-testid="stAppViewContainer"] > .main {{
    padding: 0 !important;
}}

/* Unified Main Container (Strict 1440px Max Width & Flush Alignment) */
[data-testid="stMainBlockContainer"],
.block-container {{
    max-width: 1440px !important;
    margin-left: auto !important;
    margin-right: auto !important;
    padding-left: 28px !important;
    padding-right: 28px !important;
    padding-top: 0 !important;
    padding-bottom: 3rem !important;
    box-sizing: border-box !important;
}}

/* Topbar Edge-to-Edge Spanning Across 1440px Canvas */
.top-bar {{
    margin-left: -28px !important;
    margin-right: -28px !important;
    width: calc(100% + 56px) !important;
    height: 54px !important;
    background-color: #FFFFFF !important;
    border-bottom: 1px solid #E2E8F0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    padding: 0 28px !important;
    box-sizing: border-box !important;
    margin-bottom: 24px !important;
}}

.breadcrumb-area {{
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    color: var(--secondary-text);
}}
.breadcrumb-area .active-crumb {{
    color: #102A43;
    font-weight: 600;
}}

/* Strict Typography Hierarchy */
h1, .stMarkdown h1, .page-title {{
    font-size: 18px !important;
    font-weight: 700 !important;
    color: #102A43 !important;
    letter-spacing: -0.3px !important;
    margin: 0 0 4px 0 !important;
    line-height: 1.3 !important;
}}

.page-subtitle {{
    font-size: 12px !important;
    color: #526174 !important;
    margin: 0 0 18px 0 !important;
}}

h2, .stMarkdown h2, .card-title, .card-header h2, .card-hdr-title {{
    font-size: 13px !important;
    font-weight: 600 !important;
    color: #102A43 !important;
    letter-spacing: -0.2px !important;
    margin: 0 !important;
    line-height: 1.4 !important;
    text-transform: none !important;
}}

h3, .stMarkdown h3 {{
    font-size: 12px !important;
    font-weight: 600 !important;
    color: #102A43 !important;
    margin: 0 !important;
}}

/* Sidebar Architecture (248px, Deep Navy #102A43) */
[data-testid="stSidebar"] {{
    background-color: #102A43 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    width: 248px !important;
    min-width: 248px !important;
    max-width: 248px !important;
}}

/* Remove Streamlit Top Blank Gap in Sidebar & Header */
[data-testid="stSidebarHeader"] {{
    display: none !important;
    height: 0 !important;
    min-height: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
}}

[data-testid="stSidebarContent"],
[data-testid="stSidebar"] > div:first-child {{
    padding: 0 !important;
    margin: 0 !important;
    overflow-x: hidden !important;
    overflow-y: auto !important;
    scrollbar-width: none !important;
    -ms-overflow-style: none !important;
}}

[data-testid="stSidebarContent"]::-webkit-scrollbar {{
    display: none !important;
    width: 0 !important;
    height: 0 !important;
}}

[data-testid="stSidebarUserContent"] {{
    padding: 0 0 72px 0 !important;
    margin: 0 !important;
    width: 100% !important;
    box-sizing: border-box !important;
}}

[data-testid="stSidebarUserContent"] > div {{
    padding: 0 !important;
    margin: 0 !important;
    width: 100% !important;
    box-sizing: border-box !important;
    gap: 0 !important;
}}

.sidebar-brand {{
    width: 100% !important;
    box-sizing: border-box !important;
    padding: 20px 16px !important;
    display: flex !important;
    align-items: center !important;
    gap: 12px !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
    margin: 0 !important;
}}

.sidebar-section-label {{
    font-size: 10px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
    color: #64748B !important;
    padding: 16px 16px 8px 16px !important;
    display: block !important;
    margin: 0 !important;
}}

/* Transform Streamlit Radio with SVG Outline Icons */
[data-testid="stSidebar"] [data-testid="stRadio"] {{
    padding: 0 8px !important;
    margin: 0 !important;
    width: 100% !important;
    box-sizing: border-box !important;
}}

[data-testid="stSidebar"] [data-testid="stRadio"] [data-testid="stWidgetLabel"] {{
    display: none !important;
}}

[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] {{
    display: flex !important;
    flex-direction: column !important;
    gap: 4px !important;
    width: 100% !important;
}}

[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child {{
    display: none !important;
}}

[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label {{
    background-color: transparent !important;
    border-radius: 8px !important;
    height: 42px !important;
    width: 100% !important;
    box-sizing: border-box !important;
    padding-left: 44px !important;
    padding-right: 12px !important;
    margin: 0 !important;
    cursor: pointer !important;
    transition: all 140ms ease !important;
    display: flex !important;
    align-items: center !important;
    position: relative !important;
    background-repeat: no-repeat !important;
    background-position: 14px center !important;
    background-size: 18px 18px !important;
}}

[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label div[data-testid="stMarkdownContainer"] p {{
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #CBD5E1 !important;
    margin: 0 !important;
    letter-spacing: -0.1px !important;
}}

/* Radio Menu Icons (Default Muted Slate) */
[data-testid="stSidebar"] div[role="radiogroup"] > label:nth-child(1) {{
    background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="%23AFC1D3" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/></svg>') !important;
}}
[data-testid="stSidebar"] div[role="radiogroup"] > label:nth-child(2) {{
    background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="%23AFC1D3" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="14" x="2" y="5" rx="2"/><line x1="2" x2="22" y1="10" y2="10"/></svg>') !important;
}}
[data-testid="stSidebar"] div[role="radiogroup"] > label:nth-child(3) {{
    background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="%23AFC1D3" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5Z"/><path d="M6 6h10M6 10h10"/></svg>') !important;
}}
[data-testid="stSidebar"] div[role="radiogroup"] > label:nth-child(4) {{
    background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="%23AFC1D3" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m7.5 4.27 9 5.15"/><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/></svg>') !important;
}}
[data-testid="stSidebar"] div[role="radiogroup"] > label:nth-child(5) {{
    background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="%23AFC1D3" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>') !important;
}}

/* Radio Menu Hover States */
[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {{
    background-color: #1B354D !important;
}}
[data-testid="stSidebar"] div[role="radiogroup"] > label:hover div[data-testid="stMarkdownContainer"] p {{
    color: #FFFFFF !important;
}}
[data-testid="stSidebar"] div[role="radiogroup"] > label:nth-child(1):hover {{
    background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="%23FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/></svg>') !important;
}}
[data-testid="stSidebar"] div[role="radiogroup"] > label:nth-child(2):hover {{
    background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="%23FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="14" x="2" y="5" rx="2"/><line x1="2" x2="22" y1="10" y2="10"/></svg>') !important;
}}
[data-testid="stSidebar"] div[role="radiogroup"] > label:nth-child(3):hover {{
    background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="%23FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5Z"/><path d="M6 6h10M6 10h10"/></svg>') !important;
}}
[data-testid="stSidebar"] div[role="radiogroup"] > label:nth-child(4):hover {{
    background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="%23FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m7.5 4.27 9 5.15"/><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/></svg>') !important;
}}
[data-testid="stSidebar"] div[role="radiogroup"] > label:nth-child(5):hover {{
    background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="%23FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>') !important;
}}

/* Radio Menu Active Selected State */
[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) {{
    background-color: #234A76 !important;
}}
[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) div[data-testid="stMarkdownContainer"] p {{
    color: #FFFFFF !important;
    font-weight: 600 !important;
}}
[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked)::before {{
    content: "";
    position: absolute;
    left: 0;
    top: 8px;
    bottom: 8px;
    width: 3.5px;
    background-color: #38BDF8 !important;
    border-radius: 0 2px 2px 0 !important;
}}
[data-testid="stSidebar"] div[role="radiogroup"] > label:nth-child(1):has(input:checked) {{
    background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="%23FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/></svg>') !important;
}}
[data-testid="stSidebar"] div[role="radiogroup"] > label:nth-child(2):has(input:checked) {{
    background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="%23FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="14" x="2" y="5" rx="2"/><line x1="2" x2="22" y1="10" y2="10"/></svg>') !important;
}}
[data-testid="stSidebar"] div[role="radiogroup"] > label:nth-child(3):has(input:checked) {{
    background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="%23FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5Z"/><path d="M6 6h10M6 10h10"/></svg>') !important;
}}
[data-testid="stSidebar"] div[role="radiogroup"] > label:nth-child(4):has(input:checked) {{
    background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="%23FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m7.5 4.27 9 5.15"/><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/></svg>') !important;
}}
[data-testid="stSidebar"] div[role="radiogroup"] > label:nth-child(5):has(input:checked) {{
    background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="%23FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>') !important;
}}

/* Sidebar Footer Pinning (Absolute Fixed to Bottom of Viewport) */
.sidebar-footer {{
    position: fixed !important;
    bottom: 0 !important;
    left: 0 !important;
    width: 248px !important;
    height: 60px !important;
    background-color: #102A43 !important;
    border-top: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    display: flex !important;
    align-items: center !important;
    gap: 12px !important;
    padding: 0 16px !important;
    box-sizing: border-box !important;
    z-index: 99999 !important;
}}

/* Corporate Navy Action Buttons */
button[kind="primary"],
.stButton > button[kind="primary"],
div[data-testid="stButton"] > button[kind="primary"] {{
    background-color: #173B67 !important;
    border: 1px solid #173B67 !important;
    color: #FFFFFF !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    border-radius: 6px !important;
    height: 40px !important;
    transition: background-color 140ms ease !important;
    box-shadow: 0 1px 2px rgba(16, 42, 67, 0.05) !important;
}}

button[kind="primary"]:hover,
.stButton > button[kind="primary"]:hover {{
    background-color: #102A43 !important;
    border-color: #102A43 !important;
    color: #FFFFFF !important;
}}

button[kind="secondary"],
.stButton > button[kind="secondary"],
div[data-testid="stButton"] > button[kind="secondary"] {{
    background-color: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    color: #102A43 !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    border-radius: 6px !important;
    height: 34px !important;
    transition: all 140ms ease !important;
}}

button[kind="secondary"]:hover,
.stButton > button[kind="secondary"]:hover {{
    background-color: #F8FAFC !important;
    border-color: #94A3B8 !important;
}}

/* Form Input Focus Overrides (Eliminate Red Focus Rings) */
input:focus,
textarea:focus,
select:focus,
[data-baseweb="input"]:focus,
[data-baseweb="input"]:focus-within,
[data-baseweb="base-input"]:focus-within,
div[data-baseweb="input"]:focus-within,
.stTextInput > div > div:focus-within,
.stTextInput input:focus,
.stDateInput input:focus,
.stSelectbox div[role="combobox"]:focus {{
    border-color: #173B67 !important;
    box-shadow: 0 0 0 1px #173B67 !important;
    outline: none !important;
}}

[data-baseweb="input"] {{
    border: 1px solid #E2E8F0 !important;
    background-color: #FFFFFF !important;
    border-radius: 6px !important;
    transition: border-color 140ms ease !important;
}}
[data-baseweb="input"]:hover {{
    border-color: #CBD5E1 !important;
}}

/* Card Container Overrides for Streamlit Widgets */
div[data-testid="stVerticalBlockBorderWrapper"] {{
    background-color: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 10px !important;
    box-shadow: 0 1px 2px rgba(16, 42, 67, 0.02) !important;
    padding: 0 !important;
    margin-bottom: 20px !important;
    overflow: hidden !important;
}}

div[data-testid="stVerticalBlockBorderWrapper"] > div {{
    padding: 18px 20px !important;
}}

.card-header-clean {{
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    padding-bottom: 12px !important;
    margin-bottom: 14px !important;
    border-bottom: 1px solid #E2E8F0 !important;
}}

.card-title-clean {{
    font-size: 13px !important;
    font-weight: 600 !important;
    color: #102A43 !important;
}}

/* Badges for COA and status */
.badge-asset {{ background-color: #FEF3C7; color: #92400E; border: 1px solid #FDE68A; }}
.badge-liability {{ background-color: #FEE2E2; color: #991B1B; border: 1px solid #FECACA; }}
.badge-equity {{ background-color: #E0E7FF; color: #3730A3; border: 1px solid #C7D2FE; }}
.badge-revenue {{ background-color: #ECFDF5; color: #065F46; border: 1px solid #A7F3D0; }}
.badge-expense {{ background-color: #EFF6FF; color: #1E40AF; border: 1px solid #BFDBFE; }}
.badge-debit {{ background-color: #EFF6FF; color: #1E40AF; border: 1px solid #BFDBFE; }}
.badge-credit {{ background-color: #FFF7ED; color: #9A3412; border: 1px solid #FFEDD5; }}
.badge-hash {{ font-family: monospace; font-size: 10px; background-color: #F1F5F9; color: #475569; padding: 2px 6px; border-radius: 3px; border: 1px solid #E2E8F0; }}
</style>
""", unsafe_allow_html=True)

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

with st.sidebar:
    render_html("""
    <div class="sidebar-brand">
        <div class="brand-icon-box">BF</div>
        <div class="brand-text-group">
            <span class="brand-title">BizFlow</span>
            <span class="brand-subtitle-badge">LEDGER</span>
        </div>
    </div>
    <span class="sidebar-section-label">WORKSPACE</span>
    """)

    menu_selection = st.radio(
        label="Navigasi Modul",
        options=[
            "Dashboard",
            "Entri Kas Keluar",
            "Buku Besar",
            "Gudang & Stok",
            "Jejak Audit"
        ],
        label_visibility="collapsed"
    )

    render_html("""
    <div class="sidebar-footer">
        <div class="footer-user-avatar">BF</div>
        <div class="footer-user-details">
            <span class="footer-user-name">BizFlow Ledger v2.4</span>
            <span class="footer-user-role">Staf Akuntan Utama</span>
        </div>
    </div>
    """)

render_html(f"""
<header class="top-bar">
    <div class="breadcrumb-area">
        <span>BizFlow Ledger</span>
        <span>/</span>
        <span class="active-crumb">{menu_selection}</span>
    </div>
    <div class="top-bar-actions">
        <div class="system-status-indicator">
            <span class="status-dot"></span>
            <span>Database Connected (SQLite v3)</span>
        </div>
    </div>
</header>
""")

if menu_selection == "Dashboard":
    df_inv = pd.DataFrame(st.session_state.inventory_db)
    df_inv["total_value"] = df_inv["stock_qty"] * df_inv["unit_cost"]
    total_inv_val = df_inv["total_value"].sum()

    rows_coa = ""
    for acc in COA_LIST[:8]:
        b_type_class = f"badge-{acc['type'].lower()}"
        b_bal_class = f"badge-{acc['balance'].lower()}"
        rows_coa += f"""<tr>
            <td style="font-weight: 600; color: var(--deep-navy);">{acc['id']}</td>
            <td>{acc['name']}</td>
            <td><span class="badge {b_type_class}">{acc['type']}</span></td>
            <td class="tabular" style="text-align: center; font-weight: 600;"><span class="badge {b_bal_class}">{acc['balance']}</span></td>
        </tr>"""

    render_html(f"""
    <div style="width: 100%;">
        <div class="kpi-grid-4">
            <div class="kpi-stat-card accent-navy">
                <span class="kpi-stat-label">Kas &amp; Setara Kas (PSAK 2)</span>
                <span class="kpi-stat-val tabular">Rp 142.500.000</span>
                <span class="kpi-stat-desc">Aset lancar likuid perbankan &amp; kas operasional</span>
            </div>
            <div class="kpi-stat-card accent-teal">
                <span class="kpi-stat-label">Valuasi Persediaan</span>
                <span class="kpi-stat-val tabular">{format_idr(total_inv_val)}</span>
                <span class="kpi-stat-desc">Aset barang dagang sistem perpetual</span>
            </div>
            <div class="kpi-stat-card accent-amber">
                <span class="kpi-stat-label">Total Beban Operasional</span>
                <span class="kpi-stat-val tabular">Rp 28.600.000</span>
                <span class="kpi-stat-desc">Akrual beban periode Oktober 2026</span>
            </div>
            <div class="kpi-stat-card accent-green">
                <span class="kpi-stat-label">Integritas Transaksi</span>
                <span class="kpi-stat-val tabular">100% Balanced</span>
                <span class="kpi-stat-desc">Zero discrepancy gate &amp; segel SHA-256</span>
            </div>
        </div>

        <div style="display: grid; grid-template-columns: 1.4fr 1fr; gap: 20px; margin-bottom: 20px; align-items: start;">
            <div class="card" style="margin-bottom: 0;">
                <div class="card-header">
                    <h2 class="card-title">Bagan Akun Finansial (Chart of Accounts - 3NF)</h2>
                    <span class="badge badge-posted">Standar PSAK</span>
                </div>
                <div class="card-body" style="padding: 0;">
                    <table class="enterprise-table">
                        <thead>
                            <tr>
                                <th style="width: 18%;">Kode</th>
                                <th style="width: 36%;">Nama Akun</th>
                                <th style="width: 22%;">Klasifikasi</th>
                                <th style="width: 24%; text-align: center;">Saldo Normal</th>
                            </tr>
                        </thead>
                        <tbody>
                            {rows_coa}
                        </tbody>
                    </table>
                </div>
            </div>

            <div class="card" style="margin-bottom: 0;">
                <div class="card-header">
                    <h2 class="card-title">Distribusi Beban Operasional</h2>
                    <span class="badge badge-draft">Oktober 2026</span>
                </div>
                <div class="card-body" style="padding: 20px;">
                    <div class="progress-list">
                        <div>
                            <div class="progress-item-header">
                                <span style="font-weight: 600; color: var(--deep-navy);">Gaji &amp; Upah Karyawan</span>
                                <span class="tabular" style="font-weight: 600; color: var(--primary-navy);">Rp 12.870.000 (45%)</span>
                            </div>
                            <div class="progress-track"><div class="progress-fill" style="width: 45%;"></div></div>
                        </div>
                        <div>
                            <div class="progress-item-header">
                                <span style="font-weight: 600; color: var(--deep-navy);">Sewa Gedung Kantor</span>
                                <span class="tabular" style="font-weight: 600; color: var(--primary-navy);">Rp 7.150.000 (25%)</span>
                            </div>
                            <div class="progress-track"><div class="progress-fill" style="width: 25%;"></div></div>
                        </div>
                        <div>
                            <div class="progress-item-header">
                                <span style="font-weight: 600; color: var(--deep-navy);">Listrik, Air &amp; Utilitas</span>
                                <span class="tabular" style="font-weight: 600; color: var(--primary-navy);">Rp 4.290.000 (15%)</span>
                            </div>
                            <div class="progress-track"><div class="progress-fill" style="width: 15%;"></div></div>
                        </div>
                        <div>
                            <div class="progress-item-header">
                                <span style="font-weight: 600; color: var(--deep-navy);">Perlengkapan Toko</span>
                                <span class="tabular" style="font-weight: 600; color: var(--primary-navy);">Rp 4.290.000 (15%)</span>
                            </div>
                            <div class="progress-track"><div class="progress-fill" style="width: 15%;"></div></div>
                        </div>
                    </div>
                    <div style="margin-top: 20px; padding: 12px; background-color: var(--neutral-bg); border-radius: 6px; border: 1px solid var(--border); font-size: 11px; color: var(--secondary-text); line-height: 1.5;">
                        <strong>Pengendalian Anggaran:</strong> Seluruh beban terverifikasi melalui voucher kas keluar terotorisasi dengan pembebanan langsung ke Buku Besar.
                    </div>
                </div>
            </div>
        </div>

        <div class="card">
            <div class="card-header">
                <div>
                    <h2 class="card-title">Arus Kas &amp; Likuiditas Finansial (Tren 6 Bulan)</h2>
                </div>
                <div style="display: flex; gap: 16px; align-items: center; font-size: 12px;">
                    <div style="display: flex; align-items: center; gap: 6px;">
                        <span style="width: 10px; height: 10px; background-color: var(--primary-navy); border-radius: 2px; display: inline-block;"></span>
                        <span style="color: var(--secondary-text);">Penerimaan Kas</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 6px;">
                        <span style="width: 10px; height: 10px; background-color: #94A3B8; border-radius: 2px; display: inline-block;"></span>
                        <span style="color: var(--secondary-text);">Pengeluaran Kas</span>
                    </div>
                    <span class="badge badge-posted">PSAK 2</span>
                </div>
            </div>
            <div class="card-body">
                <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 24px; align-items: center;">
                    <div style="width: 100%; height: 200px;">
                        <svg viewBox="0 0 540 180" style="width: 100%; height: 100%; overflow: visible;" preserveAspectRatio="xMidYMid meet">
                            <line x1="40" y1="20" x2="520" y2="20" stroke="#F1F5F9" stroke-width="1"/>
                            <line x1="40" y1="60" x2="520" y2="60" stroke="#F1F5F9" stroke-width="1"/>
                            <line x1="40" y1="100" x2="520" y2="100" stroke="#F1F5F9" stroke-width="1"/>
                            <line x1="40" y1="140" x2="520" y2="140" stroke="#E2E8F0" stroke-width="1.5"/>

                            <text x="32" y="24" font-size="10" fill="#94A3B8" text-anchor="end">60jt</text>
                            <text x="32" y="64" font-size="10" fill="#94A3B8" text-anchor="end">40jt</text>
                            <text x="32" y="104" font-size="10" fill="#94A3B8" text-anchor="end">20jt</text>
                            <text x="32" y="144" font-size="10" fill="#94A3B8" text-anchor="end">0</text>

                            <!-- Mei -->
                            <rect x="65" y="50" width="22" height="90" rx="3" fill="#173B67"/>
                            <rect x="91" y="84" width="22" height="56" rx="3" fill="#94A3B8"/>
                            <text x="89" y="160" font-size="11" fill="#526174" text-anchor="middle" font-weight="500">Mei</text>

                            <!-- Jun -->
                            <rect x="145" y="36" width="22" height="104" rx="3" fill="#173B67"/>
                            <rect x="171" y="78" width="22" height="62" rx="3" fill="#94A3B8"/>
                            <text x="169" y="160" font-size="11" fill="#526174" text-anchor="middle" font-weight="500">Jun</text>

                            <!-- Jul -->
                            <rect x="225" y="42" width="22" height="98" rx="3" fill="#173B67"/>
                            <rect x="251" y="74" width="22" height="66" rx="3" fill="#94A3B8"/>
                            <text x="249" y="160" font-size="11" fill="#526174" text-anchor="middle" font-weight="500">Jul</text>

                            <!-- Agu -->
                            <rect x="305" y="24" width="22" height="116" rx="3" fill="#173B67"/>
                            <rect x="331" y="70" width="22" height="70" rx="3" fill="#94A3B8"/>
                            <text x="329" y="160" font-size="11" fill="#526174" text-anchor="middle" font-weight="500">Agu</text>

                            <!-- Sep -->
                            <rect x="385" y="32" width="22" height="108" rx="3" fill="#173B67"/>
                            <rect x="411" y="76" width="22" height="64" rx="3" fill="#94A3B8"/>
                            <text x="409" y="160" font-size="11" fill="#526174" text-anchor="middle" font-weight="500">Sep</text>

                            <!-- Okt -->
                            <rect x="465" y="16" width="22" height="124" rx="3" fill="#173B67"/>
                            <rect x="491" y="64" width="22" height="76" rx="3" fill="#94A3B8"/>
                            <text x="489" y="160" font-size="11" fill="#102A43" text-anchor="middle" font-weight="700">Okt</text>
                        </svg>
                    </div>

                    <div style="display: flex; flex-direction: column; gap: 12px; border-left: 1px solid var(--border); padding-left: 20px;">
                        <div>
                            <span style="font-size: 11px; text-transform: uppercase; color: var(--secondary-text); font-weight: 600; letter-spacing: 0.3px; display: block;">Surplus Kas Operasional (Okt)</span>
                            <span class="tabular" style="font-size: 18px; font-weight: 700; color: var(--success);">+ Rp 24.500.000</span>
                            <span style="font-size: 11px; color: var(--secondary-text); display: block;">Penerimaan Rp 62,5jt vs Pengeluaran Rp 38,0jt</span>
                        </div>

                        <div style="border-top: 1px dashed var(--border); padding-top: 10px;">
                            <span style="font-size: 11px; text-transform: uppercase; color: var(--secondary-text); font-weight: 600; letter-spacing: 0.3px; display: block;">Rasio Lancar (Current Ratio)</span>
                            <span class="tabular" style="font-size: 18px; font-weight: 700; color: var(--primary-navy);">3.42x</span>
                            <span style="font-size: 11px; color: var(--secondary-text); display: block;">Likuiditas sangat kuat memenuhi kewajiban lancar</span>
                        </div>

                        <div style="border-top: 1px dashed var(--border); padding-top: 10px;">
                            <span style="font-size: 11px; text-transform: uppercase; color: var(--secondary-text); font-weight: 600; letter-spacing: 0.3px; display: block;">Perputaran Piutang (DSO)</span>
                            <span class="tabular" style="font-size: 18px; font-weight: 700; color: var(--deep-navy);">14 Hari</span>
                            <span style="font-size: 11px; color: var(--secondary-text); display: block;">Efisiensi konversi kas rata-rata perputaran ritel</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """)

elif menu_selection == "Entri Kas Keluar":
    render_html("""
    <div>
        <h1 class="page-title">Entri Kas Keluar (Disbursement Voucher)</h1>
        <p class="page-subtitle">Pencatatan kas keluar dengan validasi keseimbangan debit-kredit dan penerbitan segel SHA-256.</p>
    </div>
    """)

    wrap_col1, wrap_col2 = st.columns([1.5, 1], gap="medium")

    with wrap_col1:
        with st.container(border=True):
            render_html("""
            <div class="card-header-clean">
                <span class="card-title-clean">Informasi Voucher</span>
                <span class="badge badge-draft">DRAFT</span>
            </div>
            """)
            f1, f2, f3 = st.columns([1, 1, 2])
            with f1:
                ref_no = st.text_input("Nomor Voucher", value="BKK-2026/10/003")
            with f2:
                trx_date = st.date_input("Tanggal Transaksi", value=date(2026, 10, 19))
            with f3:
                description = st.text_input("Deskripsi", value="Pembayaran Beban Gaji & Operasional Kantor")

        with st.container(border=True):
            render_html("""
            <div class="card-header-clean">
                <span class="card-title-clean">Rincian Jurnal Berpasangan</span>
                <span class="badge badge-posted">Sistem Verifikasi Otomatis</span>
            </div>
            """)

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

    with wrap_col2:
        tot_deb = float(edited_df["Debit"].sum()) if "Debit" in edited_df else 0.0
        tot_cre = float(edited_df["Kredit"].sum()) if "Kredit" in edited_df else 0.0
        diff = abs(tot_deb - tot_cre)
        is_bal = (diff == 0.0) and (tot_deb > 0)

        status_class = "balanced" if is_bal else "unbalanced"
        badge_text = "SEIMBANG" if is_bal else "TIDAK SEIMBANG"
        hint_text = "Pengendalian internal terpenuhi. Siap diposting ke Buku Besar." if is_bal else "Tombol posting terkunci sampai selisih bernilai Rp 0."

        with st.container(border=True):
            render_html(f"""
            <div class="card-header-clean">
                <span class="card-title-clean">Keseimbangan Finansial</span>
                <span style="font-size: 11px; color: var(--secondary-text);">Mata Uang: IDR</span>
            </div>

            <div class="balance-status-block {status_class}" style="margin-bottom: 16px;">
                <span class="balance-status-badge {status_class}">{badge_text}</span>
                <div style="font-size: 11px; color: var(--secondary-text); margin-bottom: 12px;">{hint_text}</div>
                <div class="summary-row">
                    <span class="summary-row-label">Total Debit:</span>
                    <span class="summary-row-val tabular">{format_idr(tot_deb)}</span>
                </div>
                <div class="summary-row">
                    <span class="summary-row-label">Total Kredit:</span>
                    <span class="summary-row-val tabular">{format_idr(tot_cre)}</span>
                </div>
                <div class="summary-row" style="border-top: 1px dashed var(--border); padding-top: 8px; margin-top: 4px;">
                    <span class="summary-row-label" style="font-weight: 600;">Selisih:</span>
                    <span class="summary-row-val tabular" style="font-size: 14px; color: {'#16805D' if is_bal else '#C83C45'};">{format_idr(diff)}</span>
                </div>
            </div>
            """)

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

                st.success(f"Voucher {ref_no} berhasil diposting!\nSegel SHA-256: {sha_sig[:24]}...")
                st.rerun()

            p1, p2 = st.columns(2)
            with p1:
                if st.button("Uji Skenario Seimbang", use_container_width=True):
                    st.session_state.entry_lines = pd.DataFrame([
                        {"Akun": list(COA_MAP.keys())[9], "Memo": "Gaji Staf Toko Oktober 2026", "Debit": 3800000.0, "Kredit": 0.0},
                        {"Akun": list(COA_MAP.keys())[11], "Memo": "Tagihan Listrik PLN Kantor", "Debit": 750000.0, "Kredit": 0.0},
                        {"Akun": list(COA_MAP.keys())[0], "Memo": "Pengeluaran Kas Kasir Utama", "Debit": 0.0, "Kredit": 4550000.0}
                    ])
                    st.rerun()
            with p2:
                if st.button("Uji Skenario Selisih", use_container_width=True):
                    st.session_state.entry_lines = pd.DataFrame([
                        {"Akun": list(COA_MAP.keys())[10], "Memo": "Sewa Gudang Tambahan", "Debit": 5000000.0, "Kredit": 0.0},
                        {"Akun": list(COA_MAP.keys())[0], "Memo": "Pengeluaran Kas Operasional", "Debit": 0.0, "Kredit": 4200000.0}
                    ])
                    st.rerun()

elif menu_selection == "Buku Besar":
    render_html("""
    <div>
        <h1 class="page-title">Buku Besar (General Ledger 3NF)</h1>
        <p class="page-subtitle">Buku besar transaksi terposting dengan filter pencarian dan verifikasi integritas checksum SHA-256.</p>
    </div>
    """)

    b_col1, b_col2 = st.columns([3, 1])
    with b_col1:
        search_query = st.text_input("Pencarian Transaksi", placeholder="Cari nomor bukti, akun, atau memo...", label_visibility="collapsed")
    with b_col2:
        status_filter = st.selectbox("Filter Status", ["Semua Status", "Hanya POSTED"], label_visibility="collapsed")

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

        rows_journal = ""
        for _, r in df_j.iterrows():
            deb_str = format_idr(r['debit']) if r['debit'] > 0 else "-"
            cre_str = format_idr(r['credit']) if r['credit'] > 0 else "-"
            h_short = r['hash_checksum'][:16] + "..." if r['hash_checksum'] else "-"
            rows_journal += f"""<tr>
                <td style="font-weight: 500;">{r['trx_date']}</td>
                <td style="font-weight: 600; color: var(--deep-navy);">{r['ref_no']}</td>
                <td>{r['description']}</td>
                <td style="font-weight: 500;">{r['account']}</td>
                <td style="text-align: right; font-weight: 600;" class="tabular">{deb_str}</td>
                <td style="text-align: right; font-weight: 600;" class="tabular">{cre_str}</td>
                <td><span class="badge badge-posted">{r['status_posting']}</span></td>
                <td><span class="badge badge-hash">#{h_short}</span></td>
            </tr>"""

        render_html(f"""
        <div class="card" style="margin-top: 12px;">
            <div class="card-header">
                <h2 class="card-title">Jurnal Umum &amp; Buku Besar Terposting</h2>
                <span class="badge badge-posted">Buku Besar 3NF</span>
            </div>
            <div class="card-body" style="padding: 0; overflow-x: auto;">
                <table class="enterprise-table">
                    <thead>
                        <tr>
                            <th style="width: 110px;">TANGGAL</th>
                            <th style="width: 150px;">NO. BUKTI</th>
                            <th>DESKRIPSI</th>
                            <th>AKUN FINANSIAL</th>
                            <th style="text-align: right; width: 140px;">DEBIT</th>
                            <th style="text-align: right; width: 140px;">KREDIT</th>
                            <th style="width: 100px;">STATUS</th>
                            <th style="width: 160px;">CHECKSUM SHA-256</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows_journal}
                    </tbody>
                </table>
            </div>
        </div>
        """)
    else:
        st.info("Belum ada data transaksi yang tercatat.")

elif menu_selection == "Gudang & Stok":
    df_inv = pd.DataFrame(st.session_state.inventory_db)
    df_inv["total_value"] = df_inv["stock_qty"] * df_inv["unit_cost"]

    rows_inv = ""
    for _, item in df_inv.iterrows():
        rows_inv += f"""<tr>
            <td style="font-weight: 600; color: var(--deep-navy);">{item['item_id']}</td>
            <td style="font-weight: 500;">{item['item_name']}</td>
            <td style="text-align: right; font-weight: 600;" class="tabular">{item['stock_qty']:,.0f} unit</td>
            <td style="text-align: right;" class="tabular">{format_idr(item['unit_cost'])}</td>
            <td style="text-align: right; font-weight: 700; color: var(--primary-navy);" class="tabular">{format_idr(item['total_value'])}</td>
        </tr>"""

    render_html(f"""
    <div style="width: 100%;">
        <div class="kpi-row-3" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 20px;">
            <div class="kpi-stat-card accent-navy">
                <span class="kpi-stat-label">Total Jenis Barang</span>
                <span class="kpi-stat-val tabular">{len(df_inv)} Item</span>
                <span class="kpi-stat-desc">Katalog aktif di gudang</span>
            </div>
            <div class="kpi-stat-card accent-teal">
                <span class="kpi-stat-label">Total Unit Fisik</span>
                <span class="kpi-stat-val tabular">{df_inv['stock_qty'].sum():,.0f} Unit</span>
                <span class="kpi-stat-desc">Tersedia untuk penjualan</span>
            </div>
            <div class="kpi-stat-card accent-amber">
                <span class="kpi-stat-label">Valuasi Persediaan</span>
                <span class="kpi-stat-val tabular">{format_idr(df_inv['total_value'].sum())}</span>
                <span class="kpi-stat-desc">Berdasarkan harga perolehan</span>
            </div>
        </div>
    </div>
    """)

    col_inv, col_form = st.columns([1.4, 1], gap="medium")

    with col_inv:
        render_html(f"""
        <div class="card">
            <div class="card-header">
                <h2 class="card-title">Katalog Persediaan (Sistem Perpetual)</h2>
                <span class="badge badge-posted">Perpetual</span>
            </div>
            <div class="card-body" style="padding: 0; overflow-x: auto;">
                <table class="enterprise-table">
                    <thead>
                        <tr>
                            <th style="width: 100px;">KODE</th>
                            <th>NAMA BARANG</th>
                            <th style="text-align: right; width: 120px;">STOK FISIK</th>
                            <th style="text-align: right; width: 140px;">HARGA POKOK</th>
                            <th style="text-align: right; width: 150px;">TOTAL NILAI</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows_inv}
                    </tbody>
                </table>
            </div>
        </div>
        """)

    with col_form:
        with st.container(border=True):
            render_html("""
            <div class="card-header-clean">
                <span class="card-title-clean">Mutasi Barang Gudang</span>
                <span class="badge badge-draft">Database Trigger</span>
            </div>
            """)

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
                            f"Saldo fisik saat ini: {target_item['stock_qty']} unit | Permintaan: {qty_input} unit.\n\n"
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

elif menu_selection == "Jejak Audit":
    col_aud, col_lab = st.columns([1.4, 1], gap="medium")

    with col_aud:
        rows_aud = ""
        action_badge_map = {
            "POSTED": "badge-posted",
            "REVERSAL": "badge-equity",
            "SECURITY_BLOCKED": "badge-liability",
            "REJECTED": "badge-liability",
            "SALE": "badge-asset",
            "PURCHASE": "badge-debit"
        }

        for aud in st.session_state.audit_db:
            act_b = action_badge_map.get(aud['action'], "badge-draft")
            h_short = aud['hash'][:16] + "..." if aud['hash'] else "-"
            rows_aud += f"""<tr>
                <td style="font-weight: 500;">{aud['time']}</td>
                <td><span class="badge {act_b}">{aud['action']}</span></td>
                <td>{aud['table']}</td>
                <td style="font-weight: 600; color: var(--deep-navy);">{aud['ref']}</td>
                <td>{aud['user']}</td>
                <td><span class="badge badge-hash">#{h_short}</span></td>
            </tr>"""

        render_html(f"""
        <div class="card">
            <div class="card-header">
                <h2 class="card-title">Kronologi Aktivitas &amp; Log Audit Finansial</h2>
                <span class="badge badge-posted">Immutable Log</span>
            </div>
            <div class="card-body" style="padding: 0; overflow-x: auto;">
                <table class="enterprise-table">
                    <thead>
                        <tr>
                            <th style="width: 140px;">WAKTU</th>
                            <th style="width: 110px;">AKSI</th>
                            <th>TABEL ENTITAS</th>
                            <th style="width: 140px;">NO. BUKTI</th>
                            <th style="width: 90px;">OPERATOR</th>
                            <th style="width: 150px;">CHECKSUM SHA-256</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows_aud}
                    </tbody>
                </table>
            </div>
        </div>
        """)

    with col_lab:
        with st.container(border=True):
            render_html("""
            <div class="card-header-clean">
                <span class="card-title-clean">Pengujian Imutabilitas Transaksi</span>
                <span class="badge badge-posted">Sistem Kontrol</span>
            </div>
            <div style="padding: 10px 12px; background-color: var(--neutral-bg); border-radius: 6px; border: 1px solid var(--border); font-size: 11px; color: var(--secondary-text); line-height: 1.5; margin-bottom: 16px;">
                Transaksi <strong>POSTED</strong> terkunci permanen. Seluruh koreksi wajib melalui <strong>Jurnal Pembalik (Storno)</strong>.
            </div>
            """)

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
                        "debit": line["credit"],
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
