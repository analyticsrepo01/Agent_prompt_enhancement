import os
from IPython.display import JSON
import json

# Cloud project id.
PROJECT_IDS = !(gcloud config get-value core/project)
PROJECT_ID = PROJECT_IDS[0]  # @param {type:"string"}

if not PROJECT_ID:
    PROJECT_ID = str(os.environ.get("GOOGLE_CLOUD_PROJECT"))

LOCATION = "us-central1" # @param {type:"string"}

os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
os.environ["GOOGLE_CLOUD_LOCATION"] = LOCATION
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "TRUE" # Use Vertex AI API
# [your-project-id]

test_prompt = """HERE IS MY PROMPT"""

main_model = model = "gemini-2.0-flash-001"

from google import genai
from google.genai import types
import base64

def generate():
  client = genai.Client(
      vertexai=True,
      project=PROJECT_ID,
      location=LOCATION,
  )

  si_text1 = """You are adapted to serve as an intelligent medical companion. You are committed to upholding the highest standards of accuracy, reliability, and ethical considerations in healthcare.

Reply in the same language as the user request, unless instructed otherwise by the user.

Make sure to answer all parts of the user's instructions, unless they compromise safety.

For medical documentation, avoid including information that was not present in the source documents.

For diagnosis questions, try to provide relevant information but refrain from providing direct medical advice."""

  model = main_model
  contents = [
    types.Content(
      role="user",
      parts=[
        types.Part.from_text(text=test_prompt)
      ]
    )
  ]

  generate_content_config = types.GenerateContentConfig(
    temperature = 1,
    top_p = 0.95,
    max_output_tokens = 8192,
    safety_settings = [types.SafetySetting(
      category="HARM_CATEGORY_HATE_SPEECH",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_DANGEROUS_CONTENT",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_HARASSMENT",
      threshold="OFF"
    )],
    system_instruction=[types.Part.from_text(text=si_text1)],
  )

  for chunk in client.models.generate_content_stream(
    model = model,
    contents = contents,
    config = generate_content_config,
    ):
    print(chunk.text, end="")

generate()

main_medical_model = "medlm-large-1.5@001"

import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, SafetySetting, FinishReason


def generate():
    vertexai.init(
        project=PROJECT_ID,
        location="us-central1",
        api_endpoint="us-central1-aiplatform.googleapis.com"
    )
    model = GenerativeModel(
        main_medical_model,
        system_instruction=[si_text1]
    )
    responses = model.generate_content(
        [test_prompt],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )

    for response in responses:
        print(response.text, end="")

si_text1 = """You are a medical expert at Insurance firm, try to asnwer the questions medically."""

generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

safety_settings = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
]

generate()

# ### medgemma

# @title Import deployed model

# @markdown To get [online predictions](https://cloud.google.com/vertex-ai/docs/predictions/get-online-predictions), you will need a MedGemma [Vertex AI Endpoint](https://cloud.google.com/vertex-ai/docs/general/deployment) that has been deployed from Model Garden. If you have not already done so, go to the [MedGemma model card](https://console.cloud.google.com/vertex-ai/publishers/google/model-garden/medgemma) and click "Deploy options > Vertex AI" to deploy the model.

# @markdown **Note:** The examples in this notebook are intended to be used with instruction-tuned variants. Make sure to use an instruction-tuned model variant to run this notebook.

# @markdown This section gets the Vertex AI Endpoint resource that you deployed from Model Garden to use for online predictions.

# @markdown Fill in the endpoint ID and region below. You can find your deployed endpoint on the [Vertex AI online prediction page](https://console.cloud.google.com/vertex-ai/online-prediction/endpoints).

ENDPOINT_ID = "333033275960328192"  # @param {type: "string", placeholder:"e.g. 123456789"}
ENDPOINT_REGION = "asia-southeast1"  # @param {type: "string", placeholder:"e.g. us-central1"}

# @markdown Set `use_dedicated_endpoint` if you are using a [dedicated endpoint](https://cloud.google.com/vertex-ai/docs/predictions/choose-endpoint-type) (`True` by default for Model Garden deployments). Uncheck this option for all other endpoint types.

use_dedicated_endpoint = True  # @param {type: "boolean"}

# @markdown Set `is_thinking` to `True` to turn on thinking mode. **Note:** Thinking is supported for the 27B variant only.
is_thinking = True  # @param {type: "boolean"}

endpoints["endpoint"] = aiplatform.Endpoint(
    endpoint_name=ENDPOINT_ID,
    project=PROJECT_ID,
    location=ENDPOINT_REGION,
)

# Use the endpoint name to check that you are using an appropriate model variant.
# These checks are based on the default endpoint name from the Model Garden
# deployment settings.
ENDPOINT_NAME = endpoints["endpoint"].display_name
if "pt" in ENDPOINT_NAME:
    raise ValueError(
        "The examples in this notebook are intended to be used with "
        "instruction-tuned variants. Please use an instruction-tuned model."
    )

# @title #### Specify text prompt

system_instruction = "You are a helpful medical assistant."
prompt = "How do you differentiate bacterial from viral pneumonia?"  # @param {type:"string"}

# @title #### Generate responses from standard prompts

# @markdown This section shows how to send [prediction](https://cloud.google.com/vertex-ai/docs/predictions/get-online-predictions) requests to the endpoint with standard prompts using the Vertex AI SDK.

# @markdown Set `raw_response` to `True` to obtain only the model generated response. Set `raw_response` to `False` to apply additional formatting in the structure of `"Prompt:\n{prompt.strip()}\nOutput:\n{output}"`.
raw_response = True  # @param {type: "boolean"}

# @markdown Click "Show Code" to see more details.

formatted_prompt = f"{system_instruction} {prompt} <start_of_image>"

instances = [
    {
        "prompt": formatted_prompt,
        "max_tokens": 1000,
        "temperature": 0,
        "raw_response": raw_response,
    },
]

response = endpoints["endpoint"].predict(
    instances=instances, use_dedicated_endpoint=use_dedicated_endpoint
)
prediction = response.predictions[0]

display(Markdown(prediction))