# Scholar Quest: Personalized Scholarship Recommendation Chatbot

Scholar Quest is an AI-driven platform designed to streamline the process of finding scholarships for students. By analyzing individual profiles—including income, state, and other factors—it offers personalized scholarship recommendations and real-time assistance through an AI-powered chatbot.


![Screenshot 2024-12-18 144256](https://github.com/user-attachments/assets/a7bbac7e-c7dc-4258-8226-1a1539d91471)

## Problem Statement

- **Fragmented Information**: Government scholarships and policies are often dispersed across various platforms, making it challenging for students to find relevant information.
- **Unclear Eligibility Criteria**: Complex or ambiguous eligibility requirements leave students uncertain about their qualifications.
- **Lack of Personalized Guidance**: The absence of tailored assistance leads to missed opportunities for deserving students.
- **Overwhelming Process**: Navigating and applying for scholarships can be daunting without adequate support.

## Solution

Scholar Quest leverages Gemini AI to bridge the gap between students and scholarship opportunities. By collecting basic information—such as name, income, gender, and state—it provides personalized recommendations. The AI-powered chatbot offers real-time guidance on eligibility, requirements, and application processes, ensuring students can easily access and benefit from available opportunities.


![Screenshot 2024-12-18 165434](https://github.com/user-attachments/assets/a1efce59-8b1e-47b9-90d3-5ffa88bc48e5)


## Design and Architecture

1. **Frontend**:
   - Developed using HTML, CSS (with TailwindCSS), and JavaScript for a responsive and user-friendly interface.
   - Captures essential student details through intuitive forms.

2. **Backend**:
   - Built with Flask to handle routing and API integration.
   - Processes student information and matches them with relevant scholarships from a pre-loaded dataset.
   - Integrates Gemini 2.0 Flash for conversational responses.

3. **Database**:
   - Utilizes a CSV file (`scholarship_dataset_combined.csv`) containing scholarship details.
   - Filters scholarships based on education level, category, income, and other parameters to match user profiles.
   - Manages data securely in Google Cloud for reliability and scalability.

4. **AI Chatbot**:
   - Powered by Gemini 2.0 Flash, providing instant, human-like responses.
   - Supports markdown formatting for structured replies.

5. **Styling**:
   - Incorporates CSS animations (e.g., typing indicators, message fades) to enhance user experience.
   - Ensures mobile responsiveness for usability across devices.

![FINAL_SUBMISSION drawio (1)](https://github.com/user-attachments/assets/f66f9c99-c8c5-4f0e-90c0-f72192cbff66)

## Prerequisites

1. **Software Requirements**:
   - Python 3.9 or later.
   - Flask and necessary Python libraries (e.g., pandas, markdown2) installed via pip.
   - A modern web browser (e.g., Chrome, Firefox).

2. **Basic Knowledge**:
   - Familiarity with running Python scripts and Flask applications.
   - Basic understanding of HTML and CSS for potential customization.
   - Knowledge of using API keys for Gemini 2.0 Flash integration.

3. **Additional Setup**:
   - Google Cloud account configured for secure database storage.
   - Access to the `scholarship_dataset_combined.csv` file for initial data loading.
         https://www.kaggle.com/datasets/naveenpradhaph/india-scholarship-data?source=post_page-----2284686be19c--------------------------------
   - A `.env` file to securely store sensitive configurations like API keys.

## Setup and Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/scholar-quest.git
   cd scholar-quest
2. **Create a virtual environment**
   python -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   
3. **Install dependencies**
   pip install -r requirements.txt

4. Configure environment variables:

    ->Create a .env file in the root directory.
    ->Add your Gemini 2.0 API key and other necessary configurations.
   
6. Load the scholarship dataset:

    ->Ensure the scholarship_dataset_combined.csv file is in the project directory.
   
7. Run the application
      flask run
   
8.Access the chatbot:

     Open http://localhost:5000 in your browser.

![Screenshot 2024-12-18 170120](https://github.com/user-attachments/assets/7b5beb4d-2b34-459b-a703-a833e4dc7c08)



## Work Flow

1. Enter Your Details
The user begins by filling out a form with their details, such as name, income, gender, and state.

![Screenshot 2024-12-18 164136](https://github.com/user-attachments/assets/7c1bb426-8805-49a2-9dda-d8957becfe5c)



2. Submit Information
Once the details are filled out, the user submits the form to store their information securely in the system.

![Screenshot 2024-12-18 164315](https://github.com/user-attachments/assets/001d0a91-032b-4185-b392-a769315024e6)



4. Ask a Query to Scholar Quest Bot
After submitting the details, the user can interact with the Scholar Quest Bot, asking questions related to scholarships, schemes, or opportunities based on their provided information.

![Screenshot 2024-12-18 164506](https://github.com/user-attachments/assets/8ccc069c-5496-4283-b6ef-858bb0457b22)




6. Receive Necessary Information
The Scholar Quest Bot processes the query and provides the user with personalized results, including the eligibility, requirements, and application details of the relevant scholarships or government agricultural schemes.

![Screenshot 2024-12-18 164626](https://github.com/user-attachments/assets/269c31d2-507c-4ffb-9fa3-105b2a5d5d07)




## Future Scope

1. Expansion to Support Marginalized Communities: The platform can be extended to include information on government policies and schemes for tribal populations, Scheduled Castes (SC), Scheduled Tribes (ST), disabled individuals, and senior citizens.
2. Assisting Underprivileged Communities: By providing personalized and relevant details, the platform can help uplift underprivileged communities and ensure they have access to beneficial opportunities.
3. Multi-Language Support: The system can be enhanced to offer language options according to the user’s preference, overcoming language barriers and making the platform accessible to a broader audience.
