import os
import io
import re
import zipfile
import requests
from PIL import Image, ImageDraw, ImageFont

# ==========================================
# 1. KONFIGURASI FONT & CLEANER EMOJI/SIMBOL
# ==========================================
FONT_PATH_BOLD = "DejaVuSans-Bold.ttf"

def get_font(size):
    try:
        return ImageFont.truetype(FONT_PATH_BOLD, int(size))
    except Exception:
        return ImageFont.load_default()

def remove_unsupported_symbols(text):
    """
    Menghapus emoji/simbol asing yang menyebabkan kotak error (□) pada Pillow
    """
    if not text:
        return ""
    clean_text = re.sub(r'[\U00010000-\U0010ffff]', '', text)
    clean_text = re.sub(r'[\u2600-\u27BF]', '', clean_text)
    clean_text = re.sub(r'[\u2300-\u23FF]', '', clean_text)
    clean_text = re.sub(r'[\u2b50-\u2b55]', '', clean_text)
    return clean_text.strip()

def fetch_bright_aesthetic_background(pexels_key=""):
    """
    Mengambil background CERAH LAUTAN & PEGUNUNGAN PAGI (Morning Ocean, Mountain Grassland, Sunrise Sky)
    """
    if pexels_key:
        headers = {"Authorization": pexels_key}
        url = "https://api.pexels.com/v1/search?query=morning+ocean+mountain+grassland+sunrise+nature+aesthetic&per_page=30&orientation=portrait"
        try:
            res = requests.get(url, headers=headers, timeout=5)
            if res.status_code == 200:
                data = res.json()
                photos = data.get("photos", [])
                if photos:
                    import random
                    photo_url = random.choice(photos)["src"]["portrait"]
                    img_res = requests.get(photo_url, timeout=5)
                    if img_res.status_code == 200:
                        img = Image.open(io.BytesIO(img_res.content)).convert("RGB")
                        return img.resize((1080, 1920))
        except Exception:
            pass

    # Fallback Gradient Pagi Hari jika Pexels offline
    base = Image.new("RGB", (1080, 1920), color="#e0f2fe")
    draw = ImageDraw.Draw(base)
    for y in range(1920):
        r = int(186 - (y / 1920) * 80)
        g = int(230 - (y / 1920) * 40)
        b = int(253 - (y / 1920) * 90)
        draw.line([(0, y), (1080, y)], fill=(r, g, b))
    return base

# ==========================================
# 2. HELPER TEXT WRAPPER & DRAW SHADOW PEKAT
# ==========================================
def wrap_text(text, font, max_width, draw):
    lines = []
    words = text.split()
    if not words:
        return lines

    current_line = words[0]
    for word in words[1:]:
        test_line = current_line + " " + word
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if (bbox[2] - bbox[0]) <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)
    return lines

def draw_text_with_shadow(draw, position, text, font, text_color="#ffffff", shadow_color="#000000", shadow_offset=5):
    """
    Shadow pekat 8 arah agar teks berukuran cerah tetap 100% terbaca tajam di atas background terang
    """
    x, y = position
    clean_str = remove_unsupported_symbols(text)
    if not clean_str:
        return
        
    for dx in [-shadow_offset, 0, shadow_offset]:
        for dy in [-shadow_offset, 0, shadow_offset]:
            if dx != 0 or dy != 0:
                draw.text((x + dx, y + dy), clean_str, font=font, fill=shadow_color, anchor="mm")
    draw.text((x, y), clean_str, font=font, fill=text_color, anchor="mm")

