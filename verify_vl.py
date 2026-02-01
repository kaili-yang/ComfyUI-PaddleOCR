try:
    from paddleocr import PaddleOCRVL
    print("PaddleOCRVL found")
except ImportError:
    print("PaddleOCRVL NOT found")
except Exception as e:
    print(f"Error: {e}")
