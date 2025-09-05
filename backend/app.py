import os
import random
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import database
from PIL import Image, ImageDraw, ImageFont
import textwrap
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Get the base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Create directories if they don't exist
os.makedirs(os.path.join(BASE_DIR, 'generated'), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'backgrounds'), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'fonts'), exist_ok=True)

# Get available backgrounds for each theme
def get_available_backgrounds():
    backgrounds = {
        'default': [],
        'romantic': [],
        'sad': [],
        'motivational': []
    }
    
    try:
        bg_files = os.listdir(os.path.join(BASE_DIR, 'backgrounds'))
        for file in bg_files:
            if file.endswith(('.jpg', '.jpeg', '.png')):
                theme = file.split('.')[0].rstrip('0123456789')
                if theme in backgrounds:
                    backgrounds[theme].append(file)
        
        # If no specific backgrounds found, use default for all
        if not any(backgrounds.values()):
            for theme in backgrounds:
                backgrounds[theme].append('default.jpg')
                
    except Exception as e:
        print(f"Error loading backgrounds: {e}")
        for theme in backgrounds:
            backgrounds[theme].append('default.jpg')
            
    return backgrounds

# Get available fonts
def get_available_fonts():
    fonts = {
        'DancingScript': 'DancingScript-Regular.ttf',
        'GreatVibes': 'GreatVibes-Regular.ttf', 
        'Parisienne': 'Parisienne-Regular.ttf',
        'Arial': 'arial.ttf'
    }
    
    # Check which fonts are actually available
    available_fonts = {}
    for name, filename in fonts.items():
        font_path = os.path.join(BASE_DIR, 'fonts', filename)
        if os.path.exists(font_path) or filename == 'arial.ttf':
            available_fonts[name] = filename
            
    return available_fonts

# Serve static files (background images)
@app.route('/static/backgrounds/<path:filename>')
def serve_background(filename):
    return send_file(os.path.join(BASE_DIR, 'backgrounds', filename))

@app.route('/')
def home():
    return "VerseCraft API is running!"

@app.route('/api/backgrounds', methods=['GET'])
def get_backgrounds():
    return jsonify(get_available_backgrounds())

@app.route('/api/fonts', methods=['GET'])
def get_fonts():
    return jsonify(list(get_available_fonts().keys()))

@app.route('/api/posts', methods=['GET'])
def get_posts():
    theme_filter = request.args.get('theme', '')
    tag_filter = request.args.get('tag', '')
    sort_by = request.args.get('sort', 'date_desc')
    
    posts = database.get_all_posts(theme_filter, tag_filter, sort_by)
    return jsonify([{'id': post[0], 'content': post[1], 'date': post[2], 'theme': post[3], 'tags': post[4]} for post in posts])

@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.json
    content = data.get('content', '')
    theme = data.get('theme', 'default')
    tags = data.get('tags', '')

    if content:
        database.add_post(content, theme, tags)
        return jsonify({'status': 'success', 'message': 'Post added successfully'})
    else:
        return jsonify({'status': 'error', 'message': 'Content is required'})

@app.route('/api/search', methods=['GET'])
def search_posts():
    query = request.args.get('q', '')
    theme_filter = request.args.get('theme', '')
    tag_filter = request.args.get('tag', '')
    sort_by = request.args.get('sort', 'date_desc')
    
    posts = database.search_posts(query, theme_filter, tag_filter, sort_by)
    return jsonify([{'id': post[0], 'content': post[1], 'date': post[2], 'theme': post[3], 'tags': post[4]} for post in posts])

@app.route('/api/generate-image', methods=['POST'])
def generate_image():
    data = request.json
    text = data.get('content', '')
    theme = data.get('theme', 'default')
    font_name = data.get('font', 'DancingScript')
    bg_image_name = data.get('bgImage', '')
    color_hex = data.get('color', '#ffffff')

    if not text:
        return jsonify({'status': 'error', 'message': 'Content is required'})

    # Convert hex to RGB
    try:
        color_hex = color_hex.lstrip('#')
        text_color = tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))
    except:
        text_color = (255, 255, 255)  # Fallback to white

    # Get background image
    available_backgrounds = get_available_backgrounds()
    bg_images = available_backgrounds.get(theme, [])
    
    if bg_image_name and bg_image_name in bg_images:
        bg_filename = bg_image_name
    elif bg_images:
        bg_filename = random.choice(bg_images)
    else:
        bg_filename = 'default.jpg'
    
    bg_path = os.path.join(BASE_DIR, 'backgrounds', bg_filename)

    # Create image with Instagram Reel dimensions (1080x1920)
    try:
        bg_image = Image.open(bg_path)
        bg_image = bg_image.resize((1080, 1920))
    except Exception as e:
        print(f"Error loading background: {e}")
        # Fallback to a solid color background
        bg_image = Image.new('RGB', (1080, 1920), color='#000000')

    draw = ImageDraw.Draw(bg_image)

    # Get font
    available_fonts = get_available_fonts()
    font_file = available_fonts.get(font_name, available_fonts.get('DancingScript', 'arial.ttf'))
    
    if font_file != 'arial.ttf':
        font_path = os.path.join(BASE_DIR, 'fonts', font_file)
    else:
        font_path = 'arial.ttf'

    # Calculate optimal font size based on text length
    font_size = 100  # Increased base font size
    
    # Adjust font size based on text length
    text_length = len(text)
    if text_length > 300:
        font_size = 60
    elif text_length > 200:
        font_size = 70
    elif text_length > 100:
        font_size = 80
    
    # Load font
    try:
        font = ImageFont.truetype(font_path, font_size)
    except:
        try:
            font = ImageFont.truetype('arial.ttf', font_size)
        except:
            font = ImageFont.load_default()

    # Wrap text based on font size
    chars_per_line = max(15, min(25, 2000 // font_size))  # Dynamic line wrapping
    lines = textwrap.wrap(text, width=chars_per_line)

    # Calculate text position (centered)
    total_height = sum([draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1] + 20 for line in lines])
    y_position = (1920 - total_height) / 2
    
    # Add text shadow for better readability (only if text color is light)
    shadow_offset = 2
    shadow_color = (0, 0, 0, 128)
    
    # If text is dark, use white shadow instead
    if sum(text_color) < 382:  # 382 is approximately 50% of 765 (255*3)
        shadow_color = (255, 255, 255, 128)
    
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        x_position = (1080 - width) / 2
        
        # Draw shadow
        draw.text((x_position + shadow_offset, y_position + shadow_offset), line, font=font, fill=shadow_color)
        # Draw main text
        draw.text((x_position, y_position), line, font=font, fill=text_color)
        
        y_position += height + 20

    # Save image
    filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    full_path = os.path.join(BASE_DIR, 'generated', filename)
    bg_image.save(full_path)

    return send_file(full_path, mimetype='image/png', as_attachment=True, download_name=f"verse-craft-{filename}")

if __name__ == '__main__':
    app.run(debug=True)