# ==========================================
# 3. CORE RENDER ENGINE (REVISE: PART LABEL & DYNAMIC HEADER)
# ==========================================
def render_single_slide_image(bg_image, slide_data, is_slide_3=False, is_slide_5=False):
    canvas = bg_image.copy().resize((1080, 1920))
    
    # Soft Dark Overlay (25% opacity) agar background cerah tidak "memakan" huruf
    overlay = Image.new("RGBA", (1080, 1920), (15, 23, 42, 60))
    canvas.paste(overlay, (0, 0), overlay)
    
    draw = ImageDraw.Draw(canvas)

    font_settings = slide_data.get("font_setting", {})
    size_h = font_settings.get("header", 70)
    size_b = font_settings.get("body", 60 if not is_slide_3 else 48)
    size_r = font_settings.get("riwayat", 42)

    pos_h = font_settings.get("y_header", 320 if is_slide_3 else 360)
    pos_b = font_settings.get("y_body", 620 if is_slide_3 else 720)

    font_h = get_font(size_h)
    font_b = get_font(size_b)
    font_r = get_font(size_r)

    # 1. RENDER LABEL PART (HIJAU NEON #39ff14 - EYE CATCHER ATAS)
    part_label = slide_data.get("part_label", "").upper()
    if part_label:
        font_part = get_font(48)
        # Posisi di atas Header Utama
        draw_text_with_shadow(draw, (540, pos_h - 80), part_label, font_part, text_color="#39ff14", shadow_color="#000000", shadow_offset=6)

    # 2. RENDER HEADER KONTEKS DINAMIS (MAGENTA NEON #e879f9)
    header_text = slide_data.get("header", "").upper()
    if is_slide_5:
        header_text = slide_data.get("header", "PENYEMAT KETENANGAN").upper()

    if header_text:
        header_lines = wrap_text(header_text, font_h, 920, draw)
        curr_y = pos_h
        for line in header_lines:
            draw_text_with_shadow(draw, (540, curr_y), line, font_h, text_color="#e879f9", shadow_color="#000000", shadow_offset=6)
            curr_y += size_h + 14

    # 3. RENDER ISI TEKS & SLIDE 5 ENGAGEMENT
    body_text = slide_data.get("isi", "")
    cta_text = slide_data.get("cta", "")

    if is_slide_5:
        if not cta_text:
            cta_text = "Tulis jawabanmu di komentar, ketuk simpan agar tidak hilang, dan tekan ikuti untuk menyimak sambungan penyejuk jiwa di part selanjutnya."
        
        full_slide5_text = f"{body_text}\n\n{cta_text}" if body_text else cta_text
        font_s5 = get_font(52)
        s5_lines = wrap_text(full_slide5_text, font_s5, 900, draw)
        
        curr_y = pos_b
        for line in s5_lines:
            # Kuning Neon Mencolok #fef08a untuk Slide 5
            draw_text_with_shadow(draw, (540, curr_y), line, font_s5, text_color="#fef08a", shadow_color="#000000", shadow_offset=6)
            curr_y += 52 + 16
    else:
        # Tampilan Slide 1, 2, 3, 4 (Warna Cyan #38bdf8)
        if body_text:
            body_lines = wrap_text(body_text, font_b, 900, draw)
            curr_y = pos_b
            for line in body_lines:
                draw_text_with_shadow(draw, (540, curr_y), line, font_b, text_color="#38bdf8", shadow_color="#000000", shadow_offset=5)
                curr_y += size_b + 16

            # RENDER RIWAYAT HADITS SLIDE 3 (HIJAU NEON #39ff14 & BEBAS OVERLAP)
            riwayat_text = slide_data.get("riwayat", "")
            if is_slide_3 and riwayat_text:
                y_riwayat = curr_y + 60
                riwayat_lines = wrap_text(f"Riwayat {riwayat_text}", font_r, 880, draw)
                for r_line in riwayat_lines:
                    draw_text_with_shadow(draw, (540, y_riwayat), r_line, font_r, text_color="#39ff14", shadow_color="#000000", shadow_offset=5)
                    y_riwayat += size_r + 12

    return canvas

# ==========================================
# 4. FULL CAROUSEL PACK GENERATOR (ZIP)
# ==========================================
def generate_carousel_pack(slides_list, pexels_key=""):
    rendered_images = []
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for idx, slide in enumerate(slides_list):
            bg = fetch_bright_aesthetic_background(pexels_key=pexels_key)
            is_s3 = (idx == 2)
            is_s5 = (idx == 4)

            img = render_single_slide_image(bg, slide, is_slide_3=is_s3, is_slide_5=is_s5)
            rendered_images.append(img)

            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format="JPEG", quality=98)
            zip_file.writestr(f"Slide_{idx+1}.jpg", img_byte_arr.getvalue())

    return rendered_images, zip_buffer.getvalue()
