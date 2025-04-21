import datetime
import os
import subprocess
from zoneinfo import ZoneInfo

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from adk_demo.sql_tools import fix_sql, lint_sql


# Function to get the access token from gcloud
def get_gcloud_token():
    """Retrieves the Google Cloud access token.

    This function attempts to retrieve the access token by running the
    `gcloud auth print-access-token` command. If the command succeeds,
    it returns the token as a string. If the command fails, it raises an
    exception with an appropriate error message.

    Raises:
        Exception: If the `gcloud` command fails or is not installed.
            Users must be authenticated via `gcloud auth application-default login`.

    Returns:
        str: The Google Cloud access token.
    """
    try:
        result = subprocess.run(
            ["gcloud", "auth", "print-access-token"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error getting gcloud token: {e}")
        print(f"Stderr: {e.stderr}")
        raise Exception(
            "Failed to get gcloud access token. "
            "Make sure you are authenticated via 'gcloud auth application-default login'."
        ) from e
    except FileNotFoundError:
        raise Exception(
            "'gcloud' command not found. Make sure the Google Cloud CLI is installed and in your PATH."
        )


def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: A dictionary containing either the weather report or an error message.
            Example:
                {
                    "status": "success",
                    "report": "The weather in New York is sunny with a temperature of 25 degrees Celsius."
                }
            Or:
                {
                    "status": "error",
                    "error_message": "Weather information for 'city' is not available."
                }
    """
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees"
                " Celsius (41 degrees Fahrenheit)."
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: A dictionary containing either the current time or an error message.
            Example:
                {
                    "status": "success",
                    "report": "The current time in New York is 2025-04-21 14:30:00 EDT-0400"
                }
            Or:
                {
                    "status": "error",
                    "error_message": "Sorry, I don't have timezone information for city."
                }
    """
    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": (f"Sorry, I don't have timezone information for {city}."),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = f"The current time in {city} is {now.strftime('%Y-%m-%d %H:%M:%S %Z%z')}"
    return {"status": "success", "report": report}


# --- Agent Configuration ---

# Retrieve configuration from environment variables
project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
location = os.getenv("GOOGLE_CLOUD_LOCATION")

if not project_id or not location:
    raise ValueError(
        "GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION environment variables must be set."
    )

# Construct the OpenAI-compatible endpoint URL
base_url = f"https://{location}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{location}/endpoints/openapi"

# Get the access token
api_key = get_gcloud_token()

# Define the agent using the OpenAI provider
root_agent = Agent(
    model=LiteLlm(
        model="openai/google/gemini-2.0-flash-lite-001",
        api_base=base_url,
        api_key=api_key,
    ),
    name="weather_time_agent",
    description=(
        "Agent to answer questions about the time and weather in a city, and lint or fix SQL code."  # Updated description
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about the time and weather in a city, and also lint or fix provided SQL code.  You can attempt rewriting SQL so it checks out in the sql tools you have.  You are an SQL Senior Analyst"  # Updated instruction
    ),
    tools=[
        get_weather,
        get_current_time,
        lint_sql,
        fix_sql,
    ],  # Use the imported functions
)
