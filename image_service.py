import os
import pytesseract
from PIL import Image, ImageOps, ImageFilter


if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
else:
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"


def resize_image(image, max_width=750):
    width, height = image.size

    if width > max_width:
        ratio = max_width / width
        new_height = int(height * ratio)
        image = image.resize((max_width, new_height))

    return image


def clean_ocr_text(text):
    text = text.replace("|", "")
    text = text.replace("‘", "'")
    text = text.replace("’", "'")
    text = text.replace("“", '"')
    text = text.replace("”", '"')
    return text.strip()


def get_ocr_attempts(image_file):
    image = Image.open(image_file).convert("RGB")
    image = resize_image(image)

    gray = image.convert("L")
    gray = ImageOps.autocontrast(gray)
    sharp = gray.filter(ImageFilter.SHARPEN)

    inverted = ImageOps.invert(gray)
    inverted = ImageOps.autocontrast(inverted)

    attempts = [
        ("sharp", sharp),
        ("inverted", inverted)
    ]

    config = "--oem 3 --psm 6"

    results = []
    best_text = ""

    for name, img in attempts:
        try:
            text = pytesseract.image_to_string(
                img,
                config=config,
                timeout=25
            )

            text = clean_ocr_text(text)

            results.append({
                "attempt": name,
                "config": config,
                "text": text,
                "length": len(text)
            })

            if len(text) > len(best_text):
                best_text = text

            if len(best_text.strip()) > 20:
                return best_text, results

        except Exception as e:
            results.append({
                "attempt": name,
                "config": config,
                "text": "",
                "length": 0,
                "error": str(e)
            })

    return best_text, results


def extract_text_from_image(image_file):
    best_text, results = get_ocr_attempts(image_file)
    return best_text