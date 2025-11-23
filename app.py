import streamlit as st
import requests
import json
import time

# -------------------------
# Page config
# -------------------------
st.set_page_config(page_title="EduBridge – AI Learning Companion", layout="wide")
st.markdown(
    """
    <style>
        body {
            background-color: white;
            color: black;
        }
        .main-title { color: #005f9e !important; }
        .subtitle { color: #444444 !important; }
        .card { background-color: #f6f6f6 !important; border: 1px solid #dddddd !important; }
        .footer { color: #666666 !important; }
    </style>
    """,
    unsafe_allow_html=True
)


# -------------------------
# Model selection
# -------------------------
def select_model(lang):
    if lang == "English":
        return "llama3.1:8b"
    elif lang == "Telugu":
        return "gemma2:9b"
    elif lang == "Hindi":
        return "gemma2:9b"
    return "gemma2:9b"


# -------------------------
# Prompt builder
# -------------------------
def build_prompt(question, lang):

    if lang == "Telugu":
        return f"""
            మీరు ఒక మంచి విద్యా బోధకులు.
            కేవలం **తెలుగు** లోనే సమాధానం ఇవ్వండి.
            చిన్న వాక్యాలు ఉపయోగించండి.
            ఉదాహరణలు ఇవ్వండి.
            English పదాలు వాడకండి.

            ప్రశ్న: {question}
            """

    if lang == "Hindi":
        return f"""
            आप एक शैक्षणिक शिक्षक हैं।
            केवल **हिंदी** में उत्तर दें।
            सरल और छोटे वाक्यों का उपयोग करें।
            ज़रूरत हो तो उदाहरण दें।

            प्रश्न: {question}
            """

    return f"""
        You are an educational AI tutor.
        Answer ONLY in English.
        Use simple words and short sentences.
        Give examples.

        Question: {question}
        """

# -------------------------
# Ollama caller with streaming parsing
# -------------------------
def get_ai_answer(question: str, lang: str, max_retries: int = 2, timeout: int = 180) -> str:
    """
    Call local Ollama server and stream the response.
    Returns a plain text answer or a helpful error message.
    """
    model = select_model(lang)
    prompt = build_prompt(question, lang)

    url = "http://localhost:11434/api/generate"
    payload = {"model": model, "prompt": prompt, "stream": True}

    headers = {"Content-Type": "application/json"}

    # retry loop for transient issues (server warming up, brief network hiccup)
    for attempt in range(max_retries + 1):
        try:
            # Use stream=True to parse line-by-line JSON chunks
            resp = requests.post(url, json=payload, headers=headers, stream=True, timeout=timeout)

            # If the server returns a non-200, show the message body when possible
            if resp.status_code != 200:
                raw = resp.text
                return f"Model error (status {resp.status_code}): {raw}"

            full_output = ""
            # Some Ollama builds send newline-delimited JSON objects
            for line in resp.iter_lines(decode_unicode=True):
                if not line:
                    continue
                # Defensive: some lines might be plain text or partial JSON
                try:
                    data = json.loads(line)
                except Exception:
                    # if line isn't JSON, append it as text
                    full_output += line
                    continue

                # typical Ollama chunk has a "response" field
                if isinstance(data, dict) and "response" in data:
                    # "response" may be incremental text
                    full_output += data.get("response", "")

                # Some responses may include "done" or "done_reason" - ignore for now

            # Remove leading/trailing whitespace and return
            result = full_output.strip()
            if result == "":
                return "Model returned an empty response. Try again or check the server logs."
            return result

        except requests.exceptions.ConnectionError as e:
            # e.g., server not running or refused connection
            if attempt < max_retries:
                time.sleep(2)  # brief wait then retry
                continue
            return ("Error: Could not connect to local Ollama server. "
                    "Make sure `ollama serve` is running. (ConnectionError)")

        except requests.exceptions.ReadTimeout:
            if attempt < max_retries:
                time.sleep(1)
                continue
            return "Error: Model request timed out. Try again or increase timeout."

        except Exception as e:
            # Catch-all for other errors
            return f"Error communicating with AI model: {str(e)}"

    return "Unexpected error while contacting model."

# -------------------------
# UI style
# -------------------------
st.markdown(
    """
    <style>
    .main-title { font-size: 40px; font-weight: 800; color: #4ad4ff; text-align: center; margin-bottom: 6px; }
    .subtitle { font-size: 16px; color: #bdbdbd; text-align: center; margin-bottom: 20px; }
    .card { background-color: #111114; padding: 18px; border-radius: 12px; border: 1px solid #242424; }
    .answer-box { background-color: #0f3f2f; color: #d9f7e7; padding: 12px; border-radius: 6px; }
    .footer { text-align: center; color: #777; margin-top: 22px; font-size:12px }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# Header
# -------------------------
st.markdown("<div class='main-title'>EduBridge – Multilingual Learning Companion</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Ask questions in English, Telugu, or Hindi — answers designed for students.</div>", unsafe_allow_html=True)

# -------------------------
# Layout: left = Q&A, right = teacher demo
# -------------------------
left, right = st.columns([2, 1])

# Left: student Q&A
with left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Ask Your Doubt")

    lang = st.selectbox("Choose Language:", ["English", "Telugu", "Hindi"])
    question = st.text_area("Your Question:", placeholder="Ex: Photosynthesis ante emiti?")

    if st.button("Get Answer", use_container_width=True):
        if not question.strip():
            st.warning("Please enter a question before requesting an answer.")
        else:
            with st.spinner("Generating answer from local model..."):
                answer = get_ai_answer(question, lang)
            st.markdown("<div class='answer-box'><strong>EduBridge Answer:</strong></div>", unsafe_allow_html=True)
            st.write(answer)

    st.markdown("</div>", unsafe_allow_html=True)

# Right: simple Teacher Dashboard (demo)
with right:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Teacher Dashboard (Demo)")
    lesson_title = st.text_input("Lesson Title:")
    lesson_content = st.text_area("Lesson Content:")

    if st.button("Save Lesson", use_container_width=True):
        # Demo mode: does not persist to file. Expand here to save to DB or file if needed.
        st.success("Lesson saved (demo). You can enhance this to write to a file or DB.")

    st.markdown("</div>", unsafe_allow_html=True)

# Footer
# st.markdown("<div class='footer'>Tip: Start Ollama with <code>ollama serve</code> and keep it running while you use EduBridge.</div>", unsafe_allow_html=True)
