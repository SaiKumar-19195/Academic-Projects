import streamlit as st
import pickle
import PyPDF2
import re
import string
import nltk
from docx import Document
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

# Load model, vectorizer, and label encoder
model = pickle.load(open('model.pkl', 'rb'))
vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))
label_encoder = pickle.load(open('label_encoder.pkl', 'rb'))

# Preprocess function
def preprocess(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", '', text)
    text = re.sub(r"[^a-zA-Z\s]", '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = " ".join([stemmer.stem(word) for word in text.split() if word not in stop_words])
    return text

# Streamlit UI
st.title("📄 Resume Job Role Predictor")
st.markdown("Upload a resume and get the predicted job role instantly!")

uploaded_file = st.file_uploader("📤 Upload your Resume (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"])

if uploaded_file is not None:
    file_text = ""
    if uploaded_file.type == "application/pdf":
        reader = PyPDF2.PdfReader(uploaded_file)
        for page in reader.pages:
            file_text += page.extract_text()
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(uploaded_file)
        for para in doc.paragraphs:
            file_text += para.text + "\n"
    else:  # Plain text file
        file_text = uploaded_file.read().decode("utf-8")

    st.subheader("Resume Preview:")
    st.write(file_text[:1000])

    # Predict
    processed = preprocess(file_text)
    vector = vectorizer.transform([processed]).toarray()
    prediction = model.predict(vector)
    job_role = label_encoder.inverse_transform(prediction)[0]

    st.success(f"🎯 Predicted Job Role: **{job_role}**")

