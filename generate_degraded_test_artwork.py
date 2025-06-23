#!/usr/bin/env python3

import os
from PIL import Image, ImageOps
import sys

def generate_degraded_images(input_path, output_dir="test/images"):
    """Generate various degraded versions of an image for quality testing"""
    
    if not os.path.exists(input_path):
        print(f"Error: Input image '{input_path}' not found")
        return False
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Extract base filename without extension
    base_filename = os.path.splitext(os.path.basename(input_path))[0]
    
    try:
        base_image = Image.open(input_path)
        print(f"Loaded base image: {base_image.size[0]}x{base_image.size[1]}")
        
        # 1. JPEG lossy compression 4 times in a row
        print("Creating JPEG lossy 4x version...")
        lossy_4x = base_image.copy()
        for i in range(10):
            temp_path = f"{output_dir}/temp_lossy_{i}.jpg"
            lossy_4x.save(temp_path, "JPEG", quality=30)
            lossy_4x = Image.open(temp_path)
            os.remove(temp_path)
        lossy_4x.save(f"{output_dir}/{base_filename}_lossy_4x.png", "PNG")
        
        # 2. Low res version (300x300)
        print("Creating 300x300 low res version...")
        low_res = base_image.resize((300, 300), Image.Resampling.LANCZOS)
        low_res.save(f"{output_dir}/{base_filename}_low_res_300x300.png", "PNG")
        
        # 3. Shrunk to 100x100 and blown back up to 1024x1024
        print("Creating shrunk and blown up version...")
        tiny = base_image.resize((100, 100), Image.Resampling.LANCZOS)
        blown_up = tiny.resize((1024, 1024), Image.Resampling.LANCZOS)
        blown_up.save(f"{output_dir}/{base_filename}_shrunk_blown_up.png", "PNG")
        
        # 4. Cropped to not be square
        print("Creating cropped non-square version...")
        width, height = base_image.size
        crop_width = int(width * 0.8)
        crop_height = height
        left = (width - crop_width) // 2
        cropped = base_image.crop((left, 0, left + crop_width, crop_height))
        cropped.save(f"{output_dir}/{base_filename}_cropped_non_square.png", "PNG")
        
        # 5. Very high lossy JPEG compression
        print("Creating very high lossy JPEG version...")
        very_lossy_path = f"{output_dir}/{base_filename}_very_lossy.jpg"
        base_image.save(very_lossy_path, "JPEG", quality=5)
        very_lossy = Image.open(very_lossy_path)
        very_lossy.save(f"{output_dir}/{base_filename}_very_lossy.png", "PNG")
        os.remove(very_lossy_path)
        
        print(f"Generated 5 degraded image versions in {output_dir}/")
        return True
        
    except Exception as e:
        print(f"Error processing image: {e}")
        return False

def main():
    input_image = "test/images/1.png"
    
    if len(sys.argv) > 1:
        input_image = sys.argv[1]
    
    print(f"Generating degraded versions of {input_image}")
    success = generate_degraded_images(input_image)
    
    if success:
        print("Image degradation complete!")
    else:
        print("Failed to generate degraded images")
        sys.exit(1)

if __name__ == "__main__":
    main() 