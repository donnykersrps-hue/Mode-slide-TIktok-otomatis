import streamlit as st
import google.generativeai as genai
import os
from render_engine import get_pexels_video, create_voiceover, assemble_video

# ================== CONFIGURASI UTAMA & TEMA ESTETIK ==================
st.set_page_config(page_title="AI TikTok Studio", layout="wide", initial_sidebar_state="expanded")

# Inject Custom CSS untuk Tampilan Modern Dark-Gold Glassmorphism
st.markdown("""
<style>
    /* Styling Card Utama */
    .script-card {
        background: linear-gradient(135deg, rgba(25, 30, 45, 0.85) 0%, rgba(15, 18, 28, 0.95) 100%);
        border: 1px solid rgba(255, 215, 0, 0.25);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(8px);
    }
    .vo-box {
        background: rgba(255, 255, 255, 0.04);
        border-left: 4px solid #FFD700;
        border-radius: 8px;
        padding: 16px;
        font-size: 16px;
        line-height: 1.6;
        color: #E2E8F0;
        margin-top: 10px;
        margin-bottom: 15px;
    }
    .badge-gold {
        background: linear-gradient(90deg, #FFD700 0%, #FFA500 100%);
        color: #000000;
        font-weight: bold;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        display: inline-block;
        margin-bottom: 8px;
    }
    .badge-sub {
        background: rgba(255, 248, 220, 0.15);
        color: #FFF8DC;
        border: 1px solid rgba(255, 248, 220, 0.3);
        padding: 6px 14px;
        border-radius: 8px;
        font-size: 14px;
        display: inline-block;
        margin-right: 8px;
        margin-bottom: 8px;
    }
    .header-gold {
        color: #FFD700;
        font-family: 'sans-serif';
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎬 AI-Powered TikTok Content Studio")
st.caption("Otomatisasi Konten Edukasi Islami Berbasis AI & Direct FFmpeg Engine")

# Inisialisasi session state
if "step" not in st.session_state:
    st.session_state.step = 1
if "voiceover_text" not in st.session_state:
    st.session_state.voiceover_text = ""
if "keywords_list" not in st.session_state:
    st.session_state.keywords_list = []
if "text_segments" not in st.session_state:
    st.session_state.text_segments = []
if "final_video_path" not in st.session_state:
    st.session_state.final_video_path = ""
if "bgm_description" not in st.session_state:
    st.session_state.bgm_description = ""

# ================== SIDEBAR (API KEYS) ==================
gemini_key = st.secrets.get("GEMINI_API_KEY", "")
pexels_key = st.secrets.get("PEXELS_API_KEY", "")

with st.sidebar:
    st.header("🔑 Operational Panel")
    if not gemini_key:
        gemini_key = st.text_input("Gemini API Key", type="password")
    else:
        st.success("✅ Gemini Key Connected")
    if not pexels_key:
        pexels_key = st.text_input("Pexels API Key", type="password")
    else:
        st.success("✅ Pexels Key Connected")
        
    st.markdown("---")
    st.markdown("<b>Status Workflow:</b>", unsafe_allow_html=True)
    st.progress(st.session_state.step / 3)

# ================== STEP 1: GENERATE & REVISI NASKAH ==================
st.header("📝 1. Rencana & Naskah Konten AI")
topic = st.text_input("Masukkan ide konten / hadist (contoh: Hadist tentang kemuliaan shalawat di hari Jumat)")

col_btn1, col_btn2 = st.columns([1, 4])
with col_btn1:
    generate_click = st.button("✨ Generate Naskah Awal", use_container_width=True)

if generate_click:
    if not gemini_key:
        st.error("Masukkan Gemini API Key di sidebar terlebih dahulu!")
    elif not topic:
        st.warning("Topik konten harus diisi!")
    else:
        with st.spinner("Gemini 3.6 Flash meracik naskah & skema visual estetik..."):
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel('gemini-1.5-flash')

            prompt = f"""
            Kamu adalah scriptwriter & creative director profesional untuk konten edukasi islami TikTok (@ruangteduh.id88).
            Buatkan naskah video lengkap beserta konsep audio-visual dengan TARGET DURASI PRESISI 60 Sampai 70 detik tentang topik: {topic}.

            Gunakan gaya bahasa puitis, syahdu, penuh empati, dan menyentuh batin.
            Panjang teks VOICEOVER WAJIB berkisar antara 130 hingga 160 kata.

            Persyaratan Multi-Scene & Overlay:
            1. Buatkan 3 KEYWORD Pexels berbeda yang relevan dan estetik.
            2. Buatkan instruksi AUDIO BGM instrumen syahdu.
            3. Buatkan 3 BAGIAN TEKS LAYAR (OVERLAY) singkat (3-5 kata per baris) + sebutkan nomor hadits/dalilnya.
               Gunakan tanda bintang (*) untuk penanda kata kunci utama.

            Berikan format jawaban PERSIS seperti ini:
            VOICEOVER: [Teks narasi 130-160 kata]
            KEYWORDS: [Keyword 1] | [Keyword 2] | [Keyword 3]
            AUDIO_BGM: [Deskripsi BGM]
            OVERLAY_1: [Frasa ringkas Poin 1 + Tag *Highlight*] / [Nomor Hadits]
            OVERLAY_2: [Frasa ringkas Poin 2 + Tag *Highlight*] / [Nomor Hadits]
            OVERLAY_3: [Frasa ringkas Poin 3 + Tag *Highlight*] / [Nomor Hadits]
            """

            response = model.generate_content(prompt)
            raw_text = response.text

            try:
                vo = raw_text.split("VOICEOVER:")[1].split("KEYWORDS:")[0].strip()
                kw_str = raw_text.split("KEYWORDS:")[1].split("AUDIO_BGM:")[0].strip()
                bgm = raw_text.split("AUDIO_BGM:")[1].split("OVERLAY_1:")[0].strip()
                ov1 = raw_text.split("OVERLAY_1:")[1].split("OVERLAY_2:")[0].strip()
                ov2 = raw_text.split("OVERLAY_2:")[1].split("OVERLAY_3:")[0].strip()
                ov3 = raw_text.split("OVERLAY_3:")[1].strip()

                st.session_state.voiceover_text = vo
                st.session_state.keywords_list = [k.strip() for k in kw_str.split("|")]
                st.session_state.text_segments = [ov1, ov2, ov3]
                st.session_state.bgm_description = bgm
                st.session_state.step = 2
                st.rerun()

            except Exception as e:
                st.error(f"Gagal memproses parsing naskah: {e}")

# --- DISPLAY NASKAH & REVISI REALTIME (DESAIN CARDS LUXURY) ---
if st.session_state.voiceover_text:
    word_count = len(st.session_state.voiceover_text.split())
    
    # CARD DISPLAY ESTETIK
    st.markdown(f"""
    <div class="script-card">
        <span class="badge-gold">ESTIMASI DURASI: 60-70 DETIK</span>
        <h3 class="header-gold" style="margin-top: 5px; margin-bottom: 10px;">🗣️ Narasi Voiceover AI ({word_count} Kata)</h3>
        <div class="vo-box">
            {st.session_state.voiceover_text}
        </div>
        
        <div style="display: flex; gap: 20px; flex-wrap: wrap; margin-top: 15px;">
            <div style="flex: 1; min-width: 280px;">
                <h4 class="header-gold">🎬 Visual Keywords (Pexels)</h4>
                <div>
                    {"".join([f'<span class="badge-sub">📍 {kw}</span>' for kw in st.session_state.keywords_list])}
                </div>
            </div>
            <div style="flex: 1; min-width: 280px;">
                <h4 class="header-gold">🎵 Audio Background (BGM)</h4>
                <p style="color: #CBD5E1; font-size: 14px;">{st.session_state.bgm_description}</p>
            </div>
        </div>

        <h4 class="header-gold" style="margin-top: 20px;">📌 Header / Overlay Teks Emas Layar</h4>
        <ol style="color: #E2E8F0; font-size: 15px; padding-left: 20px;">
            <li>{st.session_state.text_segments[0]}</li>
            <li>{st.session_state.text_segments[1]}</li>
            <li>{st.session_state.text_segments[2]}</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

    # PANEL REVISI REALTIME
    st.markdown("### 💡 Panel Revisi Realtime (Tanpa Render Video)")
    rev_col1, rev_col2 = st.columns([3, 1])
    with rev_col1:
        revision_instruction = st.text_input("Instruksi Revisi AI", placeholder="Contoh: 'Ubah nada narasi lebih syahdu' atau 'Ganti keyword visual kedua'")
    with rev_col2:
        st.write("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        apply_rev = st.button("🔄 Terapkan Revisi", use_container_width=True)

    if apply_rev:
        if not revision_instruction:
            st.warning("Ketik instruksi revisinya terlebih dahulu!")
        else:
            with st.spinner("Gemini 3.6 Flash memperbarui rancangan naskah secara realtime..."):
                genai.configure(api_key=gemini_key)
                model = genai.GenerativeModel('gemini-1.5-flash')

                revision_prompt = f"""
                Berikut adalah naskah & rancangan visual TikTok saat ini:
                VOICEOVER: {st.session_state.voiceover_text}
                KEYWORDS: {' | '.join(st.session_state.keywords_list)}
                AUDIO_BGM: {st.session_state.bgm_description}
                OVERLAY_1: {st.session_state.text_segments[0]}
                OVERLAY_2: {st.session_state.text_segments[1]}
                OVERLAY_3: {st.session_state.text_segments[2]}

                LAKUKAN REVISI berdasarkan instruksi user berikut:
                "{revision_instruction}"

                Tetap pertahankan format jawaban PERSIS seperti ini:
                VOICEOVER: [Teks narasi revisi 130-160 kata]
                KEYWORDS: [Keyword 1] | [Keyword 2] | [Keyword 3]
                AUDIO_BGM: [Deskripsi BGM]
                OVERLAY_1: [Frasa ringkas Poin 1 + Tag *Highlight*] / [Nomor Hadits]
                OVERLAY_2: [Frasa ringkas Poin 2 + Tag *Highlight*] / [Nomor Hadits]
                OVERLAY_3: [Frasa ringkas Poin 3 + Tag *Highlight*] / [Nomor Hadits]
                """

                resp = model.generate_content(revision_prompt)
                raw_text = resp.text

                try:
                    vo = raw_text.split("VOICEOVER:")[1].split("KEYWORDS:")[0].strip()
                    kw_str = raw_text.split("KEYWORDS:")[1].split("AUDIO_BGM:")[0].strip()
                    bgm = raw_text.split("AUDIO_BGM:")[1].split("OVERLAY_1:")[0].strip()
                    ov1 = raw_text.split("OVERLAY_1:")[1].split("OVERLAY_2:")[0].strip()
                    ov2 = raw_text.split("OVERLAY_2:")[1].split("OVERLAY_3:")[0].strip()
                    ov3 = raw_text.split("OVERLAY_3:")[1].strip()

                    st.session_state.voiceover_text = vo
                    st.session_state.keywords_list = [k.strip() for k in kw_str.split("|")]
                    st.session_state.text_segments = [ov1, ov2, ov3]
                    st.session_state.bgm_description = bgm

                    st.success("Naskah & skema visual berhasil direvisi secara realtime!")
                    st.rerun()

                except Exception as e:
                    st.error(f"Gagal memproses revisi: {e}")

# ================== STEP 2: RENDER VIDEO ==================
if st.session_state.step >= 2:
    st.markdown("---")
    st.header("⚙️ 2. Eksekusi Render Video Final")
    st.caption("Tekan tombol render di bawah ini hanya jika rancangan naskah di atas sudah 100% pas.")
    
    if st.button("🚀 Mulai Render Otomatis (FFmpeg Engine)", type="primary"):
        if not pexels_key:
            st.error("Pexels API Key belum diisi!")
        else:
            v_paths = []
            for idx, kw in enumerate(st.session_state.keywords_list):
                with st.spinner(f"Mengunduh footage visual {idx+1}: '{kw}'..."):
                    p = get_pexels_video(kw, pexels_key, output_filename=f"temp_video_{idx}.mp4")
                    v_paths.append(p)

            with st.spinner("Menggenerasi suara narasi AI (Edge-TTS)..."):
                aud_path = create_voiceover(st.session_state.voiceover_text, rate="-5%")

            with st.spinner("Merakit video akhir (Header Emas + Subtitle Cream + BGM 30%)..."):
                final_path = assemble_video(
                    video_paths=v_paths,
                    audio_path=aud_path,
                    text_segments=st.session_state.text_segments,
                    bgm_description=st.session_state.bgm_description,
                    full_narration=st.session_state.voiceover_text
                )

                if final_path:
                    st.session_state.final_video_path = final_path
                    st.session_state.step = 3
                    st.rerun()
                else:
                    st.error("Render gagal. Silakan periksa log server terminal.")

# ================== STEP 3: PREVIEW VIDEO ==================
if st.session_state.step == 3 and st.session_state.final_video_path:
    st.markdown("---")
    st.header("📱 3. Preview Video Final")

    col_prev1, col_prev2 = st.columns([1, 2])
    with col_prev1:
        st.video(st.session_state.final_video_path)
        st.success("🎉 Video berhasil di-render dengan sempurna!")
