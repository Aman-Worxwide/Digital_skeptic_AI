import streamlit as st
import requests
import json

st.set_page_config(page_title="URL Answer Fetcher", page_icon="🔗")

st.title("🔗 URL Answer Fetcher")

user_url = st.text_input("Paste the URL here:")

API_ENDPOINT = "http://localhost:8000/get-answer"  

if st.button("Get Answer"):
    if user_url.strip():
        try:
            with st.spinner("Fetching answer..."):
                response = requests.post(API_ENDPOINT, json={"url": user_url}, stream=True)
                response.raise_for_status()
                
                # Handle streaming response
                answer = ""
                for line in response.iter_lines():
                    if line:
                        try:
                            data = json.loads(line.decode('utf-8'))
                            if data.get("role") == "model" and "content" in data:
                                answer = data["content"]
                                break
                        except json.JSONDecodeError:
                            continue
                
                if answer:
                    st.success("Answer fetched successfully!")
                    st.write(answer)
                else:
                    st.error("No answer received from API.")

        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching data: {e}")
        except Exception as e:
            st.error(f"Error processing response: {e}")
    else:
        st.warning("Please paste a URL first.")