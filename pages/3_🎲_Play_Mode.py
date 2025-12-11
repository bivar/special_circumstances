import streamlit as st
from src.character import Character
from src.components import play_mode_sheet
import json

st.set_page_config(
    page_title="Play Mode",
    page_icon="🎲",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("Play Mode")

# Sidebar for character selection
with st.sidebar:
    st.header("Character Management")
    
    uploaded_file = st.file_uploader("Load Character", type="json")
    if uploaded_file is not None:
        try:
            json_string = uploaded_file.getvalue().decode("utf-8")
            st.session_state.character = Character.from_json(json_string)
            st.success(f"Character '{st.session_state.character.name}' loaded!")
        except Exception as e:
            st.error(f"Could not load character: {e}")

    if 'character' in st.session_state:
        char_name = st.session_state.character.name.replace(" ", "_")
        st.download_button(
            label="Save Character",
            data=st.session_state.character.to_json(),
            file_name=f"{char_name}.json",
            mime="application/json",
        )

# Main content area
if 'character' in st.session_state:
    play_mode_sheet(st.session_state.character)
else:
    st.info("Upload a character file from the sidebar to begin your session.")
    st.image("assets/header.jpg")
