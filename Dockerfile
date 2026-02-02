FROM yanwk/comfyui-boot:cu121-v2

# Install system dependencies required by opencv-python (headless)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Install PaddlePaddle (GPU version) and PaddleOCR
# Note: paddlepaddle-gpu version should match the CUDA version if possible, 
# but pip install paddlepaddle-gpu usually grabs the latest compatible with system drivers.
# We use a specific index-url for paddle if needed, but default often works.
RUN pip install paddlepaddle-gpu paddleocr opencv-python-headless
