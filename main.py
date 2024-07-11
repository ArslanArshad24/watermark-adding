import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont

class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Watermark Application")
        self.image_path = None
        self.watermarked_image = None
        self.create_widgets()

    def create_widgets(self):
        self.upload_button = tk.Button(self.root, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=10)

        self.canvas = tk.Canvas(self.root, width=600, height=400)
        self.canvas.pack()

        self.watermark_button = tk.Button(self.root, text="Add Watermark", command=self.add_watermark)
        self.watermark_button.pack(pady=10)

        self.save_button = tk.Button(self.root, text="Save Image", command=self.save_image)
        self.save_button.pack(pady=10)

    def upload_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if self.image_path:
            self.display_image(self.image_path)

    def display_image(self, image_path):
        image = Image.open(image_path)
        image.thumbnail((600, 400))
        self.image_tk = ImageTk.PhotoImage(image)
        self.canvas.create_image(300, 200, image=self.image_tk)

    def add_watermark(self):
        if not self.image_path:
            return
        image = Image.open(self.image_path)
        # watermark_text = "Arslan logo"

        watermark_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if not watermark_path:
            return

        watermark = Image.open(watermark_path)
        watermark = watermark.resize((50, 50))  # Resize watermark as needed
        watermark = watermark.convert("RGBA")

        mask = Image.new("L", watermark.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, watermark.size[0], watermark.size[1]), fill=255)
        watermark.putalpha(mask)

        width, height = image.size
        watermark_width, watermark_height = watermark.size
        position = (width - watermark_width - 10, 10)
        
        image.paste(watermark, position, watermark)
        self.watermarked_image = image

        # Display watermarked image
        image.thumbnail((600, 400))
        self.image_tk = ImageTk.PhotoImage(image)
        self.canvas.create_image(300, 200, image=self.image_tk)

    def save_image(self):
        if self.watermarked_image:
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if save_path:
                self.watermarked_image.save(save_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()
