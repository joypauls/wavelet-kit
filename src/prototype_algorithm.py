from PIL import Image
import numpy as np
from scipy.ndimage import gaussian_filter


def process_channel(channel_data, levels, gain_factors):
    coeffs = []
    residual = channel_data.copy()
    wavelet_planes = []
    for level in range(levels):
        # Apply a Gaussian filter with increasing sigma
        sigma = 2**level
        smoothed = gaussian_filter(residual, sigma=sigma)
        # Calculate the wavelet plane
        wavelet_plane = residual - smoothed
        # Store the wavelet plane before applying gain
        wavelet_planes.append(wavelet_plane.copy())
        # Apply gain factor
        gain = gain_factors[level]
        wavelet_plane *= gain
        coeffs.append(wavelet_plane)
        # Update residual
        residual = smoothed

    # Reconstruct the channel
    reconstructed_channel = residual + sum(coeffs)
    return reconstructed_channel, wavelet_planes


def atrous_wavelet_deconvolution(image, levels, gain_factors, color=True):
    if color:
        # Convert image to RGB
        image = image.convert("RGB")
        data = np.array(image).astype(np.float32) / 255.0
        # Process each channel separately
        channels = []
        all_wavelet_planes = []
        for i in range(3):  # R, G, B channels
            channel = data[:, :, i]
            # Perform wavelet decomposition and reconstruction on this channel
            reconstructed_channel, wavelet_planes = process_channel(
                channel, levels, gain_factors
            )
            channels.append(reconstructed_channel)
            all_wavelet_planes.append(wavelet_planes)
        # Stack channels back together
        reconstructed_data = np.stack(channels, axis=2)
    else:
        # Convert image to grayscale
        image = image.convert("L")
        data = np.array(image).astype(np.float32) / 255.0  # Normalize to [0, 1]
        # Process the grayscale image
        reconstructed_data, wavelet_planes = process_channel(data, levels, gain_factors)
        all_wavelet_planes = [wavelet_planes]  # For consistency

    # Clip values to valid range
    reconstructed_data = np.clip(reconstructed_data, 0, 1)

    # Convert back to image
    if color:
        reconstructed_image = Image.fromarray(
            (reconstructed_data * 255).astype(np.uint8), "RGB"
        )
    else:
        reconstructed_image = Image.fromarray(
            (reconstructed_data * 255).astype(np.uint8), "L"
        )

    return reconstructed_image
