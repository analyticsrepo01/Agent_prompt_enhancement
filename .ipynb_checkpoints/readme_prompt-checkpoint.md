# Final Optimized Prompt

## Original Prompt
## Context:
    Evaluate the relevance and necessity of all the provided medical care in relation to each item in the ICD and surgery descriptions list using your professional medical knowledge.
   
    ## Instruction:
    For each item in the ICD and surgery descriptions list, determine:
    If the medical care is necessary for diagnostic or examination purposes.
    If the medical care is effective for the disease.
    If the benefits of medical care outweigh any risks.
    If the medical care is a standard practice for the diagnosis.
    If the medical care is essential for the disease and not for cosmetic/lifestyle purposes.
    If the medical care indirectly treats the disease.
    Medical care that is follow-up visits, repeat visits, repeat consultation, total amount, GST information, subsidies or discounts all conclude as 'yes'. Especially for GST, their descriptions may come in forms such as 'GST - ADD GST', 'GST - LESS GST'; for any descriptions that resemble these, conclude as 'yes'.
    Considering the interactions between drugs, some drugs and treatments may not be designed for the patient's diagnoses and surgeries, but rather to counteract the side effects caused by other drugs. this scenario also needs to conclude as 'yes'
    Analyse the exclusion details and verify if the treatment is relevant to the provided exclusion. if the treatment is relevant to the exclusion, conclude as 'no'. 'explanation' should be provided as the treatment is relevant to the exclusion list.
    Conversely, consider the treatment medically unnecessary if it is ineffective, has safer alternatives, is discouraged by guidelines, or if risks outweigh benefits.
   
    ## Input: Given Medical Care: {treatments}.
    ## ICD and Surgery Description list: {icd_surgery_description}.
    ## Exclusion details: {exclusions}.
   
    ### Question: are all the given medical care at least a relevant testing or treatment for one of the items in the ICD and surgery descriptions list.
   
    ### Conclusion:
    1. Explain the given result as a doctor.
    2. Given different patient profiles and medical histories, provide a probability score without an explanation based on your analysis for the Yes/No binary output you provided to indicate the likelihood of this claim getting approved.
   
    ### Response: MUST Provide the output in json format with a key "conclusion" stating yes/no of the relevance, a key "probability score" providing a probability score (0-1 scale) to indicate the likelihood of this claim getting approved with 2 decimal places, and another key "explanation" stating the explanation as a doctor. Ensure that the conclusion is "yes" only if the probability score is at least 0.5. Ensure that the explanation is given in complete sentences without any truncations.
    

## Final Prompt
## Context:
Evaluate the relevance and necessity of provided medical care in relation to the given ICD and surgery descriptions and exclusion details, using your professional medical knowledge as a doctor specializing in internal medicine.

## Instructions:

For each item in the ICD and surgery descriptions list, determine:

1.  Is the medical care necessary for diagnostic or examination purposes?
2.  Is the medical care effective for the disease?
3.  Do the benefits of the medical care outweigh any risks?
4.  Is the medical care a standard practice for the diagnosis?
5.  Is the medical care essential for the disease and not for cosmetic/lifestyle purposes?
6.  Does the medical care indirectly treat the disease (e.g., by addressing side effects of other treatments)?

**Important Considerations:**

*   Medical care that includes follow-up visits, repeat visits, repeat consultations, total amounts, GST information (e.g., 'GST - ADD GST', 'GST - LESS GST'), subsidies, or discounts should ALWAYS be considered relevant ("yes").
*   Considering the interactions between drugs, some drugs and treatments may not be designed for the patient's diagnoses and surgeries, but rather to counteract the side effects caused by other drugs. This scenario also needs to conclude as 'yes'.
*   Analyze the exclusion details. If the treatment is relevant to an exclusion, conclude "no" and provide an explanation indicating the relevance to the exclusion.
*   Conversely, consider the treatment medically unnecessary if it is ineffective, has safer alternatives, is discouraged by guidelines, or if risks outweigh benefits.

**Handling Missing Data:**

*   **CRITICAL:** If any of the input data (treatments, ICD codes, exclusions) is missing or incomplete, you MUST state that you cannot provide a valid assessment and explain why. Do NOT make any assumptions.

## Input:
*   Given Medical Care: {treatments} (List of medical treatments provided to the patient)
*   ICD and Surgery Description list: {icd_surgery_description} (List of ICD codes and descriptions of surgical procedures performed)
*   Exclusion details: {exclusions} (Details of any exclusions related to the patient's insurance or medical policy)

## Question:
Are *all* the given medical care items at least a relevant testing or treatment for *one* of the items in the ICD and surgery descriptions list, considering the exclusion details? Remember, if even *one* item is irrelevant, the answer should be "no."

## Response:
MUST Provide the output in JSON format:

```json
{
  "conclusion": "yes/no",
  "probability score": 0.00,
  "explanation": "Explanation as a doctor specializing in internal medicine."
}
```

**Instructions for the JSON Output:**

*   **conclusion:** A string, either "yes" or "no", indicating the relevance. The conclusion MUST be "yes" only if the probability score is at least 0.5.
*   **probability score:** A number between 0.00 and 1.00 (inclusive), with 2 decimal places, indicating the likelihood of the claim getting approved. Base this on your analysis of the medical care, ICD codes, and exclusions. A high probability score (e.g., 0.8-1.0) should be assigned when the medical care is clearly indicated by the ICD codes and surgery descriptions, and there are no relevant exclusions. A low probability score (e.g., 0.0-0.2) should be assigned when the medical care is clearly unrelated or contradicted by the exclusions.
*   **explanation:** A clear and concise explanation, in complete sentences, as a doctor specializing in internal medicine, justifying your conclusion and probability score. Use appropriate medical terminology.

**Example:**

```
## Input:
*   Given Medical Care: {treatments: "Lisinopril 10mg daily"}
*   ICD and Surgery Description list: {icd_surgery_description: "I10 Essential (primary) hypertension"}
*   Exclusion details: {exclusions: "None"}

## Response:
```json
{
  "conclusion": "yes",
  "probability score": 0.95,
  "explanation": "Lisinopril is an ACE inhibitor commonly prescribed to treat essential hypertension (ICD-10: I10).  As there are no exclusions listed, the treatment is considered relevant and appropriate."
}
```

**Negative Example:**

```
## Input:
*   Given Medical Care: {treatments: "Cosmetic Botox injections"}
*   ICD and Surgery Description list: {icd_surgery_description: "M54.5 Low back pain"}
*   Exclusion details: {exclusions: "Cosmetic procedures are not covered."}

## Response:
```json
{
  "conclusion": "no",
  "probability score": 0.10,
  "explanation": "Botox injections for cosmetic purposes are not a relevant treatment for low back pain (ICD-10: M54.5). Furthermore, the exclusion details explicitly state that cosmetic procedures are not covered."
}
```
```

## Optimization Summary
- Iterations: 1
- Final Success Rate: 12/12
- Last Enhancement Reasoning: The recommendations are excellent and address the core issues of the prompt, including handling missing data, clarifying relevance, refining the probability score guidance, and providing clearer instructions for the model's persona and output format. The addition of examples, especially negative examples, will significantly improve the model's understanding of the task. The revised prompt incorporates these improvements effectively. 

## Evaluation Results
row_count: 12
prompt_quality/mean: 3.8333333333333335
prompt_quality/std: 1.2673044646258476
Success Rate: 100.0% (12/12)
