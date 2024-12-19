import streamlit as st
import openai
import requests
from dotenv import load_dotenv
import os
from PIL import Image
import io
#by default it is using dall e 3 model

# Load environment variables
load_dotenv()

# Configure OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Custom CSS with dark theme
st.markdown("""
    <style>
        /* Dark theme background and elements */
        .stApp {
            background: linear-gradient(to right bottom, 
                                     #1a1a1a, 
                                     #2d2d2d);
        }
        .main {
            color: #ffffff;
        }
        .stTextInput > div > div > input {
            background-color: #3d3d3d !important;
            color: #ffffff !important;
            border-color: #4f4f4f !important;
            border-radius: 5px;
        }
        .stSelectbox > div > div > div {
            background-color: #3d3d3d !important;
            color: #ffffff !important;
        }
        .stButton > button {
            background-color: #7289da !important;
            color: white !important;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            border: none;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #5f73bc !important;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            transform: translateY(-2px);
        }
        /* Slider customization */
        .stSlider > div > div > div > div {
            background-color: #7289da !important;
        }
        /* Header styling */
        h1 {
            color: #ffffff !important;
            text-align: center;
            padding: 1rem;
            border-bottom: 2px solid #7289da;
            margin-bottom: 2rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        /* Custom container for the main content */
        .custom-container {
            background-color: rgba(45, 45, 45, 0.7);
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            margin: 1rem;
            backdrop-filter: blur(10px);
        }
        /* Style for labels */
        .stTextInput > label, .stSlider > label {
            color: #ffffff !important;
        }
        /* Download button styling */
        .stDownloadButton > button {
            background-color: #43b581 !important;
            color: white !important;
        }
        .stDownloadButton > button:hover {
            background-color: #3ca374 !important;
        }
        /* Spinner color */
        .stSpinner > div > div {
            border-top-color: #7289da !important;
        }
        /* Warning message styling */
        .stAlert {
            background-color: rgba(240, 173, 78, 0.2) !important;
            color: #ffffff !important;
        }
    </style>
""", unsafe_allow_html=True)


def generate_image(prompt, size="1024x1024"):
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size=size
        )
        return response['data'][0]['url']
    except Exception as e:
        st.error(f"Error generating image: {str(e)}")
        return None


def main():
    st.title("🌌 AI Image Generator")

    # Wrap the main content in a custom container
    with st.container():
        st.markdown('<div class="custom-container">', unsafe_allow_html=True)

        # Create columns for better layout
        col1, col2 = st.columns([2, 1])

        with col1:
            prompt = st.text_input(
                "Enter your image prompt:",
                placeholder="Example: A cyberpunk city at night",
                key="prompt_input"
            )

        with col2:
            size_options = ["256x256", "512x512", "1024x1024"]
            size = st.select_slider("Select image size:", options=size_options)

        # Center the generate button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            generate_clicked = st.button("🎨 Generate Image")

        if generate_clicked:
            if not prompt:
                st.warning("Please enter a prompt first!")
            else:
                with st.spinner("🌟 Creating your masterpiece..."):
                    image_url = generate_image(prompt, size)

                    if image_url:
                        try:
                            response = requests.get(image_url)
                            image = Image.open(io.BytesIO(response.content))

                            img_col1, img_col2, img_col3 = st.columns([1, 6, 1])
                            with img_col2:
                                st.image(image, caption=prompt, use_column_width=True)

                            buf = io.BytesIO()
                            image.save(buf, format='PNG')
                            col1, col2, col3 = st.columns([1, 2, 1])
                            with col2:
                                btn = st.download_button(
                                    label="💾 Download Image",
                                    data=buf.getvalue(),
                                    file_name=f"{prompt[:30]}.png",
                                    mime="image/png"
                                )
                        except Exception as e:
                            st.error(f"Error downloading image: {str(e)}")

        st.markdown('</div>', unsafe_allow_html=True)

    # Add footer
    st.markdown("""
        <div style='text-align: center; color: #808080; padding: 20px;'>
            Made with 💜 using Streamlit and OpenAI(dall-e-3)
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()