import streamlit as st
from streamlit_drawable_canvas import st_canvas
from torch_utils import transform_image,  get_prediction
from PIL import Image
import numpy as np
import pandas as pd
import time

from torch.nn.functional import softmax
import torch

st.set_page_config(
    page_title="Handwritten Letters Classifier",
    page_icon=":pencil:",
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


def np_to_df(outputs):  # Create a 2D array for the dataframe instead of a 1D array
    length = outputs.shape[0]  # Total outputs
    outputs = softmax(torch.from_numpy(outputs / 3.5), dim=0).cpu().detach().numpy()
    arr = []
    for pos in range(0, length):
        line = [0]*26
        line[pos] = outputs[pos]
        arr.append(line)
    return arr


# Specify brush parameters and drawing mode
stroke_width = st.sidebar.slider("Stroke width: ", 1, 100, 25)


# Create a canvas component
canvas_result = st_canvas(
    stroke_width=stroke_width,
    stroke_color="#fff",
    background_color="#000",
    height=280,
    width=280,
    drawing_mode="freedraw",
    key="canvas",
)

result = st.button("Predict")

if canvas_result.image_data is not None and result:
    outputs = predict(canvas_result.image_data)
    ind_max = np.where(outputs == max(outputs))[
        0][0]  # Index of the max element
    # Converting index to equivalent letter
    progress_bar = st.progress(0)
    for i in range(100):
        progress_bar.progress(i + 1)
        time.sleep(0.01)
    st.markdown("<h3 style = 'text-align: center;'>Prediction : {}<h3>".format(
        chr(97 + ind_max)), unsafe_allow_html=True)
    chart_data = pd.DataFrame(np_to_df(outputs), index=[
                              'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'], columns=[
                              'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])
    st.bar_chart(chart_data)
    st.balloons()
