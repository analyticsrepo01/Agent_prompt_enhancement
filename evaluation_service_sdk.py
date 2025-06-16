%pip install --upgrade --user --quiet google-cloud-aiplatform[evaluation]

import IPython

app = IPython.Application.instance()
app.kernel.do_shutdown(True)

import sys

if "google.colab" in sys.modules:
    from google.colab import auth

    auth.authenticate_user()

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

LOCATION = "us-central1"  # @param {type:"string"}
EXPERIMENT_NAME = "my-eval-task-experiment"  # @param {type:"string"}

if not PROJECT_ID or PROJECT_ID == "[your-project-id]":
    raise ValueError("Please set your PROJECT_ID")


import vertexai

vertexai.init(project=PROJECT_ID, location=LOCATION)

import pandas as pd
from vertexai.evaluation import EvalTask, PointwiseMetric, PointwiseMetricPromptTemplate
from vertexai.preview.evaluation import notebook_utils

# Your own definition of text_quality.
text_quality = PointwiseMetric(
    metric="text_quality",
    metric_prompt_template=PointwiseMetricPromptTemplate(
        criteria={
            "fluency": "Sentences flow smoothly and are easy to read, avoiding awkward phrasing or run-on sentences. Ideas and sentences connect logically, using transitions effectively where needed.",
            "entertaining": "Short, amusing text that incorporates emojis, exclamations and questions to convey quick and spontaneous communication and diversion.",
        },
        rating_rubric={
            "1": "The response performs well on both criteria.",
            "0": "The response is somewhat aligned with both criteria",
            "-1": "The response falls short on both criteria",
        },
    ),
)

print(text_quality.metric_prompt_template)

responses = [
    # An example of good text_quality
    "Life is a rollercoaster, full of ups and downs, but it's the thrill that keeps us coming back for more!",
    # An example of medium text_quality
    "The weather is nice today, not too hot, not too cold.",
    # An example of poor text_quality
    "The weather is, you know, whatever.",
]

eval_dataset = pd.DataFrame(
    {
        "response": responses,
    }
)

eval_result = EvalTask(
    dataset=eval_dataset, metrics=[text_quality], experiment=EXPERIMENT_NAME
).evaluate()

notebook_utils.display_eval_result(eval_result)

from google.cloud import aiplatform

aiplatform.ExperimentRun(
    run_name=eval_result.metadata["experiment_run"],
    experiment=eval_result.metadata["experiment"],
).delete()