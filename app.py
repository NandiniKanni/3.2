import streamlit as st
import os
from pathlib import Path
from video_generator import VideoGenerator
from script_generator import ScriptGenerator
from PIL import Image
import time

# Page config
st.set_page_config(
    page_title="AI Ad Video Generator",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(120deg, #f093fb 0%, #f5576c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(120deg, #f093fb 0%, #f5576c 100%);
        color: white;
        font-weight: bold;
        padding: 0.75rem;
        border-radius: 10px;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🎬 AI Ad Video Generator</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Transform your product images into stunning 30-second advertisement videos!</p>', unsafe_allow_html=True)

# Initialize session state
if 'video_generated' not in st.session_state:
    st.session_state.video_generated = False
if 'video_path' not in st.session_state:
    st.session_state.video_path = None

# Sidebar - Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    st.info("🔑 **API Keys Required (All FREE!)**")
    
    # API Keys from secrets or user input
    if 'HUGGINGFACE_API_KEY' in st.secrets:
        hf_key = st.secrets['HUGGINGFACE_API_KEY']
        st.success("✅ Hugging Face API Key loaded")
    else:
        hf_key = st.text_input("Hugging Face API Key", type="password", 
                               help="Get free at https://huggingface.co/settings/tokens")
    
    if 'PEXELS_API_KEY' in st.secrets:
        pexels_key = st.secrets['PEXELS_API_KEY']
        st.success("✅ Pexels API Key loaded")
    else:
        pexels_key = st.text_input("Pexels API Key (Optional)", type="password",
                                   help="Get free at https://www.pexels.com/api/")
    
    st.markdown("---")
    
    # Video Settings
    st.subheader("🎥 Video Settings")
    video_duration = st.slider("Video Duration (seconds)", 15, 45, 30)
    video_quality = st.select_slider("Quality", options=["720p", "1080p"], value="1080p")
    
    include_voiceover = st.checkbox("Include Voiceover", value=True)
    include_music = st.checkbox("Include Background Music", value=False)
    
    st.markdown("---")
    
    # Product Details (Optional)
    st.subheader("📝 Product Details (Optional)")
    product_name = st.text_input("Product Name", placeholder="Auto-detected from image")
    product_tagline = st.text_input("Tagline", placeholder="E.g., 'Innovation Redefined'")
    discount_text = st.text_input("Offer/Discount", placeholder="E.g., '50% OFF!'")

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📤 Upload Product Image")
    uploaded_file = st.file_uploader(
        "Choose a product image",
        type=['png', 'jpg', 'jpeg'],
        help="Upload a clear image of your product"
    )
    
    if uploaded_file:
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Your Product", use_container_width=True)
        
        # Save uploaded file
        temp_dir = Path("temp")
        temp_dir.mkdir(exist_ok=True)
        image_path = temp_dir / uploaded_file.name
        image.save(image_path)
        
        st.success(f"✅ Image uploaded: {uploaded_file.name}")

with col2:
    st.subheader("🎬 Generate Video")
    
    if uploaded_file:
        if st.button("🚀 Generate Advertisement Video", type="primary"):
            if not hf_key:
                st.error("❌ Please provide Hugging Face API key in sidebar!")
            else:
                # Progress tracking
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    # Step 1: Generate script
                    status_text.text("📝 Generating AI script...")
                    progress_bar.progress(20)
                    
                    script_gen = ScriptGenerator(hf_key)
                    script = script_gen.generate_script(
                        str(image_path),
                        product_name or None,
                        product_tagline or None,
                        discount_text or None
                    )
                    
                    with st.expander("📄 View Generated Script"):
                        st.write(script)
                    
                    # Step 2: Generate video
                    status_text.text("🎥 Creating video with animations...")
                    progress_bar.progress(40)
                    
                    video_gen = VideoGenerator(
                        hf_api_key=hf_key,
                        pexels_api_key=pexels_key if pexels_key else None
                    )
                    
                    status_text.text("🎨 Adding effects and transitions...")
                    progress_bar.progress(60)
                    
                    output_path = video_gen.create_ad_video(
                        image_path=str(image_path),
                        script=script,
                        duration=video_duration,
                        quality=video_quality,
                        include_voiceover=include_voiceover,
                        include_music=include_music,
                        product_name=product_name,
                        discount_text=discount_text
                    )
                    
                    status_text.text("✨ Finalizing video...")
                    progress_bar.progress(90)
                    
                    time.sleep(1)
                    progress_bar.progress(100)
                    status_text.text("✅ Video generated successfully!")
                    
                    st.session_state.video_generated = True
                    st.session_state.video_path = output_path
                    
                    st.success("🎉 Your advertisement video is ready!")
                    
                except Exception as e:
                    st.error(f"❌ Error generating video: {str(e)}")
                    st.exception(e)
    else:
        st.info("👆 Upload a product image to get started!")

# Video preview and download
if st.session_state.video_generated and st.session_state.video_path:
    st.markdown("---")
    st.subheader("🎬 Your Advertisement Video")
    
    col_preview, col_download = st.columns([2, 1])
    
    with col_preview:
        if os.path.exists(st.session_state.video_path):
            st.video(st.session_state.video_path)
    
    with col_download:
        st.markdown("### 📥 Download")
        
        with open(st.session_state.video_path, 'rb') as video_file:
            video_bytes = video_file.read()
            st.download_button(
                label="⬇️ Download MP4",
                data=video_bytes,
                file_name=f"ad_video_{int(time.time())}.mp4",
                mime="video/mp4"
            )
        
        st.info(f"📊 File size: {os.path.getsize(st.session_state.video_path) / 1024 / 1024:.2f} MB")
        
        if st.button("🔄 Generate Another Video"):
            st.session_state.video_generated = False
            st.session_state.video_path = None
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🚀 Built with Streamlit | 🤖 Powered by AI | 💯 100% Free & Open Source</p>
    <p>Get API Keys: <a href='https://huggingface.co/settings/tokens' target='_blank'>Hugging Face</a> | 
    <a href='https://www.pexels.com/api/' target='_blank'>Pexels</a></p>
</div>
""", unsafe_allow_html=True)
