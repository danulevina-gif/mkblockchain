import streamlit as st
from core import Blockchain

st.set_page_config(page_title="Qurban Blockchain Explorer", page_icon="🔗", layout="wide")
st.title("🐄 Blockchain untuk Rantai Pasok Hewan Qurban")
st.caption("Pelacakan transparan dari peternak hingga daging sampai ke penerima.")

# ---------- Data pilihan ----------
JENIS_HEWAN = {
    "Sapi": "🐄",
    "Kambing": "🐐",
    "Domba": "🐑",
    "Kerbau": "🐃",
    "Unta": "🐪",
}

TAHAP_PROSES = [
    "1. Pembelian dari Peternak",
    "2. Pemeriksaan Kesehatan Hewan",
    "3. Penyembelihan",
    "4. Pemeriksaan Daging",
    "5. Pemotongan & Pengemasan",
    "6. Distribusi ke Penerima",
]

PENERIMA = [
    "Shohibul Qurban",
    "Kerabat & Tetangga",
    "Fakir Miskin",
]

# ---------- State ----------
if "my_blockchain" not in st.session_state:
    st.session_state.my_blockchain = Blockchain()

# ---------- Sidebar: input data ----------
st.sidebar.header("➕ Tambah Data Baru")

id_hewan = st.sidebar.text_input("ID Hewan (contoh: SPI-001):")
jenis_hewan = st.sidebar.selectbox("Jenis Hewan:", list(JENIS_HEWAN.keys()))
tahap = st.sidebar.selectbox("Tahap Proses:", TAHAP_PROSES)
peternak = st.sidebar.text_input("Nama Peternak / Penyedia:")
bobot = st.sidebar.number_input("Bobot Hewan (Kg):", min_value=1, value=100)
lokasi = st.sidebar.text_input("Lokasi:")
memenuhi_syarat = st.sidebar.checkbox(
    "Memenuhi Syarat Syar'i (cukup umur, sehat, tidak cacat)", value=True
)

# Input tambahan hanya muncul saat tahap distribusi
penerima = None
jumlah_paket = None
if tahap == TAHAP_PROSES[-1]:
    penerima = st.sidebar.selectbox("Kategori Penerima:", PENERIMA)
    jumlah_paket = st.sidebar.number_input("Jumlah Paket Daging:", min_value=1, value=10)

if st.sidebar.button("Tambahkan ke Blockchain"):
    if id_hewan and peternak and lokasi:
        status = "Memenuhi Syarat" if memenuhi_syarat else "Perlu Ditinjau"
        data_transaksi = (
            f"ID: {id_hewan} | Hewan: {jenis_hewan} | Bobot: {bobot} Kg | "
            f"Tahap: {tahap} | Peternak: {peternak} | Lokasi: {lokasi} | "
            f"Status Syar'i: {status}"
        )
        if penerima:
            data_transaksi += f" | Penerima: {penerima} | Paket: {jumlah_paket}"

        st.session_state.my_blockchain.add_block(data_transaksi)
        st.sidebar.success("Data berhasil ditambahkan!")
    else:
        st.sidebar.error("Lengkapi semua data!")

# ---------- Sidebar: simulasi keamanan ----------
st.sidebar.divider()
st.sidebar.header("🧪 Simulasi Keamanan")

chain = st.session_state.my_blockchain.chain

if st.sidebar.button("Manipulasi Data Blok #2"):
    if len(chain) > 1:
        chain[1].data = "DATA DIUBAH OLEH PIHAK TIDAK BERTANGGUNG JAWAB"
    else:
        st.sidebar.warning("Tambahkan minimal 1 data dulu.")

if st.sidebar.button("Reset Blockchain"):
    st.session_state.my_blockchain = Blockchain()
    chain = st.session_state.my_blockchain.chain

# ---------- Ledger ----------
st.subheader("📙 Blockchain Ledger (Buku Besar)")

is_valid = st.session_state.my_blockchain.is_chain_valid()

col_a, col_b = st.columns(2)
col_a.metric("Total Blok", len(chain))
col_b.metric("Catatan Qurban", len(chain) - 1)

if is_valid:
    st.success("✔️ Status Jaringan: Rantai Valid (Aman)")
else:
    st.error("❌ PERINGATAN: Integritas Rantai Rusak (Telah Dimanipulasi!)")

for block in chain:
    emoji = "🔗"
    for nama, ikon in JENIS_HEWAN.items():
        if f"Hewan: {nama}" in block.data:
            emoji = ikon
            break

    with st.expander(f"{emoji} Blok #{block.index} | Hash: {block.hash[:15]}..."):
        col1, col2 = st.columns(2)

        with col1:
            st.write("**Data Payload:**")
            st.info(block.data)
            st.write(f"**Timestamp:** {block.timestamp_readable}")

        with col2:
            st.write("**Kriptografi:**")
            st.write("**Hash saat ini:**")
            st.code(block.hash, language="python")
            st.write("**Hash Sebelumnya (Pointer):**")
            st.code(block.prev_hash, language="python")