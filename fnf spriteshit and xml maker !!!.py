from tkinter import Tk, Button, Label
from tkinter.filedialog import askopenfilenames
from PIL import Image
import xml.etree.ElementTree as ET
import os

# Global variables
directions = ["idle", "up", "down", "right", "left"]
image_paths = {}

# Function to handle image selection for a specific direction
def select_images(direction):
    filenames = askopenfilenames(filetypes=[("Image Files", "*.png")])
    if filenames:
        image_paths[direction] = filenames

# Function to generate the spritesheet
def generate_spritesheet():
    if all(direction in image_paths for direction in directions):
        max_width = 0
        total_height = 0
        subtextures = []

        for direction in directions:
            images = [Image.open(filename) for filename in image_paths[direction]]
            max_width = max(max_width, max(image.size[0] for image in images))
            total_height += sum(image.size[1] for image in images)

        spritesheet = Image.new("RGBA", (max_width, total_height))
        y_offset = 0

        for direction in directions:
            images = [Image.open(filename) for filename in image_paths[direction]]
            max_height = max(image.size[1] for image in images)
            x_offset = 0

            for image in images:
                spritesheet.paste(image, (x_offset, y_offset))
                subtexture = {
                    "name": f"{os.path.splitext(os.path.basename(image.filename))[0]}_{direction}",
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
                y_offset += image.size[1]

        spritesheet.save(os.path.join(os.getcwd(), "spritesheet.png"))
        generate_xml(subtextures)
        print("Spritesheet and XML generated successfully.")
    else:
        print("Please select images for all directions.")

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

    button = Button(root, text="Select Images", command=lambda dir=direction: select_images(dir))
    button.pack()

# Create the "Generate Spritesheet" button
generate_button = Button(root, text="Generate Spritesheet", command=generate_spritesheet)
generate_button.pack()

# Run the Tkinter event loop
root.mainloop()
