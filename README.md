# Talent Scout Hiring Assistant Chatbot  

An intelligent **Hiring Assistant Chatbot** for *Talent Scout*, a fictional recruitment agency specializing in technology placements.  
The chatbot helps with the **initial screening of candidates** by gathering essential information and asking relevant technical questions based on the candidate’s declared **tech stack**.  

--- 

## 🚀 Features  

- **Interactive UI**: Built with **Streamlit** for clean and user-friendly interaction.  
- **Greeting & Overview**: Welcomes candidates and explains its purpose.  
- **Information Gathering**: Collects essential candidate details:  
  - Full Name  
  - Email Address  
  - Phone Number  
  - Years of Experience  
  - Desired Position(s)  
  - Current Location  
  - Tech Stack (programming languages, frameworks, databases, tools)  
- **Tech Stack Declaration**: Candidates declare their skills.  
- **Technical Question Generation**:  
  - Generates **3–5 tailored technical questions** based on the tech stack.  
  - Example: If a candidate lists *Python* and *Django*, the chatbot asks Python & Django-related questions.  
- **Context Handling**: Maintains conversation flow and remembers candidate inputs.  
- **Fallback Mechanism**: Provides meaningful responses for unexpected inputs.  
- **End Conversation**: Gracefully concludes with a thank-you message and next steps.  

---

## 🛠️ Tech Stack  

- **Programming Language**: Python  
- **Frontend**: [Streamlit](https://streamlit.io/)  
- **LLMs**: OpenAI GPT, Hugging Face Transformers (can use GPT-3.5, GPT-4, or LLaMA-based models)  
- **Other Libraries**:  
  - `transformers`, `sentence-transformers`  
  - `torch`, `huggingface-hub`  
  - `pydantic`, `python-dotenv`  
  - `unstructured`, `tiktoken`, `pypdf`  
  - `openai`, `langchain`  
  - `pandas`, `numpy`  

---

## 📂 Project Structure  

