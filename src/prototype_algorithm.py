# import cv2
import numpy as np
from scipy.ndimage import gaussian_filter


def process_channel(channel_data, levels, gain_factors):
    coeffs = []
    residual = channel_data.copy()
    wavelet_planes = []
    for level in range(levels):
        sigma = 2**level
        smoothed = gaussian_filter(residual, sigma=sigma)
        wavelet_plane = residual - smoothed
        # store wavelet plane before applying gain
        wavelet_planes.append(wavelet_plane.copy())
        gain = gain_factors[level]
        wavelet_plane *= gain
        coeffs.append(wavelet_plane)
        # update
        residual = smoothed

    reconstructed_channel = residual + sum(coeffs)
    return reconstructed_channel, wavelet_planes


def atrous_wavelet_deconvolution(image, levels, gain_factors, color=True):

    data = image.astype(np.float32) / 65536.0

    if color:
        # data = image.astype(np.float32) / 65536.0
        channels = []
        all_wavelet_planes = []
        for i in range(3):
            channel = data[:, :, i]
            reconstructed_channel, wavelet_planes = process_channel(
                channel, levels, gain_factors
            )
            channels.append(reconstructed_channel)
            all_wavelet_planes.append(wavelet_planes)
        reconstructed_data = np.stack(channels, axis=2)
    else:
        reconstructed_data, wavelet_planes = process_channel(data, levels, gain_factors)
        all_wavelet_planes = [wavelet_planes]

    reconstructed_data = np.clip(reconstructed_data, 0, 1)

    reconstructed_image = (reconstructed_data * 65536).astype(np.uint16)

    return reconstructed_image
