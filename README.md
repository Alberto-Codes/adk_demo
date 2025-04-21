# adk_demo

This project demonstrates a basic agent built with the Agent Development Kit (ADK).

## Getting Started

This project is configured to run in a Dev Container, which provides a pre-configured development environment with all necessary tools installed.

### Prerequisites

1.  **Dev Container:** Open this project in a Dev Container (e.g., using GitHub Codespaces or VS Code with the Dev Containers extension). The necessary tools, including Python, `uv`, and the Google Cloud CLI, are installed automatically based on the configuration in `.devcontainer/devcontainer.json`.

2.  **Environment Variables:**
    *   Copy the `.env.sample` file to a new file named `.env`.
    *   Update the `.env` file with your Google Cloud project details:
        ```bash
        # .env
        GOOGLE_GENAI_USE_VERTEXAI=TRUE
        GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID
        GOOGLE_CLOUD_LOCATION=YOUR_REGION # e.g., us-west4
        ```
    *   Replace `YOUR_PROJECT_ID` with your actual Google Cloud project ID. You can find your Project ID in the [Google Cloud Console](https://console.cloud.google.com/) dashboard after logging in.
    *   Replace `YOUR_REGION` with the desired Google Cloud region. Choose a region geographically close to you for lower latency. You can find a list of available regions for Vertex AI Generative AI [here](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations#available-regions). For example, if you are in Arizona, `us-west4` (Las Vegas) might be a good choice.

3.  **Google Cloud Authentication:**
    *   You need to authenticate with Google Cloud to use Vertex AI. Run the following command in the Dev Container terminal and follow the prompts to log in:
        ```bash
        gcloud auth application-default login
        ```

### Running the Agent

Once the prerequisites are met, you can run the agent's web interface using the following command in the terminal:

```bash
uv run adk web src
```

This command will start a local web server. If you are using GitHub Codespaces, a port will be forwarded automatically, and you can access the agent's web UI in your browser.