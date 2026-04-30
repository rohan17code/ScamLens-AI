import os
import pytesseract
from PIL import Image, ImageOps, ImageFilter


if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
else:
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"


def extract_text_from_image(image_file):
    image = Image.open(image_file).convert("RGB")

    attempts = []

    attempts.append(("original", image))

    gray = image.convert("L")
    attempts.append(("gray", gray))

    big = gray.resize((gray.width * 3, gray.height * 3))
    attempts.append(("big_gray", big))

    contrast = ImageOps.autocontrast(big)
    attempts.append(("contrast", contrast))

    sharp = contrast.filter(ImageFilter.SHARPEN)
    attempts.append(("sharp", sharp))

    inverted = ImageOps.invert(gray)
    inverted_big = inverted.resize((inverted.width * 3, inverted.height * 3))
    attempts.append(("inverted", inverted_big))

    configs = ["--psm 6", "--psm 11", "--psm 12"]

    best_text = ""
    errors = []

    print("TESSERACT PATH:", pytesseract.pytesseract.tesseract_cmd)

    for name, img in attempts:
        for config in configs:
            try:
                text = pytesseract.image_to_string(img, config=config)

                print(f"OCR attempt: {name} {config}")
                print(text)

                if len(text.strip()) > len(best_text.strip()):
                    best_text = text

            except Exception as e:
                error_message = f"{name} {config} failed: {str(e)}"
                print(error_message)
                errors.append(error_message)

    if not best_text.strip() and errors:
        print("OCR ERRORS:")
        for error in errors:
            print(error)

    return best_text