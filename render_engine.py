import io
import zipfile
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def fetch_background_image(pexels_key="", keyword="nature aesthetic calm"):
    """Mengambil gambar background HD bertema alam/estetis dari Pexels API"""
    if pexels_key:
        url = f"https://api.pexels.com/v1/search?query={keyword}&per_page=5&orientation=portrait"
        headers = {"Authorization": pexels_key}
        try:
            res = requests.get(url, headers=headers, timeout=5)
            if res.status_code == 200:
                photos = res.json().get("photos", [])
                if photos:
                    img_url = photos[0]["src"]["portrait"]
                    img_res = requests.get(img_url, timeout=5)
                    img = Image.open(io.BytesIO(img_res.content)).convert("RGB")
                    return img.resize((1080, 1920))
        except Exception:
            pass
    
    # Fallback Canvas Gelap jika API Key kosong atau timeout
    return Image.new('RGB', (1080, 1920), color=(15, 23, 42))

def draw_text_with_shadow(draw, position, text, font, font_color, shadow_color=(0, 0, 0), shadow_offset=4):
    """Menggambar teks dengan Outer Shadow/Glow tebal agar menyala tajam"""
    x, y = position
    for dx in range(-shadow_offset, shadow_offset + 1):
        for dy in range(-shadow_offset, shadow_offset + 1):
            if dx != 0 or dy != 0:
                draw.text((x + dx, y + dy), text, font=font, fill=shadow_color, anchor="mm")
    draw.text((x, y), text, font=font, fill=font_color, anchor="mm")

def wrap_text(text, font, max_width, draw):
    """Memecah kalimat panjang agar pas berada di tengah layar HP"""
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    return lines

def render_single_slide_image(bg_image, slide_data, is_slide_3=False):
    """
    Core Canvas Engine: Merender 1 Gambar Slide HD (1080x1920 px)
    Pola: Header Magenta/Emas, Body Cyan/Emas Italic + Drop Shadow
    """
    canvas = bg_image.copy().filter(ImageFilter.GaussianBlur(radius=2))
    
    # Dark Overlay (Vignette) agar teks kontras
    overlay = Image.new('RGBA', (1080, 1920), (0, 0, 0, 120))
    canvas.paste(overlay, (0, 0), overlay)
    
    draw = ImageDraw.Draw(canvas)
    
    # Font Loader
    try:
        font_header = ImageFont.truetype("DejaVuSans-Bold.ttf", 64)
        font_body = ImageFont.truetype("DejaVuSans-Oblique.ttf", 48)
        font_riwayat = ImageFont.truetype("DejaVuSans-BoldOblique.ttf", 42)
    except Exception:
        font_header = ImageFont.load_default()
        font_body = ImageFont.load_default()
        font_riwayat = ImageFont.load_default()

    # 1. RENDER HEADER (TOP AREA) - Warna Emas Mewah
    header_text = slide_data.get("header", "").upper()
    header_lines = wrap_text(header_text, font_header, 900, draw)
    
    y_start_header = 450
    for line in header_lines:
        draw_text_with_shadow(draw, (540, y_start_header), line, font_header, font_color=(234, 179, 8), shadow_offset=5)
        y_start_header += 75

    # 2. RENDER BODY TEXT (CENTER AREA) - Warna Cyan
    body_text = slide_data.get("isi", "")
    body_lines = wrap_text(body_text, font_body, 880, draw)
    
    y_start_body = 950
    for line in body_lines:
        draw_text_with_shadow(draw, (540, y_start_body), line, font_body, font_color=(34, 211, 238), shadow_offset=4)
        y_start_body += 65

    # 3. RENDER RIWAYAT HADITS SHAHIH (KHUSUS SLIDE 3)
    if is_slide_3 and "riwayat" in slide_data:
        riwayat_text = f"Riwayat\n{slide_data['riwayat']}"
        riwayat_lines = wrap_text(riwayat_text, font_riwayat, 850, draw)
        y_start_riwayat = y_start_body + 100
        for line in riwayat_lines:
            draw_text_with_shadow(draw, (540, y_start_riwayat), line, font_riwayat, font_color=(254, 240, 138), shadow_offset=4)
            y_start_riwayat += 55

    return canvas

def generate_carousel_pack(slides_list, pexels_key=""):
    """
    Fungsi Utama: Merender 5 Slide Gambar sekaligus dan membungkusnya ke file ZIP
    """
    bg_img = fetch_background_image(pexels_key=pexels_key, keyword="calm nature aesthetic")
    rendered_images = []
    
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
        for idx, slide in enumerate(slides_list):
            is_s3 = (idx == 2) # Index 2 adalah Slide 3 (Hadits Shahih)
            slide_img = render_single_slide_image(bg_img, slide, is_slide_3=is_s3)
            
            img_byte_arr = io.BytesIO()
            slide_img.save(img_byte_arr, format='JPEG', quality=95)
            img_bytes = img_byte_arr.getvalue()
            
            rendered_images.append(slide_img)
            zip_file.writestr(f"Slide_{idx+1}.jpg", img_bytes)
            
    return rendered_images, zip_buffer.getvalue()
