import os
import pytesseract
from PIL import Image, ImageOps, ImageFilter


# Windows local system
if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Render/Linux server
else:
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"


def resize_image(image, max_width=1400):
    width, height = image.size

    if width > max_width:
        ratio = max_width / width
        new_height = int(height * ratio)
        image = image.resize((max_width, new_height))

    return image


def upscale_if_small(image, min_width=900):
    width, height = image.size

    if width < min_width:
        ratio = min_width / width
        new_height = int(height * ratio)
        image = image.resize((min_width, new_height))

    return image


def preprocess_image(image):
    processed_images = []

    image = image.convert("RGB")
    image = resize_image(image)
    image = upscale_if_small(image)

    # 1. Original
    processed_images.append(("original", image))

    # 2. Grayscale
    gray = image.convert("L")
    processed_images.append(("gray", gray))

    # 3. Auto contrast
    contrast = ImageOps.autocontrast(gray)
    processed_images.append(("contrast", contrast))

    # 4. Sharpen
    sharp = contrast.filter(ImageFilter.SHARPEN)
    processed_images.append(("sharp", sharp))

    # 5. Threshold for dark text on light background
    threshold = contrast.point(lambda p: 255 if p > 150 else 0)
    processed_images.append(("threshold", threshold))

    # 6. Inverted for light text on dark background
    inverted = ImageOps.invert(gray)
    inverted = ImageOps.autocontrast(inverted)
    processed_images.append(("inverted", inverted))

    return processed_images


def clean_ocr_text(text):
    text = text.replace("|", "")
    text = text.replace("‘", "'")
    text = text.replace("’", "'")
    text = text.replace("“", '"')
    text = text.replace("”", '"')
    text = text.strip()
    return text


def extract_text_from_image(image_file):
    image = Image.open(image_file)

    processed_images = preprocess_image(image)

    configs = [
        "--oem 3 --psm 6",
        "--oem 3 --psm 11",
        "--oem 3 --psm 3"
    ]

    best_text = ""

    print("TESSERACT PATH:", pytesseract.pytesseract.tesseract_cmd)

    for name, img in processed_images:
        for config in configs:
            try:
                text = pytesseract.image_to_string(img, config=config, timeout=12)
                text = clean_ocr_text(text)

                print(f"OCR attempt: {name} {config}")
                print(text)

                if len(text) > len(best_text):
                    best_text = text

                # If OCR already found useful scam text, stop early
                lower_text = best_text.lower()

                scam_words = [
                    "lottery", "winner", "won", "prize", "claim",
                    "congratulations", "reward", "giveaway",
                    "otp", "password", "bank", "payment", "click"
                ]

                has_scam_word = any(word in lower_text for word in scam_words)

                if len(best_text) > 30 and has_scam_word:
                    return best_text

            except Exception as e:
                print(f"OCR failed for {name} {config}: {str(e)}")

    return best_text