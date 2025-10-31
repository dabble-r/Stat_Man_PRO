#!/usr/bin/env python3
"""
Script to validate and fix icon file format.
Converts images to proper ICO format for Windows executable.
"""
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("ERROR: Pillow is not installed.")
    print("Install it with: pip install pillow")
    sys.exit(1)

def fix_icon(input_path, output_path=None):
    """
    Convert or validate an icon file.
    
    Args:
        input_path: Path to input image/icon file
        output_path: Path for output ICO file (default: overwrites input)
    """
    input_path = Path(input_path)
    
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        return False
    
    if output_path is None:
        output_path = input_path
    else:
        output_path = Path(output_path)
    
    try:
        # Open and validate the image
        print(f"Opening image: {input_path}")
        img = Image.open(input_path)
        print(f"  Format: {img.format}")
        print(f"  Size: {img.size}")
        print(f"  Mode: {img.mode}")
        
        # Convert RGBA to RGB if necessary (ICO doesn't support alpha in all cases)
        if img.mode in ('RGBA', 'LA'):
            print("  Converting RGBA/LA to RGB...")
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'RGBA':
                rgb_img.paste(img, mask=img.split()[3])  # Use alpha channel as mask
            else:
                rgb_img.paste(img)
            img = rgb_img
        
        # For ICO files, Windows prefers multiple sizes
        # Create sizes: 16x16, 32x32, 48x48, 256x256
        sizes = [(16, 16), (32, 32), (48, 48), (256, 256)]
        images = []
        
        for size in sizes:
            resized = img.resize(size, Image.Resampling.LANCZOS)
            images.append(resized)
            print(f"  Created {size[0]}x{size[1]} icon")
        
        # Save as ICO with multiple sizes
        print(f"\nSaving ICO file: {output_path}")
        images[0].save(
            output_path,
            format='ICO',
            sizes=[(img.width, img.height) for img in images]
        )
        
        print(f"✓ Successfully created/updated icon file: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error processing icon: {e}")
        return False

if __name__ == "__main__":
    icon_path = Path("assets/icons/favicon.ico")
    
    if len(sys.argv) > 1:
        icon_path = Path(sys.argv[1])
    
    print("=" * 60)
    print("Icon File Validator/Converter")
    print("=" * 60)
    
    if fix_icon(icon_path):
        print("\n✓ Icon file is now in proper format for PyInstaller!")
    else:
        print("\n✗ Failed to process icon file.")
        sys.exit(1)

