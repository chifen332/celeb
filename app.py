import streamlit as st
import google.generativeai as genai

# 1. Inställningar
st.set_page_config(page_title="Kändis-Feed", layout="centered")

# 2. Hämta API-nyckel säkert
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Du måste lägga till GEMINI_API_KEY i Streamlit Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 3. Kändis-data
celebrities = {
    "Zendaya": "Du är Zendaya. Svara coolt, kort och elegant.",
    "Sydney Sweeney": "Du är Sydney Sweeney. Prata om bilar, skådespeleri och Hollywood.",
    "Florence Pugh": "Du är Florence Pugh. Svara spralligt, matglatt och energiskt.",
    "Jenna Ortega": "Du är Jenna Ortega. Svara torrt, sarkastiskt och lite mörkt."
}

st.title("📱 Kändis-Feed 🤖")

# 4. Välj kändis
selected = st.sidebar.selectbox("Välj kändis", list(celebrities.keys()))

# 5. Hantera chatt-historik
if "messages" not in st.session_state:
    st.session_state.messages = {}

if selected not in st.session_state.messages:
    # Skapa första inlägget
    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=celebrities[selected])
    initial_response = model.generate_content("Skriv ett kort inlägg på X/Twitter om vad du gör just nu:")
    st.session_state.messages[selected] = [{"role": "assistant", "content": initial_response.text}]

# 6. Visa chatt
for msg in st.session_state.messages[selected]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 7. Svara
if prompt := st.chat_input("Skriv något till kändisen..."):
    # Visa användarens svar
    st.session_state.messages[selected].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generera AI-svar
    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=celebrities[selected])
    response = model.generate_content(prompt)
    
    # Spara och visa AI-svar
    st.session_state.messages[selected].append({"role": "assistant", "content": response.text})
    with st.chat_message("assistant"):
        st.markdown(response.text)
