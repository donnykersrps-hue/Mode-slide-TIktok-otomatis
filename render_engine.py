import io
import zipfile
import requests
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageStat

def is_image_too_dark(img, threshold=80):
    """
    QUALITY CONTROL 1: Mengukur rata-rata kecerahan gambar.
    Jika rata-rata kecerahan < threshold, gambar dianggap terlalu gelap/suram.
    """
    grayscale = img.convert('L')
    stat = ImageStat.Stat(grayscale)
    avg_brightness = stat.mean[0]
    return avg_brightness < threshold

def fetch_bright_aesthetic_background(pexels_key=""):
    """
    QUALITY CONTROL 2: Mengambil gambar latar cerah, indah, dan estetis (Bright Daylight/Sunrise/Nature)
    """
    bright_keywords = [
        "bright sunrise nature landscape",
        "golden hour aesthetic nature",
        "bright sunny daylight nature",
        "beautiful bright sky landscape",
        "sunny nature background portrait"
    ]
    
    if pexels_key:
        keyword = random.choice(bright_keywords)
        url = f"https://api.pexels.com/v1/search?query={keyword}&per_page=15&orientation=portrait"
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
                        
                        # Self-Check: Pastikan gambar tidak gelap!
                        if not is_image_too_dark(img_resized, threshold=75):
                            return img_resized
        except Exception:
            pass
    
    # Fallback Canvas Cerah Warm Gradient jika Pexels offline
    fallback = Image.new('RGB', (1080, 1920), color=(251, 191, 36))
    return fallback

def load_robust_large_font(size):
    """
    QUALITY CONTROL 3: Memuat font TTF tebal berukuran BESAR (70-85px)
    Bebas dari error font default Pillow yang kerdil.
    """
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-BoldOblique.ttf",
        "DejaVuSans-Bold.ttf"
    ]
    for path in font_paths:
        try:
            return ImageFont.truetype(path, size=size)
        except Exception:
            continue
            
    # Fallback jika font lokal tidak terdeteksi
    try:
        url = "https://raw.githubusercontent.com/google/fonts/main/ofl/montserrat/Montserrat-ExtraBold.ttf"
        res = requests.get(url, timeout=3)
        if res.status_code == 200:
            return ImageFont.truetype(io.BytesIO(res.content), size=size)
    except Exception:
        pass
        
    return ImageFont.load_default()

def draw_heavy_shadow_text(draw, position, text, font, font_color, shadow_color=(0, 0, 0, 240), radius=12):
    """
    QUALITY CONTROL 4: Efek Outer Shadow / Glow Tebal Radial Pekat
    Menjamin teks menyala tajam di atas latar belakang apa pun.
    """
    x, y = position
    # Radial Multi-Pass Shadow
    for dx in range(-radius, radius + 1, 3):
        for dy in range(-radius, radius + 1, 3):
            if dx*dx + dy*dy <= radius*radius:
                draw.text((x + dx, y + dy), text, font=font, fill=shadow_color, anchor="mm")
    
    # Draw Core Main Text
    draw.text((x, y), text, font=font, fill=font_color, anchor="mm")

def wrap_text_simetris(text, font, max_width, draw):
    """Memecah kalimat agar rapi dan simetris di tengah layar HP"""
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
    - Ukuran Font Header: 76px (Magenta/Emas)
    - Ukuran Font Body: 58px (Cyan)
    - Posisional Presisi Sampel Kak Donny
    """
    canvas = bg_image.copy()
    
    # Soft Dark Vignette Overlay
    overlay = Image.new('RGBA', (1080, 1920), (0, 0, 0, 90))
    canvas.paste(overlay, (0, 0), overlay)
    
    draw = ImageDraw.Draw(canvas)
    
    # Load Font Ukuran Besar
    font_header = load_robust_large_font(size=76)
    font_body = load_robust_large_font(size=58)
    font_riwayat = load_robust_large_font(size=48)

    # 1. RENDER HEADER (TOP AREA) - Warna Magenta / Emas
    header_text = slide_data.get("header", "").upper()
    header_color = (250, 204, 21) if is_slide_5 else (232, 121, 249) # Emas / Magenta Bright
    
    header_lines = wrap_text_simetris(header_text, font_header, 920, draw)
    y_start_header = 420
    for line in header_lines:
        draw_heavy_shadow_text(draw, (540, y_start_header), line, font_header, font_color=header_color, radius=12)
        y_start_header += 95

    # 2. RENDER BODY TEXT (CENTER AREA) - Warna Cyan Menyala
    body_text = slide_data.get("isi", "")
    body_color = (34, 211, 238) # Cyan Bright
    
    body_lines = wrap_text_simetris(body_text, font_body, 900, draw)
    y_start_body = 1000
    for line in body_lines:
        draw_heavy_shadow_text(draw, (540, y_start_body), line, font_body, font_color=body_color, radius=10)
        y_start_body += 80

    # 3. RENDER RIWAYAT HADITS SHAHIH (KHUSUS SLIDE 3)
    if is_slide_3 and "riwayat" in slide_data:
        riwayat_text = f"Riwayat\n{slide_data['riwayat']}"
        riwayat_lines = wrap_text_simetris(riwayat_text, font_riwayat, 880, draw)
        y_start_riwayat = y_start_body + 100
        for line in riwayat_lines:
            draw_heavy_shadow_text(draw, (540, y_start_riwayat), line, font_riwayat, font_color=(254, 240, 138), radius=8)
            y_start_riwayat += 65

    return canvas

def generate_carousel_pack(slides_list, pexels_key=""):
    """
    Merender 5 Slide Gambar secara paralel dengan Mesin Quality Control
    """
    rendered_images = []
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
        for idx, slide in enumerate(slides_list):
            is_s3 = (idx == 2) # Index 2 adalah Slide 3
            is_s5 = (idx == 4) # Index 4 adalah Slide 5
            
            # QC Check Background Cerah
            bg_img = fetch_bright_aesthetic_background(pexels_key=pexels_key)
            slide_img = render_single_slide_image(bg_img, slide, is_slide_3=is_s3, is_slide_5=is_s5)
            
            img_byte_arr = io.BytesIO()
            slide_img.save(img_byte_arr, format='JPEG', quality=95)
            img_bytes = img_byte_arr.getvalue()
            
            rendered_images.append(slide_img)
            zip_file.writestr(f"Slide_{idx+1}.jpg", img_bytes)
            
    return rendered_images, zip_buffer.getvalue()
