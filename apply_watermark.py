from PIL import Image
import os

def watermark_img(input_path, output_path, watermark_path):
	# Open the original image
	original = Image.open(input_path).convert("RGBA")

	# Open the watermark image
	watermark = Image.open(watermark_path).convert("RGBA")

	# Calculate the position to place the watermark
	width, height = original.size
	watermark_width, watermark_height = watermark.size
	x = (width - watermark_width) // 2
	y = height - watermark_height - 10  # 10 pixels from the bottom

	# Create a new image for the watermark with an alpha layer (RGBA)
	transparent = Image.new('RGBA', (width, height), (255, 255, 255, 0))
	transparent.paste(original, (0, 0))
	transparent.paste(watermark, (x, y), mask=watermark)

	# Save the watermarked image
	watermarked = transparent.convert("RGB")  # Remove alpha for saving in jpg format.
	watermarked.save(output_path, "JPEG")

def process_images(input_dir, output_dir, watermark_path):
	for root, _, files in os.walk(input_dir):
		for file in files:
			if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
				input_path = os.path.join(root, file)
				relative_path = os.path.relpath(input_path, input_dir)
				output_path = os.path.join(output_dir, relative_path)

				# Create output directory if it doesn't exist
				os.makedirs(os.path.dirname(output_path), exist_ok=True)

				# Apply watermark
				watermark_img(input_path, output_path, watermark_path)

if __name__ == "__main__":
	input_dir = "input"
	output_dir = "output"
	watermark_path = "watermark.png"

	process_images(input_dir, output_dir, watermark_path)


