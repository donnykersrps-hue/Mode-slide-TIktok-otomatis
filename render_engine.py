import io
import zipfile
import requests
import random
import re
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageStat, ImageEnhance

# --- FUNGSI SANITIZER TEKS (CLEANER SIMBOL ANEH) ---

def clean_text_from_symbols(text):
    """
    PEMBERSIH KARTU/SIMBOL ANEH:
    Menghapus simbol non-standard, emoji rusak, atau karakter unicode anomali
    agar hasil cetak teks header & body murni, bersih, dan elegan.
    """
    if not text:
        return ""
    # Menghapus emoji & simbol unicode khusus yang berpotensi jadi kotak rusak di font
    cleaned = re.sub(r'[^\w\s\d\.,!\?\'"\(\)\-:]', '', text)
    return cleaned.strip()

# --- FUNGSI QUALITY CONTROL (BRIGHTNESS & ESTETIKA) ---

def is_image_too_dark(img, threshold=85):
    """
    QUALITY CONTROL 1: Mengukur rata-rata tingkat terang (luminance) gambar.
    """
    grayscale = img.convert('L')
    stat = ImageStat.Stat(grayscale)
    avg_brightness = stat.mean[0]
    return avg_brightness < threshold

def apply_bright_vibrant_filter(img):
    """
    QUALITY CONTROL 2: Filter Bright & Vibrant Presisi
    - Brightness: +70%
    - Saturation: +40%
    - Contrast: +25%
    """
    # 1. Kecerahan +15%
    enhancer_bright = ImageEnhance.Brightness(img)
    img = enhancer_bright.enhance(1.15)
    
    # 2. Saturasi Warna +40%
    enhancer_col = ImageEnhance.Color(img)
    img = enhancer_col.enhance(1.40)
    
    # 3. Kontras +25%
    enhancer_con = ImageEnhance.Contrast(img)
    img = enhancer_con.enhance(1.25)
    
    return img

def fetch_bright_aesthetic_background(pexels_key=""):
    """
    QUALITY CONTROL 3: Mengambil gambar latar cerah, indah, dan estetis dari Pexels API.
    """
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
                        
                        # Jika agak gelap, langsung berikan Enhancer Brightness & Saturation
                        if is_image_too_dark(img_resized, threshold=90):
                            return apply_bright_vibrant_filter(img_resized)
                        else:
                            enhancer_col = ImageEnhance.Color(img_resized)
                            return enhancer_col.enhance(1.2)
        except Exception:
            pass
    
    # Fallback Canvas Cerah Warm Gradient jika Pexels offline
    fallback = Image.new('RGB', (1080, 1920), color=(251, 191, 36))
    enhancer_fallback = ImageEnhance.Color(fallback)
    return enhancer_fallback.enhance(1.3)

# --- FUNGSI TIPOGRAFI & RENDER SLIDE ---

def load_robust_large_font(size):
    """
    QUALITY CONTROL 4: Memuat font TTF tebal berukuran BESAR (70-85px).
    """
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

def draw_perfeksionis_heavy_shadow_text(draw, position, text, font, font_color, shadow_color=(0, 0, 0, 255), radius=15):
    """
    QUALITY CONTROL 5: Radial Multi-Pass Shadow Super Pekat
    Menjamin teks menyala tajam dan terbaca sempurna di atas background cerah.
    """
    x, y = position
    for dx in range(-radius, radius + 1, 3):
        for dy in range(-radius, radius + 1, 3):
            if dx*dx + dy*dy <= radius*radius:
                draw.text((x + dx, y + dy), text, font=font, fill=shadow_color, anchor="mm")
    
    # Draw Core Main Text
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
            w = len(test_line) * 25
            
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
    Core Canvas Renderer Perfeksionis:
    - Overlay Hitam Tipis (45/255) agar Background Cerah Tetap Bening
    - Teks Bersih Murni Bebas Simbol Aneh
    """
    canvas = bg_image.copy()
    
    # Dark Overlay Tipis Presisi (Hanya 45/255)
    overlay = Image.new('RGBA', (1080, 1920), (0, 0, 0, 45))
    canvas.paste(overlay, (0, 0), overlay)
    
    draw = ImageDraw.Draw(canvas)
    
    font_header = load_robust_large_font(size=76)
    font_body = load_robust_large_font(size=58)
    font_riwayat = load_robust_large_font(size=48)

    # 1. RENDER HEADER (TOP AREA) - Bersih Tanpa Simbol Aneh
    raw_header = slide_data.get("header", "").upper()
    header_text = clean_text_from_symbols(raw_header)
    
    header_color = (250, 204, 21) if is_slide_5 else (232, 121, 249) # Emas / Magenta
    
    header_lines = wrap_text_simetris(header_text, font_header, 920, draw)
    y_start_header = 420
    for line in header_lines:
        draw_perfeksionis_heavy_shadow_text(draw, (540, y_start_header), line, font_header, font_color=header_color, radius=15)
        y_start_header += 95

    # 2. RENDER BODY TEXT (CENTER AREA) - Cyan Bright Menyala
    raw_body = slide_data.get("isi", "")
    body_text = clean_text_from_symbols(raw_body)
    body_color = (34, 211, 238) # Cyan Bright (#22d3ee)
    
    body_lines = wrap_text_simetris(body_text, font_body, 900, draw)
    y_start_body = 1000
    for line in body_lines:
        draw_perfeksionis_heavy_shadow_text(draw, (540, y_start_body), line, font_body, font_color=body_color, radius=12)
        y_start_body += 80

    # 3. RENDER RIWAYAT HADITS SHAHIH (KHUSUS SLIDE 3)
    if is_slide_3 and "riwayat" in slide_data:
        raw_riwayat = slide_data['riwayat']
        clean_riwayat = clean_text_from_symbols(raw_riwayat)
        riwayat_text = f"Riwayat\n{clean_riwayat}"
        
        riwayat_lines = wrap_text_simetris(riwayat_text, font_riwayat, 880, draw)
        y_start_riwayat = y_start_body + 110
        for line in riwayat_lines:
            draw_perfeksionis_heavy_shadow_text(draw, (540, y_start_riwayat), line, font_riwayat, font_color=(254, 240, 138), radius=10)
            y_start_riwayat += 65

    return canvas

# --- FUNGSI UTAMA GENERATE CAROUSEL PACK ---

def generate_carousel_pack(slides_list, pexels_key=""):
    """
    Fungsi Utama: Merender 5 Slide Gambar secara paralel dengan Mesin Quality Control.
    """
    rendered_images = []
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
        for idx, slide in enumerate(slides_list):
            is_s3 = (idx == 2) # Index 2 adalah Slide 3
            is_s5 = (idx == 4) # Index 4 adalah Slide 5
            
            bg_img = fetch_bright_aesthetic_background(pexels_key=pexels_key)
            slide_img = render_single_slide_image(bg_img, slide, is_slide_3=is_s3, is_slide_5=is_s5)
            
            img_byte_arr = io.BytesIO()
            slide_img.save(img_byte_arr, format='JPEG', quality=98)
            img_bytes = img_byte_arr.getvalue()
            
            rendered_images.append(slide_img)
            zip_file.writestr(f"Slide_{idx+1}.jpg", img_bytes)
            
    return rendered_images, zip_buffer.getvalue()
