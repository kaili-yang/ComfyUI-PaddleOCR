# ComfyUI-PaddleOCR-VL

A ComfyUI custom node that integrates [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) for powerful and accurate text detection and recognition.

This node leverages the PaddlePaddle deep learning framework to provide industry-leading OCR capabilities directly within your ComfyUI workflows. It supports multiple languages and offers high accuracy for various scene text recognition tasks.

## Features

- **Text Detection & Recognition**: Extract text from images with high precision.
- **Multilingual Support**: Supports Chinese, English, Japanese, Korean, French, German, and more.
- **Model Version Selection**: Choose between PP-OCRv5, PP-OCRv4, and PP-OCRv3 models.
- **Auto-Orientation**: Automatically detects and corrects text orientation (e.g., vertical text).

## Installation

1. Navigate to your ComfyUI custom nodes directory:
   ```bash
   cd ComfyUI/custom_nodes
   ```

2. Clone this repository:
   ```bash
   git clone git@github.com:kaili-yang/ComfyUI-PaddleOCR-VL.git
   ```

3. Install the required dependencies:
   ```bash
   pip install paddlepaddle paddleocr opencv-python-headless
   ```

4. Restart ComfyUI.

## Usage

1. **Add Node**: Right-click in the ComfyUI canvas and search for `PaddleOCR Text Detection`. You can typically find it under the `PaddleOCR` category.
2. **Connect Input**: Connect an image source (e.g., `Load Image`) to the `image` input of the PaddleOCR node.
3. **Configure Parameters**:
   - `language`: Select the language of the text in the image (default: `ch` for Chinese).
   - `ocr_version`: Choose the OCR model version (e.g., `PP-OCRv5`).
   - `vertical_direction`: Enable this if the text might be vertical or rotated.
4. **Get Output**: The node outputs a `text` string containing all recognized text from the image. You can connect this to a `Show Text` node or use it in other text processing workflows.

## Credits

This project wraps the amazing [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) library by PaddlePaddle. 

## License

MIT
