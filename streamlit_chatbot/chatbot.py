import streamlit as st
import pandas as pd

# Initialize session state
def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def main():

    # Title
    st.title("My First Streamlit App")
    st.header("Welcome to the dashboard")
    st.write("This is a simple demonstration of Streamlit capabilities")

    # Chatbot title
    st.title("Simple Chatbot")

    initialize_session_state()

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    if prompt := st.chat_input("What's on your mind?"):

        # User message
        with st.chat_message("user"):
            st.write(prompt)

        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        # Bot response
        response = f"You said: {prompt}"

        with st.chat_message("assistant"):
            st.write(response)

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

    # Sample DataFrame
    df = pd.DataFrame({
        'Month': ['January', 'February', 'March', 'January'],
        'Price': [1000, 1500, 2000, 1200]
    })

    # Sidebar
    st.sidebar.header("Filters")

    # Dropdown
    selected_month = st.sidebar.selectbox(
        "Select Month",
        options=df['Month'].unique()
    )

    # Slider
    price_range = st.sidebar.slider(
        "Select Price Range",
        min_value=0,
        max_value=3000,
        value=(0, 3000)
    )

    # Filtered Data
    filtered_df = df[
        (df['Month'] == selected_month) &
        (df['Price'] >= price_range[0]) &
        (df['Price'] <= price_range[1])
    ]

    st.write("Filtered Data")
    st.dataframe(filtered_df)

if __name__ == "__main__":
    main()

