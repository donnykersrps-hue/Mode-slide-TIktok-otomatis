import streamlit as st
import pandas as pd

# 1. Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="Ruang Teduh - Schedule Matrix",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Inject Custom CSS Perfeksionis (Micro-Interactions, Hover Glow, & Badge Styling)
custom_css = """
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');

    /* Theme Base Reset */
    .stApp {
        background-color: #0b1120;
        color: #f8fafc;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Container Header Luxury Glassmorphism */
    .header-box {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 1px solid rgba(234, 179, 8, 0.35);
        border-radius: 20px;
        padding: 28px 36px;
        margin-bottom: 25px;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(12px);
        transition: all 0.3s ease;
    }
    
    .header-box:hover {
        border-color: rgba(234, 179, 8, 0.6);
        box-shadow: 0 15px 40px rgba(234, 179, 8, 0.15);
    }

    .brand-badge {
        display: inline-block;
        background: linear-gradient(90deg, rgba(234, 179, 8, 0.2) 0%, rgba(202, 138, 4, 0.1) 100%);
        color: #fef08a;
        padding: 6px 16px;
        border-radius: 30px;
        font-size: 13px;
        font-weight: 700;
        border: 1px solid rgba(234, 179, 8, 0.4);
        margin-bottom: 12px;
        letter-spacing: 0.5px;
    }

    .header-title {
        color: #ffffff;
        font-size: 32px;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
    }

    .header-subtitle {
        color: #94a3b8;
        font-size: 15px;
        margin-top: 6px;
    }

    /* Metric Cards Glow */
    div[data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 15px 20px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    
    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        border-color: rgba(234, 179, 8, 0.4);
    }

    div[data-testid="stMetricValue"] {
        color: #fef08a !important;
        font-weight: 800 !important;
        font-size: 26px !important;
    }

    div[data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-weight: 600 !important;
    }

    /* MICRO-INTERACTION: Radio Option Buttons (Menyala & Terangkat Saat Disentuh Kursor) */
    div[data-testid="stRadioButton"] label {
        background: rgba(30, 41, 59, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 12px !important;
        padding: 10px 22px !important;
        color: #cbd5e1 !important;
        font-weight: 600 !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
        margin-right: 8px !important;
    }

    /* Hover State (Efek Menyala Emas) */
    div[data-testid="stRadioButton"] label:hover {
        background: rgba(234, 179, 8, 0.18) !important;
        border-color: #eab308 !important;
        color: #fef08a !important;
        box-shadow: 0 0 16px rgba(234, 179, 8, 0.45) !important;
        transform: translateY(-2px) !important;
    }

    /* Active State (Tombol Terpilih) */
    div[data-testid="stRadioButton"] label[data-checked="true"] {
        background: linear-gradient(135deg, #eab308 0%, #ca8a04 100%) !important;
        color: #0f172a !important;
        font-weight: 800 !important;
        border-color: #fef08a !important;
        box-shadow: 0 4px 20px rgba(234, 179, 8, 0.5) !important;
    }

    /* Streamlit DataFrame Custom Container */
    div[data-testid="stDataFrame"] {
        background-color: #1e293b;
        border-radius: 16px;
        border: 1px solid #334155;
        padding: 12px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.35);
    }

    /* Download Button Premium Hover */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #eab308 0%, #ca8a04 100%) !important;
        color: #0f172a !important;
        font-weight: 800 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        box-shadow: 0 4px 20px rgba(234, 179, 8, 0.35) !important;
        transition: all 0.25s ease !important;
    }

    .stDownloadButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(234, 179, 8, 0.6) !important;
        background: linear-gradient(135deg, #facc15 0%, #eab308 100%) !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 3. Data Schedule Matrix Gebrakan Emas
data = [
    # RABU
    {"Day_Code": "Rabu", "Hari & Tanggal": "Rabu, 12 Agu 2026", "Jam Upload": "13.00 WIB", "Group List / Playlist": "Ciri Wanita Ahli Surga", "Part": "Part 1/5", "Tema Postingan": "Ciri 1 - Menjaga Shalat & Kehormatan", "Hook / Cover (Slide 1)": "Untukmu wanita yang lelah, ini janji peleram gelisahmu...", "Isi Hadits (Slide 3)": "Jika wanita menjaga shalat 5 waktu, berpuasa, dan menjaga kehormatannya... (HR. Ahmad)", "Tautan Sambungan (Slide 5)": "Lanjut Part 2 jam 13.00 ini juga di playlist 🌿", "5 Hashtag Booster": "#WanitaSholehah #PenatHati #HaditsKetenangan #SelfReminder #AmalanLangit"},
    {"Day_Code": "Rabu", "Hari & Tanggal": "Rabu, 12 Agu 2026", "Jam Upload": "13.00 WIB", "Group List / Playlist": "Ciri Wanita Ahli Surga", "Part": "Part 2/5", "Tema Postingan": "Ciri 2 - Kesabaran & Kelembutan Batin", "Hook / Cover (Slide 1)": "Sifat kecil yang membuat pintu surga terbuka lebar...", "Isi Hadits (Slide 3)": "Wanita yang sabar dan penuh kasih sayang... (HR. Thabrani)", "Tautan Sambungan (Slide 5)": "Lanjut Part 3 jam 16.30 Sore ini ya 🌿", "5 Hashtag Booster": "#WanitaSholehah #PenatHati #HaditsKetenangan #SelfReminder #AmalanLangit"},
    {"Day_Code": "Rabu", "Hari & Tanggal": "Rabu, 12 Agu 2026", "Jam Upload": "16.30 WIB", "Group List / Playlist": "Ciri Wanita Ahli Surga", "Part": "Part 3/5", "Tema Postingan": "Ciri 3 - Pelipur Duka dalam Rumah", "Hook / Cover (Slide 1)": "Saat suami/keluarga lelah, dirimu jadi penenangnya...", "Isi Hadits (Slide 3)": "Maukah kuberitahu simpanan terbaik? Wanita sholehah yang menyenangkan saat dipandang... (HR. Abu Daud)", "Tautan Sambungan (Slide 5)": "Lanjut Part 4 jam 19.00 Malam ini ya 🌿", "5 Hashtag Booster": "#WanitaSholehah #PenatHati #HaditsKetenangan #SelfReminder #AmalanLangit"},
    {"Day_Code": "Rabu", "Hari & Tanggal": "Rabu, 12 Agu 2026", "Jam Upload": "19.00 WIB", "Group List / Playlist": "Ciri Wanita Ahli Surga", "Part": "Part 4/5", "Tema Postingan": "Ciri 4 - Menjaga Lisan & Prasangka", "Hook / Cover (Slide 1)": "Lisan yang teduh adalah perhiasan batin sesungguhnya...", "Isi Hadits (Slide 3)": "Jaminlah bagiku apa yang ada di antara dua tulang dagumu (lisan)... (HR. Bukhari)", "Tautan Sambungan (Slide 5)": "Lanjut Part 5 jam 20.00 Malam ini 🌿", "5 Hashtag Booster": "#WanitaSholehah #PenatHati #HaditsKetenangan #SelfReminder #AmalanLangit"},
    {"Day_Code": "Rabu", "Hari & Tanggal": "Rabu, 12 Agu 2026", "Jam Upload": "20.00 WIB", "Group List / Playlist": "Ciri Wanita Ahli Surga", "Part": "Part 5/5", "Tema Postingan": "Ciri 5 - Ridho pada Takdir Allah", "Hook / Cover (Slide 1)": "Puncak ketenangan saat batin pasrah fully...", "Isi Hadits (Slide 3)": "...Maka dikatakan padanya: Masuklah ke surga dari pintu mana saja yang kamu suka. (HR. Ahmad)", "Tautan Sambungan (Slide 5)": "Cek Playlist Ciri Wanita Ahli Surga untuk ulasan lengkapnya 🌿", "5 Hashtag Booster": "#WanitaSholehah #PenatHati #HaditsKetenangan #SelfReminder #AmalanLangit"},

    # KAMIS
    {"Day_Code": "Kamis", "Hari & Tanggal": "Kamis, 13 Agu 2026", "Jam Upload": "13.00 WIB", "Group List / Playlist": "Seri: Hati Seorang Wanita", "Part": "Part 1/5", "Tema Postingan": "Mengapa Hati Wanita Mudah Lelah?", "Hook / Cover (Slide 1)": "Untuk kamu yang hatinya sering merasa sangat lelah...", "Isi Hadits (Slide 3)": "Aku wasiatkan kepada kalian untuk berbuat baik kepada wanita... (HR. Bukhari)", "Tautan Sambungan (Slide 5)": "Lanjut Part 2 jam 13.00 ini juga di playlist 🌿", "5 Hashtag Booster": "#RuangJiwa #PenatHati #HaditsKetenangan #SelfReminder #AmalanLangit"},
    {"Day_Code": "Kamis", "Hari & Tanggal": "Kamis, 13 Agu 2026", "Jam Upload": "13.00 WIB", "Group List / Playlist": "Seri: Hati Seorang Wanita", "Part": "Part 2/5", "Tema Postingan": "Rahasia Senyum di Tengah Ujian", "Hook / Cover (Slide 1)": "Simak nomor 2... Rahasia sabar yang tak terlihat mata.", "Isi Hadits (Slide 3)": "Sungguh menakjubkan urusan seorang mukmin... jika ditimpa kesusahan ia bersabar. (HR. Muslim)", "Tautan Sambungan (Slide 5)": "Lanjut Part 3 jam 16.30 Sore ini 🌿", "5 Hashtag Booster": "#RuangJiwa #PenatHati #HaditsKetenangan #SelfReminder #AmalanLangit"},
    {"Day_Code": "Kamis", "Hari & Tanggal": "Kamis, 13 Agu 2026", "Jam Upload": "16.30 WIB", "Group List / Playlist": "Seri: Hati Seorang Wanita", "Part": "Part 3/5", "Tema Postingan": "Saat Air Mata Jadi Doa", "Hook / Cover (Slide 1)": "Bukan lemah, tapi caramu mengadu pada-Nya...", "Isi Hadits (Slide 3)": "Mana saja doa yang dipanjatkan hamba saat bersujud... (HR. Muslim)", "Tautan Sambungan (Slide 5)": "Lanjut Part 4 jam 19.00 Malam nanti 🌿", "5 Hashtag Booster": "#RuangJiwa #PenatHati #HaditsKetenangan #SelfReminder #AmalanLangit"},
    {"Day_Code": "Kamis", "Hari & Tanggal": "Kamis, 13 Agu 2026", "Jam Upload": "19.00 WIB", "Group List / Playlist": "Seri: Hati Seorang Wanita", "Part": "Part 4/5", "Tema Postingan": "Luasnya Maaf Wanita Sholehah", "Hook / Cover (Slide 1)": "Melepaskan beban dendam demi kedamaian jiwa...", "Isi Hadits (Slide 3)": "Barangsiapa memaafkan dan berbuat baik maka pahalanya atas Allah. (QS. Asy-Syura: 40)", "Tautan Sambungan (Slide 5)": "Lanjut Part 5 puncak jam 20.00 🌿", "5 Hashtag Booster": "#RuangJiwa #PenatHati #HaditsKetenangan #SelfReminder #AmalanLangit"},
    {"Day_Code": "Kamis", "Hari & Tanggal": "Kamis, 13 Agu 2026", "Jam Upload": "20.00 WIB", "Group List / Playlist": "Seri: Hati Seorang Wanita", "Part": "Part 5/5", "Tema Postingan": "Balasan Mahkota Cahaya", "Hook / Cover (Slide 1)": "Kesabaranmu hari ini adalah mahkotamu kelak...", "Isi Hadits (Slide 3)": "Pahala orang yang bersabar tanpa batas... (QS. Az-Zumar: 10)", "Tautan Sambungan (Slide 5)": "Simpan Playlist Seri: Hati Seorang Wanita ini ya 🌿", "5 Hashtag Booster": "#RuangJiwa #PenatHati #HaditsKetenangan #SelfReminder #AmalanLangit"},

    # JUMAT
    {"Day_Code": "Jumat", "Hari & Tanggal": "Jumat, 14 Agu 2026", "Jam Upload": "13.00 WIB", "Group List / Playlist": "Seri: Baiti Jannati", "Part": "Part 1/5", "Tema Postingan": "Rumah yang Dirindukan Surga", "Hook / Cover (Slide 1)": "Bukan tentang mewahnya, tapi indahnya kedamaian...", "Isi Hadits (Slide 3)": "Sebaik-baik rumah adalah yang di dalamnya ada kedamaian dan zikir... (HR. Muslim)", "Tautan Sambungan (Slide 5)": "Lanjut Part 2 jam 13.00 ini juga 🌿", "5 Hashtag Booster": "#RumahTeduh #PenatHati #HaditsKetenangan #SelfReminder #AmalanLangit"},
    {"Day_Code": "Jumat", "Hari & Tanggal": "Jumat, 14 Agu 2026", "Jam Upload": "13.00 WIB", "Group List / Playlist": "Seri: Baiti Jannati", "Part": "Part 2/5", "Tema Postingan": "Keberkahan Lisan Seorang Ibu", "Hook / Cover (Slide 1)": "Doamu adalah benteng penyelamat keluarga...", "Isi Hadits (Slide 3)": "Tiga doa yang tidak ditolak, salah satunya doa orang tua... (HR. Tirmidzi)", "Tautan Sambungan (Slide 5)": "Lanjut Part 3 jam 16.30 Sore nanti 🌿", "5 Hashtag Booster": "#RumahTeduh #PenatHati #HaditsKetenangan #SelfReminder #AmalanLangit"},
    {"Day_Code": "Jumat", "Hari & Tanggal": "Jumat, 14 Agu 2026", "Jam Upload": "16.30 WIB", "Group List / Playlist": "Seri: Baiti Jannati", "Part": "Part 3/5", "Tema Postingan": "Menjadi Pelindung dari Gelisah", "Hook / Cover (Slide 1)": "Saat pintu rumah dibuka, hilangkan semua penat...", "Isi Hadits (Slide 3)": "Dunia adalah perhiasan, dan sebaik-baik perhiasan adalah wanita sholehah. (HR. Muslim)", "Tautan Sambungan (Slide 5)": "Lanjut Part 4 jam 19.00 Malam ini 🌿", "5 Hashtag Booster": "#RumahTeduh #PenatHati #HaditsKetenangan #SelfReminder #AmalanLangit"},
    {"Day_Code": "Jumat", "Hari & Tanggal": "Jumat, 14 Agu 2026", "Jam Upload": "19.00 WIB", "Group List / Playlist": "Seri: Baiti Jannati", "Part": "Part 4/5", "Tema Postingan": "Amalan Pengikat Keharmonisan", "Hook / Cover (Slide 1)": "Trik kecil Rasulullah menjaga kehangatan rumah...", "Isi Hadits (Slide 3)": "Kalian tidak akan masuk surga sampai kalian saling mencintai... (HR. Muslim)", "Tautan Sambungan (Slide 5)": "Lanjut Part 5 jam 20.00 Puncak 🌿", "5 Hashtag Booster": "#RumahTeduh #PenatHati #HaditsKetenangan #SelfReminder #AmalanLangit"},
    {"Day_Code": "Jumat", "Hari & Tanggal": "Jumat, 14 Agu 2026", "Jam Upload": "20.00 WIB", "Group List / Playlist": "Seri: Baiti Jannati", "Part": "Part 5/5", "Tema Postingan": "Kerajaan Kecil Menuju Surga", "Hook / Cover (Slide 1)": "Semoga rumah kita menjadi kumpulannya kelak di surga...", "Isi Hadits (Slide 3)": "Bisa berkumpul bersama keluarga di surga Adn... (QS. Ar-Ra'd: 23)", "Tautan Sambungan (Slide 5)": "Cek Playlist Seri: Baiti Jannati lengkapnya di profil 🌿", "5 Hashtag Booster": "#RumahTeduh #PenatHati #HaditsKetenangan #SelfReminder #AmalanLangit"}
]

df = pd.DataFrame(data)

# 4. Header Section
st.markdown("""
<div class="header-box">
    <span class="brand-badge">🌿 Ruang Teduh - Schedule Matrix</span>
    <h1 class="header-title">Spreadsheet Gebrakan Emas (3 Hari)</h1>
    <p class="header-subtitle">Jadwal posting terstruktur Siang, Sore & Malam | 15 Konten Serial TikTok Mode Slide</p>
