import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json
import io
import hashlib
from datetime import datetime
import google.generativeai as genai

# ==========================================
# 1. KONFIGURASI HALAMAN & SECRETS
# ==========================================
st.set_page_config(
    page_title="Ruang Teduh - Auto Content Engine",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

GEMINI_KEY = st.secrets.get("GEMINI_API_KEY", "")
PEXELS_KEY = st.secrets.get("PEXELS_API_KEY", "")

if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)

# ==========================================
# 2. GEMINI AI BRAIN ENGINE (HIGH ENGAGEMENT & NO META-LABELING)
# ==========================================
def generate_5part_with_gemini(topic_name):
    if not GEMINI_KEY:
        st.error("❌ GEMINI_API_KEY tidak ditemukan di Streamlit Secrets.")
        return None

    prompt = f"""
    Kamu adalah seorang Manager Konten & Pakar Strategi TikTok Algoritma FYP untuk akun "Ruang Teduh" (Niche: Islami, Self-Reminder, Ketenangan Hati, Dakwah Mendidik & Emosional).
    
    Tugasmu:
    Buatkan serial naskah 5 Part berdasarkan Topik Utama: "{topic_name}".
    
    ATURAN BAKU POLA SLIDE (SANGAT WAJIB PADA SETIAP PART):
    - SLIDE 1 (COVER): Hook emosional memikat batin + Judul Serial.
    - SLIDE 2 (KONTEKS): Relevansi masalah batin/kehidupan sehari-hari.
    - SLIDE 3 (INTI DALIL - WAJIB HADITS SHAHIH): Harus memuat Teks Hadits Shahih / Ayat Al-Qur'an lengkap dengan nama Perawinya (contoh: HR. Bukhari, HR. Muslim, HR. Tirmidzi, dll).
    - SLIDE 4 (TADABBUR): Hikmah, perenungan mendalam, dan penyejuk jiwa.
    - SLIDE 5 (CLOSING & CTA HIGH ENGAGEMENT): 
      * DILARANG KERAS menggunakan kata "Slide 5", "Slide Terakhir", "Akhir Part", atau sejenisnya!
      * Header harus memikat batin (Contoh: "PENYEMAT KETENANGAN 🤍", "HARAPAN & DO'A 🌿").
      * Isi teks berupa perenungan mendalam yang menyentuh jiwa dan memancing respon batin.
      * Wajib memuat Call To Action (CTA) 4-Pilar Algoritma untuk meledakkan engagement: memancing komentar (Comment Rate), mengajak simpan agar tidak hilang (Save Rate), menekan ikuti/follow (Follow Rate), dan ajakan menyimak sambungan di "part selanjutnya" secara natural.
      * Contoh CTA Slide 5: "Tulis jawabanmu di komentar 💬, ketuk 📌 simpan agar tidak hilang, dan tekan ikuti (follow) untuk menyimak sambungan penyejuk jiwa di part selanjutnya ✨"

    Format Wajib Output: Berikan HANYA JSON MURNI tanpa format markdown ```json ... ```, dengan struktur objek array berisi 5 item seperti contoh berikut:
    [
      {{
        "part_num": 1,
        "title": "Part 1 - Judul Part Ringkas",
        "slot": "Siang (13.00 WIB)",
        "playlist": "{topic_name}",
        "caption": "Teks Caption TikTok lengkap dengan emoji, Call to Action ke playlist, dan 5 hashtag relevan.",
        "slides": [
          {{"title": "SLIDE 1 (COVER)", "header": "HEADER SINGKAT 🌿", "isi": "Teks hook memikat hati..."}},
          {{"title": "SLIDE 2 (KONTEKS)", "header": "HEADER KONTEKS ✨", "isi": "Teks penjelasan batin..."}},
          {{"title": "SLIDE 3 (DALIL SHAHIH)", "header": "LANDASAN HADITS 🤲", "isi": "Matan/Arti Hadits Shahih relevan...", "riwayat": "(HR. Bukhari / Muslim / Tirmidzi)"}},
          {{"title": "SLIDE 4 (TADABBUR)", "header": "HEADER TADABBUR 🤍", "isi": "Teks hikmah mendalam..."}},
          {{"title": "SLIDE 5 (CLOSING & CTA)", "header": "PENYEMAT KETENANGAN 🤍", "isi": "Teks perenungan batin...", "cta": "Tulis jawabanmu di komentar 💬, ketuk 📌 simpan agar tidak hilang, dan tekan ikuti (follow) untuk menyimak sambungan penyejuk jiwa di part selanjutnya ✨"}}
        ]
      }}
    ]
    """

    try:
        model = genai.GenerativeModel("gemini-3.6-flash")
        response = model.generate_content(prompt)
        
        clean_text = response.text.strip()
        if clean_text.startswith("```json"):
            clean_text = clean_text.replace("```json", "", 1)
        if clean_text.endswith("```"):
            clean_text = clean_text[:-3]
        clean_text = clean_text.strip()

        data = json.loads(clean_text)
        return data
    except Exception as e:
        st.error(f"⚠️ Gagal menghubungi Manager AI (Gemini): {e}")
        return None

