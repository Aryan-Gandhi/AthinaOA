## Project Overview
This project lets you upload a PDF file and interactively ask questions about its content using conversational AI. The application uses Streamlit for the front end, LangChain for text processing, and OpenAI for generating embeddings and responses.

## Prerequisites
Before running this project, ensure you have the following installed on your local machine:
- Python 3.9 
- Pip (Python package installer)

## Project Structure
- `app.py`: The main application script.
- `requirements.txt`: A file listing all the dependencies required to run the project.
- `.env`: A file to store environment variables such as API keys.
- `notebooks/`: A directory for Jupyter notebooks.
  - `evaluations.ipynb`: Code for evaluating the model on the test dataset.
  - `OpenAI_Athina.ipynb`: Notebook for getting the LLM outputs and the context by running the chatbot model on the test dataset.
  - `testset_generator.ipynb`: Code used to generate the test dataset.
- `datasets/`: A directory for dataset files.
  - `RAGA_results.csv`: Evaluation results after RAGA was used for evaluation on the test dataset.
  - `results.csv`: The entire dataset containing questions, ground truths, LLM outputs, and context.
  - `test_dataset.csv`: A robust, comprehensive dataset of query-answer pairs.
- `athina.pdf`: A sample PDF document to test the application.
- `experiments/`: The folder containing the tests done using Llama-2-chat and Mistral-7b.

## Setup Instructions

### 1. Clone the Repository
Clone the repository to your local machine using the following command:
```sh
git clone https://github.com/Aryan-Gandhi/AthinaOA.git
cd AthinaOA
```

### 2. Create a Virtual Environment
Create and activate a virtual environment to manage dependencies:
```sh
python -m venv venv
source venv/bin/activate 
```

### 3. Install Dependencies
Install the required dependencies using the following command:
```sh
pip install -r requirements.txt
```

### 4. Run the Application
Execute the Streamlit application using the following command:
```sh
streamlit run app.py --server.enableXsrfProtection false
```

This command will start a local server and provide you with a URL (typically `http://localhost:8501`) that you can open in your web browser to interact with the application.

### 5. If the webpage does not load, click enter and manually go to the URL shown

### 6. Please enter the API key sent in the email before uploading files

## Using the Application

### 1. Upload a PDF
- Open the provided URL in your web browser.
- Use the file uploader widget to upload a PDF file (e.g., `athina.pdf`).

### 2. Ask Questions
- After the PDF is uploaded and processed, type your question in the input box provided.
- Press Enter or click on the submit button to get an answer based on the content of the PDF.


## Troubleshooting
- Ensure all dependencies are installed correctly.
- Verify that your API key is correctly set in the `.env` file.
- Check for any error messages in the terminal where you run the `streamlit run app.py --server.enableXsrfProtection false` command for debugging purposes.

## Contact
For any questions or issues, please reach out to aryangan@usc.edu.
