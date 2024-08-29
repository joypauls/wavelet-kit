import streamlit as st
import cv2
import numpy as np
from PIL import Image


# Function to convert the image to the selected color space and split the channels
def convert_and_split(image, color_space):
    if color_space == "RGB":
        converted = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        channels = cv2.split(converted)
        channel_labels = ["R", "G", "B"]
    elif color_space == "HSV":
        converted = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        channels = cv2.split(converted)
        channel_labels = ["H", "S", "V"]
    else:
        converted = image
        channels = [converted]
        channel_labels = ["Original"]

    return channels, channel_labels


# Streamlit app
def main():
    st.title("Image Color Space Viewer")
    st.write(
        "Upload an image or use a built-in test image to view its channels in different color spaces."
    )

    # Option to upload an image or use a test image
    option = st.radio("Select Image Source", ("Upload Image", "Use Test Image"))

    if option == "Upload Image":
        uploaded_file = st.file_uploader(
            "Choose an image...", type=["jpg", "jpeg", "png"]
        )

        if uploaded_file is not None:
            image = np.array(Image.open(uploaded_file))
        else:
            st.warning("Please upload an image to proceed.")
            return
    else:
        # Load a local test image
        test_image_path = "./src/images/peppers.png"
        image = cv2.imread(test_image_path)

        if image is None:
            st.error("Failed to load the test image. Please check the path.")
            return

    if image is not None:
        st.image(
            cv2.cvtColor(image, cv2.COLOR_BGR2RGB),
            caption="Original Image",
            use_column_width=True,
        )

        color_space = st.selectbox("Select Color Space", ("RGB", "HSV", "Grayscale"))

        channels, channel_labels = convert_and_split(image, color_space)

        st.write(f"Displaying channels for {color_space} color space:")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.image(
                channels[0],
                caption=f"{channel_labels[0]} Channel",
                use_column_width=True,
            )

        with col2:
            st.image(
                channels[1],
                caption=f"{channel_labels[1]} Channel",
                use_column_width=True,
            )

        with col3:
            st.image(
                channels[2],
                caption=f"{channel_labels[2]} Channel",
                use_column_width=True,
            )

        # for channel, label in zip(channels, channel_labels):
        #     if len(channel.shape) == 2:  # Grayscale or single channel
        #         st.image(channel, caption=f"{label} Channel", use_column_width=True)
        #     else:
        #         st.image(
        #             cv2.merge([channel] * 3),
        #             caption=f"{label} Channel",
        #             use_column_width=True,
        #         )
    else:
        st.error("Failed to load the test image.")


if __name__ == "__main__":
    main()
