import streamlit as st
from src.components import character_creation_wizard

st.set_page_config(
    page_title="Create Character",
    page_icon="➕",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.title("Character Creation")

st.image("assets/create_character.jpg")

character_creation_wizard()