</div>
""", unsafe_allow_html=True)

# 5. Top KPI Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Postingan", "15 Konten")
col2.metric("Durasi Program", "3 Hari")
col3.metric("Format Postingan", "5 Slide TikTok")
col4.metric("Jumlah Playlist", "3 Group List")

st.markdown("---")

# 6. Filter & Action Row
filter_col, download_col = st.columns([3, 1])

with filter_col:
    selected_day = st.radio(
        "Filter Jadwal Hari:",
        options=["Semua Hari", "Rabu (Ciri Wanita Ahli Surga)", "Kamis (Seri: Hati Seorang Wanita)", "Jumat (Seri: Baiti Jannati)"],
        horizontal=True
    )

# Filter Logic
if "Rabu" in selected_day:
    filtered_df = df[df['Day_Code'] == 'Rabu']
elif "Kamis" in selected_day:
    filtered_df = df[df['Day_Code'] == 'Kamis']
elif "Jumat" in selected_day:
    filtered_df = df[df['Day_Code'] == 'Jumat']
else:
    filtered_df = df.copy()

# Drop Internal Helper Column
display_df = filtered_df.drop(columns=['Day_Code'])

# Download Button
csv_data = display_df.to_csv(index=False).encode('utf-8')
with download_col:
    st.download_button(
        label="📥 Download Excel (.csv)",
        data=csv_data,
        file_name="Jadwal_Gebrakan_Emas_3Hari.csv",
        mime="text/csv",
        use_container_width=True
    )

# 7. Interactive Streamlit Data Table
st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Hari & Tanggal": st.column_config.TextColumn("Hari & Tanggal", width="medium"),
        "Jam Upload": st.column_config.TextColumn("Jam Upload", width="small"),
        "Group List / Playlist": st.column_config.TextColumn("Group List / Playlist", width="medium"),
        "Part": st.column_config.TextColumn("Part", width="small"),
        "Tema Postingan": st.column_config.TextColumn("Tema Postingan", width="large"),
        "Hook / Cover (Slide 1)": st.column_config.TextColumn("Hook Cover (Slide 1)", width="large"),
        "Isi Hadits (Slide 3)": st.column_config.TextColumn("Isi Hadits (Slide 3)", width="large"),
        "Tautan Sambungan (Slide 5)": st.column_config.TextColumn("Tautan Sambungan", width="medium"),
        "5 Hashtag Booster": st.column_config.TextColumn("5 Hashtag Booster", width="large"),
    }
)

st.caption("✨ *Tips: Gunakan pencarian built-in di pojok kanan atas tabel Streamlit di atas untuk mencari keyword atau hashtag tertentu.*")
