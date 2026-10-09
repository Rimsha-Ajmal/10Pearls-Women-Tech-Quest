
import streamlit as st
import pandas as pd
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()
MODEL = "claude-haiku-4-5"


def ask_claude(prompt, system="You are a helpful assistant."):
    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


st.title("My AI App")

uploaded = st.file_uploader(
    "Synthetic_Banking_Treasury_Sample_Data.xlsx",
    type=["csv", "xlsx"]
)

if uploaded is not None:
    try:
        if uploaded.name.lower().endswith(".xlsx"):
            df = pd.read_excel(uploaded, engine="openpyxl")
        else:
            df = pd.read_csv(uploaded, encoding="utf-8-sig")

        st.success("Dataset uploaded successfully!")
        st.dataframe(df.head())

        question = st.text_input("Ask a question about the data")

        if st.button("Ask") and question:
            with st.spinner("Thinking..."):
                sample = df.head(50).to_csv(index=False)
                prompt = (
                    f"Here is a dataset sample:\n{sample}\n\n"
                    f"Question: {question}"
                )
                st.write(ask_claude(prompt))

    except Exception as e:
        st.error(f"Error processing the uploaded file: {e}")