
import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000/api/chat"

st.set_page_config(
    page_title="NovaRetail IT Support",
    page_icon="💻",
    layout="centered",
)

# -------------------- Styling --------------------

st.markdown("""
<style>
    .block-container {
        max-width: 850px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1 {
        font-size: 1.8rem !important;
        font-weight: 650 !important;
    }

    .subtitle {
        color: #8b929e;
        margin-top: -10px;
        margin-bottom: 25px;
    }

    div.stButton > button {
        border-radius: 12px;
        min-height: 45px;
        white-space: normal;
        text-align: left;
    }

    [data-testid="stChatMessage"] {
        border-radius: 14px;
        padding: 12px 16px;
    }
</style>
""", unsafe_allow_html=True)


# -------------------- Header --------------------

st.title("💻 NovaRetail IT Support")

st.markdown(
    '<div class="subtitle">'
    'Your company IT helpdesk · Simple, reliable support'
    '</div>',
    unsafe_allow_html=True,
)


# -------------------- Session State --------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

if "selected_topic" not in st.session_state:
    st.session_state.selected_topic = None


# -------------------- Topic and Question Data --------------------

topics = {
    "🌐 Network": [
        "How do I troubleshoot my VPN connection?",
        "What should I do if my VPN keeps disconnecting?",
    ],
    "🔐 Account & Security": [
        "What should I do if I cannot approve my multi-factor authentication request?",
        "What should I do if I receive an unexpected MFA request?",
    ],
    "💻 Laptop & Devices": [
        "My company laptop is running slowly. What should I do?",
        "What should I do if my laptop overheats?",
    ],
    "📦 Software": [
        "What is NovaRetail's software installation policy?",
    ],
    "☎️ IT Helpdesk": [
        "How can I contact the NovaRetail IT Service Desk?",
    ],
}


# -------------------- Topic Selection --------------------

if not st.session_state.messages:
    st.subheader("How can we help?")
    st.caption("Choose a topic to explore common questions.")

    columns = st.columns(2)

    for index, topic in enumerate(topics):
        with columns[index % 2]:
            if st.button(
                topic,
                key=f"topic_{index}",
                use_container_width=True,
            ):
                st.session_state.selected_topic = topic
                st.rerun()

    # Display questions only after a topic is selected
    selected_topic = st.session_state.selected_topic

    if selected_topic:
        st.divider()

        col1, col2 = st.columns([4, 1])

        with col1:
            st.subheader(selected_topic)

        with col2:
            if st.button("← Back", key="back_to_topics"):
                st.session_state.selected_topic = None
                st.rerun()

        st.caption("Choose a question:")

        for index, question in enumerate(topics[selected_topic]):
            if st.button(
                question,
                key=f"question_{index}",
                use_container_width=True,
            ):
                st.session_state.pending_question = question
                st.rerun()


# -------------------- Conversation History --------------------

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# -------------------- Chat Input --------------------

typed_question = st.chat_input("Describe your IT issue...")

# A selected suggestion takes priority over typed input
if st.session_state.pending_question:
    question = st.session_state.pending_question
    st.session_state.pending_question = None
else:
    question = typed_question


# -------------------- Send Question to FastAPI --------------------

if question:
    # Show the user's question
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    # Get the answer
    with st.chat_message("assistant"):
        with st.spinner("Checking company documents..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"question": question},
                    timeout=180,
                )

                response.raise_for_status()
                answer = response.json()["answer"]

            except requests.Timeout:
                answer = (
                    "The request took too long. Please try again."
                )

            except requests.ConnectionError:
                answer = (
                    "I couldn't connect to the IT support service. "
                    "Please check that FastAPI is running."
                )

            except requests.RequestException as error:
                answer = (
                    "Something went wrong while processing your question. "
                    f"Please try again. Details: {error}"
                )

        st.markdown(answer)

    # Save the answer in chat history
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
