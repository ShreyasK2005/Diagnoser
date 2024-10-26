import requests
import spacy
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
import openai
from flask_cors import CORS

# Function to scrape common symptoms from a webpage
def scrape_symptoms(url):
    # Send a GET request to the webpage
    page = requests.get(url)

    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(page.content, "html.parser")

    # Assuming symptoms are in <ul> tags or similar
    symptoms_section = soup.find("section", {"h2": "Symptoms"})  # Adjust this based on the page structure
    if not symptoms_section:
        symptoms_section = soup  # If no section ID, search the whole page

    # Get all list items <li> under this section (assuming symptoms are in a list)
    symptoms = symptoms_section.find_all("li")

    # Extract and return the symptoms as text
    symptoms_text = [symptom.get_text() for symptom in symptoms]
    return symptoms_text

# Example: Cleveland Clinic's webpage about multiple myeloma
url = "https://www.mayoclinic.org/diseases-conditions/multiple-myeloma/symptoms-causes/syc-20353378"
symptoms = scrape_symptoms(url)



app = Flask(__name__)
CORS(app)

# API Key
openai.api_key = "sk-vFN-A5Ksx-REH-qun8aEt-cljY6H0sWHVEOuHzCsv3T3BlbkFJ0Dc_QWbAIRT3n0klEuDcnJmoa0_FsnfIobhGjdw14A"


def interact_with_chatbot():
    print("Welcome to the Multiple Myeloma Chatbot! Type 'exit' to end the chat.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Ending chat. Goodbye!")
            break

        try:
            # Updated method to create a chat completion
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                     "content": f"Provides any specifications the user has related to Multiple Myeloma, can also use information gathered on symptoms to ask a survey (if user says yes to 3 or more symtpoms then refer them to a doctor), aks questions one by one and then depending on whether the user says yes or no ask a logical follow up question about similair symptoms"
                                f"The information is related to Multiple Myeloma {symptoms}"},
                    {"role": "user", "content": user_input}
                ]
            )

            response_content = completion.choices[0].message['content']  # Access the message content
            print(f"ChatGPT: {response_content}")  # Print response to terminal
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    interact_with_chatbot()  # Start the interactive chatbot session