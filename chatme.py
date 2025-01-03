import streamlit as st
import requests
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI

def run():
    # Name and Descriptions for the App
    st.title("AI-Bot: Workout Recommender 🤖")
    st.write(
        """
        Your intelligent fitness companion for personalized workout plans and weekly gym schedules. 
        Just type your fitness goals, level, or specific preferences, and let the AI handle the rest.
        """
    )
    st.markdown("---")
    
    try:
        llm = ChatOpenAI(model="gpt-4o-mini",
                         openai_api_key=st.secrets["openai"]["OPENAI_API_KEY"],
                         temperature=0.7)
    except Exception as e:
        st.error(f"Error initializing the AI model: {e}")
        st.stop()


    # Fetches a list of exercises from a local API, extracting the JSON data under the key exercises
    try:
        api_url = "http://127.0.0.1:5000/list_all"  # API endpoint for exercises list
        response = requests.get(api_url)
    
        if response.status_code == 200:
            data = response.json()  # Extracting the JSON data
            exercises = data['exercises']  # Extracting the exercise names
        else:
            st.error(f"Failed to retrieve data from API. Status code: {response.status_code}")
            st.stop()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data from the API: {e}")
        st.stop()


    # Defines an LLM prompt that can answer user's question.
    # The prompt can recommends workout plans and explains exercises based on a provided list of exercises.
    # The prompt can handles off-topic questions gracefully.

    prompt = """
    You are a highly intelligent AI assistant and a fitness expert. 
    Your job is to recommend weekly workout sessions tailored to the user's preferences and goals.

    Use the following list of exercise names:
    {exercises}

    Please provide clear, informative recommendations based on the user’s question: {question}

    When recommending workout sessions, provide only the names of the exercises, **no detailed information or instructions**. If the question asks for a list of workouts (such as a workout plan), return only the names of the exercises, with no further details.

    For a weekly or monthly workout plan:
    - Organize the plan by days of the week, from Day 1 to Day 7 (e.g., Day 1: Exercise 1, Exercise 2, ...; Day 2: Rest day).
    - Include rest days explicitly if applicable (e.g., "Day 3: Rest day").
    - Specify the number of repetitions for each workout.
    - You can provide a workout plan for up to one month. If the user requests a plan longer than one month, politely inform them that the service is limited to one month. However, you can suggest that for subsequent months, they can repeat the same plan while progressively increasing repetitions or weights for continued improvement.
    - If the user does not specify their fitness level or the focus of their workout (e.g., strength, cardio, etc.), ask them to clarify their preferences to ensure the workout plan is tailored to their needs.

    When the user asks for details on a specific exercise (e.g., "Can you give me the instructions for Squats?", or "How to squat?"):
    - Provide detailed step-by-step workout instructions for the requested exercise.
    - Make sure the instructions are clear and easy to follow, ensuring the user understands how to perform the exercise correctly and safely.
    
    If the user asks a question OUTSIDE the scope of exercises and workout plan or if the user asks something that seems like a math question (e.g., "3+3"), respond with: "Sorry, I can only assist with questions related to gym workouts and exercises."
    Or if the user asks about an exercise not listed in list of exercise, respond with: "Unfortunately, we don't provide information for this exercise."

    Respond in a friendly and motivational tone.
    """

    # Defines a prompt template with placeholders (question, exercises) for dynamic input in LLM responses.
    llm_prompt = PromptTemplate(template=prompt,
                                input_variables=["question", "exercises"])

    # Creates a persistent session state in Streamlit to store and retain conversation history.
    if "historical" not in st.session_state:
        st.session_state.historical = []

    # Combines the LLM and prompt template into a chain for managing interactions, with detailed logging enabled (verbose=True).
    llm_chain = LLMChain(llm=llm, prompt=llm_prompt, verbose=True)


    def to_pascal_case(text):
        """
        The function transforms a string into Pascal case with underscores between words
        Input: push up exercise"
        Output: "Push_Up_Exercise").
        """
        words = text.split()
        return '_'.join(word.capitalize() for word in words)
    
    def extract_exercise_name(response, exercises):
        """
        Returning the first matched exercise in Pascal case.
        If response var = push up and exercise var = PushUp
        Output: PushUp
        """
        response_pascal = to_pascal_case(response)
        for exercise in exercises:
            exercise_pascal = to_pascal_case(exercise)
            if exercise_pascal.lower() in response_pascal.lower():
                return exercise_pascal
        return None

    def should_display_images(question):
        """
        Returns True if the question contains "caranya", "how to", or "cara", indicating images should be displayed.
        Otherwise, returns False.
        """
        keywords = ["caranya", "how to", "cara"]
        return any(keyword in question.lower() for keyword in keywords)
    

    def display_images(exercise_name):
        """
        Displays two images for a given exercise with captions indicating the step (e.g., "Step 1" and "Step 2").
        """
        try:
            for i in range(2):
                img_url = f"http://127.0.0.1:5000/exercises/{exercise_name}/images/{i}.jpg"
                exercise_name_img = exercise_name.lower()
                exercise_name_img = exercise_name.replace("_", " ")
                st.image(img_url, caption=f"Step {i+1} - {exercise_name_img} ", use_column_width=True)
        except Exception as e:
            st.error(f"Error loading images for {exercise_name}: {e}")


    # Checks if openai_model exists in session state; if not, initializes it to "gpt-4o-mini" to preserve the setting across reruns.
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4o-mini"
    
    # Checks if historical exists in session state; if not, initializes it as an empty list.
    if "historical" not in st.session_state:
        st.session_state.historical = []

    # Loops through st.session_state.historical and displays each message using st.chat_message() and st.markdown() on app reruns.
    for message in st.session_state.historical:
        with st.chat_message(message["role"]):
            st.markdown(message["message"])



    # Displays a chat input box and ask the user to submit a fitness-related question, which it will be stored in prompt var.
    if question := st.chat_input("Enter your fitness-related question here"):
        try:
            # Retrieves conversation history from st.session_state.historical, then combines it with the user's latest question.
            conversation_context = "\n".join([f"{entry['message']}" for entry in st.session_state.historical])
            full_question = f"{conversation_context}\nUser: {question}\nAI:"
            
            # Passes the full question and exercises list to the LLM chain to generate a response, which is stored in response.
            response = llm_chain.run({
                "question": full_question,
                "exercises": ", ".join(exercises)
            })
            
            # Appends the user's question to st.session_state.historical with the role "user".
            st.session_state.historical.append({"role": "user", "message": question})
            
            # Displays the user's message in the chat
            with st.chat_message("user"):
                st.markdown(question)
            
            # Displays the assistant's message in the chat
            with st.chat_message("assistant"):
                st.markdown(response)
                
                # Extracts the exercise name from the assistant's response.
                exercise_name = extract_exercise_name(response, exercises)

                # If an exercise name is found and the question asks for images, it converts the name to Pascal case and displays the images.
                if exercise_name and should_display_images(question):
                    exercise_name_pascal = to_pascal_case(exercise_name)
                    display_images(exercise_name_pascal)

            # Adds the assistant's response to the conversation history for app persistence.
            st.session_state.historical.append({"role": "assistant", "message": response})  

        except Exception as e:
            st.error(f"Error occurred: {e}")

# Run the app
if __name__ == "__main__":
    run()