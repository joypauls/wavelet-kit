⚠️ _This project is a prototype. Use at your own risk._

# Wavelet Kit

A tool for wavelet-based image deconvolution focused on the planetary imaging use case.

<div align="center">
    <img width="60%" src="./morlet_wavelet_visual.svg">
</div>

The [lucky imaging](https://en.wikipedia.org/wiki/Lucky_imaging) method is used by both amateur and professional astronomers to compensate for the effects of atmospheric seeing when imaging objects from ground-based telescopes. This method involves taking many short-exposure images, stacking the best ones to improve the signal-to-noise ratio, and applying deconvolution to sharpen the stacked image. Wavelet Kit offers tools meant to enhance the experience of the deconvolution process.

## Experimental Results

<div align="center">
    <img src="./test_results.png">
</div>

## Development

### Setup Environment

Requires poetry. Right now the whole project comes bundled together with app and dev dependencies mixed.

`poetry install`
