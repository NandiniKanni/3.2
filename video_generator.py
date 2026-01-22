from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import numpy as np
from gtts import gTTS
import os
from pathlib import Path
import requests
import io

class VideoGenerator:
    def __init__(self, hf_api_key, pexels_api_key=None):
        self.hf_api_key = hf_api_key
        self.pexels_api_key = pexels_api_key
        self.output_dir = Path("outputs")
        self.output_dir.mkdir(exist_ok=True)
        self.temp_dir = Path("temp")
        self.temp_dir.mkdir(exist_ok=True)
        
    def create_ad_video(self, image_path, script, duration=30, quality="1080p",
                       include_voiceover=True, include_music=False,
                       product_name=None, discount_text=None):
        """Main function to create advertisement video"""
        
        # Set resolution
        width, height = (1080, 1920) if quality == "1080p" else (720, 1280)
        fps = 30
        
        # Load product image
        product_img = Image.open(image_path).convert("RGBA")
        
        # Create video clips
        clips = []
        
        # Scene 1: Hook & Reveal (0-5s)
        clips.append(self.create_hook_scene(product_img, width, height, fps, product_name))
        
        # Scene 2: Benefits Explosion (5-15s)
        clips.append(self.create_benefits_scene(product_img, width, height, fps))
        
        # Scene 3: Social Proof (15-20s)
        clips.append(self.create_social_proof_scene(product_img, width, height, fps))
        
        # Scene 4: Urgency & CTA (20-25s)
        clips.append(self.create_urgency_scene(product_img, width, height, fps, discount_text))
        
        # Scene 5: Epic Close (25-30s)
        clips.append(self.create_closing_scene(product_img, width, height, fps, product_name))
        
        # Concatenate all scenes
        final_video = concatenate_videoclips(clips, method="compose")
        
        # Add voiceover if requested
        if include_voiceover:
            audio_path = self.generate_voiceover(script)
            if audio_path and os.path.exists(audio_path):
                audio = AudioFileClip(audio_path)
                # Trim or loop audio to match video duration
                if audio.duration < final_video.duration:
                    audio = audio.set_duration(final_video.duration)
                else:
                    audio = audio.subclip(0, final_video.duration)
                final_video = final_video.set_audio(audio)
        
        # Export video
        output_path = self.output_dir / f"ad_video_{int(os.times().elapsed * 1000)}.mp4"
        final_video.write_videofile(
            str(output_path),
            fps=fps,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile=str(self.temp_dir / 'temp-audio.m4a'),
            remove_temp=True,
            preset='medium'
        )
        
        return str(output_path)
    
    def create_hook_scene(self, product_img, width, height, fps, product_name):
        """0-5s: Dramatic reveal with zoom and glow"""
        duration = 5
        frames = []
        
        for frame_num in range(duration * fps):
            t = frame_num / (duration * fps)
            
            # Create background with gradient
            bg = Image.new('RGB', (width, height), (20, 20, 30))
            draw = ImageDraw.Draw(bg)
            
            # Add radial gradient effect
            for y in range(height):
                for x in range(width):
                    dist = ((x - width/2)**2 + (y - height/2)**2)**0.5
                    max_dist = ((width/2)**2 + (height/2)**2)**0.5
                    brightness = int(50 * (1 - dist/max_dist))
                    draw.point((x, y), (20 + brightness, 20 + brightness, 30 + brightness))
            
            # Zoom effect: start small, zoom in
            scale = 0.3 + (t * 0.7)
            
            # Rotate product
            rotation = t * 360
            
            # Resize and rotate product
            prod_size = int(min(width, height) * 0.6 * scale)
            product_resized = product_img.resize((prod_size, prod_size), Image.Resampling.LANCZOS)
            product_rotated = product_resized.rotate(rotation, expand=False)
            
            # Add glow effect
            glow = product_rotated.copy()
            glow = glow.filter(ImageFilter.GaussianBlur(radius=20))
            enhancer = ImageEnhance.Brightness(glow)
            glow = enhancer.enhance(1.5)
            
            # Composite images
            x_pos = (width - product_rotated.width) // 2
            y_pos = (height - product_rotated.height) // 2
            
            bg.paste(glow, (x_pos, y_pos), glow)
            bg.paste(product_rotated, (x_pos, y_pos), product_rotated)
            
            # Add text overlay
            if product_name and t > 0.5:
                alpha = min((t - 0.5) * 2, 1)
                self.add_text(bg, product_name.upper(), width//2, height//4, 
                            size=80, alpha=int(alpha * 255))
            
            frames.append(np.array(bg))
        
        return ImageSequenceClip(frames, fps=fps)
    
    def create_benefits_scene(self, product_img, width, height, fps):
        """5-15s: Benefits with pop-in animations"""
        duration = 10
        frames = []
        
        benefits = [
            "Premium Quality",
            "Innovative Design",
            "Long Lasting",
            "Best Value"
        ]
        
        for frame_num in range(duration * fps):
            t = frame_num / (duration * fps)
            
            # Dark gradient background
            bg = self.create_gradient_bg(width, height, (30, 30, 50), (50, 30, 70))
            
            # Show product (smaller, to the side)
            prod_size = int(min(width, height) * 0.4)
            product_resized = product_img.resize((prod_size, prod_size), Image.Resampling.LANCZOS)
            
            x_prod = width // 4
            y_prod = (height - product_resized.height) // 2
            bg.paste(product_resized, (x_prod, y_prod), product_resized)
            
            # Animate benefits one by one
            benefit_index = int(t * len(benefits))
            
            for i, benefit in enumerate(benefits[:benefit_index + 1]):
                if i == benefit_index:
                    # Current benefit: pop-in animation
                    progress = (t * len(benefits)) - benefit_index
                    scale = min(progress * 2, 1)
                    alpha = int(scale * 255)
                else:
                    # Previous benefits: fully visible
                    scale = 1
                    alpha = 255
                
                y_offset = height // 3 + (i * 120)
                self.add_text(bg, f"✓ {benefit}", width * 3 // 4, y_offset, 
                            size=int(50 * scale), alpha=alpha, color=(255, 215, 0))
            
            frames.append(np.array(bg))
        
        return ImageSequenceClip(frames, fps=fps)
    
    def create_social_proof_scene(self, product_img, width, height, fps):
        """15-20s: Social proof with reviews"""
        duration = 5
        frames = []
        
        for frame_num in range(duration * fps):
            t = frame_num / (duration * fps)
            
            bg = self.create_gradient_bg(width, height, (40, 20, 60), (20, 40, 80))
            
            # Show product in center
            prod_size = int(min(width, height) * 0.5)
            product_resized = product_img.resize((prod_size, prod_size), Image.Resampling.LANCZOS)
            
            x_prod = (width - product_resized.width) // 2
            y_prod = (height - product_resized.height) // 2
            bg.paste(product_resized, (x_prod, y_prod), product_resized)
            
            # Add 5-star rating
            stars = "★★★★★"
            self.add_text(bg, stars, width//2, height//4, size=60, color=(255, 215, 0))
            
            # Add review count
            self.add_text(bg, "10,000+ Happy Customers", width//2, height//4 + 80, 
                        size=40, color=(255, 255, 255))
            
            # Add trust badge
            if t > 0.3:
                alpha = min((t - 0.3) * 2, 1)
                self.add_text(bg, "🏆 #1 CHOICE", width//2, height * 3 // 4, 
                            size=50, alpha=int(alpha * 255), color=(255, 215, 0))
            
            frames.append(np.array(bg))
        
        return ImageSequenceClip(frames, fps=fps)
    
    def create_urgency_scene(self, product_img, width, height, fps, discount_text):
        """20-25s: Urgency with discount badge"""
        duration = 5
        frames = []
        
        for frame_num in range(duration * fps):
            t = frame_num / (duration * fps)
            
            # Red gradient for urgency
            bg = self.create_gradient_bg(width, height, (80, 20, 20), (120, 30, 30))
            
            # Pulsing product
            pulse = 1 + (np.sin(t * 10) * 0.1)
            prod_size = int(min(width, height) * 0.5 * pulse)
            product_resized = product_img.resize((prod_size, prod_size), Image.Resampling.LANCZOS)
            
            x_prod = (width - product_resized.width) // 2
            y_prod = (height - product_resized.height) // 2
            bg.paste(product_resized, (x_prod, y_prod), product_resized)
            
            # Discount badge
            discount = discount_text or "50% OFF"
            self.add_text(bg, discount, width//2, height//4, size=90, 
                        color=(255, 255, 0), alpha=int((1 + np.sin(t * 8)) / 2 * 255))
            
            # Urgency text
            self.add_text(bg, "LIMITED TIME ONLY!", width//2, height * 3 // 4, 
                        size=50, color=(255, 255, 255))
            
            # CTA button
            if t > 0.5:
                self.add_text(bg, "👉 SHOP NOW 👈", width//2, height * 7 // 8, 
                            size=60, color=(0, 255, 0))
            
            frames.append(np.array(bg))
        
        return ImageSequenceClip(frames, fps=fps)
    
    def create_closing_scene(self, product_img, width, height, fps, product_name):
        """25-30s: Epic closing with brand"""
        duration = 5
        frames = []
        
        for frame_num in range(duration * fps):
            t = frame_num / (duration * fps)
            
            # Fade to black
            brightness = int(255 * (1 - t))
            bg = Image.new('RGB', (width, height), (brightness//5, brightness//5, brightness//5))
            
            if t < 0.6:
                # Product explosion effect
                scale = 1 + (t * 2)
                alpha = int(255 * (1 - t / 0.6))
                
                prod_size = int(min(width, height) * 0.6 * scale)
                product_resized = product_img.resize((prod_size, prod_size), Image.Resampling.LANCZOS)
                
                # Apply fade
                product_faded = Image.new('RGBA', product_resized.size, (0, 0, 0, 0))
                product_faded.paste(product_resized, (0, 0))
                product_faded.putalpha(alpha)
                
                x_prod = (width - product_resized.width) // 2
                y_prod = (height - product_resized.height) // 2
                bg.paste(product_faded, (x_prod, y_prod), product_faded)
            
            # Final CTA
            if t > 0.4:
                alpha = min((t - 0.4) / 0.6, 1)
                brand = product_name or "GET YOURS NOW"
                self.add_text(bg, brand.upper(), width//2, height//2, 
                            size=70, alpha=int(alpha * 255), color=(255, 255, 255))
                
                if t > 0.6:
                    self.add_text(bg, "www.yourstore.com", width//2, height * 2 // 3, 
                                size=40, alpha=int((t - 0.6) / 0.4 * 255), color=(200, 200, 200))
            
            frames.append(np.array(bg))
        
        return ImageSequenceClip(frames, fps=fps)
    
    def create_gradient_bg(self, width, height, color1, color2):
        """Create gradient background"""
        bg = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(bg)
        
        for y in range(height):
            t = y / height
            r = int(color1[0] * (1-t) + color2[0] * t)
            g = int(color1[1] * (1-t) + color2[1] * t)
            b = int(color1[2] * (1-t) + color2[2] * t)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        return bg
    
    def add_text(self, img, text, x, y, size=50, color=(255, 255, 255), alpha=255):
        """Add text to image"""
        draw = ImageDraw.Draw(img, 'RGBA')
        
        try:
            # Try to use a nice font
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
        except:
            font = ImageFont.load_default()
        
        # Get text bounding box
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Center text
        position = (x - text_width // 2, y - text_height // 2)
        
        # Add text with alpha
        color_with_alpha = (*color, alpha)
        draw.text(position, text, font=font, fill=color_with_alpha)
    
    def generate_voiceover(self, script):
        """Generate voiceover using gTTS"""
        try:
            audio_path = self.temp_dir / "voiceover.mp3"
            tts = gTTS(text=script, lang='en', slow=False)
            tts.save(str(audio_path))
            return str(audio_path)
        except Exception as e:
            print(f"Error generating voiceover: {e}")
            return None
