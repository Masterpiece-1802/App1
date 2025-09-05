# 🎨 VerseCraft - Shayari & Poetry Creator

A beautiful web application for creating, designing, and sharing shayaris and poetry with stunning visual backgrounds and customizable text styling.

🌐 **Live Demo:** [verse-craft.pages.dev](https://verse-craft.pages.dev)

---

## ✨ Features

### 🖌️ Creative Tools

- **Multiple Themes:** Default, Romantic, Sad, Motivational
- **Background Selection:** Unique backgrounds for each theme
- **Font Customization:** Fonts like Dancing Script, Great Vibes, Parisienne, Arial
- **Text Formatting:** Bold, italic, and underline support
- **Color Picker:** 8 text colors with gradient previews
- **Text Positioning:** Fine-tune text placement with arrow controls

### 💡 User Experience

- **Real-time Preview:** Instantly see your changes
- **Auto-save:** Drafts saved automatically
- **Responsive Design:** Works on desktop, tablet, and mobile
- **Dark/Light Mode:** Easy theme toggle
- **Emoji Support:** Add emojis with an integrated picker

### 📦 Storage & Management

- **Local Storage:** Creations saved in browser
- **Search & Filter:** Find shayaris by text, theme, or tags
- **Recent Items:** Quick access to latest work
- **Copy Functionality:** Copy one or multiple shayaris

### 📤 Export & Sharing

- **Image Generation:** Download as 1080x1920 high-quality images
- **Social Sharing:** Share to Facebook, Twitter, WhatsApp, Instagram
- **Text-to-Speech:** Listen to your shayaris aloud
- **Copy to Clipboard:** Share text easily anywhere

---

## 🚀 How to Use

1. **Create:** Type your shayari in the text area
2. **Customize:**
   - Select a theme matching your mood
   - Pick a background image
   - Choose fonts, colors, and formatting
   - Adjust text position if needed
3. **Preview:** Watch your creation in real time
4. **Save:** Store your shayari in the collection
5. **Share:** Download as image, share on social media, or copy text

---

## 🛠️ Technical Architecture

### Frontend (Cloudflare Pages)

- **HTML5:** Semantic markup
- **CSS3:** Gradients, animations, responsive design
- **JavaScript (ES6+):** localStorage API & modern DOM
- **Bootstrap 5:** Responsive grid and components
- **html2canvas:** Client-side image generation
- **Emoji Picker:** Integrated emoji selection

### Backend (Flask - PythonAnywhere)

- **Image Generation:** Server-side high-quality rendering
- **Background Management:** Multiple theme-based backgrounds
- **Font Handling:** Custom fonts with proper rendering
- **Persistence Storage:** SQLite for storing shayaris
- **API Endpoints:** RESTful operations
- **CORS Handling:** Secure communication between frontend & backend

---

## 🔌 APIs Used

- **Unsplash:** High-quality backgrounds
- **Google Fonts:** Typography options
- **Web Speech API:** Text-to-speech

---

## 🔧 Backend API Endpoints

- `GET /api/backgrounds` → Available backgrounds by theme
- `GET /api/fonts` → Available fonts
- `GET /api/posts` → All posts with optional filters
- `POST /api/posts` → Add a new post
- `GET /api/search` → Search posts with filters
- `POST /api/generate-image` → Generate and download image

---

## 🎨 Customization

### Adding New Backgrounds

1. Add images to `backgrounds/`
2. Update `get_available_backgrounds()` in `app.py`
3. Add CSS rules for new themes in `style.css`

### Adding New Fonts

1. Add font files to `fonts/`
2. Update `get_available_fonts()` in `app.py`
3. Add font classes in `style.css`

### Modifying Themes

- Edit **CSS custom properties** in `:root` and `[data-theme="dark"]` sections

---

## 📝 Why Python Backend?

- **High-Quality Rendering:** Consistent images across devices
- **Advanced Text Processing:** Handles wrapping, fonts, shadows
- **Background Management:** Dynamic theme-based assets
- **Persistence:** Database storage with search & filters
- **CORS Support:** Secure cross-origin requests

---

## 🔧 Installation (Local Development)

### 1. Clone & Setup

git clone https://github.com/your-username/verse-craft.git
cd verse-craft

### 2. Setup Python Backend

python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py

### 3. Run Frontend

# Using Python’s built-in server

python -m http.server 8000

# 🙏 Acknowledgments

- Unsplash → Background images
- Google Fonts → Typography
- Font Awesome → Icons
- Emoji Picker Element → Emoji integration

# 🌟 VerseCraft: **Where words meet beauty. Create, share, and inspire with beautifully crafted shayaris and poetry.**
