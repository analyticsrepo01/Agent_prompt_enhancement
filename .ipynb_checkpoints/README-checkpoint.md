# LangGraph Prompt Optimization System

A sophisticated 4-agent system built with LangGraph that automatically optimizes prompts through iterative testing and enhancement.

## Overview

This system uses a multi-agent workflow to systematically improve prompts by:
1. Generating challenging test datasets
2. Executing prompts against test cases
3. Evaluating performance using Vertex AI
4. Providing enhancement recommendations and validation

## Architecture

The system consists of 4 specialized agents:

### Agent 1: Dataset Generator
- Creates diverse test cases for prompt evaluation
- Generates challenging scenarios to prevent overfitting
- Adapts dataset difficulty based on initial performance
- Saves datasets with metadata for reproducibility

### Agent 2: Prompt Executor
- Executes current prompt against all test cases
- Collects actual outputs for evaluation
- Handles errors gracefully during execution

### Agent 3: Evaluation Analyzer
- Uses Vertex AI evaluation metrics for quality assessment
- Calculates success rates and performance metrics
- Generates specific enhancement recommendations
- Tracks iteration history for comparison

### Agent 4: Enhancement Validator
- Validates enhancement recommendations
- Creates improved prompt versions
- Determines when to continue or finalize optimization
- Selects best performing prompt from history

## Features

- **Iterative Optimization**: Runs multiple iterations (minimum 3, maximum 5) to find optimal prompt
- **Intelligent Dataset Generation**: Creates challenging test cases that expose prompt weaknesses
- **Comprehensive Evaluation**: Uses both automated metrics and LLM-based analysis
- **Performance Tracking**: Maintains detailed history of all iterations
- **Automatic Finalization**: Intelligently selects best prompt based on performance
- **Result Persistence**: Saves datasets and results for analysis

## Usage

1. **Setup Dependencies**:
```bash
pip install langgraph langchain-google-vertexai google-cloud-aiplatform[evaluation] pandas
```

2. **Configure Google Cloud**:
```python
PROJECT_ID = "your-project-id"
LOCATION = "us-central1"
```

3. **Run Optimization**:
```python
# Initialize state with your prompt
initial_state = {
    "original_prompt": "Your prompt here",
    "current_prompt": "Your prompt here",
    "iteration": 1,
    "max_iterations": 5
}

# Execute workflow
final_state = app.invoke(initial_state)
```

## Example Use Cases

- **Medical Claim Processing**: Optimizing prompts for healthcare decision-making
- **E-commerce Product Descriptions**: Enhancing marketing copy generation
- **Customer Service**: Improving automated response quality
- **Content Moderation**: Refining classification accuracy

## Output Files

- `datasets/test_dataset_*.json`: Generated test datasets with metadata
- `readme_prompt.md`: Comprehensive optimization results and final prompt

## Performance Metrics

The system tracks:
- Success rate across test cases
- Iteration-by-iteration improvement
- Best performing prompt identification
- Detailed evaluation summaries

## Technical Details

- **Framework**: LangGraph for agent orchestration
- **LLM**: Google Vertex AI (Gemini 2.0 Flash)
- **Evaluation**: Vertex AI evaluation metrics
- **Storage**: JSON files for datasets and results
