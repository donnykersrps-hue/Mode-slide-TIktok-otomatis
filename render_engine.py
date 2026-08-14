import io
import zipfile
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def get_remote_font(font_url, size):
    """Mendownload font TTF berkualitas HD agar tidak menggunakan font default Pillow yang kerdil"""
    try:
        res = requests.get(font_url, timeout=5)
        if res.status_code == 200:
            return ImageFont.truetype(io.BytesIO(res.content), size=size)
    except Exception:
        pass
    return ImageFont.load_default()

def fetch_background_image(pexels_key="", keyword="nature aesthetic calm"):
    """Mengambil gambar background HD bertema alam/estetis dari Pexels API"""
    if pexels_key:
        url = f"https://api.pexels.com/v1/search?query={keyword}&per_page=10&orientation=portrait"
        headers = {"Authorization": pexels_key}
        try:
            res = requests.get(url, headers=headers, timeout=5)
            if res.status_code == 200:
                photos = res.json().get("photos", [])
                if photos:
                    import random
                    photo = random.choice(photos)
                    img_url = photo["src"]["portrait"]
                    img_res = requests.get(img_url, timeout=5)
                    img = Image.open(io.BytesIO(img_res.content)).convert("RGB")
                    return img.resize((1080, 1920))
        except Exception:
            pass
    
    # Fallback Canvas Gelap Estetis
    return Image.new('RGB', (1080, 1920), color=(15, 23, 42))

def draw_heavy_shadow_text(draw, position, text, font, font_color, shadow_color=(0, 0, 0, 230), radius=8):
    """
    Menghasilkan efek Outer Shadow / Glow tebal pekat melingkar
    persis seperti pada sampel contoh Kak Donny
    """
    x, y = position
    # Draw Radial Shadow Multi-Layer
    for dx in range(-radius, radius + 1, 2):
        for dy in range(-radius, radius + 1, 2):
            if dx*dx + dy*dy <= radius*radius:
                draw.text((x + dx, y + dy), text, font=font, fill=shadow_color, anchor="mm")
    
    # Draw Core Text
    draw.text((x, y), text, font=font, fill=font_color, anchor="mm")

def wrap_text(text, font, max_width, draw):
    """Memecah kalimat panjang agar pas berada di tengah layar HP secara simetris"""
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        try:
            bbox = draw.textbbox((0, 0), test_line, font=font)
            w = bbox[2] - bbox[0]
        except Exception:
            w = len(test_line) * 20
            
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
    Core Canvas Renderer Perfeksionis (Presisi Sampel Kak Donny):
    - Header: Magenta / Emas (#d946ef / #facc15)
    - Body: Cyan / Emas Italic (#22d3ee)
    - Drop Shadow Tebal Pekat
    """
    canvas = bg_image.copy().filter(ImageFilter.GaussianBlur(radius=1))
    
    # Dark Vignette Soft Overlay
    overlay = Image.new('RGBA', (1080, 1920), (0, 0, 0, 85))
    canvas.paste(overlay, (0, 0), overlay)
    
    draw = ImageDraw.Draw(canvas)
    
    # Load Font HD dari CDN Google Fonts
    font_bold_url = "https://github.com/google/fonts/raw/main/ofl/montserrat/Montserrat-ExtraBold.ttf"
    font_italic_url = "https://github.com/google/fonts/raw/main/ofl/montserrat/Montserrat-BoldItalic.ttf"
    
    font_header = get_remote_font(font_bold_url, 66)
    font_body = get_remote_font(font_italic_url, 52)
    font_riwayat = get_remote_font(font_italic_url, 46)

    # 1. RENDER HEADER (TOP AREA) - Magenta (#e0e7ff / #c084fc / #f3e8ff)
    header_text = slide_data.get("header", "").upper()
    
    # Jika Slide 5 (Closing), Pakai Kuning Emas
    header_color = (250, 204, 21) if is_slide_5 else (216, 180, 254) # Magenta Muda / Emas
    
    header_lines = wrap_text(header_text, font_header, 880, draw)
    y_start_header = 400
    for line in header_lines:
        draw_heavy_shadow_text(draw, (540, y_start_header), line, font_header, font_color=header_color, radius=10)
        y_start_header += 85

    # 2. RENDER BODY TEXT (CENTER AREA) - Warna Cyan (#22d3ee)
    body_text = slide_data.get("isi", "")
    body_color = (34, 211, 238) # Cyan Menyala
    
    body_lines = wrap_text(body_text, font_body, 860, draw)
    y_start_body = 1000
    for line in body_lines:
        draw_heavy_shadow_text(draw, (540, y_start_body), line, font_body, font_color=body_color, radius=8)
        y_start_body += 75

    # 3. RENDER RIWAYAT HADITS SHAHIH (KHUSUS SLIDE 3 - AREA BWAH)
    if is_slide_3 and "riwayat" in slide_data:
        riwayat_text = f"Riwayat\n{slide_data['riwayat']}"
        riwayat_lines = wrap_text(riwayat_text, font_riwayat, 840, draw)
        y_start_riwayat = y_start_body + 90
        for line in riwayat_lines:
            draw_heavy_shadow_text(draw, (540, y_start_riwayat), line, font_riwayat, font_color=(254, 240, 138), radius=8)
            y_start_riwayat += 60

    return canvas

def generate_carousel_pack(slides_list, pexels_key=""):
    """
    Merender 5 Slide Gambar secara paralel dan membungkusnya ke file ZIP
    """
    rendered_images = []
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
        for idx, slide in enumerate(slides_list):
            is_s3 = (idx == 2) # Index 2 adalah Slide 3
            is_s5 = (idx == 4) # Index 4 adalah Slide 5
            
            # Fetch Background Beda-Beda Tiap Slide
            bg_img = fetch_background_image(pexels_key=pexels_key, keyword="nature aesthetic calm")
            slide_img = render_single_slide_image(bg_img, slide, is_slide_3=is_s3, is_slide_5=is_s5)
            
            img_byte_arr = io.BytesIO()
            slide_img.save(img_byte_arr, format='JPEG', quality=95)
            img_bytes = img_byte_arr.getvalue()
            
            rendered_images.append(slide_img)
            zip_file.writestr(f"Slide_{idx+1}.jpg", img_bytes)
            
    return rendered_images, zip_buffer.getvalue()
