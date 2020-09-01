import streamlit as st
from streamlit_drawable_canvas import st_canvas
from torch_utils import transform_image,  get_prediction
from PIL import Image
import numpy as np

st.beta_set_page_config(
    page_title="Handwritten Letters Classifier",
    page_icon=":rainbow:",
)


hide_streamlit_style = """
            <style>
            # MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.title("Handwritten Letters Classifier")


def predict(image):
    image = Image.fromarray((image[:, :, 0]).astype(np.uint8))
    image = image.resize((28, 28))
    tensor = transform_image(image)
    prediction = get_prediction(tensor)
    return prediction


# Specify brush parameters and drawing mode
stroke_width = st.sidebar.slider("Stroke width: ", 1, 100, 40)
drawing_mode = st.sidebar.selectbox(
    "Drawing tool:", ("freedraw", "transform")
)

# Create a canvas component
canvas_result = st_canvas(
    stroke_width=stroke_width,
    stroke_color="#fff",
    background_color="#000",
    height=280,
    width=280,
    drawing_mode=drawing_mode,
    key="canvas",
)

result = st.button("Predict")

# Do something interesting with the image data
if canvas_result.image_data is not None and result:
    st.write("Prediction : ", predict(canvas_result.image_data))
