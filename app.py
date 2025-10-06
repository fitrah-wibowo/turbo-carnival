import subprocess
from langchain_ollama import OllamaLLM
import streamlit as st
import os

# ================================
# 📂 PAKSAKAN LOKASI MODEL OLLAMA
# ================================
os.environ["OLLAMA_MODELS"] = r"D:\FITRAH DATA 2 (PENTING)\OLLAMA"

# ------------------------
# Function to get available models from Ollama
# ------------------------
def get_available_models():
    """Return list of available Ollama models"""
    try:
        result = subprocess.run(["ollama", "list"], stdout=subprocess.PIPE, text=True)
        lines = result.stdout.strip().split("\n")
        models = []
        for line in lines[1:]:
            model_name = line.split()[0]
            models.append(model_name)
        return models
    except Exception as e:
        st.error(f"Error reading models: {e}")
        return []

# ------------------------
# Streamlit UI setup
# ------------------------

st.set_page_config(page_title="Ollama Chatbot", page_icon="🤖", layout="wide")
st.title("🤖 AI Chatbot with Auto-detected Ollama Models")

# ------------------------
# Get Ollama models location
# ------------------------
def get_models_location():
    ollama_home = os.environ.get('OLLAMA_MODELS', '~/.ollama/models')
    models_path = os.path.expanduser(ollama_home)
    return models_path

# ------------------------
# Display models location
# ------------------------
models_location = get_models_location()
st.info(f"📁 **Models Location:** `{models_location}`")

# ------------------------
# Fetch models dynamically
# ------------------------
available_models = get_available_models()

if available_models:
    selected_model = st.selectbox("Select a model:", available_models)

    llm = OllamaLLM(model=selected_model)

    st.write("💬 Ask your questions below:")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Your question:"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            response = llm.invoke(prompt)
        except Exception as e:
            response = f"❌ Error: {e}"

        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
else:
    st.error("No models detected. Please pull models using `ollama pull <model>`.")
    st.info(f"💡 Models will be stored in: `{models_location}`")
