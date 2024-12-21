import os
from PIL import Image
import glob

def apply_watermark(image_path, watermark_path, output_path, scale_factor=0.15, padding=10):
    """
    Apply watermark to an image and save it
    
    Args:
        image_path: Path to the source image
        watermark_path: Path to the watermark image (must be PNG with transparency)
        output_path: Path where the watermarked image will be saved
        scale_factor: Size of watermark relative to the main image (default: 0.15)
        padding: Padding from the bottom-right corner in pixels (default: 10)
    """
    # Open the main image
    with Image.open(image_path) as base_image:
        # Convert image to RGBA for processing
        if base_image.mode != 'RGBA':
            base_image = base_image.convert('RGBA')
        
        # Open and resize watermark
        with Image.open(watermark_path) as watermark:
            # Calculate new size for watermark based on the main image size
            watermark_width = int(base_image.width * scale_factor)
            watermark_height = int(watermark_width * watermark.height / watermark.width)
            
            # Resize watermark maintaining aspect ratio
            watermark = watermark.resize((watermark_width, watermark_height), Image.Resampling.LANCZOS)
            
            # Calculate position (bottom-right with padding)
            position = (
                base_image.width - watermark_width - padding,
                base_image.height - watermark_height - 200
            )
            
            # Create a new transparent layer for the watermark
            transparent = Image.new('RGBA', base_image.size, (0, 0, 0, 0))
            transparent.paste(watermark, position, watermark)
            
            # Combine the images
            output_image = Image.alpha_composite(base_image, transparent)
            
            # Convert back to RGB if saving as JPEG
            output_extension = os.path.splitext(output_path)[1].lower()
            if output_extension in ['.jpg', '.jpeg']:
                # Create white background and paste RGBA image on top
                final_image = Image.new('RGB', output_image.size, (255, 255, 255))
                final_image.paste(output_image, mask=output_image.split()[3])  # Use alpha channel as mask
            else:
                final_image = output_image
            
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Save the image
            final_image.save(output_path, quality=95)

def process_images(input_folder, output_folder, watermark_path, scale_factor=0.15, padding=10):
    """
    Process all images in input folder and its subfolders
    
    Args:
        input_folder: Root folder containing images to process
        output_folder: Root folder where processed images will be saved
        watermark_path: Path to the watermark image
        scale_factor: Size of watermark relative to the main image
        padding: Padding from the bottom-right corner in pixels
    """
    # Supported image formats (case-insensitive)
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff', 
                       '*.JPG', '*.JPEG', '*.PNG', '*.BMP', '*.TIFF']
    
    # Get all image files recursively
    processed_files = set()  # To avoid processing duplicates due to case variations
    
    for extension in image_extensions:
        pattern = os.path.join(input_folder, '**', extension)
        for image_path in glob.glob(pattern, recursive=True):
            # Skip if we've already processed this file (case-insensitive check)
            if image_path.lower() in processed_files:
                continue
                
            processed_files.add(image_path.lower())
            
            # Calculate relative path to maintain folder structure
            rel_path = os.path.relpath(image_path, input_folder)
            output_path = os.path.join(output_folder, rel_path)
            
            try:
                apply_watermark(
                    image_path=image_path,
                    watermark_path=watermark_path,
                    output_path=output_path,
                    scale_factor=scale_factor,
                    padding=padding
                )
                print(f"Processed: {rel_path}")
            except Exception as e:
                print(f"Error processing {rel_path}: {str(e)}")

# Example usage
if __name__ == "__main__":
    input_folder = "input"
    output_folder = "output"
    watermark_path = "watermark.png"  # Your watermark image (must be PNG with transparency)
    scale_factor = 0.18  # Watermark size relative to main image
    padding = 300  # Pixels from bottom-right corner
    
    process_images(
        input_folder=input_folder,
        output_folder=output_folder,
        watermark_path=watermark_path,
        scale_factor=scale_factor,
        padding=padding
    )