import streamlit as st
from pathlib import Path
import streamlit.components.v1 as components
def main():
    st.set_page_config(layout="wide")
    st.title('Developer Code')
    st.markdown('---')

    st.header('Automation In Spam Detection Code')
    st.markdown('---')
    st.write('''
    The algorithm works by mapping messages into a high-dimensional space based on features like word patterns
    and frequency.
    It then finds the optimal hyperplane that separates spam from non-spam.
    The algorithm automatically classifies new messages by determining which side of the hyperplane they fall on, 
    enabling fast and accurate spam detection.
    ''')
    html_file=Path('wordnetlemmatizer.html')
    components.html(html_file.read_text(encoding='utf-8',errors='replace'),height=1000,scrolling=True)
if __name__ == '__main__':
    main()