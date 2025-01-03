# **DL Large Language Model**
# **AI-Bot Workout Recommender**

Promoting a healthier lifestyle with personalized workout recommendations, smart scheduling, and fitness guidance.

---

## **Background**

Maintaining a healthy lifestyle in Indonesia comes with several obstacles:

1. **Insufficient Physical Activity**: Many individuals lead sedentary lives and lack consistent exercise habits.
2. **Financial Barriers**: Gym memberships are often out of reach for a significant portion of the population due to high costs.
3. **Rising Preventable Diseases**: Chronic conditions like diabetes, obesity, and heart disease are becoming more common but can be reduced through regular exercise.

Additionally, ChatGPT's free model, while highly capable of generating text-based responses, has several limitations:
1. **Inability to Provide Images**: Visual workout exercise demonstrations can not be made, which limits its usefulness for tasks requiring visual guidance.
2. **Inconsistencies**: Occasional inaccuracies, repetition, or a lack of depth when addressing complex or niche topics.

**AI-Bot** empowers users to achieve fitness goals with workout advice, personalized plans, and fitness-related answers.

   
---

## **How to Use**

### **Step-by-Step Usage**
1. **Access the Website**: Open the AI-Bot homepage to begin.
2. **Enter Your Query**: Input your workout-related question or request in the chat box.
3. **Send**: Press the "Submit" button to engage with the chatbot.
4. **Receive Suggestions**: Get tailored workout plans, schedules, or answers based on your input.

---

## **Sample Questions**

1. Please make a workout schedule three times a week for one month focusing on the upper body.
2. How can I do a Pull-Up?


---



## **Technical Overview**

### **Development Process**  
1. The app uses an AI model **GPT-4o Mini** with **Streamlit** and **LangChain** to process the user's query.
2. The app generates responses based on a list of exercises fetched from a **local API**.
3. The app stores and displays user queries and AI responses in a **chat-like interface**.
4. The app displays **images** for exercises when requested.
5. The app maintains a **conversation history** to provide contextual responses
6. The app ensures that **off-topic** questions are handled gracefully.

### **Libraries Used**  
- Python  
- Streamlit  
- Pandas  
- Plotly  
- Hugging Face Transformers  

---

## **Limitation**  

**Slow Response**: The app takes approximately 8 seconds to generate a response, which may feel a bit slow for users seeking quicker interactions.

---

## **Authors**: Fauzan Azhima, Muhammad Nuzul, Karmenia Lontoh, and Satrio Tri Nugroho
