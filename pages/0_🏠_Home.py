import streamlit as st

st.set_page_config(
    page_title="Special Circumstances RPG Character Manager",
    page_icon="🎲",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS for styling ---
st.markdown("""
<style>
    /* Center the main header image */
    div[data-testid="stImage"] > img {
        display: block;
        margin-left: auto;
        margin-right: auto;
    }

    /* Style the feature columns */
    @media (min-width: 576px) {
        div[data-testid="stHorizontalBlock"] > div[data-testid="stVerticalBlock"] {
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            padding: 25px;
            margin: 0 10px;
            border: 1px solid #262730;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
# The image is now centered by the CSS above
st.image("assets/header.jpg", width=800)

st.divider()

st.title("Special Circumstances RPG Character Manager")
st.subheader("Create and manage your RPG characters with ease!")

st.markdown("---")

# --- FEATURES ---
st.header("Features")
col1, col2 = st.columns(2)

with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/2098/2098402.png", width=100)
    st.subheader("Create Character")
    st.write("Fill out a form to generate a new character sheet in Markdown format.")
    st.page_link("pages/1_➕_Create_Character.py", label="**Go to Create Character**", use_container_width=True)

with col2:
    st.image("https://cdn-icons-png.flaticon.com/512/3597/3597088.png", width=100)
    st.subheader("Edit Character")
    st.write("Upload an existing character sheet to edit and update it.")
    st.page_link("pages/2_📝_Edit_Character.py", label="**Go to Edit Character**", use_container_width=True)

st.markdown("---")
