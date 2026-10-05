import streamlit as st
from core import Block, Blockchain

st.set_page_config(page_title="Supply Chain Kopi", page_icon="☕", layout="wide")
st.title(" ☕ Sistem Pelacakan Rantai Pasok Kopi")

if "kopi_chain" not in st.session_state:
    st.session_state.kopi_chain = Blockchain()

# --- Modifikasi Tugas: Menambahkan Simulasi Serangan (Hacking) ---
with st.sidebar:
    st.header("⚙️ Panel Developer")
    st.markdown("Gunakan tombol di bawah ini untuk mensimulasikan peretasan data pada Blockchain.")
    
    # Ubah Data Secara Paksa (Tombol HACK BLOK 1)
    if st.button("🚨 HACK BLOK 1"):
        # Mencegah error jika pengguna menekan tombol sebelum ada blok tambahan selain Genesis
        if len(st.session_state.kopi_chain.chain) > 1:
            # Manipulasi Memori
            st.session_state.kopi_chain.chain[1].data = "DATA PALSU!"
            st.error("Peretasan Berhasil! Data blok index 1 telah diubah secara paksa.")
        else:
            st.warning("Gagal! Tambahkan minimal 1 blok terlebih dahulu (Mine Block).")

    st.markdown("---")

    st.subheader("🛡️ Validasi Sistem")
    if st.button("🛡️ Cek Integritas Rantai"):
        if st.session_state.kopi_chain.is_chain_valid():
            st.success("Status Jaringan: AMAN (Rantai Valid)")
        else: 
            st.error("Status Jaringan: BAHAYA (Data telah dimanipulasi!)")

# Bungkus input dan tombol ke dalam st.form
with st.form(key="form_tambah_data", clear_on_submit=True):
    st.markdown("**Masukkan Data Pengiriman Baru**")
    
    # Membagi layout menjadi 3 kolom agar tampilan form lebih rapi (sejajar)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        jumlah_kg = st.number_input("Jumlah (kg):", min_value=1, step=1)
    with col2:
        lokasi = st.text_input("Asal Lokasi:")
    with col3:
        nama_pengirim = st.text_input("Nama Pengirim:")
    
    submit_button = st.form_submit_button("⛏️ Mine Block ( Tambah Data )")

    if submit_button:
        # Validasi: Pastikan input teks (lokasi dan nama) tidak kosong
        if lokasi and nama_pengirim:
            
            # GABUNGKAN DATA: Format ketiga variabel menjadi satu kesatuan teks
            data_kopi = f"{jumlah_kg} kg | Dari: {lokasi} | Pengirim: {nama_pengirim}"
            
            new_index = len(st.session_state.kopi_chain.chain)
            new_block = Block(new_index, data_kopi, "")

            with st.spinner("Sedang mencari Hash yang tepat (Mining)..."):
                st.session_state.kopi_chain.add_block(new_block)

            st.success(f"Berhasil! Data '{data_kopi}' diamankan ke dalam rantai.")
        else:
            st.warning("Gagal! Mohon lengkapi kolom Asal Lokasi dan Nama Pengirim.")

st.subheader("📕 Buku Besar (Ledger)")
for block in st.session_state.kopi_chain.chain:
    with st.expander(f"Blok #{block.index} - Hash: {block.hash[:15]}..."):
        st.write(f"**Waktu:** {block.timestamp_readable}")
        st.write(f"**Data:** {block.data}")
        st.write(f"**Nonce:** {block.nonce}")
        st.write(f"**Previous Hash:** {block.previous_hash}")
        st.info(f"**Hash:** {block.hash}")