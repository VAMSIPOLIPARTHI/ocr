import fitz
import numpy as np
import threading

ocr = None
ocr_lock = threading.Lock()

def get_ocr():
    global ocr
    with ocr_lock:
        if ocr is None:
            import os
            print(f"DEBUG: Current UID: {os.getuid()}")
            print(f"DEBUG: HOME: {os.environ.get('HOME')}")
            from paddleocr import PaddleOCR
            print("Downloading/Initializing PaddleOCR models...")
            ocr = PaddleOCR(use_angle_cls=False, lang="en", show_log=True, use_gpu=False)
    return ocr




def extract_text(file_bytes, ext):
    ocr_instance = get_ocr()
    all_text = ""

    if ext in ["jpg", "jpeg", "png"]:
        import cv2
        # Convert bytes to numpy array for PaddleOCR
        img = cv2.imdecode(np.frombuffer(file_bytes, np.uint8), cv2.IMREAD_COLOR)
        if img is None:
            return ""
        result = ocr_instance.ocr(img) or []
        for block in result:
            if block is None: continue
            for line in block:
                all_text += line[1][0] + " "

    elif ext == "pdf":
        # Open PDF from memory stream
        pdf = fitz.open(stream=file_bytes, filetype="pdf")
        for page in pdf:
            pix = page.get_pixmap()
            img = np.frombuffer(pix.samples, dtype=np.uint8)
            img = img.reshape(pix.height, pix.width, pix.n)

            result = ocr_instance.ocr(img) or []
            for block in result:
                if block is None: continue
                for line in block:
                    all_text += line[1][0] + " "
        pdf.close()


    return all_text.strip().lower()

