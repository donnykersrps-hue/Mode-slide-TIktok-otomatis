import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json
import io
from datetime import datetime
import google.generativeai as genai

# ==========================================
# 1. KONFIGURASI HALAMAN
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
# 2. GEMINI AI BRAIN ENGINE (MANAGER KONTEN)
# ==========================================
def generate_5part_with_gemini(topic_name):
    """
    Manager AI Engine: Meminta Gemini meracik naskah 5 Part terstruktur
    dalam format JSON murni yang siap disajikan ke Content Queue GUI.
    """
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
    - SLIDE 5 (CLOSING & CTA): Ajakan simpan/lanjut part + CTA produk Al-Qur'an/buku di keranjang kuning.

    Struktur 5 Part Serial:
    - Part 1: Hook emosional + Pengenalan topik. (Slot: Siang (13.00 WIB))
    - Part 2: Kelembutan batin saat diuji + Hadits Pelipur Duka. (Slot: Siang (13.00 WIB))
    - Part 3: Penenang gelisah keluarga / lingkungan terdekat + Hadits Akhlak/Keluarga. (Slot: Sore (16.30 WIB))
    - Part 4: Menjaga lisan & kesucian hati + Hadits Berkata Baik/Diam. (Slot: Malam (19.00 WIB))
    - Part 5: Puncak pasrah & keridhoan batin + Hadits Pintu Surga/Keridhoan Allah. (Slot: Malam (20.00 WIB))

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
          {{"title": "SLIDE 5 (CLOSING)", "header": "HEADER CLOSING 🔗", "isi": "Teks ajakan lanjut ke Part berikutnya...", "cta": "(Sebutkan produk Al-Qur'an/buku di keranjang kuning✨)"}}
        ]
      }}
    ]
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
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
# 3. INJECT CUSTOM CSS INTERAKTIF (GOLD -> CYAN)
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

    .playlist
