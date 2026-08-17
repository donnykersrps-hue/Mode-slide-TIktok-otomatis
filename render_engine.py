import os
import io
import zipfile
import requests
from PIL import Image, ImageDraw, ImageFont

# ==========================================
# 1. KONFIGURASI FONT & BACKGROUND DEFAULT
# ==========================================
FONT_PATH_BOLD = "DejaVuSans-Bold.ttf"

def get_font(size):
    try:
        return ImageFont.truetype(FONT_PATH_BOLD, int(size))
    except Exception:
        return ImageFont.load_default()

def fetch_bright_aesthetic_background(pexels_key=""):
    if pexels_key:
        headers = {"Authorization": pexels_key}
        url = "https://api.pexels.com/v1/search?query=aesthetic+nature+warm+light&per_page=15&orientation=portrait"
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

    base = Image.new("RGB", (1080, 1920), color="#0f172a")
    draw = ImageDraw.Draw(base)
    for y in range(1920):
        r = int(15 + (y / 1920) * 35)
        g = int(23 + (y / 1920) * 45)
        b = int(42 + (y / 1920) * 60)
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

def draw_text_with_shadow(draw, position, text, font, text_color="#ffffff", shadow_color="#000000", shadow_offset=4):
    x, y = position
    for dx in [-shadow_offset, 0, shadow_offset]:
        for dy in [-shadow_offset, 0, shadow_offset]:
            if dx != 0 or dy != 0:
                draw.text((x + dx, y + dy), text, font=font, fill=shadow_color, anchor="mm")
    draw.text((x, y), text, font=font, fill=text_color, anchor="mm")

# ==========================================
# 3. CORE RENDER ENGINE (DYNAMIC SPACING & MAGENTA GLOW)
# ==========================================
def render_single_slide_image(bg_image, slide_data, is_slide_3=False, is_slide_5=False):
    canvas = bg_image.copy().resize((1080, 1920))
    draw = ImageDraw.Draw(canvas)

    font_settings = slide_data.get("font_setting", {})
    size_h = font_settings.get("header", 74)
    size_b = font_settings.get("body", 64 if not is_slide_3 else 50)
    size_r = font_settings.get("riwayat", 42)

    pos_h = font_settings.get("y_header", 320 if is_slide_3 else 350)
    pos_b = font_settings.get("y_body", 680 if is_slide_3 else 780)

    font_h = get_font(size_h)
    font_b = get_font(size_b)
    font_r = get_font(size_r)

    # 1. RENDER HEADER (KEMBALI KE MAGENTA NEON ESTETIK)
    header_text = slide_data.get("header", "").upper()
    if is_slide_5:
        header_text = slide_data.get("header", "PENYEMAT KETENANGAN 🤍").upper()

    if header_text:
        header_lines = wrap_text(header_text, font_h, 920, draw)
        curr_y = pos_h
        for line in header_lines:
            # Warna Magenta Neon #e879f9 dengan Shadow Pekat
            draw_text_with_shadow(draw, (540, curr_y), line, font_h, text_color="#e879f9", shadow_color="#000000", shadow_offset=5)
            curr_y += size_h + 12

    # 2. RENDER ISI TEKS (BODY / HADITS / PERENUNGAN)
    body_text = slide_data.get("isi", "")
    curr_y_body_end = pos_b

    if body_text:
        body_lines = wrap_text(body_text, font_b, 900, draw)
        curr_y = pos_b
        color_body = "#38bdf8" if not is_slide_5 else "#f8fafc"
        for line in body_lines:
            draw_text_with_shadow(draw, (540, curr_y), line, font_b, text_color=color_body, shadow_color="#000000", shadow_offset=4)
            curr_y += size_b + 16
        curr_y_body_end = curr_y

    # 3. RENDER SUB-TEKS / RIWAYAT (SLIDE 3) DAN CTA (SLIDE 5) SECARA DINAMIS
    riwayat_text = slide_data.get("riwayat", "")
    cta_text = slide_data.get("cta", "")

    if is_slide_5 and not cta_text:
        cta_text = "Tulis jawabanmu di komentar 💬, ketuk 📌 simpan agar tidak hilang, dan tekan ikuti (follow) untuk menyimak sambungan penyejuk jiwa di part selanjutnya ✨"

    # SLIDE 3: Riwayat Hadits diletakkan mengalir tepat di bawah matan (tidak terlalu bawah)
    if is_slide_3 and riwayat_text:
        y_riwayat = curr_y_body_end + 45
        draw_text_with_shadow(draw, (540, y_riwayat), f"Riwayat {riwayat_text}", font_r, text_color="#fef08a", shadow_color="#000000", shadow_offset=3)
    
    # SLIDE 5: CTA diletakkan mengalir tepat di bawah kalimat perenungan (bebas bentrok/menumpuk)
    elif is_slide_5 and cta_text:
        cta_lines = wrap_text(cta_text, font_r, 880, draw)
        curr_y_cta = curr_y_body_end + 50
        for line in cta_lines:
            draw_text_with_shadow(draw, (540, curr_y_cta), line, font_r, text_color="#fef08a", shadow_color="#000000", shadow_offset=3)
            curr_y_cta += size_r + 10

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
