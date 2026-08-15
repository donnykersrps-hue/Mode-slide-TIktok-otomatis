import io
import zipfile
import requests
import random
import re
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageStat, ImageEnhance

# --- FUNGSI SANITIZER TEKS (CLEANER SIMBOL ANEH) ---

def clean_text_from_symbols(text):
    """
    PEMBERSIH SIMBOL ANEH:
    Menghapus simbol non-standard, emoji rusak, atau karakter unicode anomali.
    """
    if not text:
        return ""
    cleaned = re.sub(r'[^\w\s\d\.,!\?\'"\(\)\-:]', '', text)
    return cleaned.strip()

# --- FUNGSI QUALITY CONTROL (BRIGHTNESS & ESTETIKA) ---

def is_image_too_dark(img, threshold=85):
    """QUALITY CONTROL 1: Mengukur rata-rata tingkat terang (luminance) gambar."""
    grayscale = img.convert('L')
    stat = ImageStat.Stat(grayscale)
    avg_brightness = stat.mean[0]
    return avg_brightness < threshold

def apply_bright_vibrant_filter(img):
    """QUALITY CONTROL 2: Filter Bright & Vibrant Presisi"""
    enhancer_bright = ImageEnhance.Brightness(img)
    img = enhancer_bright.enhance(1.15)
    
    enhancer_col = ImageEnhance.Color(img)
    img = enhancer_col.enhance(1.40)
    
    enhancer_con = ImageEnhance.Contrast(img)
    img = enhancer_con.enhance(1.25)
    
    return img

def fetch_bright_aesthetic_background(pexels_key=""):
    """QUALITY CONTROL 3: Mengambil gambar latar cerah dari Pexels API."""
    bright_keywords = [
        "bright sunrise nature landscape",
        "golden hour aesthetic nature",
        "bright sunny daylight nature",
        "beautiful bright sky landscape",
        "sunny nature background portrait",
        "vibrant daylight landscape"
    ]
    
    if pexels_key:
        keyword = random.choice(bright_keywords)
        url = f"https://api.pexels.com/v1/search?query={keyword}&per_page=20&orientation=portrait"
        headers = {"Authorization": pexels_key}
        try:
            res = requests.get(url, headers=headers, timeout=5)
            if res.status_code == 200:
                photos = res.json().get("photos", [])
                if photos:
                    random.shuffle(photos)
                    for photo in photos:
                        img_url = photo["src"]["portrait"]
                        img_res = requests.get(img_url, timeout=5)
                        img = Image.open(io.BytesIO(img_res.content)).convert("RGB")
                        img_resized = img.resize((1080, 1920))
                        
                        if is_image_too_dark(img_resized, threshold=90):
                            return apply_bright_vibrant_filter(img_resized)
                        else:
                            enhancer_col = ImageEnhance.Color(img_resized)
                            return enhancer_col.enhance(1.2)
        except Exception:
            pass
    
    fallback = Image.new('RGB', (1080, 1920), color=(251, 191, 36))
    enhancer_fallback = ImageEnhance.Color(fallback)
    return enhancer_fallback.enhance(1.3)

# --- FUNGSI TIPOGRAFI & RENDER SLIDE PERFEKSIONIS ---

def load_robust_large_font(size):
    """QUALITY CONTROL 4: Memuat font TTF tebal berukuran Dinamis."""
    font_paths = [
        "/usr/share/fonts/truetype/montserrat/Montserrat-ExtraBold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "DejaVuSans-Bold.ttf"
    ]
    for path in font_paths:
        try:
            return ImageFont.truetype(path, size=size)
        except Exception:
            continue
            
    return ImageFont.load_default()

def draw_perfeksionis_heavy_shadow_text(draw, position, text, font, font_color, shadow_color=(0, 0, 0, 255), radius=14):
    """QUALITY CONTROL 5: Radial Multi-Pass Shadow Super Pekat"""
    x, y = position
    for dx in range(-radius, radius + 1, 3):
        for dy in range(-radius, radius + 1, 3):
            if dx*dx + dy*dy <= radius*radius:
                draw.text((x + dx, y + dy), text, font=font, fill=shadow_color, anchor="mm")
    
    draw.text((x, y), text, font=font, fill=font_color, anchor="mm")

def wrap_text_simetris(text, font, max_width, draw):
    """Memecah kalimat agar rapi, simetris, dan seimbang di tengah layar HP."""
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        try:
            bbox = draw.textbbox((0, 0), test_line, font=font)
            w = bbox[2] - bbox[0]
        except Exception:
            w = len(test_line) * 24
            
        if w <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    return lines

