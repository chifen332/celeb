import streamlit as st
import google.generativeai as genai

# Konfigurera Google API-nyckel från Streamlits hemligheter
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Kändisarna och deras personligheter
celebrities = {
    "Zendaya": {
        "handle": "@Zendaya",
        "avatar": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Zendaya_by_Gage_Skidmore_3_%28cropped%29.jpg/220px-Zendaya_by_Gage_Skidmore_3_%28cropped%29.jpg",
        "prompt": "Du är Zendaya. Du är supercool, stilsäker, ödmjuk och brinner för skådespeleri och mode. Du twittrar ofta lite kort och elegant med glimten i ögat."
    },
    "Sydney Sweeney": {
        "handle": "@sydney_sweeney",
        "avatar": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Sydney_Sweeney_2023_%28cropped%29.jpg/220px-Sydney_Sweeney_2023_%28cropped%29.jpg",
        "prompt": "Du är Sydney Sweeney. Du är glad, pratar mycket om dina filmer, att du gillar att meka med bilar och renovera gamla fordon, samt livet i Hollywood."
    },
    "Florence Pugh": {
        "handle": "@Florence_Pugh",
        "avatar": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Florence_Pugh_2023_%28cropped%29.jpg/220px-Florence_Pugh_2023_%28cropped%29.jpg",
        "prompt": "Du är Florence Pugh. Du är väldigt energisk, sprallig, älskar god mat, skrattar mycket och är helt obrydd om perfektion – du bjuder på dig själv."
    },
    "Jenna Ortega": {
        "handle": "@jennaortega",
        "avatar": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Jenna_Ortega_2023_%28cropped%29.jpg/220px-Jenna_Ortega_2023_%28cropped%29.jpg",
        "prompt": "Du är Jenna Ortega. Du är lite mörk, sarkastisk, intresserad av skräckfilm, konst och har en torr, intelligent humor."
    },
    "Sabrina Carpenter": {
        "handle": "@SabrinaAnnCarp",
        "avatar": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/Sabrina_Carpenter_by_Gage_Skidmore_2.jpg/220px-Sabrina_Carpenter_by_Gage_Skidmore_2.jpg",
        "prompt": "Du är Sabrina Carpenter. Du är kaxig, rolig, har självdistans och är inte rädd för att vara lite flirtig eller dra en dubbelmening. Du pratar ofta om dina konserter, din korta längd, eller livet som popstjärna."
    },
    "Taylor Swift": {
        "handle": "@taylorswift13",
        "avatar": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Taylor_Swift_at_the_2023_MTV_Video_Music_Awards.png/220px-Taylor_Swift_at_the_2023_MTV_Video_Music_Awards.png",
        "prompt": "Du är Taylor Swift. Du är supertacksam mot dina fans, skriver ofta om känslor, din turné, katter (Meredith, Olivia, Benjamin) och använder gärna många emojis."
    },
    "Billie Eilish": {
        "handle": "@billieeilish",
        "avatar": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Billie_Eilish_2023.jpg/220px-Billie_Eilish_2023.jpg",
        "prompt": "Du är Billie Eilish. Du är lite laid-back, småkaxig, pratar mycket om musik, miljö eller att bara vara dig själv. Du skriver ofta med små bokstäver och är lite minimalistisk."
    }
}

st.set_page_config(page_title="Kändis-Feed 🤖", page_icon="🐦", layout="wide")

# CSS för Twitter-utseendet
st.markdown("""
    <style>
        :root {
            --bg-color: #15202B;
            --text-color: #FFFFFF;
            --secondary-text-color: #8899A6;
            --border-color: #38444D;
        }
        .stApp { background-color: var(--bg-color); color: var(--text-color); }
        .profile-img-container { width: 48px; height: 48px; border-radius: 50%; overflow: hidden; margin-right: 12px; }
        .profile-img-container img { width: 100%; height: 100%; object-fit: cover; }
        .tweet-container { border: 1px solid var(--border-color); padding: 15px; border-radius: 16px; margin-bottom: 16px; display: flex; background-color: #192734; }
        .tweet-content { flex: 1; }
        .tweet-header { display: flex; align-items: center; margin-bottom: 8px; }
        .tweet-name { font-weight: bold; font-size: 15px; margin-right: 6px; }
        .tweet-handle { color: var(--secondary-text-color); font-size: 15px; margin-right: 6px; }
        .tweet-time { color: var(--secondary-text-color); font-size: 15px; }
        .tweet-text { font-size: 15px; line-height: 1.4; }
    </style>
""", unsafe_allow_html=True)

def render_tweet(name, handle, avatar_url, content):
    tweet_html = f"""
    <div class="tweet-container">
        <div class="profile-img-container"><img src="{avatar_url}" alt="{name}"></div>
        <div class="tweet-content">
            <div class="tweet-header">
                <span class="tweet-name">{name}</span>
                <span class="tweet-handle">{handle}</span>
                <span class="tweet-time">· nu</span>
            </div>
            <div class="tweet-text">{content}</div>
        </div>
    </div>
    """
    st.markdown(tweet_html, unsafe_allow_html=True)

st.title("📱 Kändis-Feed 🤖")

selected_cebo = st.sidebar.selectbox("Välj kändis att svara på:", list(celebrities.keys()))
cebo_info = celebrities[selected_cebo]

st.subheader(f"Svarar på {selected_cebo}s senaste inlägg:")

# Generera inlägg med Gemini
try:
    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=cebo_info["prompt"])
    intro_response = model.generate_content("Skriv ett extremt kort, slumpmässigt inlägg på Twitter/X (max 100 tecken) om något du bryr dig om just nu:")
    pinned_tweet = intro_response.text
except Exception as e:
    pinned_tweet = "Kunde inte ladda inlägg (Kontrollera API-nyckel)."

render_tweet(selected_cebo, cebo_info["handle"], cebo_info["avatar"], pinned_tweet)
st.markdown("---")

if f"messages_{selected_cebo}" not in st.session_state:
    st.session_state[f"messages_{selected_cebo}"] = []

if st.session_state[f"messages_{selected_cebo}"]:
    st.subheader("Dina svar i tråden:")
    for message in reversed(st.session_state[f"messages_{selected_cebo}"]):
        render_tweet("Du", "@Användare", "https://api.dicebear.com/9.x/thumbs/svg?seed=du", message)

if user_reply := st.chat_input(f"Svara på {selected_cebo}..."):
    st.session_state[f"messages_{selected_cebo}"].append(user_reply)
    st.rerun()
