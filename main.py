import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime

# ==========================================
# 1. KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="Ruang Teduh - Auto Content Engine",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. INJECT CUSTOM CSS (MINIMALIS & MEWAH)
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

    /* CARD RINGKAS CONTENT QUEUE */
    .part-card-compact {
        background: #1e293b;
        border: 1px solid rgba(234, 179, 8, 0.25);
        border-radius: 16px;
        padding: 18px 24px;
        margin-bottom: 16px;
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

    .slide-item {
        background: rgba(15, 23, 42, 0.6);
        border-left: 4px solid #eab308;
        border-radius: 0 10px 10px 0;
        padding: 10px 14px;
        margin-bottom: 8px;
    }

    .stButton>button {
        border-radius: 10px !important;
        font-weight: 700 !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ==========================================
# 3. TOP BAR JAM REALTIME & ENGINE STATUS
# ==========================================
top_bar_html = """
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700&family=JetBrains+Mono:wght@700&display=swap" rel="stylesheet">
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
        <div class="status-badge">⚡ AUTOMATION ENGINE: READY</div>
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
# 4. MOCK DATA GENERATOR (DUMMY UNTUK CONCEPT)
# ==========================================
def get_compact_parts_data(topic_name):
    clean_topic = topic_name.strip()
    return [
        {
            "part_num": i,
            "title": f"Part {i} - Serial {clean_topic}",
            "slot": ["Siang (13.00 WIB)", "Siang (13.00 WIB)", "Sore (16.30 WIB)", "Malam (19.00 WIB)", "Malam (20.00 WIB)"][i-1],
            "playlist": clean_topic,
            "caption": f"{clean_topic} (Part {i}) 🌿\n\nUntukmu yang sedang lelah, ini janji peleram gelisahmu... 💔\n\n#RuangTeduh #SelfReminder",
            "slides": [
                {"title": "SLIDE 1 (COVER)", "header": f"RAHASIA {clean_topic.upper()} 🌿", "isi": "\"Untukmu jiwa yang lelah, ini janji peleram gelisahmu tak pernah ingkar...\""},
                {"title": "SLIDE 2 (KONTEKS)", "header": "MENJAGA DALAM KELELAHAN ✨", "isi": "\"Di tengah himpitan duniawi, ada keistiqamahan kecil yang dinilai sangat agung.\""},
                {"title": "SLIDE 3 (DALIL)", "header": "LANDASAN UTAMA 🤲", "isi": f"\"Barangsiapa senantiasa menjaga keistiqamahan {clean_topic.lower()}, Allah bukakan ketenangan...\"", "riwayat": "(HR. Muslim)"},
                {"title": "SLIDE 4 (TADABBUR)", "header": "BENTENG JIWA 🤍", "isi": "\"Ketenangan adalah hadirnya rasa percaya penuh pada takdir-Nya.\""},
                {"title": "SLIDE 5 (CLOSING)", "header": "BERSAMBUNG 🔗", "isi": f"\"Simak Part berikutnya di playlist '{clean_topic}' (Cek Profil 🌿)\"", "cta": "(Al-Qur'an terjemahan di keranjang kuning✨)"}
            ]
        } for i in range(1, 6)
    ]

# ==========================================
# 5. HEADER & INPUT CONTROL
# ==========================================
st.markdown("""
<div class="header-box">
    <span class="brand-badge">🤖 Ruang Teduh AI Control Center</span>
    <h1 class="header-title">Dashboard Generator & Automation 5 Part</h1>
    <p class="header-subtitle">Tampilan ringkas & interaktif untuk eksekusi cepat pembuatan konten TikTok</p>
</div>
""", unsafe_allow_html=True)

topic_input = st.text_input("💡 Masukkan Topik Konten Utama:", value="Syarat utama pintu taubat", placeholder="Contoh: Rahasia Sedekah Subuh, Syarat Pintu Taubat, dll.")
btn_generate = st.button("🚀 Racik Content Queue 5 Part")

# ==========================================
# 6. RINGKASAN CONTENT QUEUE (GUI BARU)
# ==========================================
if btn_generate or topic_input:
    st.markdown("---")
    st.markdown(f"### 🌿 CONTENT QUEUE RINGKAS: `{topic_input}`")
    
    parts_data = get_compact_parts_data(topic_input)
    
    for part in parts_data:
        st.markdown(f"""
        <div class="part-card-compact">
            <div class="part-header">📌 PART {part['part_num']}/5: {part['title']}</div>
            <div style="margin-bottom: 12px;">
                <span class="slot-badge">⏰ Slot: {part['slot']}</span>
                <span class="playlist-badge">📂 Playlist: {part['playlist']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 3 TOMBOL AKSI UTAMA DI SETIAP BARIS PART
        col_btn1, col_btn2, col_btn3 = st.columns([1.5, 1, 1])

        with col_btn1:
            # Pop-Up / Expander untuk Pratinjau Teks & Slide tanpa memenuhi layar
            with st.expander(f"👁️ Pratinjau Teks & Slide (Part {part['part_num']})"):
                st.markdown("**📝 Caption TikTok:**")
                st.code(part['caption'], language="text")
                st.markdown("**🎨 Rincian 5 Slide:**")
                for s in part['slides']:
                    st.markdown(f"""
                    <div class="slide-item">
                        <div style="color: #fef08a; font-weight:700;">{s['title']}</div>
                        <div><b>Header:</b> {s['header']}</div>
                        <div><b>Isi:</b> {s['isi']}</div>
                    </div>
                    """, unsafe_allow_html=True)

        with col_btn2:
            st.button(f"🎬 Render Video", key=f"btn_vid_{part['part_num']}", use_container_width=True)

        with col_btn3:
            st.button(f"📸 Render Carousel", key=f"btn_slide_{part['part_num']}", use_container_width=True)

        st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)
