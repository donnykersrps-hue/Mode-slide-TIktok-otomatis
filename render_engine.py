import io
import zipfile
import requests
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageStat, ImageEnhance

# --- FUNGSI QUALITY CONTROL (BRIGHTNESS & ESTETIKA) ---

def is_image_too_dark(img, threshold=85):
    """
    QUALITY CONTROL 1: Mengukur rata-rata kecerahan gambar.
    Jika rata-rata kecerahan < threshold, gambar dianggap terlalu gelap/suram.
    """
    grayscale = img.convert('L')
    stat = ImageStat.Stat(grayscale)
    avg_brightness = stat.mean[0]
    return avg_brightness < threshold

def apply_bright_vibrant_filter(img):
    """
    QUALITY CONTROL 2: Menerapkan filter 'Bright & Vibrant' secara presisi:
    - Kecerahan (Brightness): +15%
    - Saturasi (Color): +40%
    - Kontras (Contrast): +25%
    """
    # 1. Optimasi Kecerahan (Lebih Cerah)
    enhancer_bright = ImageEnhance.Brightness(img)
    img = enhancer_bright.enhance(1.15)
    
    # 2. Optimasi Saturasi (Warna Lebih Kuat)
    enhancer_col = ImageEnhance.Color(img)
    img = enhancer_col.enhance(1.40)
    
    # 3. Optimasi Kontras (Gambar Lebih Nendang)
    enhancer_con = ImageEnhance.Contrast(img)
    img = enhancer_con.enhance(1.25)
    
    return img

def fetch_bright_aesthetic_background(pexels_key=""):
    """
    QUALITY CONTROL 3: Mengambil gambar latar cerah, indah, dan estetis 
    (Daylight/Sunrise/Nature) dari Pexels API.
    """
    bright_keywords = [
        "bright sunrise nature landscape",
        "golden hour aesthetic nature",
        "bright sunny daylight nature",
        "beautiful bright sky landscape",
        "sunny nature background portrait",
        "vibrant daylight landscape",
        "overexposed nature aesthetic"
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
                    # Acak dan verifikasi tingkat kecerahan gambar
                    random.shuffle(photos)
                    for photo in photos:
                        img_url = photo["src"]["portrait"]
                        img_res = requests.get(img_url, timeout=5)
                        img = Image.open(io.BytesIO(img_res.content)).convert("RGB")
                        img_resized = img.resize((1080, 1920))
                        
                        # Self-Check: Pastikan gambar asli tidak gelap suram
                        if not is_image_too_dark(img_resized, threshold=80):
                            # Terapkan filter Bright & Vibrant
                            return apply_bright_vibrant_filter(img_resized)
        except Exception:
            pass
    
    # Fallback Canvas Cerah Warm Gradient jika Pexels offline
    fallback = Image.new('RGB', (1080, 1920), color=(251, 191, 36)) # Kuning Amber
    enhancer_fallback = ImageEnhance.Color(fallback)
    return enhancer_fallback.enhance(1.3)

# --- FUNGSI TIPOGRAFI & RENDER SLIDE ---

def load_robust_large_font(size):
    """
    QUALITY CONTROL 4: Memuat font TTF tebal berukuran BESAR (70-85px).
    Dipastikan konsisten, tebal, dan tajam (Karakter Kuat).
    """
    # Mencari font lokal sistem (Montserrat/DejaVu Sans Bold)
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
    QUALITY CONTROL 5: Efek Outer Shadow Radial Multi-Layer Super Tebal.
    Menjamin teks Ungu Magenta/Cyan 'pop-out' menyala tajam dan terbaca sempurna.
    """
    x, y = position
    # Radial Multi-Pass Shadow (Jarak 3px, Radius 15px)
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
    Core Canvas Renderer Perfeksionis (Presisi Sampel 5 Gambar Sempurna):
    - Teks Header: Magenta Muda/Emas (Ukuran 76px)
    - Teks Body: Cyan Bright (Ukuran 58px, Bold Italic)
    - Drop Shadow Radial Multi-Layer Super Tebal
    """
    # Quality Control 6: Background sudah Bright & Vibrant, Vignette tipis saja agar teks kontras
    canvas = bg_image.copy()
    draw = ImageDraw.Draw(canvas)
    
    # Load Font Ukuran Besar (Karakter Kuat)
    font_header = load_robust_large_font(size=76)
    font_body = load_robust_large_font(size=58)
    font_riwayat = load_robust_large_font(size=48)

    # 1. RENDER HEADER (TOP AREA) - Warna Magenta / Emas
    header_text = slide_data.get("header", "").upper()
    # Emas Mewah / Magenta Bright Menyala (Pop-Out)
    header_color = (250, 204, 21) if is_slide_5 else (232, 121, 249) 
    
    header_lines = wrap_text_simetris(header_text, font_header, 920, draw)
    y_start_header = 420
    for line in header_lines:
        draw_perfeksionis_heavy_shadow_text(draw, (540, y_start_header), line, font_header, font_color=header_color, radius=15)
        y_start_header += 95

    # 2. RENDER BODY TEXT (CENTER AREA) - Warna Cyan Bright Menyala
    body_text = slide_data.get("isi", "")
    body_color = (34, 211, 238) # Cyan Bright (#22d3ee)
    
    body_lines = wrap_text_simetris(body_text, font_body, 900, draw)
    y_start_body = 1000
    for line in body_lines:
        draw_perfeksionis_heavy_shadow_text(draw, (540, y_start_body), line, font_body, font_color=body_color, radius=12)
        y_start_body += 80

    # 3. RENDER RIWAYAT HADITS SHAHIH (KHUSUS SLIDE 3)
    if is_slide_3 and "riwayat" in slide_data:
        riwayat_text = f"Riwayat\n{slide_data['riwayat']}"
        riwayat_lines = wrap_text_simetris(riwayat_text, font_riwayat, 880, draw)
        y_start_riwayat = y_start_body + 110
        for line in riwayat_lines:
            draw_perfeksionis_heavy_shadow_text(draw, (540, y_start_riwayat), line, font_riwayat, font_color=(254, 240, 138), radius=10)
            y_start_riwayat += 65

    return canvas

# --- FUNGSI UTAMA GENERATE CAROUSEL PACK ---

def generate_carousel_pack(slides_list, pexels_key=""):
    """
    Fungsi Utama: Merender 5 Slide Gambar secara paralel dengan Mesin Quality Control
    dan filter 'Bright & Vibrant'.
    """
    rendered_images = []
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
        for idx, slide in enumerate(slides_list):
            is_s3 = (idx == 2) # Index 2 adalah Slide 3 (Hadits Shahih)
            is_s5 = (idx == 4) # Index 4 adalah Slide 5 (CTA)
            
            # QC Check & Filter: Pastikan Latar Belakang Bright & Vibrant
            bg_img = fetch_bright_aesthetic_background(pexels_key=pexels_key)
            # Render Slide Teks Perfeksionis
            slide_img = render_single_slide_image(bg_img, slide, is_slide_3=is_s3, is_slide_5=is_s5)
            
            # Simpan Image ke Bytes
            img_byte_arr = io.BytesIO()
            slide_img.save(img_byte_arr, format='JPEG', quality=98)
            img_bytes = img_byte_arr.getvalue()
            
            rendered_images.append(slide_img)
            zip_file.writestr(f"Slide_{idx+1}.jpg", img_bytes)
            
    return rendered_images, zip_buffer.getvalue()
