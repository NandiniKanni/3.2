import requests
from PIL import Image
import base64
import io

class ScriptGenerator:
    def __init__(self, hf_api_key):
        self.hf_api_key = hf_api_key
        self.api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
        self.headers = {"Authorization": f"Bearer {hf_api_key}"}
    
    def generate_script(self, image_path, product_name=None, tagline=None, discount=None):
        """Generate advertisement script using Hugging Face"""
        
        # Analyze image to detect product type
        product_type = self.detect_product_type(image_path)
        
        # Build prompt
        prompt = self.build_prompt(product_type, product_name, tagline, discount)
        
        # Call Hugging Face API
        try:
            script = self.call_hf_api(prompt)
            return script
        except Exception as e:
            print(f"Error generating script: {e}")
            # Fallback script
            return self.generate_fallback_script(product_name or product_type)
    
    def detect_product_type(self, image_path):
        """Simple product type detection based on image characteristics"""
        try:
            img = Image.open(image_path)
            
            # Basic heuristics (can be improved with actual image classification)
            width, height = img.size
            aspect_ratio = width / height
            
            # Analyze dominant colors
            img_rgb = img.convert('RGB')
            pixels = list(img_rgb.getdata())
            avg_color = tuple(sum(c) // len(pixels) for c in zip(*pixels))
            
            # Simple classification logic
            if aspect_ratio > 1.5:
                return "electronic device"
            elif aspect_ratio < 0.7:
                return "beauty product"
            else:
                return "lifestyle product"
        
        except Exception as e:
            return "premium product"
    
    def build_prompt(self, product_type, product_name, tagline, discount):
        """Build prompt for AI script generation"""
        
        name = product_name or f"revolutionary {product_type}"
        tag = tagline or "Innovation meets excellence"
        offer = discount or "exclusive limited-time offer"
        
        prompt = f"""[INST] Write a compelling 30-second advertisement voiceover script for {name}.

Product: {name}
Tagline: {tag}
Offer: {offer}

The script should:
- Hook viewers in the first 3 seconds
- Highlight 3 key benefits
- Create urgency
- End with a strong call-to-action
- Be exactly 80-100 words
- Sound exciting and professional
- Use powerful, action-oriented language

Write ONLY the voiceover script, no other text. [/INST]"""
        
        return prompt
    
    def call_hf_api(self, prompt):
        """Call Hugging Face Inference API"""
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 250,
                "temperature": 0.7,
                "top_p": 0.9,
                "do_sample": True,
                "return_full_text": False
            }
        }
        
        response = requests.post(self.api_url, headers=self.headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                script = result[0].get('generated_text', '')
                # Clean up the script
                script = script.strip()
                # Remove any [INST] tags if present
                script = script.replace('[INST]', '').replace('[/INST]', '').strip()
                return script
            else:
                raise Exception("Unexpected API response format")
        else:
            raise Exception(f"API error: {response.status_code} - {response.text}")
    
    def generate_fallback_script(self, product_name):
        """Generate a basic fallback script if API fails"""
        
        scripts = {
            "electronic device": f"""Introducing {product_name} – the future is here! 
                Experience lightning-fast performance, stunning design, and cutting-edge technology. 
                Whether you're working, creating, or playing, this is the device that does it all. 
                Join thousands of satisfied customers worldwide. 
                Limited time offer – don't miss out! 
                Order now and transform the way you work and play!""",
            
            "beauty product": f"""Discover {product_name} – your secret to radiant confidence! 
                Premium ingredients, proven results, dermatologist approved. 
                Feel the difference from day one. Loved by beauty experts everywhere. 
                Transform your routine with this game-changing formula. 
                Exclusive offer available now – your best self is waiting! 
                Shop today and glow like never before!""",
            
            "lifestyle product": f"""Meet {product_name} – designed for your extraordinary life! 
                Premium quality meets unbeatable style. Durable, versatile, absolutely essential. 
                Trusted by thousands who demand the best. 
                This isn't just a product – it's an upgrade to your lifestyle. 
                Special launch pricing – grab yours before it's gone! 
                Order now and elevate every moment!""",
            
            "default": f"""Introducing {product_name} – innovation you can feel! 
                Superior quality, exceptional design, unmatched performance. 
                Join the revolution of satisfied customers. 
                Don't settle for ordinary when extraordinary is within reach. 
                Limited time exclusive offer – act fast! 
                Get yours today and experience the difference!"""
        }
        
        # Find matching script or use default
        for key in scripts:
            if key in product_name.lower():
                return scripts[key].replace('\n', ' ').strip()
        
        return scripts["default"].replace('\n', ' ').strip()