def render_single_slide_image(bg_image, slide_data, is_slide_3=False, is_slide_5=False):
    """
    Core Canvas Renderer Perfeksionis dengan UKURAN FONT CYAN JUMBO
    Ramah untuk audiens dewasa & orang tua.
    """
    canvas = bg_image.copy()
    
    # Dark Overlay Tipis (45/255)
    overlay = Image.new('RGBA', (1080, 1920), (0, 0, 0, 45))
    canvas.paste(overlay, (0, 0), overlay)
    
    draw = ImageDraw.Draw(canvas)
    
    raw_header = slide_data.get("header", "").upper()
    header_text = clean_text_from_symbols(raw_header)
    
    raw_body = slide_data.get("isi", "")
    body_text = clean_text_from_symbols(raw_body)
    
    # AUTO-SCALER DENGAN FONT JUMBO UNTUK BACAAN ORANG TUA
    if is_slide_3 or len(body_text) > 100:
        size_header = 70
        size_body = 52       # Ditingkatkan dari 42px ke 52px
        size_riwayat = 42
        y_start_header = 320
        y_start_body = 720
        line_spacing_header = 85
        line_spacing_body = 72
    else:
        size_header = 80
        size_body = 68       # Ditingkatkan dari 56px ke 68px (SANGAT JELAS)
        size_riwayat = 48
        y_start_header = 380
        y_start_body = 920
        line_spacing_header = 100
        line_spacing_body = 90

    font_header = load_robust_large_font(size=size_header)
    font_body = load_robust_large_font(size=size_body)
    font_riwayat = load_robust_large_font(size=size_riwayat)

    # 1. RENDER HEADER (TOP AREA)
    header_color = (250, 204, 21) if is_slide_5 else (232, 121, 249) # Emas / Magenta
    header_lines = wrap_text_simetris(header_text, font_header, 920, draw)
    
    for line in header_lines:
        draw_perfeksionis_heavy_shadow_text(draw, (540, y_start_header), line, font_header, font_color=header_color, radius=14)
        y_start_header += line_spacing_header

    # 2. RENDER BODY TEXT (CENTER AREA) - Cyan Bright JUMBO
    body_color = (34, 211, 238) # Cyan Bright (#22d3ee)
    body_lines = wrap_text_simetris(body_text, font_body, 900, draw)
    
    for line in body_lines:
        draw_perfeksionis_heavy_shadow_text(draw, (540, y_start_body), line, font_body, font_color=body_color, radius=14)
        y_start_body += line_spacing_body

    # 3. RENDER RIWAYAT HADITS SHAHIH (KHUSUS SLIDE 3)
    if is_slide_3 and "riwayat" in slide_data:
        raw_riwayat = slide_data['riwayat']
        clean_riwayat = clean_text_from_symbols(raw_riwayat)
        riwayat_text = f"Riwayat\n{clean_riwayat}"
        
        riwayat_lines = wrap_text_simetris(riwayat_text, font_riwayat, 880, draw)
        y_start_riwayat = min(y_start_body + 40, 1450)
        
        for line in riwayat_lines:
            draw_perfeksionis_heavy_shadow_text(draw, (540, y_start_riwayat), line, font_riwayat, font_color=(254, 240, 138), radius=10)
            y_start_riwayat += 55

    return canvas

# --- FUNGSI UTAMA GENERATE CAROUSEL PACK ---

def generate_carousel_pack(slides_list, pexels_key=""):
    """Fungsi Utama: Merender 5 Slide Gambar secara paralel dengan Font Jumbo."""
    rendered_images = []
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
        for idx, slide in enumerate(slides_list):
            is_s3 = (idx == 2)
            is_s5 = (idx == 4)
            
            bg_img = fetch_bright_aesthetic_background(pexels_key=pexels_key)
            slide_img = render_single_slide_image(bg_img, slide, is_slide_3=is_s3, is_slide_5=is_s5)
            
            img_byte_arr = io.BytesIO()
            slide_img.save(img_byte_arr, format='JPEG', quality=98)
            img_bytes = img_byte_arr.getvalue()
            
            rendered_images.append(slide_img)
            zip_file.writestr(f"Slide_{idx+1}.jpg", img_bytes)
            
    return rendered_images, zip_buffer.getvalue()
