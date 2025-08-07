import pickle
import streamlit as st

# Load the TF-IDF vectorizer and SVM model separately
tfidf_loaded = pickle.load(open("tfidf_vectorizer.pickle", "rb"))
svm_loaded_model = pickle.load(open("SVC.pickle.dat", "rb"))



# Function to predict if the input message is spam or not
def predict_spam(message):
    # Transform the message using the TF-IDF vectorizer
    message_tfidf = tfidf_loaded.transform([message])

    # Convert the sparse matrix to a dense format
    message_tfidf_dense = message_tfidf.toarray()

    # Predict using the loaded SVM model
    prediction = svm_loaded_model.predict(message_tfidf_dense)
    return st.warning("""## ⚠️⚠️SPAM ALERT⚠️⚠️:This message has been flagged as potentially malicious.  
### Possible Threat Categories.

#### 1.Phishing

#### 2.Social Engineering

#### 3.Financial Fraud

#### 4.Identity Spoofing

#### 5.Malicious URLs

#### 6.Malware Delivery
  
  
## Proceed with extreme caution...""") if prediction == 1 else st.info("""## ✅✅ This message is not spam ✅✅: 
## This message does not appear to be spam based on the current threat detection algorithms.
### Suggested Categories For Non-Spam Messages

#### 1.Personal Communication

#### 2.Work/Professional

#### 3.Support/Feedback

#### 4.Transactional

#### 5.Informational/Educational
   
## You may proceed normally, but always stay vigilant.""")

st.title('Wanheda For Defensive Security')
st.code(' Defensive Security for a Spam-Free Future')
st.markdown('---')
col1, col2 = st.columns(2)
with col1:
    st.image('wanheda.png')
with col2:
    st.title('Wanheda Spam Detector')

st.markdown("---")

st.subheader('Introduction')
st.write('''
Wanheda is a next-generation SMS and email spam detection system built with a strong foundation
in defensive security principles. Designed to identify, analyze, and neutralize malicious messages
in real-time, Wanheda leverages advanced filtering algorithms and threat intelligence to protect
users from phishing, social engineering, and unsolicited spam. 
''')

st.markdown("---")

st.header('Algorithm Functionality')

st.write('''
In spam detection,The algorithm works by converting SMSs into feature vectors.
The algorithm then finds a decision boundary that best separates spam from non-spam SMS. 
It looks at the message’s structure, language, and behavior — like unusual links, 
suspicious words, or strange sender patterns. Once a message shows signs of being harmful or unwanted, 
Wanheda flags it
''')

st.markdown("---")

st.write("## Message Type Selection")

col1, col2 = st.columns(2)
with col1:
    st.image('email.jpeg')
with col2:
    message_type=st.radio("Select the message type",['SMS','Email'])

    if message_type=='SMS':
        st.info('The system will analyse SMS messages')
    else:
        st.info('The system will analyse Email messages')
st.markdown('---')

col1, col2 = st.columns(2)
with col1:
    st.image('scamalert2.jpg')
with col2:
    st.image('scamalert.jpg')

# User input for the message to check
user_message = st.text_area('Enter the message to check:')

# Button to trigger prediction
if st.button('Submit'):
    if user_message:
        result = predict_spam(user_message)
        st.info('#### The message was analysed by an automated algorithm and classification is based on past Data.So prediction made should also be reconsidered incase of misclassification')
    else:
        st.write('Please enter a message to check.')





