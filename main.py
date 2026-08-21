import streamlit as st
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
# 2. GEMINI AI BRAIN ENGINE (UPDATED: PART_LABEL & HIGH ENGAGEMENT)
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
    - SLIDE 1 (COVER): 
      * Harus menyertakan "part_label" (contoh: "PART - 1", "PART - 2", dst).
      * Header berupa Judul Konteks Spesifik yang berbeda di setiap part (contoh: "ALLAH BERSAMA ORANG SABAR", "RAHASIA DOA TERTUNDA").
      * Isi teks berupa pertanyaan/pernyataan pemicu rasa penasaran (Hook).
    - SLIDE 2 (KONTEKS): Relevansi masalah batin/kehidupan sehari-hari dengan jembatan logika yang mulus dari Slide 1.
    - SLIDE 3 (INTI DALIL - WAJIB HADITS SHAHIH): Memuat Teks Hadits Shahih / Ayat Al-Qur'an lengkap dengan perawinya (contoh: HR. Bukhari, HR. Muslim, HR. Tirmidzi).
    - SLIDE 4 (TADABBUR): Hikmah, perenungan mendalam, dan penyejuk jiwa.
    - SLIDE 5 (CLOSING & CTA HIGH ENGAGEMENT): 
      * DILARANG KERAS menggunakan kata "Slide 5", "Slide Terakhir", "Akhir Part", atau sejenisnya!
      * Header harus memikat batin (Contoh: "PENYEMAT KETENANGAN 🤍").
      * Wajib memuat Call To Action (CTA) 4-Pilar Algoritma: Tulis komentar, Simpan, Follow, dan ajakan menyimak "part selanjutnya" secara natural untuk memotong cooldown.

    Format Wajib Output: Berikan HANYA JSON MURNI tanpa format markdown ```json ... ```, dengan struktur objek array berisi 5 item seperti contoh berikut:
    [
      {{
        "part_num": 1,
        "title": "Part 1 - Judul Part Ringkas",
        "slot": "Siang (13.00 WIB)",
        "playlist": "{topic_name}",
        "caption": "Teks Caption TikTok lengkap dengan emoji, Call to Action ke playlist, dan 5 hashtag relevan.",
        "slides": [
          {{"title": "SLIDE 1 (COVER)", "part_label": "PART - 1", "header": "ALLAH BERSAMA ORANG SABAR", "isi": "Mengapa doamu belum kunjung terkabul? Mungkinkah Allah menyuruhmu sabar?"}},
          {{"title": "SLIDE 2 (KONTEKS)", "header": "RASA MENANTI ✨", "isi": "Menunggu jawaban atas doa-doa di sepertiga malam sering kali membuat hati goyah..."}},
          {{"title": "SLIDE 3 (DALIL SHAHIH)", "header": "LANDASAN HADITS 🤲", "isi": "Doa seorang hamba akan senantiasa dikabulkan selama ia tidak berdoa untuk dosa...", "riwayat": "(HR. Muslim No. 2735)"}},
          {{"title": "SLIDE 4 (TADABBUR)", "header": "RAHASIA TAKDIR 🤍", "isi": "Allah tidak pernah terlambat maupun terlalu cepat. Kesabaranmu sedang menyiapkan jiwa..."}},
          {{"title": "SLIDE 5 (CLOSING & CTA)", "header": "MUARA KETENANGAN 🤍", "isi": "Percayalah, takdir Allah tidak pernah salah alamat.", "cta": "Tuliskan 'Aamiin' di komentar, ketuk simpan agar tak hilang, dan tekan ikuti untuk menyimak sambungan penyejuk jiwa di part selanjutnya ✨"}}
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

    iframe {
        background: transparent !important;
        border: none !important;
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

    .stTextArea textarea, .stTextInput input, .stNumberInput input {
        background-color: #1e293b !important;
        color: #fef08a !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        border: 1px solid rgba(34, 211, 238, 0.4) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
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
# 4. STICKY BULAN SABIT BERPIJAR & AUDIO ENGINE
# ==========================================
audio_floating_html = """
<!DOCTYPE html>
<html>
<head>
    <link href="[https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&display=swap](https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&display=swap)" rel="stylesheet">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        html, body { background: transparent !important; font-family: 'Plus Jakarta Sans', sans-serif; overflow: visible; }
        .moon-player-container { position: fixed; top: 10px; right: 25px; z-index: 999999; display: flex; flex-direction: column; align-items: flex-end; }
        .moon-btn { width: 56px; height: 56px; border-radius: 50%; background: rgba(15, 23, 42, 0.9); border: 2px solid #fef08a; display: flex; justify-content: center; align-items: center; cursor: pointer; transition: all 0.5s ease; }
        .moon-btn.active { background: radial-gradient(circle, #fffbeb 0%, #fef08a 40%, #d97706 100%); box-shadow: 0 0 25px #fef08a; transform: scale(1.12); }
        .moon-btn.off { opacity: 0.7; border-color: #64748b; }
        .spotify-card { position: absolute; top: 68px; right: 0; width: 310px; background: rgba(15, 23, 42, 0.95); border: 1px solid rgba(254, 240, 138, 0.4); border-radius: 18px; padding: 16px; display: none; flex-direction: column; gap: 12px; }
        .spotify-card.show { display: flex; }
        .song-title { color: #fef08a; font-size: 13px; font-weight: 800; }
        .song-artist { color: #94a3b8; font-size: 11px; }
        .player-controls { display: flex; align-items: center; justify-content: center; gap: 18px; }
        .play-main-btn { width: 40px; height: 40px; border-radius: 50%; background: #fef08a; color: #0f172a; display: flex; justify-content: center; align-items: center; font-weight: 800; cursor: pointer; }
    </style>
</head>
<body>
    <div class="moon-player-container">
        <div class="moon-btn off" id="moon-toggle" onclick="togglePlayState()">
            <span style="font-size: 28px;">🌙</span>
        </div>
        <div class="spotify-card" id="spotify-drawer">
            <div>
                <div class="song-title">Dengan Nafas-Mu</div>
                <div class="song-artist">Ungu - Special Ruang Teduh Session</div>
            </div>
            <div class="player-controls">
                <div class="play-main-btn" onclick="togglePlayState()">▶</div>
            </div>
        </div>
    </div>
    <audio id="bg-audio" src="[https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3](https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3)"></audio>
    <script>
        const audio = document.getElementById("bg-audio");
        const moonBtn = document.getElementById("moon-toggle");
        function togglePlayState() {
            if (audio.paused) {
                audio.play(); moonBtn.classList.remove("off"); moonBtn.classList.add("active");
            } else {
                audio.pause(); moonBtn.classList.remove("active"); moonBtn.classList.add("off");
            }
        }
    </script>
</body>
</html>
"""
st.html(audio_floating_html)

# ==========================================
# 5. TOP BAR JAM REALTIME
# ==========================================
top_bar_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { background-color: #0f172a; font-family: sans-serif; }
        .top-bar { width: 100%; height: 46px; background: rgba(15, 23, 42, 0.95); border-bottom: 1px solid rgba(234, 179, 8, 0.35); display: flex; align-items: center; justify-content: space-between; padding: 0 16px; }
        .clock-time { font-family: monospace; font-size: 14px; font-weight: 700; color: #fef08a; }
        .status-badge { background: rgba(34, 197, 94, 0.15); color: #4ade80; font-size: 11px; font-weight: 700; padding: 4px 12px; border-radius: 20px; }
    </style>
</head>
<body>
    <div class="top-bar">
        <span class="clock-time" id="digital-clock">00:00:00 WIB</span>
        <div class="status-badge">⚡ SUPER CREATOR: ACTIVE</div>
    </div>
    <script>
        function updateClock() {
            const now = new Date();
            document.getElementById('digital-clock').textContent = String(now.getHours()).padStart(2, '0') + ':' + String(now.getMinutes()).padStart(2, '0') + ':' + String(now.getSeconds()).padStart(2, '0') + ' WIB';
        }
        setInterval(updateClock, 1000); updateClock();
    </script>
</body>
</html>
"""
st.html(top_bar_html)

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
            
            keys_to_clear = [k for k in st.session_state.keys() if k.startswith(("cap_", "h_", "b_", "r_", "p_"))]
            for k in keys_to_clear:
                del st.session_state[k]

            st.session_state["parts_data"] = ai_result
            st.session_state["active_topic"] = topic_input
            st.session_state["carousel_previews"] = {}
            st.session_state["rendered_slide_cache"] = {}
            st.success("✅ Manager AI Berhasil Meracik 5 Part Content Queue!")

# ==========================================
# 7. COMPACT CANVAS ENGINE (WITH PART LABEL SUPPORT)
# ==========================================
def render_compact_interactive_canvas(header_text, body_text, part_label="", riwayat_text="", header_size=70, body_size=60, fr_size=42, pos_h=360, pos_b=720):
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
                cursor: move; padding: 4px; word-wrap: break-word; outline: none;
            }}
            .text-part {{
                color: #39ff14; font-size: 12px; font-weight: 900;
                text-shadow: 0 0 8px #000, 1px 1px 0 #000; top: {max(10, int((pos_h - 80) * 0.22))}px;
            }}
            .text-header {{
                color: #e879f9; font-size: {int(header_size * 0.22)}px; font-weight: 900;
                text-shadow: 0 0 8px #000, 1px 1px 0 #000; top: {int(pos_h * 0.22)}px;
            }}
            .text-body {{
                color: #38bdf8; font-size: {int(body_size * 0.22)}px; font-weight: 800;
                text-shadow: 0 0 8px #000, 1px 1px 0 #000; top: {int(pos_b * 0.22)}px;
            }}
            .text-riwayat {{
                color: #39ff14; font-size: {int(fr_size * 0.22)}px; font-weight: 700;
                text-shadow: 0 0 6px #000; top: 340px;
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
            <div class="hint-tag">⚡ Direct Canvas Preview</div>
            {"<div class='draggable-text text-part'>" + part_label + "</div>" if part_label else ""}
            <div class="draggable-text text-header">{header_text}</div>
            <div class="draggable-text text-body">{body_text}</div>
            {"<div class='draggable-text text-riwayat'>Riwayat<br>" + riwayat_text + "</div>" if riwayat_text else ""}
        </div>
    </body>
    </html>
    """
    st.html(html_code)

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
            
            # FORM NASKAH TEKS (SUPPORT PART_LABEL UNTUK SLIDE 1)
            if s_idx == 0 or 'part_label' in s:
                s['part_label'] = st.text_input(f"Label Part S1 (Hijau Neon)", value=s.get('part_label', f'PART - {p_num}'), key=f"p_{p_num}_{s_idx}_{t_hash}")
                
            s['header'] = st.text_input(f"Header S{s_idx+1}", value=s.get('header', ''), key=f"h_{p_num}_{s_idx}_{t_hash}")
            s['isi'] = st.text_area(f"Isi S{s_idx+1}", value=s.get('isi', ''), key=f"b_{p_num}_{s_idx}_{t_hash}", height=85)
            
            if 'riwayat' in s or s_idx == 2:
                s['riwayat'] = st.text_input(f"Riwayat Hadits S{s_idx+1}", value=s.get('riwayat', ''), key=f"r_{p_num}_{s_idx}_{t_hash}")

            # CONTROL FONT SIZE & COORDINATE POSITIONING
            st.markdown("##### 📏 Ukuran Font & Presisi Posisi Y-Offset")
            c_f1, c_f2 = st.columns(2)
            with c_f1:
                fh = st.number_input(f"Size Header S{s_idx+1}", min_value=30, max_value=120, value=s.get('font_setting', {}).get('header', 70), step=2, key=f"fh_{p_num}_{s_idx}_{t_hash}")
                pos_h = st.number_input(f"Posisi Y Header S{s_idx+1}", min_value=100, max_value=1200, value=s.get('font_setting', {}).get('y_header', 320 if s_idx==2 else 360), step=10, key=f"yh_{p_num}_{s_idx}_{t_hash}")
            with c_f2:
                fb = st.number_input(f"Size Body S{s_idx+1}", min_value=25, max_value=100, value=s.get('font_setting', {}).get('body', 60 if s_idx != 2 else 48), step=2, key=f"fb_{p_num}_{s_idx}_{t_hash}")
                pos_b = st.number_input(f"Posisi Y Body S{s_idx+1}", min_value=200, max_value=1600, value=s.get('font_setting', {}).get('y_body', 620 if s_idx==2 else 720), step=10, key=f"yb_{p_num}_{s_idx}_{t_hash}")
            
            fr = 42
            if s_idx == 2:
                fr = st.number_input(f"Size Riwayat S{s_idx+1}", min_value=20, max_value=80, value=s.get('font_setting', {}).get('riwayat', 42), step=2, key=f"fr_{p_num}_{s_idx}_{t_hash}")

            # OVERRIDE S['FONT_SETTING']
            s['font_setting'] = {
                "header": fh,
                "body": fb,
                "riwayat": fr,
                "y_header": pos_h,
                "y_body": pos_b
            }

            # AUTO RENDER PILLOW ENGINE
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
                    part_label=s.get('part_label', ''),
                    riwayat_text=s.get('riwayat', '') if selected_edit_idx==2 else "",
                    header_size=fh,
                    body_size=fb,
                    fr_size=fr,
                    pos_h=pos_h,
                    pos_b=pos_b
                )

                st.markdown('<div class="btn-apply">', unsafe_allow_html=True)
                btn_apply = st.button(f"⚡ Apply Changes & Render Visual (Slide {s_idx+1})", key=f"btn_apply_{p_num}_{s_idx}_{t_hash}", width="stretch")
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
                        width="stretch"
                    )

        # AREA TOMBOL RENDER MASAL FULL PACK 5 SLIDE
        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
        c_v, c_s = st.columns(2)
        with c_v:
            st.button(f"🎬 Render Video Part {p_num}", key=f"btn_vid_{p_num}_{t_hash}", width="stretch")
        with c_s:
            if st.button(f"📸 Render Full Carousel (ZIP 5 Slide) Part {p_num}", key=f"btn_slide_{p_num}_{t_hash}", width="stretch"):
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
                    st.image(img, caption=f"Slide {idx+1}", width="stretch")
            
            st.download_button(
                label=f"💾 Download 5 Slide HD (ZIP) Ter-Sync Edit - Part {p_num}",
                data=preview_info["zip"],
                file_name=f"RuangTeduh_Part_{p_num}_{datetime.now().strftime('%Y%m%d')}.zip",
                mime="application/zip",
                key=f"dl_zip_sync_{p_num}_{t_hash}",
                width="stretch"
            )

        st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)
