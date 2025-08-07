import streamlit as st
import google.generativeai as genai
from google.api_core import retry
from google.api_core import exceptions as google_exceptions
import time


def main():
    # Initialize app with wide layout
    st.set_page_config(layout="wide")
    st.title("AI Automation For BlueTeamers")
    st.markdown('---')

    # Header section with logo and title
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image('blueteamergpt.jpeg', width=400)
    with col2:
        st.title('BlueTeamerGPT')
        st.code('AI-Driven Defense for a Safer Cyber World')
        st.code('For Red and Blue Teamers')

    # Load Gemini API key from Streamlit secrets
    try:
        gemini_api_key = st.secrets["api"]["GEMINI_API_KEY"]
    except KeyError:
        st.error("GEMINI_API_KEY not found in Streamlit secrets. Please check your secrets.toml or Streamlit Cloud settings.")
        st.stop()

    # Configure Gemini with error handling
    try:
        with st.spinner("Connecting To BlueTeamerGPT"):
            genai.configure(api_key=gemini_api_key)
            model = genai.GenerativeModel(
                'gemini-1.5-flash',
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=200,
                    temperature=0.3
                )
            )
    except Exception as e:
        st.error(f"Failed to configure Gemini: {str(e)}")
        st.stop()

    system_instruction = (
        "You are strictly a systems and security assistant chatbot for red teamers and blue teamers in cybersecurity. "
        "If asked something which is not within your scope, answer with "
        "'I am just a systems and security assistant so I cannot help you with that.' "
        "You answer questions and give advice on how to secure systems and avoid exploitation. "
        "Keep your responses brief and limit them to 200 tokens. "
        "Answer respectfully when someone uses abusive language."
    )

    # Custom retry configuration
    custom_retry = retry.Retry(
        initial=1.0,
        maximum=10.0,
        multiplier=2.0,
        deadline=60.0,
        predicate=retry.if_exception_type(
            google_exceptions.DeadlineExceeded,
            google_exceptions.ServiceUnavailable
        )
    )

    # Function to display roles correctly
    def translate_role(role):
        return "assistant" if role == "model" else role

    # Initialize chat session with retry logic
    if "chat_session" not in st.session_state:
        try:
            with st.spinner("Initializing BlueTeamerGPT security protocols..."):
                st.session_state.chat_session = model.start_chat(history=[])
                custom_retry(st.session_state.chat_session.send_message)(
                    content=system_instruction,
                    generation_config=genai.types.GenerationConfig(
                        max_output_tokens=200,
                        temperature=0.3
                    )
                )
        except Exception as e:
            st.error(f"Failed to initialize chat session: {str(e)}")
            st.stop()

    # Show conversation history
    if "chat_session" in st.session_state:
        for message in st.session_state.chat_session.history[1:]:
            with st.chat_message(translate_role(message.role)):
                st.markdown(message.parts[0].text)

    # Get user input
    user_prompt = st.chat_input(" Ready when you are")
    if user_prompt:
        st.chat_message("user").markdown(user_prompt)

        try:
            with st.spinner("BlueTeamerGPT is analyzing your query..."):
                response = custom_retry(st.session_state.chat_session.send_message)(
                    content=user_prompt,
                    generation_config=genai.types.GenerationConfig(
                        max_output_tokens=200,
                        temperature=0.3
                    ),
                    stream=False
                )
            with st.chat_message("assistant"):
                st.markdown(response.text)

        except google_exceptions.DeadlineExceeded:
            with st.spinner(""):
                time.sleep(0.5)
                st.error("Our systems are experiencing high load. Please try again in a moment.")
        except Exception as e:
            with st.spinner(""):
                time.sleep(0.5)
                st.error(f"Security systems overloaded: {str(e)}")

if __name__ == '__main__':
    main()
