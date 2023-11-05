import pytesseract
from PIL import Image
import re
import datetime
time = datetime.datetime.now()

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
def image_to_str():
    Image_path = 'received_line.jpeg'

    image = Image.open(Image_path)
    text = pytesseract.image_to_string(image, lang='tha')
    name_pattern = r"(นาย|น\.ส\.|ด\.ช\.|ด\.ญ\.)\s([^\s]+)"
    name_match = re.search(name_pattern, text)
    name_prefix = name_match.group(1)
    name = name_match.group(2)

    # ค้นหาจำนวนเงินจากข้อความ
    amount_pattern = r"\s+(\d+\.\d+)\s+บาท"
    amount_match = re.search(amount_pattern, text)
    amount = amount_match.group(1)

    with open('test.txt', 'a', encoding='utf-8') as file:
        file.write(f'{name_prefix} {name} {amount} บาท {time.strftime("%d/%m/%y")} {time.strftime("%X")} \n')
    return f'{name_prefix} {name} {amount} บาท'