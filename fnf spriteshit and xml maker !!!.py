from tkinter import Tk, Button, Label
from tkinter.filedialog import askopenfilename
from PIL import Image
import xml.etree.ElementTree as ET
import os

# Global variables
directions = ["idle", "up", "down", "right", "left"]
image_paths = {}
frame_counts = 4

# Function to handle image selection for a specific direction and frame
def select_image(direction, frame):
    filename = askopenfilename(filetypes=[("Image Files", "*.png")])
    if filename:
        if direction not in image_paths:
            image_paths[direction] = {}

        image_paths[direction][frame] = filename
        print(f"Selected image for {direction} - Frame {frame}: {filename}")
    else:
        print(f"No image selected for {direction} - Frame {frame}.")

# Function to generate the spritesheet
def generate_spritesheet():
    if all(direction in image_paths and len(image_paths[direction]) == frame_counts for direction in directions):
        max_width = 0
        total_height = 0
        subtextures = []

        for direction in directions:
            images = [Image.open(filename) for filename in image_paths[direction].values()]
            max_width = max(max_width, max(image.size[0] for image in images))
            total_height += sum(image.size[1] for image in images)

        spritesheet = Image.new("RGBA", (max_width, total_height))
        y_offset = 0

        for direction in directions:
            images = [Image.open(filename) for filename in image_paths[direction].values()]
            max_height = max(image.size[1] for image in images)
            x_offset = 0
            frame_number = 1

            for image in images:
                spritesheet.paste(image, (x_offset, y_offset))
                subtexture = {
                    "name": f"char_{direction}{frame_number:04d}",
                    "x": str(x_offset),
                    "y": str(y_offset),
                    "width": str(image.size[0]),
                    "height": str(image.size[1]),
                    "frameX": "0",
                    "frameY": "0",
                    "frameWidth": str(image.size[0]),
                    "frameHeight": str(image.size[1])
                }
                subtextures.append(subtexture)
                x_offset += image.size[0]
                frame_number += 1

            y_offset += max_height

        spritesheet.save(os.path.join(os.getcwd(), "spritesheet.png"))
        generate_xml(subtextures)
        print("Spritesheet and XML generated successfully.")
    else:
        print("Please select images for all directions and frames.")

# Function to generate the XML file
def generate_xml(subtextures):
    root = ET.Element("TextureAtlas", imagePath="spritesheet.png")

    for subtexture in subtextures:
        sub = ET.SubElement(root, "SubTexture", attrib=subtexture)

    tree = ET.ElementTree(root)
    tree.write(os.path.join(os.getcwd(), "spritesheet.xml"))

# Create the Tkinter application
root = Tk()

# Create labels and buttons for image selection
for direction in directions:
    label = Label(root, text=direction)
    label.pack()

    for frame in range(1, frame_counts + 1):
        button = Button(root, text=f"Select Image - Frame {frame:02d}", command=lambda dir=direction, f=frame: select_image(dir, f))
        button.pack()

# Create the "Generate Spritesheet" button
generate_button = Button(root, text="Generate Spritesheet", command=generate_spritesheet)
generate_button.pack()

# Run the Tkinter event loop
root.mainloop()
