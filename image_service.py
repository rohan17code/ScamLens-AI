import os
import pytesseract
from PIL import Image, ImageOps, ImageFilter


if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
else:
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"


def resize_image(image, max_width=1000):
    width, height = image.size

    if width > max_width:
        ratio = max_width / width
        new_height = int(height * ratio)
        image = image.resize((max_width, new_height))

    return image


def clean_ocr_text(text):
    return text.replace("|", "").strip()


def extract_text_from_image(image_file):
    image = Image.open(image_file).convert("RGB")
    image = resize_image(image)

    gray = image.convert("L")
    contrast = ImageOps.autocontrast(gray)
    sharp = contrast.filter(ImageFilter.SHARPEN)

    attempts = [
        ("original", image),
        ("sharp", sharp)
    ]

    configs = [
        "--oem 3 --psm 6",
        "--oem 3 --psm 11"
    ]

    best_text = ""

    scam_words = [
        "lottery", "winner", "won", "prize", "claim",
        "congratulations", "reward", "giveaway",
        "otp", "password", "bank", "payment", "click",
        "link", "http", "www"
    ]

    for name, img in attempts:
        for config in configs:
            try:
                text = pytesseract.image_to_string(img, config=config, timeout=6)
                text = clean_ocr_text(text)

                print(f"OCR attempt: {name} {config}")
                print(text)

                if len(text) > len(best_text):
                    best_text = text

                lower_text = text.lower()

                if any(word in lower_text for word in scam_words):
                    return text

            except Exception as e:
                print(f"OCR failed for {name} {config}: {str(e)}")

    return best_text