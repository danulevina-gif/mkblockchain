import streamlit as st
from core import Blockchain

st.set_page_config(page_title="Blockchain Explorer", page_icon="🔗", layout="wide")
st.title("📦 Blockchain for Halal Coffee Supply Chain")

if 'my_blockchain' not in st.session_state:
    st.session_state.my_blockchain = Blockchain()

st.sidebar.header("➕ Tambah Data Baru")

petani = st.sidebar.text_input("Nama Petani: ")
jumlah_kopi = st.sidebar.number_input("Jumlah Panen (Kg): ", min_value=1)
lokasi = st.sidebar.text_input("Lokasi Kebun: ")

if  st.sidebar.button("Tambahkan ke Blockchain: "):
    if petani and lokasi:
        data_transaksi = f"Petani: {petani} | Panen: {jumlah_kopi} Kg | Lokasi: {lokasi}"
        st.session_state.my_blockchain.add_block(data_transaksi)
        st.sidebar.success("Data berhasil ditambahkan!")
    else:
        st.sidebar.error("Lengkapi semua data!")

st.subheader("📙 Blockchain Ledger (Buku Besar)")

is_valid = st.session_state.my_blockchain.is_chain_valid()
if is_valid:
    st.success("✔️ Status Jaringan: Rantai Valid (Aman)")
else:
    st.error("❌ PERINGATAN: Integritas Rantai Rusak (Telah Dimanipulasi!")

for block in st.session_state.my_blockchain.chain:
    with st.expander(f"Blok #{block.index} | Hash: {block.hash[:15]}..."):
        col1, col2 = st.columns(2)

        with col1:
            st.write("**Data Payload:**")
            st.info(block.data)
            st.write(f"**Timestamp:** {block.timestamp_readable}")

        with col2:
            st.write("**Kriptografi:**")
            st.write(f"**Hash saat ini:**")
            st.code(block.hash, language='python')
            st.write(f"**Hash Sebelumnya (Pointer):**")
            st.code(block.prev_hash, language='python')