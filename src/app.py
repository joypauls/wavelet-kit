import streamlit as st
import cv2

from prototype_algorithm import atrous_wavelet_deconvolution

# import numpy as np
# from PIL import Image

DEFAULT_LAYERS = 6
MIN_LAYERS = 1
MAX_LAYERS = 8
MIN_LAYER_GAIN = 0.0
MAX_LAYER_GAIN = 20.0


def build_sidebar():
    hide_elements = """
        <style>
            div[data-testid="stSliderTickBarMin"],
            div[data-testid="stSliderTickBarMax"] {
                display: none;
            }
        </style>
    """
    st.markdown(hide_elements, unsafe_allow_html=True)

    # wavelet = st.sidebar.selectbox("Select Wavelet:", ["B-Spline"])
    layers = st.sidebar.number_input(
        "Layers", MIN_LAYERS, MAX_LAYERS, DEFAULT_LAYERS, 1
    )
    layer_gain_values = []
    for i in range(layers):
        layer_gain_values.append(
            st.sidebar.slider(f"Layer {i+1}", MIN_LAYER_GAIN, MAX_LAYER_GAIN, 1.0, 0.1)
        )
    return layer_gain_values


# Streamlit app
def main():
    # st.title("Image Color Space Viewer")

    # Load a local test image
    test_image_path = "./src/images/stacked_jupiter.tiff"
    image = cv2.imread(test_image_path, cv2.IMREAD_UNCHANGED)

    st.set_page_config(
        page_title="App",
        page_icon="",
    )

    layer_gain_values = build_sidebar()

    if image is None:
        st.error("Failed to load the test image. Please check the path.")
        return

    if image is not None:
        # st.markdown(layer_gain_values)

        reconstructed_image = atrous_wavelet_deconvolution(
            image, len(layer_gain_values), layer_gain_values, color=True
        )

        reconstructed_image_8bit = cv2.normalize(
            reconstructed_image, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U
        )
        image_8bit = cv2.normalize(
            image, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U
        )

        # st.markdown(reconstructed_image)

        show_original = st.toggle("Show Original Image", False)

        st.image(
            image_8bit if show_original else reconstructed_image_8bit,
            caption="Original Image" if show_original else "Processed Image",
            use_column_width=True,
            channels="BGR",
        )

    else:
        st.error("Failed to load the test image.")


main()
