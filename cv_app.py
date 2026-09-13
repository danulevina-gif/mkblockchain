import streamlit as st

st.set_page_config(page_title="CV Digital Mahasiswa", page_icon="🎓", layout="centered")

st.sidebar.title("⚙️ Pengaturan Profil")
st.sidebar.write("Masukkan data diri anda dibawah ini : ")

nama = st.sidebar.text_input("Nama Lengkap", "Danu Suryana")
nim = st.sidebar.text_input("NIM", "2530801070")
jurusan = st.sidebar.selectbox("Jurusan", ["Informatika", "Sistem informasi", "Teknik Komputer", "Teknik Elektro"])
pengalaman_organisasi = st.sidebar.text_area("Pengalaman Organisasi")
deskripsi = st.sidebar.text_area("Deskripsi Singkat (Bio)", "Saya adalah mahasiswa yang tertarik pada bidang pengembangan perangkat lunak dan analisis data.")
foto_profil = st.sidebar.file_uploader("Unggah Foto Profil (Opsional)", type=['jpg', 'jpeg', 'png'])
punya_magang = st.sidebar.checkbox("Punya Pengalaman Magang/Sertifikasi?")

st.title("🎓 Curriculum Vitae Digital")
st.markdown("---")

kolom_kiri, kolom_kanan = st.columns([2, 1])

with kolom_kiri:
    st.header(nama)
    st.subheader(f"{jurusan} | NIM: {nim}")
    st.write(deskripsi)

with kolom_kanan:
    if foto_profil is not None:
        st.image(foto_profil, width=200, caption="Foto Profil")
    else:
        st.info("Belum ada foto yang diunggah.")

st.subheader("👥 Pengalaman Organisasi")
if pengalaman_organisasi.strip():
    st.write(pengalaman_organisasi)
else:
    st.write("_Belum ada pengalaman organisasi yang diisi._")

detail_magang = ""
if punya_magang:
    detail_magang = st.sidebar.text_area("Detail Magang / Sertifikasi")
if punya_magang and detail_magang.strip():
    st.subheader("🏆 Magang & Sertifikasi")
    st.success(detail_magang)

st.markdown("### 🛠️ Keahlian Teknis")

st.sidebar.markdown("---")
st.sidebar.subheader("Atur Kemahiran Skill")
skill_python = st.sidebar.slider("Python", 0, 100, 80)
skill_web = st.sidebar.slider("Web Development", 0, 100, 60)
skill_db = st.sidebar.slider("Database", 0, 100, 70)

st.write(f"**Python** ({skill_python}%)")
st.progress(skill_python)

st.write(f"**Web Development (HTML/CSS)** ({skill_web}%)")
st.progress(skill_web)

st.write(f"**Database (SQL)** ({skill_db}%)")
st.progress(skill_db)

st.divider()

st.markdown("### 📬 Hubungi Saya")

username = "".join(e for e in nama.lower() if e.isalnum())

with st.expander("Klik untuk melihat detail kontak"):
    st.write(f"📧 **Email:** {username}@mahasiswa.univ.ac.id")
    st.write(f"🔗 **LinkedIn:** [linkedin.com/in/{username}](https://linkedin.com/in/{username})")
    st.write(f"🐙 **GitHub:** [github.com/{username}](https://github.com/{username})")

data_cv = f"Nama: {nama}\nNIM: {nim}\nJurusan: {jurusan}"
st.download_button(
    label="📥 Download Data CV",
    data=data_cv,
    file_name="cv_mahasiswa.txt",
    mime="text/plain"
)