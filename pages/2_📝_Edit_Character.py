import streamlit as st
from src.character import Character
from src.components import character_sheet
import json

st.set_page_config(
    page_title="Edit Character",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("View & Edit Character")

# Sidebar for uploading, downloading, and dice rolling
with st.sidebar:
    st.header("Character Management")

    # --- Template Download ---
    # Create a blank character to serve as a template
    template_char = Character()
    # Set default name to empty so user knows to fill it
    template_char.name = "" 
    template_json = template_char.to_json()

    st.download_button(
        label="Download Template (.json)",
        data=template_json,
        file_name="character_template.json",
        mime="application/json",
    )
    st.caption("New to the app? Download a template file, fill it out, and upload it below.")
    st.divider()
    
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
    
    st.divider()

# Main content area
if 'character' in st.session_state:
    character_sheet(st.session_state.character)
else:
    st.info("Upload a character file from the sidebar to begin.")
    st.image("assets/header.jpg")