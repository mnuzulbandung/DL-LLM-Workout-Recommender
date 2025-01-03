## **Deploys the App Locally**

1. Download all the files.
2. Prepare a folder (e.g., Project_LLM_01) that contains the app.py, api.py, or chatme.py file.
3. To authenticate and authorize access to the OpenAI model's services, an API-Key is needed.
    -   Login and deposit funds into the OpenAI platform [page](https://platform.openai.com/settings/organization/billing/overview). This project will use the GPT-4o Mini model with specifications and prices available on this [page](https://openai.com/api/pricing/). Payment is based on how many times the model is used.
    -   On this [page](https://platform.openai.com/settings/organization/projects), create a new project.
    -   On this [page](https://platform.openai.com/settings/organization/api-keys), create an API key based on the previous project. Do not share your API key with others or expose it in the browser or other client-side code.
4. To ensure the API-key is not used by unauthorized individuals, secrets.toml is needed.
    - Add the following script, input the API-Key, and save it as secrets.toml.
        ```toml
        [openai]  
        OPENAI_API_KEY = "your_openai_api_key_here"
        ```
    - Create a new folder within Project_LLM_01 named .streamlit.
    - Place the secrets.toml file inside the .streamlit folder.
5. Run the api.py file by opening the command prompt; go to the Project_LLM_01 folder; execute the following script:
    ```cd
    python api.py
    ```
6. Run the app.py file by opening a NEW command prompt; go to the Project_LLM_01 folder; execute the following script:
    ```cd
    streamlit run app.py
    ```

