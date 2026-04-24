
# Try this App here at: 
https://automaticjobpilot.streamlit.app/

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

## Deploy To ECS Fargate

This repo now includes a basic ECS Fargate deployment setup:

- `Dockerfile`
- `task-definition.json`
- `ecs-task-execution-trust-policy.json`
- `scripts/deploy-ecs.ps1`

### Prerequisites

1. Create or use an existing ECR repository.
2. Create an ECS cluster and Fargate service.
3. Create an ALB target group that forwards traffic to container port `8501`.
4. Store `OPENAI_API_KEY` in AWS Secrets Manager.
5. Create an execution role trusted by `ecs-tasks.amazonaws.com` and attach the standard `AmazonECSTaskExecutionRolePolicy`.
6. Grant the execution role permission to read the referenced secret.

### Important Runtime Settings

- Container port: `8501`
- Streamlit health endpoint: `/_stcore/health`
- Required secret: `OPENAI_API_KEY`
- Optional environment variable: `OPENAI_MODEL`

### Recommended ALB Health Check

- Path: `/_stcore/health`
- Port: `traffic-port`
- Matcher: `200`

### Deployment Flow

1. Update placeholders in `task-definition.json`:
   - `<AWS_ACCOUNT_ID>`
   - `<AWS_REGION>`
   - Secrets Manager ARN
   - Role ARNs
2. Build, push, register, and deploy:

   ```powershell
   .\scripts\deploy-ecs.ps1 `
     -AwsRegion us-east-1 `
     -AwsAccountId 123456789012 `
     -ClusterName my-ecs-cluster `
     -ServiceName job-application-copilot `
     -RepositoryName job-application-copilot `
     -ImageTag latest `
     -OpenAIModel gpt-5-mini
   ```

3. Wait for the ECS service deployment to finish and confirm the ALB target is healthy.

### Notes

- The app binds to `0.0.0.0:8501`, which is correct for containers and Fargate.
- The app will fail during startup if `OPENAI_API_KEY` is missing.
- The Docker image includes a container health check that uses Streamlit's health endpoint.

