import streamlit as st
import cv2
# import numpy as np
# from PIL import Image

def build_sidebar():
    st.sidebar.title("Image Color Space Viewer")
    # st.sidebar.markdown(
    #     """
    #     This app allows you to view an image in different color spaces. 
    #     You can select the color space from the dropdown menu.
    #     """
    # )
    color_space = st.sidebar.selectbox(
        "Select algorithm:", ["Wavelet 1", "Wavelet 2"]
    )
    st.sidebar.markdown("Layers")
    st.sidebar.slider("Layer 1", 0.0, 1.0, 0.5)
    st.sidebar.slider("Layer 2", 0.0, 1.0, 0.5)
    st.sidebar.slider("Layer 3", 0.0, 1.0, 0.5)
    return color_space


# Streamlit app
def main():
    # st.title("Image Color Space Viewer")

    # Load a local test image
    test_image_path = "./src/images/stacked_jupiter.tiff"
    image = cv2.imread(test_image_path)

    build_sidebar()

    if image is None:
        st.error("Failed to load the test image. Please check the path.")
        return

    if image is not None:
        st.image(
            cv2.cvtColor(image, cv2.COLOR_BGR2RGB),
            caption="Original Image",
            use_column_width=True,
        )

    else:
        st.error("Failed to load the test image.")


if __name__ == "__main__":
    main()
