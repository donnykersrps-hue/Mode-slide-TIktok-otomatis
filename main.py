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
        html, body { background: transparent !important; font-family: 'Plus Jakarta Sans', sans-serif; overflow: visible;
