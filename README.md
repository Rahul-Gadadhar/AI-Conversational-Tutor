Data Science AI Tutor  
An interactive, AI-powered Data Science Tutor built with Streamlit, LangChain, and Google Generative AI. This tool provides personalized tutoring on data science topics—such as statistics, machine learning, data analysis, and programming—with real-time conversation and code examples.  
  
Features  
Conversational Interface: Chat with an AI tutor in a sleek Streamlit web app.  
Session Management: Start, switch, or clear conversations with unique session IDs.  
Memory & Context: Uses LangChain’s ConversationBufferMemory to keep track of dialogue context.  
Automated Titles: Generates descriptive conversation titles using a generative AI model.  
Focused Expertise: Delivers explanations and examples solely on data science topics.  
Installation     
Clone the repository:  
bash  
git clone https://github.com/your-username/data-science-ai-tutor.git  
cd data-science-ai-tutor  
Install dependencies:  
bash  
Copy  
Edit  
pip install streamlit langchain python-dotenv  
# Also ensure you have the ChatGoogleGenerativeAI package if not already installed  
Configure your environment:  
Create a .env file in the root directory.  
Add your Google API key:  
ini  
Copy  
Edit  
GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY  
Usage  
Run the application using Streamlit:  
  
bash  
Copy  
Edit  
streamlit run Data_Science_tutor.py  
Then, open your browser to interact with your personal data science tutor!  
