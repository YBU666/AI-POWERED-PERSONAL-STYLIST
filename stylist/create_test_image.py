from PIL import Image, ImageDraw, ImageFont
import os

# Create a new image with a white background
image = Image.new('RGB', (512, 512), 'white')
draw = ImageDraw.Draw(image)

# Add some simple shapes
draw.rectangle([100, 100, 400, 400], outline='black', width=2)
draw.ellipse([200, 200, 300, 300], fill='gray')

# Save the image
image.save('test_image.jpg', 'JPEG') 