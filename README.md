# Job Application Copilot

An AI-powered tool to help with job applications by generating tailored resume bullets and cover letters.

## Features

- AI agents for planning, writing, and verifying job application materials
- Streamlit web interface
- LangGraph workflow orchestration

## Project Structure

```
.
├── src/                    # Core application code
│   ├── __init__.py
│   ├── config.py          # Configuration settings
│   ├── llm_client.py      # LLM client setup
│   ├── schemas.py         # Data schemas
│   ├── state.py           # Application state
│   └── workflow.py        # LangGraph workflow
├── agents/                 # AI agent implementations
│   ├── __init__.py
│   ├── cover_letter_agent.py
│   ├── planner.py
│   ├── verifier.py
│   └── writer.py
├── data/                   # Data files
│   ├── cover_letter.txt
│   └── tailored_bullets.txt
├── tests/                  # Test files
│   └── test.py
├── .streamlit/             # Streamlit configuration
│   └── config.toml
├── app.py                  # Streamlit application
├── main.py                 # CLI entry point
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
└── README.md
```

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables in `.env`:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

### Web Interface (Streamlit)

Run the Streamlit app:
```bash
streamlit run app.py
```

### Command Line

Run the CLI version:
```bash
python main.py
```

## Deployment

### Streamlit Cloud (Recommended)

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub account
3. Select the `job-application-copilot` repository
4. Set the main file path to `app.py`
5. Add secrets in the "Advanced settings" section:
   ```
   OPENAI_API_KEY = "your_openai_api_key_here"
   OPENAI_MODEL = "gpt-4"  # or your preferred model
   ```
6. Click "Deploy"

### Heroku

1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create your-app-name`
4. Set environment variables:
   ```bash
   heroku config:set OPENAI_API_KEY=your_key_here
   heroku config:set OPENAI_MODEL=gpt-4
   ```
5. Deploy:
   ```bash
   git push heroku master
   ```

### Railway

1. Go to [railway.app](https://railway.app)
2. Connect GitHub repository
3. Add environment variables in the Variables section
4. Deploy automatically

### Docker Deployment

For platforms supporting Docker (AWS, GCP, DigitalOcean, etc.):

```bash
docker build -t job-app-copilot .
docker run -p 8501:8501 -e OPENAI_API_KEY=your_key job-app-copilot
```

## Environment Variables

Required environment variables:
- `OPENAI_API_KEY`: Your OpenAI API key
- `OPENAI_MODEL`: Model to use (default: gpt-4-mini)

## Configuration

- `.streamlit/config.toml`: Streamlit configuration
- `config.py`: Application configuration
- `.env`: Environment variables