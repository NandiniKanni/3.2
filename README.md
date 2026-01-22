# 🎬 AI Ad Video Generator

Transform product images into professional 30-second advertisement videos using AI!

## 🚀 Features

- ✅ **AI-Powered Script Generation** - Automatic voiceover script creation
- ✅ **Cinematic Animations** - 3D product rotations, zooms, effects
- ✅ **Professional Voiceover** - AI-generated natural speech
- ✅ **Multiple Scenes** - Hook, benefits, social proof, urgency, CTA
- ✅ **100% Free** - Uses only free APIs and tools
- ✅ **Easy to Use** - Simple drag-and-drop interface

## 📋 Prerequisites

### Free API Keys Required:

1. **Hugging Face API Key** (Required)
   - Sign up at: https://huggingface.co/join
   - Get your key: https://huggingface.co/settings/tokens
   - Click "New token" → Name it → Copy the token
   - **Limit:** 1000+ requests per day (FREE forever!)

2. **Pexels API Key** (Optional - for stock backgrounds)
   - Sign up at: https://www.pexels.com/api/new/
   - **Limit:** 200 requests per hour (FREE forever!)

## 🛠️ Installation

### Option 1: Local Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-ad-video-generator.git
cd ai-ad-video-generator

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Option 2: Deploy to Streamlit Cloud

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/ai-ad-video-generator.git
   git push -u origin main
   ```

2. **Deploy on Streamlit:**
   - Go to https://share.streamlit.io/
   - Click "New app"
   - Select your repository
   - Set main file: `app.py`
   - Click "Deploy"

3. **Add Secrets:**
   - In Streamlit Cloud dashboard → "Settings" → "Secrets"
   - Add your API keys:
   ```toml
   HUGGINGFACE_API_KEY = "hf_xxxxxxxxxxxxx"
   PEXELS_API_KEY = "xxxxxxxxxxxxx"
   ```

## 🎯 Usage

1. **Upload Product Image**
   - Click "Browse files" or drag & drop
   - Supports: PNG, JPG, JPEG

2. **Configure Settings** (Optional)
   - Video duration (15-45 seconds)
   - Quality (720p/1080p)
   - Enable/disable voiceover
   - Add product name, tagline, discount

3. **Generate Video**
   - Click "Generate Advertisement Video"
   - Wait 30-60 seconds
   - Preview and download MP4!

## 📁 Project Structure

```
ai-ad-video-generator/
├── app.py                 # Main Streamlit application
├── video_generator.py     # Video creation engine
├── script_generator.py    # AI script generation
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .streamlit/
│   └── secrets.toml      # API keys (don't commit!)
├── temp/                 # Temporary files (auto-created)
└── outputs/              # Generated videos (auto-created)
```

## 🎨 Video Structure (30 seconds)

1. **0-5s:** Hook & Reveal - Dramatic product intro with zoom/rotation
2. **5-15s:** Benefits Explosion - Feature callouts with animations
3. **15-20s:** Social Proof - Reviews, ratings, trust badges
4. **20-25s:** Urgency & CTA - Discount badge, call-to-action
5. **25-30s:** Epic Close - Brand finale with website

## 🔧 Troubleshooting

### "API Key Invalid" Error
- Double-check your Hugging Face token
- Make sure it's a "Read" or "Write" token
- Verify in secrets.toml or Streamlit Cloud secrets

### Video Generation Fails
- Check internet connection (needs to download models)
- Ensure FFmpeg is installed (included in moviepy)
- Try with a smaller image (< 5MB)

### Slow Generation
- First run downloads AI models (~500MB) - be patient!
- Use 720p instead of 1080p for faster processing
- Reduce video duration

### No Sound in Video
- Make sure voiceover is enabled
- Check if gTTS can access Google services
- Try generating again

## 🌟 Advanced Customization

### Change Video Quality
```python
# In app.py, modify:
video_quality = st.select_slider("Quality", 
    options=["480p", "720p", "1080p", "4K"], 
    value="1080p")
```

### Add Custom Background Music
```python
# In video_generator.py, add:
background_music = AudioFileClip("music.mp3")
final_video = final_video.set_audio(
    CompositeAudioClip([voiceover, background_music.volumex(0.3)])
)
```

### Use Different AI Models
```python
# In script_generator.py, change:
self.api_url = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf"
```

## 📊 API Rate Limits

| Service | Free Tier | Limit |
|---------|-----------|-------|
| Hugging Face | ✅ Free | 1000+ requests/day |
| Pexels | ✅ Free | 200 requests/hour |
| gTTS | ✅ Free | Unlimited |
| Streamlit Cloud | ✅ Free | 1GB RAM, public apps |

## 🤝 Contributing

Pull requests welcome! For major changes, please open an issue first.

## 📝 License

MIT License - feel free to use for your projects!

## 🎓 Perfect for Hackathons!

- ✅ Impressive AI demo
- ✅ Real working product
- ✅ Scalable architecture
- ✅ Free to run
- ✅ Easy to present

## 🆘 Support

- **Issues:** https://github.com/yourusername/ai-ad-video-generator/issues
- **Discussions:** https://github.com/yourusername/ai-ad-video-generator/discussions

## 🎉 Credits

Built with:
- [Streamlit](https://streamlit.io/) - Web framework
- [MoviePy](https://zulko.github.io/moviepy/) - Video editing
- [Hugging Face](https://huggingface.co/) - AI models
- [gTTS](https://gtts.readthedocs.io/) - Text-to-speech
- [Pillow](https://python-pillow.org/) - Image processing

---

**Made with ❤️ for hackathons and makers worldwide!**

Star ⭐ this repo if you found it helpful!
