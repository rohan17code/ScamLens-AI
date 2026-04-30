import os
import pytesseract
from PIL import Image, ImageOps, ImageFilter


# Windows local system
if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Render/Linux server
else:
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"


def resize_image(image, max_width=1200):
    width, height = image.size

    if width > max_width:
        ratio = max_width / width
        new_height = int(height * ratio)
        image = image.resize((max_width, new_height))

    return image


def extract_text_from_image(image_file):
    image = Image.open(image_file).convert("RGB")
    image = resize_image(image)

    attempts = []

    # Original image
    attempts.append(("original", image))

    gray = image.convert("L")
    attempts.append(("gray", gray))

    contrast = ImageOps.autocontrast(gray)
    sharp = contrast.filter(ImageFilter.SHARPEN)
    attempts.append(("sharp", sharp))

    configs = ["--psm 6", "--psm 11"]

    best_text = ""

    print("TESSERACT PATH:", pytesseract.pytesseract.tesseract_cmd)

    for name, img in attempts:
        for config in configs:
            try:
                text = pytesseract.image_to_string(img, config=config, timeout=8)

                print(f"OCR attempt: {name} {config}")
                print(text)

                if len(text.strip()) > len(best_text.strip()):
                    best_text = text

                # Stop early if text is already good
                if len(best_text.strip()) > 20:
                    return best_text

            except Exception as e:
                print(f"{name} {config} failed: {str(e)}")

    return best_text