# ==========================================
# 3. CUSTOM CSS
# ==========================================
custom_css = """
<style>
    @import url('[https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@600;800&display=swap](https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@600;800&display=swap)');

    .stApp {
        background-color: #0f172a !important;
        color: #f8fafc !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    .header-box {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid rgba(234, 179, 8, 0.35);
        border-radius: 20px;
        padding: 24px 30px;
        margin-top: 10px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    }

    .brand-badge {
        display: inline-block;
        background: rgba(234, 179, 8, 0.15);
        color: #fef08a;
        padding: 4px 14px;
        border-radius: 30px;
        font-size: 12px;
        font-weight: 700;
        border: 1px solid rgba(234, 179, 8, 0.3);
        margin-bottom: 8px;
    }

    .header-title {
        color: #ffffff;
        font-size: 26px;
        font-weight: 800;
        margin: 0;
    }

    .header-subtitle {
        color: #94a3b8;
        font-size: 13px;
        margin-top: 4px;
    }

    .part-card-compact {
        background: #1e293b;
        border: 1px solid rgba(234, 179, 8, 0.3);
        border-radius: 16px;
        padding: 18px 24px;
        margin-bottom: 12px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
    }

    .part-header {
        color: #fef08a;
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .slot-badge {
        background: #334155;
        color: #38bdf8;
        padding: 4px 12px;
        border-radius: 8px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 12px;
        font-weight: 600;
        display: inline-block;
        margin-right: 8px;
    }

    .playlist-badge {
        background: rgba(168, 85, 247, 0.2);
        color: #c084fc;
        padding: 4px 12px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 600;
        border: 1px solid rgba(168, 85, 247, 0.3);
        display: inline-block;
    }

    div[data-testid="stExpander"] {
        border: 1px solid rgba(236, 72, 153, 0.6) !important;
        border-radius: 14px !important;
        background: rgba(30, 41, 59, 0.85) !important;
        box-shadow: 0 0 18px rgba(236, 72, 153, 0.3) !important;
    }

    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #1e293b !important;
        color: #fef08a !important;
        border: 2px solid #ec4899 !important;
        border-radius: 12px !important;
        box-shadow: 0 0 15px rgba(236, 72, 153, 0.5), inset 0 0 10px rgba(236, 72, 153, 0.2) !important;
        font-weight: 700 !important;
        transition: all 0.3s ease-in-out !important;
    }

    .stSelectbox div[data-baseweb="select"]:hover > div {
        border-color: #00f0ff !important;
        box-shadow: 0 0 22px #00f0ff, inset 0 0 12px #00f0ff !important;
    }

    .stTextArea textarea, .stTextInput input, .stNumberInput input, div[data-baseweb="input"] input, div[data-baseweb="textarea"] textarea {
        background-color: #1e293b !important;
        color: #fef08a !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        border: 1px solid rgba(34, 211, 238, 0.4) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    div[data-baseweb="base-input"], div[data-baseweb="input"], div[data-baseweb="textarea"] {
        background-color: #1e293b !important;
        border: 1px solid rgba(34, 211, 238, 0.4) !important;
        border-radius: 10px !important;
    }

    .stButton>button, .stDownloadButton>button {
        background: linear-gradient(135deg, #eab308 0%, #ca8a04 100%) !important;
        color: #0f172a !important;
        font-weight: 800 !important;
        border: 1px solid #fef08a !important;
        border-radius: 12px !important;
        padding: 10px 18px !important;
        box-shadow: 0 4px 15px rgba(234, 179, 8, 0.3) !important;
        transition: all 0.25s ease-in-out !important;
    }

    .stButton>button:hover, .stDownloadButton>button:hover {
        background: linear-gradient(135deg, #00f0ff 0%, #0284c7 100%) !important;
        color: #ffffff !important;
        border-color: #00f0ff !important;
        box-shadow: 0 0 25px #00f0ff, 0 0 10px rgba(0, 240, 255, 0.8) !important;
        transform: translateY(-2px) !important;
    }

    .btn-apply button {
        background: linear-gradient(135deg, #00f0ff 0%, #0284c7 100%) !important;
        color: #ffffff !important;
        border-color: #38bdf8 !important;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.4) !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ==========================================
# 4. STICKY FLOATING BULAN SABIT BERPIJAR & MINI SPOTIFY AUDIO ENGINE
# ==========================================
audio_floating_html = """
<!DOCTYPE html>
<html>
<head>
    <link href="[https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&family=JetBrains+Mono:wght@700&display=swap](https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&family=JetBrains+Mono:wght@700&display=swap)" rel="stylesheet">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background: transparent; font-family: 'Plus Jakarta Sans', sans-serif; overflow: visible; }
        
        /* STICKY FLOATING CONTAINER */
        .moon-player-container {
            position: fixed; top: 12px; right: 20px; z-index: 999999;
            display: flex; flex-direction: column; align-items: flex-end;
        }

        /* BULAN SABIT BERPIJAR BUTTON */
        .moon-btn {
            width: 52px; height: 52px; border-radius: 50%;
            background: #0f172a; border: 2px solid #fef08a;
            display: flex; justify-content: center; align-items: center;
            cursor: pointer; transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative; box-shadow: 0 0 10px rgba(254, 240, 138, 0.2);
        }

        .moon-icon {
            font-size: 26px; line-height: 1; transition: all 0.4s ease;
            filter: drop-shadow(0 0 2px rgba(254, 240, 138, 0.5));
        }

        /* MODE ON: CAHAYA BERPIJAR TERANG MNERANGI SEKITAR */
        .moon-btn.active {
            background: radial-gradient(circle, #fef08a 0%, #ca8a04 100%);
            border-color: #ffffff;
            box-shadow: 0 0 25px #fef08a, 0 0 50px rgba(254, 240, 138, 0.8), 0 0 80px rgba(234, 179, 8, 0.6);
            transform: scale(1.08) rotate(-10deg);
        }

        .moon-btn.active .moon-icon {
            color: #0f172a; transform: scale(1.1);
            filter: drop-shadow(0 0 8px #ffffff);
        }

        /* MODE OFF: REDUP HALUS */
        .moon-btn.off {
            opacity: 0.65; border-color: #64748b;
            box-shadow: 0 0 5px rgba(0,0,0,0.5);
        }

        /* MINI SPOTIFY-STYLE CONTROLLER DRAWER */
        .spotify-card {
            position: absolute; top: 62px; right: 0; width: 310px;
            background: rgba(15, 23, 42, 0.94); backdrop-filter: blur(16px);
            border: 1px solid rgba(254, 240, 138, 0.4); border-radius: 18px;
            padding: 16px; box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6), 0 0 25px rgba(234, 179, 8, 0.2);
            display: none; flex-direction: column; gap: 12px; transition: all 0.3s ease;
        }

        .spotify-card.show { display: flex; animation: fadeInSlide 0.35s ease forwards; }

        @keyframes fadeInSlide {
            from { opacity: 0; transform: translateY(-10px) scale(0.95); }
            to { opacity: 1; transform: translateY(0) scale(1); }
        }

        .song-title { color: #fef08a; font-size: 13px; font-weight: 800; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .song-artist { color: #94a3b8; font-size: 11px; font-weight: 600; margin-top: 2px; }

        .player-controls { display: flex; align-items: center; justify-content: center; gap: 16px; margin-top: 4px; }
        .control-btn { background: none; border: none; color: #fef08a; font-size: 18px; cursor: pointer; transition: transform 0.2s; }
        .control-btn:hover { transform: scale(1.2); color: #00f0ff; }
        .play-main-btn {
            width: 38px; height: 38px; border-radius: 50%; background: linear-gradient(135deg, #eab308 0%, #ca8a04 100%);
            color: #0f172a; display: flex; justify-content: center; align-items: center; font-size: 16px; font-weight: 800; cursor: pointer;
            box-shadow: 0 0 12px rgba(234, 179, 8, 0.5); transition: all 0.2s ease;
        }
        .play-main-btn:hover { transform: scale(1.1); box-shadow: 0 0 20px #00f0ff; }

        .progress-bar-bg { width: 100%; height: 4px; background: rgba(255,255,255,0.15); border-radius: 4px; overflow: hidden; cursor: pointer; }
        .progress-fill { width: 30%; height: 100%; background: #00f0ff; border-radius: 4px; transition: width 0.2s linear; }
    </style>
</head>
<body>
    <div class="moon-player-container">
        <!-- TOMBOL BULAN SABIT STICKY -->
        <div class="moon-btn off" id="moon-toggle" onclick="togglePlayState()" title="Klik untuk Memutar Audio Suasana Ruang Teduh">
            <span class="moon-icon">🌙</span>
        </div>

        <!-- SPOTIFY MINI DRAWER -->
        <div class="spotify-card" id="spotify-drawer">
            <div>
                <div class="song-title" id="song-name">Dengan Nafas-Mu</div>
                <div class="song-artist" id="artist-name">Ungu - Indonesian Islamic Band Session</div>
            </div>

            <div class="progress-bar-bg" id="progress-container" onclick="seekAudio(event)">
                <div class="progress-fill" id="progress-bar"></div>
            </div>

            <div class="player-controls">
                <button class="control-btn" onclick="prevTrack()">⏮</button>
                <div class="play-main-btn" id="play-btn-icon" onclick="togglePlayState()">▶</div>
                <button class="control-btn" onclick="nextTrack()">⏭</button>
            </div>
        </div>
    </div>

    <audio id="bg-audio" loop>
        <source src="[https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=islamic-background-112677.mp3](https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=islamic-background-112677.mp3)" type="audio/mpeg">
    </audio>

    <script>
        const playlist = [
            { title: "Dengan Nafas-Mu", artist: "Ungu - Special Ruang Teduh", src: "[https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=islamic-background-112677.mp3](https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=islamic-background-112677.mp3)" },
            { title: "Cenhar Hati Penyejuk Batin", artist: "Letto / Acoustic Session", src: "[https://cdn.pixabay.com/download/audio/2022/03/15/audio_c8c8a70f3b.mp3?filename=meditation-islamic-10499.mp3](https://cdn.pixabay.com/download/audio/2022/03/15/audio_c8c8a70f3b.mp3?filename=meditation-islamic-10499.mp3)" },
            { title: "Tuhan", artist: "Gigi - Instrument Penyejuk Jiwa", src: "[https://cdn.pixabay.com/download/audio/2022/01/18/audio_d0a13f69d2.mp3?filename=spiritual-breath-15634.mp3](https://cdn.pixabay.com/download/audio/2022/01/18/audio_d0a13f69d2.mp3?filename=spiritual-breath-15634.mp3)" }
        ];

        let currentIdx = 0;
        const audio = document.getElementById("bg-audio");
        const moonBtn = document.getElementById("moon-toggle");
        const drawer = document.getElementById("spotify-drawer");
        const playBtnIcon = document.getElementById("play-btn-icon");
        const songName = document.getElementById("song-name");
        const artistName = document.getElementById("artist-name");
        const progressBar = document.getElementById("progress-bar");

        moonBtn.addEventListener("mouseenter", () => drawer.classList.add("show"));
        document.addEventListener("click", (e) => {
            if (!document.querySelector(".moon-player-container").contains(e.target)) {
                drawer.classList.remove("show");
            }
        });

        function loadTrack(idx) {
            currentIdx = idx;
            audio.src = playlist[currentIdx].src;
            songName.textContent = playlist[currentIdx].title;
            artistName.textContent = playlist[currentIdx].artist;
        }

        function togglePlayState() {
            if (audio.paused) {
                audio.play();
                moonBtn.classList.remove("off");
                moonBtn.classList.add("active");
                playBtnIcon.textContent = "❚❚";
            } else {
                audio.pause();
                moonBtn.classList.remove("active");
                moonBtn.classList.add("off");
                playBtnIcon.textContent = "▶";
            }
        }

        function nextTrack() {
            currentIdx = (currentIdx + 1) % playlist.length;
            loadTrack(currentIdx);
            audio.play();
            moonBtn.classList.add("active");
            playBtnIcon.textContent = "❚❚";
        }

        function prevTrack() {
            currentIdx = (currentIdx - 1 + playlist.length) % playlist.length;
            loadTrack(currentIdx);
            audio.play();
            moonBtn.classList.add("active");
            playBtnIcon.textContent = "❚❚";
        }

        audio.addEventListener("timeupdate", () => {
            if (audio.duration) {
                const pct = (audio.currentTime / audio.duration) * 100;
                progressBar.style.width = pct + "%";
            }
        });

        function seekAudio(e) {
            const rect = document.getElementById("progress-container").getBoundingClientRect();
            const pos = (e.clientX - rect.left) / rect.width;
            audio.currentTime = pos * audio.duration;
        }
    </script>
</body>
</html>
"""
components.html(audio_floating_html, height=70)

# ==========================================
# 5. TOP BAR JAM REALTIME
# ==========================================
top_bar_html = """
<!DOCTYPE html>
<html>
<head>
    <link href="[https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700&family=JetBrains+Mono:wght@700&display=swap](https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700&family=JetBrains+Mono:wght@700&display=swap)" rel="stylesheet">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background-color: #0f172a; font-family: 'Plus Jakarta Sans', sans-serif; }
        .top-bar {
            width: 100%; height: 46px; background: rgba(15, 23, 42, 0.95);
            border-bottom: 1px solid rgba(234, 179, 8, 0.35);
            display: flex; align-items: center; justify-content: space-between; padding: 0 16px;
        }
        .clock-card {
            display: flex; align-items: center; gap: 8px; background: rgba(30, 41, 59, 0.85);
            border: 1px solid rgba(234, 179, 8, 0.3); border-radius: 8px; padding: 4px 12px;
        }
        .clock-time { font-family: 'JetBrains Mono', monospace; font-size: 14px; font-weight: 700; color: #fef08a; }
        .clock-date { font-size: 11px; color: #94a3b8; border-left: 1px solid rgba(255, 255, 255, 0.15); padding-left: 8px; }
        .status-badge {
            background: rgba(34, 197, 94, 0.15); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.3);
            font-size: 11px; font-weight: 700; padding: 4px 12px; border-radius: 20px;
        }
    </style>
</head>
<body>
    <div class="top-bar">
        <div class="clock-card">
            <span class="clock-time" id="digital-clock">00:00:00 WIB</span>
            <span class="clock-date" id="digital-date">Loading...</span>
        </div>
        <div class="status-badge">⚡ SUPER CREATOR: ACTIVE</div>
    </div>
    <script>
        function updateClock() {
            const now = new Date();
            const hours = String(now.getHours()).padStart(2, '0');
            const minutes = String(now.getMinutes()).padStart(2, '0');
            const seconds = String(now.getSeconds()).padStart(2, '0');
            document.getElementById('digital-clock').textContent = hours + ':' + minutes + ':' + seconds + ' WIB';
            const options = { weekday: 'long', year: 'numeric', month: 'short', day: 'numeric' };
            document.getElementById('digital-date').textContent = now.toLocaleDateString('id-ID', options);
        }
        setInterval(updateClock, 1000); updateClock();
    </script>
</body>
</html>
"""
components.html(top_bar_html, height=50)

# ==========================================
# 6. HEADER & INPUT CONTROL
# ==========================================
st.markdown("""
<div class="header-box">
    <span class="brand-badge">🤖 Ruang Teduh AI Control Center</span>
    <h1 class="header-title">Dashboard Generator & Automation 5 Part</h1>
    <p class="header-subtitle">Gemini AI Manager meracik naskah 5 Part → Direct Interactive Canvas Studio → Render Carousel HD</p>
</div>
""", unsafe_allow_html=True)

topic_input = st.text_input("💡 Masukkan Topik Konten Utama:", value="Rahasia keajaiban doa seorang istri", placeholder="Contoh: Rahasia Sedekah Subuh, Syarat Pintu Taubat, dll.")
btn_generate = st.button("🚀 Racik Content Queue 5 Part (via Gemini AI)")

if "parts_data" not in st.session_state:
    st.session_state["parts_data"] = None
if "carousel_previews" not in st.session_state:
    st.session_state["carousel_previews"] = {}
if "rendered_slide_cache" not in st.session_state:
    st.session_state["rendered_slide_cache"] = {}
if "topic_hash" not in st.session_state:
    st.session_state["topic_hash"] = "default"

if btn_generate:
    with st.spinner("👤 Manager AI (Gemini) sedang meracik naskah & jadwal 5 Part..."):
        ai_result = generate_5part_with_gemini(topic_input)
        if ai_result:
            new_hash = hashlib.md5(f"{topic_input}_{datetime.now().timestamp()}".encode()).hexdigest()[:8]
            st.session_state["topic_hash"] = new_hash
            
            keys_to_clear = [k for k in st.session_state.keys() if k.startswith(("cap_", "h_", "b_", "r_"))]
            for k in keys_to_clear:
                del st.session_state[k]

            st.session_state["parts_data"] = ai_result
            st.session_state["active_topic"] = topic_input
            st.session_state["carousel_previews"] = {}
            st.session_state["rendered_slide_cache"] = {}
            st.success("✅ Manager AI Berhasil Meracik 5 Part Content Queue!")

# ==========================================
# 7. COMPACT CANVAS ENGINE
# ==========================================
def render_compact_interactive_canvas(header_text, body_text, riwayat_text="", header_size=76, body_size=68, fr_size=44, pos_h=380, pos_b=880):
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link href="[https://fonts.googleapis.com/css2?family=Montserrat:wght@800;900&display=swap](https://fonts.googleapis.com/css2?family=Montserrat:wght@800;900&display=swap)" rel="stylesheet">
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; user-select: none; }}
            body {{ background: #0f172a; display: flex; justify-content: center; align-items: center; padding: 6px; font-family: 'Montserrat', sans-serif; }}
            
            .canvas-container {{
                position: relative; width: 240px; height: 426px;
                background: linear-gradient(135deg, rgba(30, 41, 59, 0.4) 0%, rgba(15, 23, 42, 0.6) 100%),
                            radial-gradient(circle at 50% 30%, #f59e0b 0%, #d97706 40%, #0f172a 100%);
                background-size: cover; background-position: center;
                border-radius: 14px; border: 2px solid #00f0ff;
                box-shadow: 0 0 20px rgba(0, 240, 255, 0.45); overflow: hidden;
            }}

            .draggable-text {{
                position: absolute; width: 92%; left: 4%; text-align: center;
                cursor: move; padding: 4px; border: 1px dashed transparent;
                transition: border 0.2s ease, font-size 0.2s ease; word-wrap: break-word; outline: none;
            }}

            .draggable-text:hover {{ border: 1px dashed #00f0ff; background: rgba(0, 240, 255, 0.12); }}
            .draggable-text:focus {{ border: 1px solid #e879f9; background: rgba(15, 23, 42, 0.75); cursor: text; }}

            .text-header {{
                color: #e879f9; font-size: {int(header_size * 0.23)}px; font-weight: 900;
                text-shadow: 0 0 8px #000, 1px 1px 0 #000, -1px -1px 0 #000;
                top: {int(pos_h * 0.22)}px;
            }}

            .text-body {{
                color: #22d3ee; font-size: {int(body_size * 0.23)}px; font-weight: 800;
                text-shadow: 0 0 8px #000, 1px 1px 0 #000, -1px -1px 0 #000;
                top: {int(pos_b * 0.22)}px;
            }}

            .text-riwayat {{
                color: #fef08a; font-size: {int(fr_size * 0.24)}px; font-weight: 700;
                text-shadow: 0 0 6px #000, 1px 1px 0 #000; top: 340px;
            }}

            .hint-tag {{
                position: absolute; top: 8px; left: 8px; background: rgba(15, 23, 42, 0.85);
                color: #00f0ff; font-size: 9px; font-weight: 700; padding: 3px 8px; border-radius: 15px;
                border: 1px solid #00f0ff; pointer-events: none; z-index: 10;
            }}
        </style>
    </head>
    <body>
        <div class="canvas-container">
            <div class="hint-tag">⚡ Double-Click Edit / Drag Teks Presisi</div>
            
            <div class="draggable-text text-header" id="drag-header" contenteditable="true" spellcheck="false">
                {header_text}
            </div>

            <div class="draggable-text text-body" id="drag-body" contenteditable="true" spellcheck="false">
                {body_text}
            </div>

            {"<div class='draggable-text text-riwayat' id='drag-riwayat' contenteditable='true' spellcheck='false'>Riwayat<br>" + riwayat_text + "</div>" if riwayat_text else ""}
        </div>

        <script>
            function setupInteractiveText(elmnt) {{
                if (!elmnt) return;
                var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
                var isEditing = false;

                elmnt.ondblclick = function() {{
                    isEditing = true;
                    elmnt.focus();
                }};

                elmnt.onblur = function() {{
                    isEditing = false;
                }};

                elmnt.onmousedown = function(e) {{
                    if (isEditing || document.activeElement === elmnt) return;
                    e = e || window.event; e.preventDefault();
                    pos3 = e.clientX; pos4 = e.clientY;
                    document.onmouseup = closeDragElement;
                    document.onmousemove = elementDrag;
                }};

                function elementDrag(e) {{
                    e = e || window.event; e.preventDefault();
                    pos1 = pos3 - e.clientX; pos2 = pos4 - e.clientY;
                    pos3 = e.clientX; pos4 = e.clientY;
                    elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
                    elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
                }}

                function closeDragElement() {{
                    document.onmouseup = null; document.onmousemove = null;
                }}
            }}

            setupInteractiveText(document.getElementById("drag-header"));
            setupInteractiveText(document.getElementById("drag-body"));
            setupInteractiveText(document.getElementById("drag-riwayat"));
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=450)

# ==========================================
# 8. MAIN CONTENT QUEUE ENGINE
# ==========================================
if st.session_state.get("parts_data"):
    parts_data = st.session_state["parts_data"]
    active_topic = st.session_state.get("active_topic", topic_input)
    t_hash = st.session_state.get("topic_hash", "default")

    st.markdown("---")
    st.markdown(f"### 🌿 CONTENT QUEUE TERATUR: `{active_topic}`")
    
    for idx_part, part in enumerate(parts_data):
        p_num = part['part_num']
        st.markdown(f"""
        <div class="part-card-compact">
            <div class="part-header">📌 PART {p_num}/5: {part['title']}</div>
            <div style="margin-bottom: 8px;">
                <span class="slot-badge">⏰ Slot: {part['slot']}</span>
                <span class="playlist-badge">📂 Playlist: {part['playlist']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander(f"🛠️ Studio Editor Direct Canvas (Part {p_num})", expanded=True):
            st.markdown("**📝 Caption TikTok:**")
            part['caption'] = st.text_area(f"Edit Caption Part {p_num}", value=part['caption'], key=f"cap_{p_num}_{t_hash}", height=90)
            
            st.markdown("---")
            st.markdown("### 🎛️ Selectbox Editor Naskah & Direct Canvas Studio")
            
            selected_edit_idx = st.selectbox(
                f"Pilih Slide yang Ingin Disunting (Part {p_num}):",
                options=[0, 1, 2, 3, 4],
                format_func=lambda x: f"Slide {x+1} - {part['slides'][x].get('header', 'Slide ' + str(x+1))}",
                key=f"edit_slide_select_{p_num}_{t_hash}"
            )
            
            s = part['slides'][selected_edit_idx]
            s_idx = selected_edit_idx
            cache_key = f"{p_num}_{s_idx}_{t_hash}"
            
            st.markdown(f"#### 📌 Menyesuaikan {s['title']}")
            
            # FORM NASKAH TEKS
            s['header'] = st.text_input(f"Header S{s_idx+1}", value=s.get('header', ''), key=f"h_{p_num}_{s_idx}_{t_hash}")
            s['isi'] = st.text_area(f"Isi S{s_idx+1}", value=s.get('isi', ''), key=f"b_{p_num}_{s_idx}_{t_hash}", height=85)
            
            if 'riwayat' in s or s_idx == 2:
                s['riwayat'] = st.text_input(f"Riwayat Hadits S{s_idx+1}", value=s.get('riwayat', ''), key=f"r_{p_num}_{s_idx}_{t_hash}")

            # CONTROL FONT SIZE & COORDINATE POSITIONING
            st.markdown("##### 📏 Ukuran Font & Presisi Posisi Y-Offset")
            c_f1, c_f2 = st.columns(2)
            with c_f1:
                fh = st.number_input(f"Size Header S{s_idx+1}", min_value=30, max_value=120, value=s.get('font_setting', {}).get('header', 76), step=2, key=f"fh_{p_num}_{s_idx}_{t_hash}")
                pos_h = st.number_input(f"Posisi Y Header S{s_idx+1}", min_value=100, max_value=1200, value=s.get('font_setting', {}).get('y_header', 360 if s_idx==2 else 380), step=10, key=f"yh_{p_num}_{s_idx}_{t_hash}")
            with c_f2:
                fb = st.number_input(f"Size Body S{s_idx+1}", min_value=25, max_value=100, value=s.get('font_setting', {}).get('body', 68 if s_idx != 2 else 52), step=2, key=f"fb_{p_num}_{s_idx}_{t_hash}")
                pos_b = st.number_input(f"Posisi Y Body S{s_idx+1}", min_value=200, max_value=1600, value=s.get('font_setting', {}).get('y_body', 760 if s_idx==2 else 880), step=10, key=f"yb_{p_num}_{s_idx}_{t_hash}")
            
            fr = 44
            if s_idx == 2:
                fr = st.number_input(f"Size Riwayat S{s_idx+1}", min_value=20, max_value=80, value=s.get('font_setting', {}).get('riwayat', 44), step=2, key=f"fr_{p_num}_{s_idx}_{t_hash}")

            # OVERRIDE S['FONT_SETTING'] DENGAN INPUT EDITING TERBARU
            s['font_setting'] = {
                "header": fh,
                "body": fb,
                "riwayat": fr,
                "y_header": pos_h,
                "y_body": pos_b
            }

            # AUTO RENDER PILLOW ENGINE SEBELUM DITAMPILKAN
            if cache_key not in st.session_state["rendered_slide_cache"]:
                try:
                    from render_engine import render_single_slide_image, fetch_bright_aesthetic_background
                    preview_bg = fetch_bright_aesthetic_background(pexels_key=PEXELS_KEY)
                    rendered_img = render_single_slide_image(
                        preview_bg, s, 
                        is_slide_3=(s_idx==2), 
                        is_slide_5=(s_idx==4)
                    )
                    img_byte_arr = io.BytesIO()
                    rendered_img.save(img_byte_arr, format='JPEG', quality=98)
                    st.session_state["rendered_slide_cache"][cache_key] = {
                        "img": rendered_img,
                        "bytes": img_byte_arr.getvalue()
                    }
                except Exception as e_ren:
                    st.error(f"⚠️ Gagal merender visual: {e_ren}")

            # LAYOUT 2 KOLOM BERDAMPINGAN
            col_canvas, col_render = st.columns(2)

            with col_canvas:
                st.markdown("##### 🎨 Interactive Canvas Editor")
                render_compact_interactive_canvas(
                    header_text=s.get('header', ''),
                    body_text=s.get('isi', ''),
                    riwayat_text=s.get('riwayat', '') if selected_edit_idx==2 else "",
                    header_size=fh,
                    body_size=fb,
                    fr_size=fr,
                    pos_h=pos_h,
                    pos_b=pos_b
                )

                st.markdown('<div class="btn-apply">', unsafe_allow_html=True)
                btn_apply = st.button(f"⚡ Apply Changes & Render Visual (Slide {s_idx+1})", key=f"btn_apply_{p_num}_{s_idx}_{t_hash}", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

                if btn_apply:
                    try:
                        from render_engine import render_single_slide_image, fetch_bright_aesthetic_background
                        preview_bg = fetch_bright_aesthetic_background(pexels_key=PEXELS_KEY)
                        rendered_img = render_single_slide_image(
                            preview_bg, s, 
                            is_slide_3=(s_idx==2), 
                            is_slide_5=(s_idx==4)
                        )
                        img_byte_arr = io.BytesIO()
                        rendered_img.save(img_byte_arr, format='JPEG', quality=98)
                        st.session_state["rendered_slide_cache"][cache_key] = {
                            "img": rendered_img,
                            "bytes": img_byte_arr.getvalue()
                        }
                    except Exception as e_ren:
                        st.error(f"⚠️ Gagal merender visual: {e_ren}")

            with col_render:
                st.markdown("##### 📱 Direct JPG Render Preview")
                if cache_key in st.session_state["rendered_slide_cache"]:
                    st.image(
                        st.session_state["rendered_slide_cache"][cache_key]["img"],
                        caption=f"Hasil Gambar JPG Slide {s_idx+1} (100% Identik)",
                        width=250
                    )

                    st.download_button(
                        label=f"💾 Download Gambar Slide {s_idx+1} (.jpg)",
                        data=st.session_state["rendered_slide_cache"][cache_key]["bytes"],
                        file_name=f"RuangTeduh_Part{p_num}_Slide{s_idx+1}.jpg",
                        mime="image/jpeg",
                        key=f"dl_single_{p_num}_{s_idx}_{t_hash}",
                        use_container_width=True
                    )

        # AREA TOMBOL RENDER MASAL FULL PACK 5 SLIDE
        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
        c_v, c_s = st.columns(2)
        with c_v:
            st.button(f"🎬 Render Video Part {p_num}", key=f"btn_vid_{p_num}_{t_hash}", use_container_width=True)
        with c_s:
            if st.button(f"📸 Render Full Carousel (ZIP 5 Slide) Part {p_num}", key=f"btn_slide_{p_num}_{t_hash}", use_container_width=True):
                try:
                    from render_engine import generate_carousel_pack
                    
                    with st.spinner(f"🎨 Merender 5 Gambar Carousel HD Sinkron Part {p_num}..."):
                        images, zip_data = generate_carousel_pack(
                            part.get('slides', []), 
                            pexels_key=PEXELS_KEY
                        )
                        st.session_state["carousel_previews"][p_num] = {
                            "images": images,
                            "zip": zip_data
                        }
                    st.success(f"✅ Render Carousel Part {p_num} Selesai & Ter-Sinkronisasi Perfect!")
                except Exception as e:
                    st.error(f"⚠️ Gagal merender carousel: {e}")

        # GALERI & TOMBOL DOWNLOAD ZIP SINKRON
        if p_num in st.session_state.get("carousel_previews", {}):
            preview_info = st.session_state["carousel_previews"][p_num]
            st.markdown(f"#### 🎨 Galeri Lengkap Hasil Render Part {p_num}:")
            
            c1, c2, c3, c4, c5 = st.columns(5)
            cols = [c1, c2, c3, c4, c5]
            
            for idx, img in enumerate(preview_info["images"]):
                with cols[idx]:
                    st.image(img, caption=f"Slide {idx+1}", use_container_width=True)
            
            st.download_button(
                label=f"💾 Download 5 Slide HD (ZIP) Ter-Sync Edit - Part {p_num}",
                data=preview_info["zip"],
                file_name=f"RuangTeduh_Part_{p_num}_{datetime.now().strftime('%Y%m%d')}.zip",
                mime="application/zip",
                key=f"dl_zip_sync_{p_num}_{t_hash}",
                use_container_width=True
            )

        st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)
