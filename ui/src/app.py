import streamlit as st
from utils import classify_doc

# Set page configuration
st.set_page_config(
    page_title="DoClasiq"
)


# Inject custom CSS to hide the Streamlit state
hide_streamlit_style = """
            <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)



# Page content
st.markdown(
    """
    <div style="text-align: center;">
        <h1>DoClasiq</h1>
        <h3>Welcome to DoClasiq</h3>
        <h4>Start Classifying Documents and extracting key data!</h4>
    </div>
    """,
    unsafe_allow_html=True
)


file = st.file_uploader("Upload Pdf files", type=["pdf"])

if st.button("Submit"):
    with st.spinner("classification in progress..."):
        classified_output, extracted_data = classify_doc(file)
        st.write("Classified as: ", classified_output)
        st.write("Extracted Data: ", extracted_data)
    