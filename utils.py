import numpy as np
import cv2
import paddle
import sys
import os

def tensor_to_cv2_img(image):
    """
    Converts a ComfyUI image tensor (batch) to a list of OpenCV-compatible numpy arrays (BGR).
    """
    # Assuming input is a torch tensor or numpy array [B, H, W, C] or [H, W, C] in range 0-1
    if hasattr(image, 'cpu'):
        image = image.cpu().numpy()
        
    results = []
    
    # Handle single image vs batch
    if len(image.shape) == 3:
        # [H, W, C] -> list of one
        batch_images = [image]
    else:
        # [B, H, W, C]
        batch_images = image
        
    for img in batch_images:
        # Convert 0-1 float to 0-255 uint8
        img_255 = (img * 255).astype(np.uint8)
        # Convert RGB (ComfyUI default) to BGR (OpenCV default)
        img_bgr = cv2.cvtColor(img_255, cv2.COLOR_RGB2BGR)
        results.append(img_bgr)
        
    return results

def get_paddle_hw_kwargs():
    """
    Intelligently determines the hardware arguments for PaddleOCR initialization.
    Ports logic from PaddleOCR's tools/infer/utility.py to ensure best compatibility
    across Windows, Mac (MPS/CPU), and Linux (CUDA/ROCm).
    
    Returns:
        dict: Kwargs compatible with PaddleXPipelineWrapper (device, enable_mkldnn, etc.)
    """
    kwargs = {}
    
    # 1. Detect Hardware -> 'device' argument
    # PaddleXPipelineWrapper expects 'device': str (e.g. "gpu", "cpu", "npu", "xpu", "gpu:0")
    
    device = "cpu" # default
    
    if paddle.is_compiled_with_cuda() or paddle.device.is_compiled_with_rocm():
        device = "gpu"
        print("DEBUG: PaddleOCR using GPU (CUDA/ROCm)")
    elif sys.platform == 'darwin':
        # Mac MPS check
        # Paddle 2.5+ usually handles 'gpu' on Mac as MPS/Metal if available.
        # However, explicit 'mps' string isn't standard in common_args.py checks (it checks "gpu", "cpu", "npu", "xpu", "mlu").
        # If installed with metal support, 'gpu' often works. 
        # But to be safe on M-series, we often just say 'cpu' or let Paddle auto-detect if we pass nothing?
        # common_args sets default to "gpu" if not specified and CUDA available.
        
        # Let's try "gpu" if available, else "cpu".
        # Actually checking `paddle.device.get_device()` is safer.
        current_device = paddle.device.get_device()
        if 'gpu' in current_device or 'mps' in current_device:
             device = "gpu" # Paddle unified device name often maps mps to gpu in high level APIs
        else:
             device = "cpu"
    else:
        # Check for XPU/NPU
        if hasattr(paddle, 'is_compiled_with_custom_device'):
            try:
                if paddle.is_compiled_with_custom_device('npu'):
                    device = "npu"
                elif paddle.is_compiled_with_custom_device('xpu'):
                    device = "xpu"
                elif paddle.is_compiled_with_custom_device('mlu'):
                    device = "mlu"
            except:
                pass

    kwargs['device'] = device

    # 2. Handle OneDNN (MKLDNN)
    # Windows typically has issues with OneDNN + some AVX instrs or specific Paddle versions.
    if sys.platform == 'win32':
        # KNOWN ISSUE: PaddleOCR on Windows with MKLDNN can crash (NotImplementedError).
        kwargs['enable_mkldnn'] = False
        print("DEBUG: Forced enable_mkldnn=False for Windows compatibility")
    else:
        # On Linux/Mac, we can try to leave it default.
        # But if we are on CPU, enabling it is good.
        if device == "cpu":
             # We let Paddle default decide, or explicitly enable if we want speed.
             # _common_args defaults enable_mkldnn to True usually (DEFAULT_ENABLE_MKLDNN checking needed, typically True).
             pass

    return kwargs
