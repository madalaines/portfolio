import os
import random
from PIL import Image, ImageDraw
import numpy as np
import uuid

def generate_random_artwork(output_dir):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Generate a unique identifier for the artwork
    filename = str(uuid.uuid4()) + ".png"

    # Generate random size for the artwork
    width = random.randint(200, 800)
    height = random.randint(200, 800)

    # Generate a random background color
    background_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # Create a new image with white background
    image = Image.new("RGB", (width, height), background_color)

    # Create a drawing context
    draw = ImageDraw.Draw(image)

    # Generate random shapes
    num_shapes = random.randint(5, 20)
    for _ in range(num_shapes):
        # Generate random shape parameters
        shape = random.choice(["rectangle", "circle", "triangle", "ellipse"])
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)

        # Ensure x1 <= x2 and y1 <= y2
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)

        # Generate random color for the shape
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        # Draw the shape
        if shape == "rectangle":
            draw.rectangle([x1, y1, x2, y2], fill=color)
        elif shape == "circle":
            draw.ellipse([x1, y1, x2, y2], fill=color)
        elif shape == "triangle":
            draw.polygon([(x1, y1), (x2, y2), (x1 + (x2 - x1) // 2, y1 + (y2 - y1))], fill=color)
        elif shape == "ellipse":
            draw.ellipse([x1, y1, x2, y2], fill=color)

    # Save the artwork as PNG
    filepath = os.path.join(output_dir, filename)
    image.save(filepath)
    return filename
