import os
import pytesseract
from PIL import Image, ImageOps, ImageFilter


if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
else:
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"


def resize_image(image, max_width=1400):
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


def extract_text_from_image(image_file):
    image = Image.open(image_file).convert("RGB")
    image = resize_image(image)

    attempts = []

    # 1. Original image
    attempts.append(("original", image))

    # 2. Grayscale
    gray = image.convert("L")
    attempts.append(("gray", gray))

    # 3. Auto contrast grayscale
    contrast = ImageOps.autocontrast(gray)
    attempts.append(("contrast", contrast))

    # 4. Sharpen
    sharp = contrast.filter(ImageFilter.SHARPEN)
    attempts.append(("sharp", sharp))

    # 5. Inverted image for white text on dark background
    inverted = ImageOps.invert(gray)
    inverted = ImageOps.autocontrast(inverted)
    attempts.append(("inverted", inverted))

    # 6. Threshold image
    threshold = inverted.point(lambda p: 255 if p > 140 else 0)
    attempts.append(("threshold", threshold))

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

    print("TESSERACT PATH:", pytesseract.pytesseract.tesseract_cmd, flush=True)

    for name, img in attempts:
        for config in configs:
            try:
                text = pytesseract.image_to_string(img, config=config, timeout=15)
                text = clean_ocr_text(text)

                print("OCR attempt:", name, config, flush=True)
                print(text, flush=True)

                if len(text) > len(best_text):
                    best_text = text

                lower_text = text.lower()

                if len(text) > 20 and any(word in lower_text for word in scam_words):
                    return text

            except Exception as e:
                print("OCR failed:", name, config, str(e), flush=True)

    return best_text