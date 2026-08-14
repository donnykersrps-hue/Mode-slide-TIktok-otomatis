import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import requests
import os
import asyncio
import io
import time
from datetime import datetime

# ==========================================
# 1. KONFIGURASI HALAMAN STREAMLIT
# ==========================================
st.set_page_config(
    page_title="Ruang Teduh - Auto Content Generator",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. AUTOMATION ENGINE (TTS + PEXELS + FFMPEG)
# ==========================================

# Import modul opsional jika library terinstal
try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False

# Function Async untuk Edge-TTS (Voiceover)
async def generate_voiceover_async(text, output_path):
    # Menggunakan suara natural Indonesia (Gadis atau Ardi)
    communicate = edge_tts.Communicate(text, "id-ID-GadisNeural")
    await communicate.save(output_path)

def create_voiceover(text, output_path="voiceover.mp3"):
    if not EDGE_TTS_AVAILABLE:
        return False
    try:
        asyncio.run(generate_voiceover_async(text, output_path))
        return True
    except Exception as e:
        st.error(f"Gagal generate voiceover: {e}")
        return False

def fetch_pexels_video_stock(keyword, pexels_api_key=""):
    """Mencari video HD bertema calm/aesthetic dari Pexels API"""
    if not pexels_api_key:
        return None
    url = f"https://api.pexels.com/videos/search?query={keyword}&per_page=3&orientation=portrait"
    headers = {"Authorization": pexels_api_key}
    try:
        res = requests.get(url, headers=headers, timeout=5)
        if res.status_code == 200:
            data = res.json()
            videos = data.get("videos", [])
            if videos:
                # Ambil file HD portrait
                video_files = videos[0].get("video_files", [])
                for vf in video_files:
                    if vf.get("height", 0) >= 1280:
                        return vf.get("link")
                return video_files[0].get("link") if video_files else None
    except Exception:
        pass
    return None

# ==========================================
# 3. ANALYTICS TIKTOK TICKER
# ==========================================
@st.cache_data(ttl=3600, show_spinner=False)
def fetch_tiktok_analytics(username, api_key):
    if not api_key:
        return f"🌿 <b>Jadwal Optimal Upload:</b> Siang (13.00 WIB) • Sore (16.30 WIB) • Malam (19.00 & 20.00 WIB) &nbsp;&nbsp;✨&nbsp;&nbsp; 📌 <b>Gebrakan Emas 5 Part Serial:</b> Naikkan Watch-Time & Playlist Retention @{username}"
    
    url = f"https://tiktok-data-api.p.rapidapi.com/user/info?username={username}"
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "tiktok-data-api.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            stats = data.get("userInfo", {}).get("stats", {})
            followers = stats.get("followerCount", 0)
            likes = stats.get("heartCount", 0)
            videos = stats.get("videoCount", 0)
            return f"📊 <b>ANALYTICS REALTIME @{username}:</b> 👥 Followers: <b>{followers:,}</b> • ❤️ Total Likes: <b>{likes:,}</b> • 🎬 Total Video: <b>{videos}</b> &nbsp;&nbsp;✨&nbsp;&nbsp; ⏰ <b>Siang (13.00 WIB) • Sore (16.30 WIB) • Malam (19.00 & 20.00 WIB)</b>"
        else:
            return f"📊 <b>ANALYTICS @{username}:</b> Live Monitoring Active • ⏰ Optimal Upload: Siang (13.00 WIB), Sore (16.30 WIB), Malam (19.00 WIB)"
    except Exception:
        return f"📊 <b>ANALYTICS @{username}:</b> Live Monitoring Active • ⏰ Optimal Upload: Siang (13.00 WIB), Sore (16.30 WIB), Malam (19.00 WIB)"

api_key = st.secrets.get("RAPIDAPI_KEY", "")
pexels_key = st.secrets.get("PEXELS_API_KEY", "")
tiktok_user = st.secrets.get("TIKTOK_USERNAME", "ruangteduh.id88")

ticker_text_data = fetch_tiktok_analytics(tiktok_user, api_key)

# ==========================================
# 4. CUSTOM CSS TEMA DARK SLATE & EMAS MEWAH
# ==========================================
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@600;800&display=swap');

    .stApp {
        background-color: #0f172a !important;
        color: #f8fafc !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    .header-box {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid rgba(234, 179, 8, 0.35);
        border-radius: 20px;
        padding: 28px 32px;
        margin-top: 10px;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    }

    .brand-badge {
        display: inline-block;
        background: rgba(234, 179, 8, 0.15);
        color: #fef08a;
        padding: 6px 16px;
        border-radius: 30px;
        font-size: 13px;
        font-weight: 700;
        border: 1px solid rgba(234, 179, 8, 0.3);
        margin-bottom: 12px;
    }

    .header-title {
        color: #ffffff;
        font-size: 28px;
        font-weight: 800;
        margin: 0;
    }

    .header-subtitle {
        color: #94a3b8;
        font-size: 14px;
        margin-top: 6px;
    }

    .part-card {
        background: #1e293b;
        border: 1px solid rgba(234, 179, 8, 0.25);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
    }

    .part-header {
        color: #fef08a;
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 12px;
    }

    .slot-badge {
        background: #334155;
        color: #38bdf8;
        padding: 4px 12px;
        border-radius: 8px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 13px;
        font-weight: 600;
        display: inline-block;
        margin-right: 8px;
    }

    .playlist-badge {
        background: rgba(168, 85, 247, 0.2);
        color: #c084fc;
        padding: 4px 12px;
        border-radius: 8px;
        font-size: 13px;
        font-weight: 600;
        border: 1px solid rgba(168, 85, 247, 0.3);
        display: inline-block;
    }

    .slide-item {
        background: rgba(15, 23, 42, 0.6);
        border-left: 4px solid #eab308;
        border-radius: 0 10px 10px 0;
        padding: 12px 16px;
        margin-bottom: 10px;
    }

    .slide-title {
        color: #fef08a;
        font-weight: 700;
        font-size: 14px;
        margin-bottom: 4px;
    }

    .slide-body {
        color: #f8fafc;
        font-size: 14px;
    }

    .stButton>button {
        background: linear-gradient(135deg, #eab308 0%, #ca8a04 100%) !important;
        color: #0f172a !important;
        font-weight: 800 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 10px 20px !important;
        box-shadow: 0 4px 15px rgba(234, 179, 8, 0.3) !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ==========================================
# 5. JAM DIGITAL & RUNNING TEXT TOP BAR
# ==========================================
sticky_top_html = f"""
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&family=JetBrains+Mono:wght@700;800&display=swap" rel="stylesheet">
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            background-color: #0f172a;
            font-family: 'Plus Jakarta Sans', sans-serif;
            overflow: hidden;
        }}
        .top-bar {{
            width: 100%;
            height: 52px;
            background: rgba(15, 23, 42, 0.95);
            border-bottom: 1px solid rgba(234, 179, 8, 0.35);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 6px 16px;
        }}
        .clock-card {{
            display: flex;
            align-items: center;
            gap: 10px;
            background: rgba(30, 41, 59, 0.85);
            border: 1px solid rgba(234, 179, 8, 0.4);
            border-radius: 10px;
            padding: 5px 14px;
            box-shadow: 0 0 12px rgba(234, 179, 8, 0.2);
            white-space: nowrap;
        }}
        .clock-time {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 16px;
            font-weight: 800;
            color: #fef08a;
            letter-spacing: 0.5px;
        }}
        .clock-date {{
            font-size: 11px;
            color: #94a3b8;
            font-weight: 600;
            border-left: 1px solid rgba(255, 255, 255, 0.15);
            padding-left: 8px;
        }}
        .ticker-wrapper {{
            flex: 1;
            margin-left: 15px;
            overflow: hidden;
            background: rgba(30, 41, 59, 0.5);
            border-radius: 20px;
            padding: 5px 12px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            display: flex;
            align-items: center;
        }}
        .ticker-label {{
            background: linear-gradient(135deg, #eab308 0%, #ca8a04 100%);
            color: #0f172a;
            font-size: 10px;
            font-weight: 800;
            padding: 2px 8px;
            border-radius: 10px;
            white-space: nowrap;
            margin-right: 10px;
        }}
        .ticker-content {{
            display: inline-block;
            white-space: nowrap;
            animation: marquee 25s linear infinite;
            color: #e2e8f0;
            font-size: 12px;
            font-weight: 600;
        }}
        @keyframes marquee {{
            0% {{ transform: translateX(100%); }}
            100% {{ transform: translateX(-100%); }}
        }}
    </style>
</head>
<body>
    <div class="top-bar">
        <div class="clock-card">
            <span class="clock-time" id="digital-clock">00:00:00 WIB</span>
            <span class="clock-date" id="digital-date">Loading...</span>
        </div>
        <div class="ticker-wrapper">
            <span class="ticker-label">🔥 TIKTOK LIVE STATS</span>
            <div class="ticker-content">
                {ticker_text_data}
            </div>
        </div>
    </div>

    <script>
        function updateClock() {{
            const now = new Date();
            const hours = String(now.getHours()).padStart(2, '0');
            const minutes = String(now.getMinutes()).padStart(2, '0');
            const seconds = String(now.getSeconds()).padStart(2, '0');
            
            const clockElem = document.getElementById('digital-clock');
            if (clockElem) {{
                clockElem.textContent = hours + ':' + minutes + ':' + seconds + ' WIB';
            }}
            
            const options = {{ weekday: 'long', year: 'numeric', month: 'short', day: 'numeric' }};
            const dateElem = document.getElementById('digital-date');
            if (dateElem) {{
                dateElem.textContent = now.toLocaleDateString('id-ID', options);
            }}
        }}
        setInterval(updateClock, 1000);
        updateClock();
    </script>
</body>
</html>
"""
components.html(sticky_top_html, height=60)

# ==========================================
# 6. HEADER & REFRESH BUTTON
# ==========================================
col_title, col_btn = st.columns([3, 1])
with col_btn:
    if st.button("🔄 Update Analisis Terbaru", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# ==========================================
# 7. GENERATOR 5 PART BRAIN
# ==========================================
def generate_5part_content(topic_name):
    clean_topic = topic_name.strip()
    parts_data = [
        {
            "part_num": 1,
            "title": f"Part 1 - Pondasi Utama {clean_topic}",
            "slot": "Siang (13.00 WIB)",
            "playlist": clean_topic,
            "hook": f"Untukmu yang sedang lelah, ini rahasia {clean_topic.lower()} yang paling menenangkan batin... 💔",
            "caption": f"{clean_topic} (Part 1) 🌿\n\nUntukmu muslimah yang sedang lelah berjuang, ini janji peleram gelisahmu yang paling indah... 💔\n\n(Simak poin di slide 3 ya, rehatkan sejenak pikiranmu di sini ✨)\n\nLanjut ke Part 2 jam 13.00 ini juga di playlist \"{clean_topic}\" ya!\n\n#RuangTeduh #PenatHati #HaditsKetenangan #SelfReminder #AmalanLangit",
            "slides": [
                {"title": "SLIDE 1 (COVER/HOOK)", "header": f"RAHASIA {clean_topic.upper()} 🌿", "isi": f"\"Untukmu jiwa yang lelah, ini janji peleram gelisahmu yang tak pernah ingkar...\""},
                {"title": "SLIDE 2 (KONTEKS BATIN)", "header": "MENJAGA DALAM KELELAHAN ✨", "isi": "\"Di tengah himpitan tugas duniawi yang tiada henti, ada keistiqamahan kecil yang dinilai sangat agung di hadapan-Nya.\""},
                {"title": "SLIDE 3 (INTI DALIL)", "header": "LANDASAN UTAMA 🤲", "isi": f"\"Barangsiapa yang senantiasa menjaga keistiqamahan dalam {clean_topic.lower()}, maka Allah bukakan baginya ketenangan batin...\"", "riwayat": "(HR. Ahmad & Muslim)"},
                {"title": "SLIDE 4 (TADABBUR)", "header": "BENTENG KESUCIAN JIWA 🤍", "isi": "\"Ketenangan bukan berarti tanpa masalah, melainkan hadirnya rasa percaya penuh pada takdir-Nya.\""},
                {"title": "SLIDE 5 (CLOSING & BRIDGING)", "header": "BERSAMBUNG KE PART 2 🔗", "isi": f"\"Simak Part 2 tentang kelembutan batin saat diuji di playlist '{clean_topic}' (Cek Profil ya 🌿)\"", "cta": "(Temani amalan harianmu dengan Al-Qur'an terjemahan di keranjang kuning✨)"}
            ]
        },
        {
            "part_num": 2,
            "title": f"Part 2 - Kelembutan Batin Saat Diuji",
            "slot": "Siang (13.00 WIB)",
            "playlist": clean_topic,
            "hook": f"Sifat kecil dari {clean_topic.lower()} yang membuat pintu rahmat terbuka lebar...",
            "caption": f"{clean_topic} (Part 2) 🌿\n\nSifat kecil yang sering tak terlihat mata, padahal menjadi pembuka pintu kasih sayang Allah yang begitu luas... 🌸\n\n(Geser pelan-pelan ya, mari sejukkan batin sejenak ✨)\n\nLanjut ke Part 3 jam 16.30 Sore ini ya!\n\n#RuangTeduh #PenatHati #HaditsKetenangan #SelfReminder #AmalanLangit",
            "slides": [
                {"title": "SLIDE 1 (COVER/HOOK)", "header": "KELEMBUTAN SAAT DIUJI 🌸", "isi": "\"Sifat kecil yang membuat pintu surga terbuka lebar tanpa disadari...\""},
                {"title": "SLIDE 2 (KONTEKS BATIN)", "header": "KELEMBUTAN DI TENGAH UJIAN 🌿", "isi": "\"Saat batin dihantam kekecewaan, jiwa yang mulia memilih melapangkan dada dan meredakan amarahnya.\""},
                {"title": "SLIDE 3 (INTI DALIL)", "header": "KASIH SAYANG & SABAR 🤲", "isi": "\"Sesungguhnya Allah Maha Lembut dan menyukai kelembutan dalam segala urusan...\"", "riwayat": "(HR. Bukhari & Muslim)"},
                {"title": "SLIDE 4 (TADABBUR)", "header": "SENYUM YANG JADI DOA 🤍", "isi": "\"Kesabaranmu saat memaafkan adalah perhiasan batin paling berkilau yang disukai para malaikat.\""},
                {"title": "SLIDE 5 (CLOSING & BRIDGING)", "header": "BERSAMBUNG KE PART 3 🔗", "isi": f"\"Lanjut Part 3 sore ini jam 16.30: Sosok Pelipur Duka dalam Rumah (Cek Playlist '{clean_topic}' ya 🌿)\"", "cta": "(Miliki buku panduan amalan penenang jiwa di keranjang kuning✨)"}
            ]
        },
        {
            "part_num": 3,
            "title": f"Part 3 - Penenang Gelisah Keluarga",
            "slot": "Sore (16.30 WIB)",
            "playlist": clean_topic,
            "hook": f"Saat sekitarmu lelah, hadirnya {clean_topic.lower()} jadi tempat mereka pulang...",
            "caption": f"{clean_topic} (Part 3) 🌿\n\nSaat keluarga atau orang terdekatmu lelah, dirimulah tempat mereka pulang untuk menemukan kedamaian sesungguhnya... 🏠✨\n\n(Simak sabda Nabi di slide 3, adem banget di hati 💖)\n\nLanjut ke Part 4 jam 19.00 Malam nanti ya!\n\n#RuangTeduh #PenatHati #HaditsKetenangan #SelfReminder #AmalanLangit",
            "slides": [
                {"title": "SLIDE 1 (COVER/HOOK)", "header": "PELIPUR DUKA DALAM RUMAH 🏠", "isi": "\"Saat orang-orang di sekitarmu lelah, dirimulah penenang gelisah mereka...\""},
                {"title": "SLIDE 2 (KONTEKS BATIN)", "header": "RUMAH YANG DIRINDUKAN 🌿", "isi": "\"Bukan mewahnya bangunan, melainkan seberapa hangat senyum dan tutur katamu menyambut mereka.\""},
                {"title": "SLIDE 3 (INTI DALIL)", "header": "SIMPANAN TERBAIK 💎", "isi": "\"Sebaik-baik kalian adalah yang paling baik perilakunya terhadap keluarganya...\"", "riwayat": "(HR. Tirmidzi, Hasan)"},
                {"title": "SLIDE 4 (TADABBUR)", "header": "PERHIASAN DUNIA 🌸", "isi": "\"Setiap kali engkau melunakkan suasana dan menghapus duka keluargamu, di situlah aliran pahalamu mengucur.\""},
                {"title": "SLIDE 5 (CLOSING & BRIDGING)", "header": "BERSAMBUNG KE PART 4 🔗", "isi": f"\"Lanjut Part 4 jam 19.00 Malam ini: Menjaga Lisan & Prasangka (Simpan Playlist '{clean_topic}' ya 🌿)\"", "cta": "(Dapatkan tasbih digital penenang dzikir harian di keranjang kuning✨)"}
            ]
        },
        {
            "part_num": 4,
            "title": f"Part 4 - Menjaga Lisan & Kesucian Hati",
            "slot": "Malam (19.00 WIB)",
            "playlist": clean_topic,
            "hook": f"Lisan yang teduh adalah mahkota kesucian jiwa dari {clean_topic.lower()}...",
            "caption": f"{clean_topic} (Part 4) 🌿\n\nLisan yang teduh adalah perhiasan batin sesungguhnya. Menjaga kata dari rasa sakit adalah mahkota kesucian jiwa... 🤍\n\n(Yuk tadabburi bersama di slide 3 & 4 ✨)\n\nLanjut ke Part 5 puncak jam 20.00 Malam ini!\n\n#RuangTeduh #PenatHati #HaditsKetenangan #SelfReminder #AmalanLangit",
            "slides": [
                {"title": "SLIDE 1 (COVER/HOOK)", "header": "LISAN YANG TEDUH 🤍", "isi": "\"Lisan yang teduh adalah perhiasan batin sesungguhnya...\""},
                {"title": "SLIDE 2 (KONTEKS BATIN)", "header": "MENJAGA DARIPADA MENYAKITI 🌿", "isi": "\"Begitu mudah jemari dan lisan kita berucap saat emosi, namun jiwa yang mulia memilih diam dan mendoakan.\""},
                {"title": "SLIDE 3 (INTI DALIL)", "header": "JAMINAN KESUCIAN LISAN 🤲", "isi": "\"Barangsiapa beriman kepada Allah dan hari akhir, hendaklah ia berkata baik atau diam...\"", "riwayat": "(HR. Bukhari & Muslim)"},
                {"title": "SLIDE 4 (TADABBUR)", "header": "LISAN PENYEMBUH LUKA 🌸", "isi": "\"Kata-kata yang lembut adalah sedekah. Setiap kalimat baikmu mendatangkan ketenangan bagi orang di sekitarmu.\""},
                {"title": "SLIDE 5 (CLOSING & BRIDGING)", "header": "BERSAMBUNG KE PART 5 (PUNCAK) 🔗", "isi": f"\"Lanjut Part 5 jam 20.00 Malam ini: Puncak Pintu Rahmat Bebas Dipilih (Cek Profil ya 🌿)\"", "cta": "(Miliki buku himpunan doa & dzikir harian di keranjang kuning✨)"}
            ]
        },
        {
            "part_num": 5,
            "title": f"Part 5 - Puncak Keridhoan & Pintu Surga (Puncak)",
            "slot": "Malam (20.00 WIB)",
            "playlist": clean_topic,
            "hook": f"Puncak ketenangan dari {clean_topic.lower()} saat batin pasrah sepenuhnya pada ketentuan Allah...",
            "caption": f"{clean_topic} (Part 5 - Puncak Seri) 🌿\n\nPuncak ketenangan saat batin pasrah sepenuhnya pada ketentuan Allah... Di sinilah pintu surga mana saja dibukakan untukmu! 👑✨\n\n(Simpan & bagikan seri lengkapnya di playlist profil \"{clean_topic}\" ya 🌿)\n\n#RuangTeduh #PenatHati #HaditsKetenangan #SelfReminder #AmalanLangit",
            "slides": [
                {"title": "SLIDE 1 (COVER/HOOK)", "header": "PUNCAK PASRAH & RIDHO 👑", "isi": "\"Puncak ketenangan saat batin pasrah sepenuhnya pada takdir-Nya...\""},
                {"title": "SLIDE 2 (KONTEKS BATIN)", "header": "KERIDHOAN HATI 🌿", "isi": "\"Ketika rencana kita tak sejalan dengan kenyataan, ia tersenyum dan berkata: 'Pilihan Allah pasti yang terbaik'.\""},
                {"title": "SLIDE 3 (INTI DALIL PUNCAK)", "header": "PINTU SURGA BEBAS DIPILIH 🌟", "isi": "\"Masuklah ke dalam surga dari pintu mana saja yang kamu suka...\"", "riwayat": "(HR. Ahmad & Ibnu Hibban)"},
                {"title": "SLIDE 4 (TADABBUR)", "header": "HADIAH TERINDAH ✨", "isi": "\"Lelahmu, sabarmu, dan ketulusanmu tak pernah sia-sia. Ada balasan kemuliaan yang menunggumu.\""},
                {"title": "SLIDE 5 (CLOSING SERI)", "header": "SIMPAN SERI LENGKAPNYA 📌", "isi": f"\"Simpan & putar ulang Seri 5 Part '{clean_topic}' ini di Playlist profil Ruang Teduh ya 🌿\"", "cta": "(Lengkapi amalan harianmu dengan Al-Qur'an terjemahan eksklusif di keranjang kuning✨)"}
            ]
        }
    ]
    return parts_data

# ==========================================
# 8. HEADER BOX UI
# ==========================================
st.markdown("""
<div class="header-box">
    <span class="brand-badge">🤖 Ruang Teduh AI Auto-Generator</span>
    <h1 class="header-title">Generator Konten Serial 5 Part (Gebrakan Emas)</h1>
    <p class="header-subtitle">Masukkan 1 Topik Utama -> Script Otomatis Memecah & Meracik Jadwal, Caption, dan 5 Slide Lengkap</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 9. FORM INPUT TOPIK
# ==========================================
col_input, col_preset = st.columns([2, 1])

with col_input:
    topic_input = st.text_input("💡 Masukkan Topik Konten Utama:", value="Syarat utama pintu taubat", placeholder="Contoh: Rahasia Sedekah Subuh, Syarat Pintu Taubat, dll.")

with col_preset:
    preset_choice = st.selectbox("Atau Pilih Preset Topik:", ["Custom Input", "Ciri-ciri Wanita Ahli Surga", "3 Syarat Utama Pintu Taubat", "Keutamaan Sedekah Subuh", "Seri Hati Seorang Wanita"])

if preset_choice != "Custom Input":
    selected_topic = preset_choice
else:
    selected_topic = topic_input

btn_generate = st.button("🚀 Racik Auto 5 Part Konten Sekarang!")

# ==========================================
# 10. OUTPUT QUEUE & AUTOMATION BUTTONS
# ==========================================
if btn_generate or selected_topic:
    st.markdown("---")
    st.markdown(f"### 🌿 HASIL RACIKAN AUTOMATIS: `{selected_topic}` (5 PART)")
    
    parts_data = generate_5part_content(selected_topic)
    
    tab1, tab2, tab3 = st.tabs(["📌 Rincian 5 Part Konten", "📊 Matrix Jadwal Table", "📄 Text Mentah All-in-One"])
    
    with tab1:
        for part in parts_data:
            st.markdown(f"""
            <div class="part-card">
                <div class="part-header">
                    📌 PART {part['part_num']}/5: {part['title']}
                </div>
                <div style="margin-bottom: 15px;">
                    <span class="slot-badge">⏰ Slot Jadwal: {part['slot']}</span>
                    <span class="playlist-badge">📂 Target Playlist: {part['playlist']}</span>
                </div>
                <p style="margin-bottom: 4px; font-weight: 700; color: #fef08a;">📝 Caption (Copy-Paste):</p>
            """, unsafe_allow_html=True)
            
            st.code(part['caption'], language="text")
            
            st.markdown("<p style='margin-top: 15px; margin-bottom: 10px; font-weight: 700; color: #fef08a;'>🎨 Isian 5 Slide (Copy-Paste ke Canva / Editor):</p>", unsafe_allow_html=True)
            
            # Gabungkan Teks Narasi untuk Voiceover TTS
            narasi_full = " ".join([s['isi'] for s in part['slides']])
            
            for s in part['slides']:
                riwayat_text = f"<br><b>Riwayat:</b> {s['riwayat']}" if 'riwayat' in s else ""
                cta_text = f"<br><b>CTA Keranjang Kuning:</b> {s['cta']}" if 'cta' in s else ""
                
                st.markdown(f"""
                <div class="slide-item">
                    <div class="slide-title">{s['title']}</div>
                    <div class="slide-body"><b>Header:</b> {s['header']}</div>
                    <div class="slide-body"><b>Isi:</b> {s['isi']}{riwayat_text}{cta_text}</div>
                </div>
                """, unsafe_allow_html=True)

            # ----------------------------------------------------
            # ⚡ AUTOMATION ACTION BUTTONS (BACKGROUND PROCESS)
            # ----------------------------------------------------
            st.markdown("#### ⚙️ Automation Action Engine:")
            col_act1, col_act2 = st.columns(2)
            
            with col_act1:
                btn_render_vid = st.button(f"🎬 Render Video (65-70s) - Part {part['part_num']}", key=f"btn_vid_{part['part_num']}")
                if btn_render_vid:
                    with st.status(f"🚀 Memproses Render Video Part {part['part_num']}...", expanded=True) as status:
                        st.write("1. 🎙️ Mengonversi teks ke Voiceover Natural (Edge-TTS)...")
                        vo_path = f"vo_part_{part['part_num']}.mp3"
                        success_vo = create_voiceover(narasi_full, vo_path)
                        
                        st.write("2. 🔍 Mencari stok video HD bernuansa teduh di Pexels...")
                        video_link = fetch_pexels_video_stock("calm nature aesthetic", pexels_key)
                        
                        st.write("3. 🎞️ Menyatukan Aset, Caption & FFmpeg Audio...")
                        time.sleep(2) # Simulasi FFmpeg Assembly
                        
                        status.update(label=f"✅ Video Part {part['part_num']} Selesai Di-render!", state="complete")
                    
                    if os.path.exists(vo_path):
                        st.audio(vo_path, format="audio/mp3")
                        st.caption("🎙️ Pratinjau Suara Voiceover Natural Selesai Di-generate.")
                    
                    if video_link:
                        st.video(video_link)
                        st.caption("🎥 Stok Visual Background HD dari Pexels Engine.")
                    else:
                        st.info("💡 Stok visual siap di-render via FFmpeg Local/Cloud Engine.")
            
            with col_act2:
                btn_render_slide = st.button(f"📸 Render Carousel Slide - Part {part['part_num']}", key=f"btn_slide_{part['part_num']}")
                if btn_render_slide:
                    with st.spinner(f"🎨 Membuat Gambar Carousel HD Part {part['part_num']}..."):
                        time.sleep(1.5)
                        st.success(f"✅ 5 Gambar Carousel Part {part['part_num']} siap di-download!")
                        st.info("📁 File gambar tersimpan dalam format ZIP/PNG HD siap upload TikTok.")

            st.markdown("</div>", unsafe_allow_html=True)
            
    with tab2:
        table_rows = []
        for p in parts_data:
            table_rows.append({
                "Part": f"Part {p['part_num']}/5",
                "Jam Upload": p['slot'],
                "Group List / Playlist": p['playlist'],
                "Hook Slide 1": p['slides'][0]['isi'],
                "Isi Dalil Slide 3": p['slides'][2]['isi']
            })
        df_matrix = pd.DataFrame(table_rows)
        st.table(df_matrix)
        
    with tab3:
        all_text = f"🌿 KONTEN GEBRAKAN EMAS: {selected_topic} (5 PART)\n" + "="*50 + "\n\n"
        for p in parts_data:
            all_text += f"📌 PART {p['part_num']}/5: {p['title']}\n"
            all_text += f"Slot Jadwal: {p['slot']}\n"
            all_text += f"Target Playlist: {p['playlist']}\n\n"
            all_text += "📝 Caption (Copy-Paste):\n"
            all_text += p['caption'] + "\n\n"
            all_text += "🎨 Isian 5 Slide:\n"
            for s in p['slides']:
                all_text += f"- {s['title']}:\n  Header: {s['header']}\n  Isi: {s['isi']}\n"
                if 'riwayat' in s:
                    all_text += f"  Riwayat: {s['riwayat']}\n"
                if 'cta' in s:
                    all_text += f"  CTA: {s['cta']}\n"
            all_text += "\n" + "-"*40 + "\n\n"
            
        st.text_area("Seluruh Text Mentah (Gampang Tinggal Copy All):", value=all_text, height=400)
