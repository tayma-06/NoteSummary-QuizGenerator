import streamlit as st
from api_calling import note_generator, audio_transcript, quiz_generator
from PIL import Image

st.title("Note Summary and Quiz Generator")
st.markdown("Upload upto 3 images to generate Note summary and Quizzes")
st.divider()

with st.sidebar:
    st.header("Controls")

    #images
    images = st.file_uploader("Upload the photos of your note", type=["jpg","jpeg","png"], accept_multiple_files=True)
    pil_images = [Image.open(img) for img in images]
    if pil_images:
        if len(images) > 3:
            st.error("Upload at max 3 images")
        else:
            st.subheader("Uploaded Images")
            col = st.columns(len(images))
            for i, img in enumerate(images):
                col[i].image(img)
    
    #difficulty
    selected_option = st.selectbox("Enter the difficulty of your quiz", ("Easy", "Medium", "Hard"), index = None)

    #button
    pressed = st.button("Click the button to initiate AI", type="primary")

if pressed:
    if not images:
        st.error("You must upload 1 image")
    if not selected_option:
        st.error("You must select a difficulty")
    
    if images and selected_option:
        #note
        with st.container(border=True):
            st.subheader("Your Note")
            with st.spinner("Generating your note..."):
                generated_notes = note_generator(pil_images)
                st.markdown(generated_notes)

        #audio transcript
        with st.container(border=True):
            st.subheader("Audio Transcript")
            with st.spinner("Generating audio transcript..."):
                generated_notes = generated_notes.replace("#", "").replace("##", "").replace("###", "")
                generated_notes = generated_notes.replace("*", "").replace("-", "").replace("**", "")
                generated_notes = generated_notes.replace("\n", " ") 
                generated_notes = generated_notes.replace(",", "").replace(".", "") 
                audio_buffer = audio_transcript(generated_notes)
                st.audio(audio_buffer)

        #quiz
        with st.container(border=True):
            st.subheader(f"Quiz ({selected_option} difficulty)")
            with st.spinner("Generating quiz..."):
                quizzes = quiz_generator(pil_images, selected_option)
                st.markdown(quizzes)