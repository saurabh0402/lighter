import numpy as np

def rgb_to_linear(arr):
    arr = arr.astype(np.float64)
    arr = arr/255.0
    return np.where(arr <= 0.04045, arr / 12.92, ((arr + 0.055) / 1.055) ** 2.4)

def linear_to_rgb(arr):
    arr = np.where(arr <= 0.0031308, arr * 12.92, 1.055 * (arr ** (1 / 2.4)) - 0.055)
    arr = np.clip(arr*255, 0, 255)
    return arr.astype(np.int16)
