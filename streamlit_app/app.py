import streamlit as st
from transformers import BertTokenizer, BertForSequenceClassification
import torch


@st.cache_resource
def load_model():
    model = BertForSequenceClassification.from_pretrained("choco07/phishing-bert")
    tokenizer = BertTokenizer.from_pretrained("choco07/phishing-bert")
    return model, tokenizer

model, tokenizer = load_model()

st.title("Phishing Email Detector")
email_checker =st.text_area("paste the email text here brochacho: ", height="content")
if st.button("Check email"):
    inputs = tokenizer(email_checker, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs) ##i dont rlly understand how ** works here like idk man
    probs = torch.softmax(outputs.logits, dim=1)[0]
    label = "Phishing" if torch.argmax(probs).item() == 1 else "legit"
    confidence = probs.max().item()
    st.write(f"**{label}** (confidence: {confidence:.2%})")