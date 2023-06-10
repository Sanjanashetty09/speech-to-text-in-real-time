# Libraries to be used ------------------------------------------------------------

import streamlit as st
import requests
import json
import os
import speech_recognition as sr

# title and favicon ------------------------------------------------------------

st.set_page_config(
    page_title="Speech-to-Text Transcription App", layout="wide"
)

# App layout width -------------------------------------------------


def _max_width_():
    max_width_str = f"max-width: 1200px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>
    """,
        unsafe_allow_html=True,
    )


_max_width_()

# logo and header -------------------------------------------------

c30, c31, c32 = st.columns([2.5, 1, 3])

with c30:
    st.image("logo.png", width=350)
    st.header("")

with c32:

    st.title("")
    st.title("")
    st.caption("")
    st.caption("")
    st.caption("")
    st.caption("")
    st.caption("")
    st.caption("")

    st.write(
        "&nbsp &nbsp Made in [![this is an image link](https://i.imgur.com/iIOA6kU.png)](https://www.streamlit.io/)&nbsp, with :heart: by [@DataChaz](https://www.charlywargnier.com/) | [![this is an image link](https://i.imgur.com/thJhzOO.png)](https://www.buymeacoffee.com/cwar05)"
    )

st.text("")
st.markdown(
    f"""
                    The speech to text recognition is done via the [Facebook's Wav2Vec2 model.](https://huggingface.co/facebook/wav2vec2-large-960h)
                    """
)
st.text("")

# region Main

# multi navbar -------------------------------------------------


def main():
    pages = {
        "👾 Free mode (2MB per API call)": demo
        #,"🤗 Full mode (with your API key)": API_key,
    }

    if "page" not in st.session_state:
        st.session_state.update(
            {
                # Default page
                "page": "Home",
            }
        )

    with st.sidebar:
        page = st.radio("Select your mode", tuple(pages.keys()))

    pages[page]()


# endregion main

# Free mode -------------------------------------------------



def demo():

    c1, c2, c3 = st.columns([1, 4, 1])
    with c2:
        with st.form(key="my_form"):
            submit_button = st.form_submit_button(label="Start Transcription 🎤")
            stop_button=st.form_submit_button(label="Stop Transcription")
        if submit_button:
            st.info("Transcription started...")  
            r = sr.Recognizer()  
            def transcribe_audio():
                with sr.Microphone() as source:
                    audio = r.listen(source)
                    try:
                        text = r.recognize_google(audio)
                        st.write(text)
                    except sr.UnknownValueError:
                        st.warning("Could not understand audio")
                    except sr.RequestError as e:
                        st.error(f"Could not request results; {e}")          
                if submit_button:
                    transcribe_audio()
                if stop_button:
                    return
            #call the function
            transcribe_audio() 



# Custom API key mode -------------------------------------------------


def API_key():

    c1, c2, c3 = st.columns([1, 4, 1])
    with c2:

        with st.form(key="my_form"):

            text_input = st.text_input("Enter your HuggingFace API key")

            f = st.file_uploader("", type=[".wav"])

            st.info(
                f"""
                        👆 Upload a .wav file. Or try a sample: [Wav sample 01](https://github.com/CharlyWargnier/CSVHub/blob/main/Wave_files_demos/Welcome.wav?raw=true) | [Wav sample 02](https://github.com/CharlyWargnier/CSVHub/blob/main/Wave_files_demos/The_National_Park.wav?raw=true)
                        """
            )

            submit_button = st.form_submit_button(label="Transcribe")

    if not submit_button:

        st.stop()

    else:

        try:

            if f is not None:
                path_in = f.name
                # Get file size from buffer
                # Source: https://stackoverflow.com/a/19079887
                old_file_position = f.tell()
                f.seek(0, os.SEEK_END)
                getsize = f.tell()  # os.path.getsize(path_in)
                f.seek(old_file_position, os.SEEK_SET)
                getsize = round((getsize / 1000000), 1)
                # st.caption("The size of this file is: " + str(getsize) + "MB")
                # getsize

                if getsize < 30:  # File more than 30MB

                    # To read file as bytes:
                    bytes_data = f.getvalue()

                    api_token = "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"

                    headers = {"Authorization": f"Bearer {api_token}"}
                    API_URL = "https://api-inference.huggingface.co/models/facebook/wav2vec2-base-960h"

                    def query(data):
                        response = requests.request(
                            "POST", API_URL, headers=headers, data=data
                        )
                        return json.loads(response.content.decode("utf-8"))

                    data = query(bytes_data)

                    # data = query(bytes_data)

                    values_view = data.values()
                    value_iterator = iter(values_view)
                    text_value = next(value_iterator)
                    text_value = text_value.lower()

                    st.success(text_value)

                    c0, c1 = st.columns([2, 2])

                    with c0:
                        st.download_button(
                            "Download the transcription",
                            text_value,
                            file_name=None,
                            mime=None,
                            key=None,
                            help=None,
                            on_click=None,
                            args=None,
                            kwargs=None,
                        )

                else:
                    st.error(
                        "This app is still in early development so we've maxed out the file size limit. Please try again with a smaller file."
                    )
                    st.stop()

            else:
                path_in = None
                st.info(
                    f"""
                        👆 Upload a .wav file. Or try a sample: [Wav sample 01](https://github.com/CharlyWargnier/CSVHub/blob/main/Wave_files_demos/Welcome.wav?raw=true) | [Wav sample 02](https://github.com/CharlyWargnier/CSVHub/blob/main/Wave_files_demos/The_National_Park.wav?raw=true)
                        """
                )

        except ValueError:
            "ValueError"


# Notes about the app -------------------------------------------------

with st.expander("ℹ️ - About this app", expanded=False):

    st.write(
        """     

-   I have modified this app only for the free mode version 
-   The Free mode is limited to 2MB of the audio file. 
-   I have defined a function called transcribe_audio to perform the speech to text operation
	    """
    )

    st.markdown("")

with st.expander("🔆 Coming soon!", expanded=False):

    st.write(
        """  
-   Add more embedding models
-   Add more languages
-   Allow for larger wave files to be reviewed (currently limited to 30 MB)
-   Try using the api key method

	    """
    )

    st.markdown("")

if __name__ == "__main__":
    main()