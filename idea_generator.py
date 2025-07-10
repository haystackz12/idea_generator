import streamlit as st
import openai
import os
# from dotenv import load_dotenv # REMOVE THIS LINE

# Load environment variables (your OpenAI API key)
# load_dotenv() # REMOVE THIS LINE

# Configure OpenAI API client
# Use st.secrets to access secrets stored in Streamlit Cloud
# It's good practice to get the API key from environment variables
# openai.api_key = os.getenv("OPENAI_API_KEY") # REMOVE OR COMMENT OUT THIS LINE
openai.api_key = st.secrets["OPENAI_API_KEY"] # ADD THIS LINE

# --- Streamlit App Configuration ---
st.set_page_config(
    page_title="💡 AI Idea Generator",
    page_icon="🧠",
    layout="centered"
)

st.title("💡 AI Idea Generator")
st.markdown("Enter a topic, and I'll brainstorm some creative ideas for you!")

# --- User Inputs ---
topic = st.text_input("Enter your topic (e.g., 'new app ideas', 'marketing strategies for a local cafe', 'ways to improve productivity')", "")

num_ideas = st.slider("How many ideas do you want?", min_value=1, max_value=10, value=5)

# --- Generate Ideas Button ---
if st.button("Generate Ideas"):
    if topic:
        with st.spinner("Generating ideas..."):
            try:
                # Construct the prompt for the OpenAI API
                prompt = f"Brainstorm {num_ideas} unique and creative ideas for: {topic}. Present them as a numbered list."

                # Call the OpenAI API
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",  # You can try "gpt-4" if you have access and want potentially better results
                    messages=[
                        {"role": "system", "content": "You are a creative brainstorming assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500,  # Max length of the generated response
                    temperature=0.8  # Higher temperature means more creative/random output
                )

                # Extract and display the generated ideas
                generated_text = response.choices[0].message.content
                st.subheader("Here are your ideas:")
                st.write(generated_text)

            except openai.APIError as e:
                st.error(f"OpenAI API Error: {e}")
                st.info("Please check your API key and network connection.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
                st.info("Please try again or check your input.")
    else:
        st.warning("Please enter a topic to generate ideas.")

st.markdown("---")
st.caption("Powered by OpenAI and Streamlit")