# **Digital Skeptic AI**

I have developed a simple and user-friendly frontend where you can paste any URL into a box and instantly receive a complete report of the article, including all the key requirements.

The code is designed to be modular and reusable. The information crawling logic is implemented in a separate function, making it easy to reuse as a standalone tool just have to to add agent.tool on it and change in prompt. This means we can either:

1.Directly extract the required data when a URL is provided, or

2.Integrate it as a tool within an agent framework, allowing the agent to fetch and process the response on demand.

This separation of concerns makes the system flexible, maintainable, and easy to extend for future use cases.

## **Installation and Setup**

=> Keep the python version <=3.12

=> Install all files from requirements.txt

=> Add open Api key like given in .env .example

## **Running files**

=>to run frontend you can use this command 

        streamlit run app.py

=>to run backend you can run this command
        
        uvicorn main:app --reload
