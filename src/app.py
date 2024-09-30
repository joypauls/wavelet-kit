import streamlit as st
import cv2

# import numpy as np
# from PIL import Image

DEFAULT_LAYERS = 6
MIN_LAYERS = 1
MAX_LAYERS = 8
MIN_LAYER_GAIN = 0.0
MAX_LAYER_GAIN = 10.0


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

    wavelet = st.sidebar.selectbox("Select Wavelet:", ["B-Spline"])
    layers = st.sidebar.number_input(
        "Layers", MIN_LAYERS, MAX_LAYERS, DEFAULT_LAYERS, 1
    )
    layer_gain_values = []
    for i in range(layers):
        layer_gain_values.append(
            st.sidebar.slider(f"Layer {i+1}", MIN_LAYER_GAIN, MAX_LAYER_GAIN, 1.0, 0.1)
        )
    return wavelet, layer_gain_values


# Streamlit app
def main():
    # st.title("Image Color Space Viewer")

    # Load a local test image
    test_image_path = "./src/images/stacked_jupiter.tiff"
    image = cv2.imread(test_image_path)

    wavelet, layer_gain_values = build_sidebar()

    if image is None:
        st.error("Failed to load the test image. Please check the path.")
        return

    if image is not None:
        st.markdown(layer_gain_values)
        st.image(
            cv2.cvtColor(image, cv2.COLOR_BGR2RGB),
            caption="Original Image",
            use_column_width=True,
        )

    else:
        st.error("Failed to load the test image.")


if __name__ == "__main__":
    main()
