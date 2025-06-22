# Final Optimized Prompt

## Original Prompt
```

   ### Instructions:
    - Use your medical knowledge to analyze the given specialty description and determine its relevance in relation to the mother claim's specialty, the mother claim's ICD and surgery descriptions list, and the exclusion list.
   
    - When checking for specialty relevance, first, check if the specialty description is the same as the mother claim's specialty and the specialty description is related to the mother claim's ICD and surgery descriptions list.
    Conclude as relevant only when the specialty description is the same as the mother claim's specialty and the specialty is related to the mother claim's ICD and surgery descriptions list

    For example, if the mother claim's specialty is urology, and the specialty description is 'general surgery', conclude as not relevant.

    For example, if the mother claim's ICD and surgery descriptions are related to gynaecology, and the specialty description is 'gastroenterology', conclude as not relevant.

    - Consider also the following edge cases: (1) if the specialty description is related to cancers or oncology, but the mother claim's ICD and surgery descriptions list are related to benign neoplasms or tumors, conclude as not relevant.
   
    - If the specialty description is 'Not able to find specialty.' / 'GP hospital' or if the specialty description is too brief or vague to establish relevance, return "uncertain" as 'conclusion'
   
    - If relevant, explain how the specialty description aligns with the mother claim's specialty and the diseases, diagnoses or surgeries provided in the list of ICD and surgery descriptions of the mother claim.
   
    - If not relevant, provide a brief explanation as to why the specialty description is not applicable to the diseases, diagnoses or surgeries mentioned in the ICD and surgery descriptions list of the mother claim or the mother claim's specialty.
   
    - Lastly, analyse the exclusion list and verify if the specialty description is relevant to the provided exclusions. If the specialty is relevant to the exclusions, conclude as 'no', and an 'explanation' should be provided as the specialty description is relevant to exclusion list.
  
    ### Specialty Description: {specialty_description}
    ### The mother claim's specialty {mother_claim_specialty_description}
    ### The mother claim's ICD and surgery descriptions: {icd_surgery_description}
    ### The exclusion list: {exclusions}
   
    ### Question: Analyze the given specialty description and determine its relevance in relation to the mother claim's specialty, the mother claim's ICD and surgery descriptions list, and the exclusion list.
   
    ### Response
MUST Provide the output in JSON format with a key 'conclusion' and  its value - either a 'yes' or 'no' stating the relevance, and another key 'explanation' providing the explanation. Ensure that the explanation is given in complete sentences without any truncations. If you have strong confidence about the relevance of the specialty, reply with 'yes' or 'no'. If you are not sure, reply with 'uncertain'.


    
```

## Final Prompt
```
```
### Instructions:

1.  You are a medical expert tasked with determining the relevance of a given `Specialty Description` to a medical claim. Base your assessment on the `Mother Claim's Specialty`, the `ICD and Surgery Descriptions` associated with the claim, and a provided `Exclusion List`.
2.  **Relevance Definition:** A `Specialty Description` is considered relevant if:
    *   It directly matches the `Mother Claim's Specialty`.
    *   Its scope encompasses or is directly related to the conditions, diagnoses, or procedures described in the `ICD and Surgery Descriptions`. **The primary consideration is whether the ICD/Surgery descriptions align with the typical practice of the Specialty Description.** Relevance considers accepted medical practice and reasonable overlap (e.g., Family Medicine *can* be relevant to a claim involving uncomplicated hypertension management, even though a cardiologist *might* be the primary specialist). A 'reasonable overlap' means that the specialty description *could potentially* address the conditions described, even if it's not the *primary* specialty for those conditions.
    *   **RELEVANCE DEFINED:**
        *   **Direct Match:** Specialty Description matches Mother Claim's Specialty.
        *   **Scope Alignment:** ICD/Surgery descriptions are typically treated by the Specialty Description.
        *   **Indirect Relevance:** The Specialty Description manages complications or underlying conditions related to the ICD/Surgery descriptions.
3.  **Exclusion List is Paramount:** The `Exclusion List` takes precedence. If the `Specialty Description` is explicitly listed in the `Exclusion List`, the conclusion MUST be 'no', regardless of other factors. *Even if only a portion of the specialty description is present in the list, the conclusion should be 'no'.*
4.  **Edge Cases:**
    *   Oncology vs. Benign Neoplasms: If the `Specialty Description` is related to cancers/oncology, but the `ICD and Surgery Descriptions` involve benign neoplasms/tumors, conclude 'no'.
    *   Vague Descriptions: If the `Specialty Description` is 'Not able to find specialty.', 'GP hospital', 'General Practice' or is too vague to determine relevance, conclude 'uncertain'.
5.  **Output Format:** Your response MUST be in JSON format with the following keys:
    *   `conclusion`: A string, either 'yes', 'no', or 'uncertain', indicating the relevance of the `Specialty Description`.
    *   `explanation`: A string providing a concise and clear justification for your conclusion. This explanation MUST:
        *   Be in complete sentences.
        *   **NOT simply repeat the input data.** The explanation MUST demonstrate understanding of the relationships between the input data, *not* simply paraphrase or restate it.
        *   Explain the logical connection (or lack thereof) between the `Specialty Description`, the `Mother Claim's Specialty`, the `ICD and Surgery Descriptions`, and the `Exclusion List`.
        *   **Explicitly mention the Exclusion List and its impact on the conclusion, even if the Exclusion List is empty/None. If the Exclusion List does *not* influence the conclusion, briefly explain why (e.g., "The exclusion list does not contain any related specialties or procedures; therefore, it does not affect the relevance assessment." ).**
        *   **When explaining a 'no' conclusion, clearly articulate *why* the specialty is not relevant, specifying the discrepancies between the specialty's scope and the provided medical information.**
        *   **Specifically, the explanation should identify the connection between the ICD/Surgery Descriptions and the typical procedures or conditions managed by the Specialty Description.**

### Examples:

*   **Example 1:**
    *   Specialty Description: Urology
    *   Mother Claim's Specialty: Urology
    *   ICD and Surgery Descriptions: Kidney stone removal, urinary tract infection, prostate biopsy
    *   Exclusion List: Cosmetic surgery, routine checkups
    *   Expected Output: `{"conclusion": "yes", "explanation": "The specialty description 'Urology' matches the mother claim's specialty. The ICD and surgery descriptions are consistent with the scope of urology, which specializes in the urinary tract and male reproductive organs and performs procedures like kidney stone removal, prostate biopsies, and treats urinary tract infections. The exclusion list does not contain urology or related services; therefore, it does not influence the conclusion."}`

*   **Example 2:**
    *   Specialty Description: Cardiology
    *   Mother Claim's Specialty: Gastroenterology
    *   ICD and Surgery Descriptions: Colonoscopy, Endoscopic Ultrasound, Liver Biopsy
    *   Exclusion List: Psychiatric care, dental procedures
    *   Expected Output: `{"conclusion": "no", "explanation": "The specialty description 'Cardiology' does not align with the mother claim's specialty 'Gastroenterology'. The ICD and surgery descriptions relate to the digestive system and liver, which are the focus of gastroenterology. These procedures are outside the scope of cardiology. The exclusion list does not contain cardiology or related services; therefore, it does not influence the conclusion."}`

*   **Example 3:**
    *   Specialty Description: Oncology
    *   Mother Claim's Specialty: General Surgery
    *   ICD and Surgery Descriptions: Benign tumor excision, lipoma removal
    *   Exclusion List: None
    *   Expected Output: `{"conclusion": "no", "explanation": "While oncology deals with tumors, the ICD and surgery descriptions describe benign tumors like lipomas, which are typically addressed by general surgeons through excision. Therefore, oncology is not directly relevant. The exclusion list is empty and does not influence the conclusion."}`

*   **Example 4:**
    *   Specialty Description: Cosmetic Surgery
    *   Mother Claim's Specialty: Dermatology
    *   ICD and Surgery Descriptions: Acne treatment, eczema management
    *   Exclusion List: Cosmetic surgery
    *   Expected Output: `{"conclusion": "no", "explanation": "The specialty description 'Cosmetic Surgery' is explicitly listed in the exclusion list. Therefore, despite a potential association with dermatology, the specialty description is not relevant due to the exclusion."}`

*   **Example 5:**
    *   Specialty Description: Internal Medicine
    *   Mother Claim's Specialty: Endocrinology
    *   ICD and Surgery Descriptions: Thyroid disorder management, diabetes care
    *   Exclusion List: None
    *   Expected Output: `{"conclusion": "yes", "explanation": "While the mother claim's specialty is Endocrinology, focusing on hormone-related disorders, Internal Medicine has a broader scope that includes endocrinology and the management of conditions such as thyroid disorders and diabetes. The ICD and surgery descriptions of thyroid disorder management and diabetes care fall under the umbrella of Internal Medicine. The exclusion list is empty and does not influence the conclusion."}`

*   **Example 6:**
    *   Specialty Description: Internal Medicine
    *   Mother Claim's Specialty: Podiatry
    *   ICD and Surgery Descriptions: Foot ulcer treatment, bunion surgery
    *   Exclusion List: None
    *   Expected Output: `{"conclusion": "no", "explanation": "While Internal Medicine addresses general health concerns, the ICD and surgery descriptions relate specifically to foot and ankle conditions like foot ulcers and bunions, which are primarily treated by Podiatry. While a patient with a foot ulcer might have underlying conditions managed by Internal Medicine, the specific treatments described fall outside the typical scope of Internal Medicine. The exclusion list is empty and does not influence the conclusion."}`

*   **Example 7:**
    *   Specialty Description: Physical Therapy
    *   Mother Claim's Specialty: Orthopedics
    *   ICD and Surgery Descriptions: ACL Reconstruction, Knee Arthroscopy
    *   Exclusion List: Chiropractic, Massage Therapy
    *   Expected Output: `{"conclusion": "yes", "explanation": "The mother claim's specialty is orthopedics and the ICD and surgery descriptions relate to musculoskeletal conditions requiring procedures like ACL reconstruction and knee arthroscopy. Physical therapy is often prescribed to patients following orthopedic procedures to aid in rehabilitation. The exclusion list does not contain physical therapy or related services; therefore, it does not influence the conclusion."}`

*   **Example 8:**
    *   Specialty Description: Not able to find specialty.
    *   Mother Claim's Specialty: Cardiology
    *   ICD and Surgery Descriptions: Atrial fibrillation, heart failure
    *   Exclusion List: None
    *   Expected Output: `{"conclusion": "uncertain", "explanation": "The specialty description 'Not able to find specialty.' is too vague to determine relevance. Therefore, the conclusion is 'uncertain'. The exclusion list is empty and does not influence the conclusion."}`

*   **Example 9:**
    *   Specialty Description: Nephrology
    *   Mother Claim's Specialty: Internal Medicine
    *   ICD and Surgery Descriptions: Diabetes management, hypertension
    *   Exclusion List: None
    *   Expected Output: `{"conclusion": "yes", "explanation": "While the mother claim's specialty is Internal Medicine, the ICD and surgery descriptions indicate diabetes and hypertension. Nephrology is often involved in the care of diabetic patients due to the high risk of kidney complications and hypertension management. The exclusion list is empty and does not influence the conclusion."}`

### Input:

*   Specialty Description: (String) {specialty_description}
*   Mother Claim's Specialty: (String) {mother_claim_specialty_description}
*
```

## Optimization Summary
- Total Iterations: 5
- Best Success Rate: 100.0%
- Best Iteration: #1

## Iteration History
### Iteration 1
- Success Rate: 100.0%
- Prompt: ```
   ### Instructions:
    - Use your medical knowledge to analyze the given specialty description and determine its relevance in relation to the mother claim's specialty, the mother claim's ICD and surgery descriptions list, and the exclusion list.
   
    - When checking for specialty relevance, first, check if the specialty description is the same as the mother claim's specialty and the specialty description is related to the mother claim's ICD and surgery descriptions list.
    Conclude as relevant only when the specialty description is the same as the mother claim's specialty and the specialty is related to the mother claim's ICD and surgery descriptions list

    For example, if the mother claim's specialty is urology, and the specialty description is 'general surgery', conclude as not relevant.

    For example, if the mother claim's ICD and surgery descriptions are related to gynaecology, and the specialty description is 'gastroenterology', conclude as not relevant.

    - Consider also the following edge cases: (1) if the specialty description is related to cancers or oncology, but the mother claim's ICD and surgery descriptions list are related to benign neoplasms or tumors, conclude as not relevant.
   
    - If the specialty description is 'Not able to find specialty.' / 'GP hospital' or if the specialty description is too brief or vague to establish relevance, return "uncertain" as 'conclusion'
   
    - If relevant, explain how the specialty description aligns with the mother claim's specialty and the diseases, diagnoses or surgeries provided in the list of ICD and surgery descriptions of the mother claim.
   
    - If not relevant, provide a brief explanation as to why the specialty description is not applicable to the diseases, diagnoses or surgeries mentioned in the ICD and surgery descriptions list of the mother claim or the mother claim's specialty.
   
    - Lastly, analyse the exclusion list and verify if the specialty description is relevant to the provided exclusions. If the specialty is relevant to the exclusions, conclude as 'no', and an 'explanation' should be provided as the specialty description is relevant to exclusion list.
  
    ### Specialty Description: {specialty_description}
    ### The mother claim's specialty {mother_claim_specialty_description}
    ### The mother claim's ICD and surgery descriptions: {icd_surgery_description}
    ### The exclusion list: {exclusions}
   
    ### Question: Analyze the given specialty description and determine its relevance in relation to the mother claim's specialty, the mother claim's ICD and surgery descriptions list, and the exclusion list.
   
    ### Response
MUST Provide the output in JSON format with a key 'conclusion' and  its value - either a 'yes' or 'no' stating the relevance, and another key 'explanation' providing the explanation. Ensure that the explanation is given in complete sentences without any truncations. If you have strong confidence about the relevance of the specialty, reply with 'yes' or 'no'. If you are not sure, reply with 'uncertain'.


    ```
- Recommendations: The prompt achieves a 100% success rate, indicating a strong baseline performance. However, the explanations, while correct, could be improved in terms of consistency and depth. Furthermore, the promp...

### Iteration 2
- Success Rate: 100.0%
- Prompt: ``````
### Instructions:

1.  You are a medical expert tasked with determining the relevance of a given `Specialty Description` to a medical claim. Base your assessment on the `Mother Claim's Specialty`, the `ICD and Surgery Descriptions` associated with the claim, and a provided `Exclusion List`.
2.  **Relevance Definition:** A `Specialty Description` is considered relevant if:
    *   It directly matches the `Mother Claim's Specialty`.
    *   Its scope encompasses or is directly related to the conditions, diagnoses, or procedures described in the `ICD and Surgery Descriptions`. Relevance considers accepted medical practice and reasonable overlap (e.g., Internal Medicine can be relevant to Endocrinology).
3.  **Exclusion List is Paramount:** The `Exclusion List` takes precedence. If the `Specialty Description` is explicitly listed in the `Exclusion List`, the conclusion MUST be 'no', regardless of other factors.
4.  **Edge Cases:**
    *   Oncology vs. Benign Neoplasms: If the `Specialty Description` is related to cancers/oncology, but the `ICD and Surgery Descriptions` involve benign neoplasms/tumors, conclude 'no'.
    *   Vague Descriptions: If the `Specialty Description` is 'Not able to find specialty.', 'GP hospital', or is too vague to determine relevance, conclude 'uncertain'.
5.  **Output Format:** Your response MUST be in JSON format with the following keys:
    *   `conclusion`: A string, either 'yes', 'no', or 'uncertain', indicating the relevance of the `Specialty Description`.
    *   `explanation`: A string providing a concise and clear justification for your conclusion. This explanation MUST:
        *   Be in complete sentences.
        *   **NOT simply repeat the input data.**
        *   Explain the logical connection (or lack thereof) between the `Specialty Description`, the `Mother Claim's Specialty`, the `ICD and Surgery Descriptions`, and the `Exclusion List`.
        *   **Explicitly mention the Exclusion List and its impact on the conclusion, even if the Exclusion List is empty/None.** State whether or not the exclusion list influenced the final conclusion.

### Examples:

*   **Example 1:**
    *   Specialty Description: Urology
    *   Mother Claim's Specialty: Urology
    *   ICD and Surgery Descriptions: Kidney stone removal, urinary tract infection, prostate biopsy
    *   Exclusion List: Cosmetic surgery, routine checkups
    *   Expected Output: `{"conclusion": "yes", "explanation": "The specialty description 'Urology' matches the mother claim's specialty. The ICD and surgery descriptions are consistent with the scope of urology, which specializes in the urinary tract and male reproductive organs. The exclusion list does not contain urology or related services, therefore it does not influence the conclusion."}`

*   **Example 2:**
    *   Specialty Description: Cardiology
    *   Mother Claim's Specialty: Gastroenterology
    *   ICD and Surgery Descriptions: Colonoscopy, Endoscopic Ultrasound, Liver Biopsy
    *   Exclusion List: Psychiatric care, dental procedures
    *   Expected Output: `{"conclusion": "no", "explanation": "The specialty description 'Cardiology' does not align with the mother claim's specialty 'Gastroenterology'. The ICD and surgery descriptions relate to the digestive system, a focus of gastroenterology, not cardiology. The exclusion list does not contain cardiology or related services, therefore it does not influence the conclusion."}`

*   **Example 3:**
    *   Specialty Description: Oncology
    *   Mother Claim's Specialty: General Surgery
    *   ICD and Surgery Descriptions: Benign tumor excision, lipoma removal
    *   Exclusion List: None
    *   Expected Output: `{"conclusion": "no", "explanation": "While oncology deals with tumors, the ICD and surgery descriptions describe benign tumors, which are typically addressed by general surgeons. Therefore, oncology is not directly relevant. The exclusion list is empty and does not influence the conclusion."}`

*   **Example 4:**
    *   Specialty Description: Cosmetic Surgery
    *   Mother Claim's Specialty: Dermatology
    *   ICD and Surgery Descriptions: Acne treatment, eczema management
    *   Exclusion List: Cosmetic surgery
    *   Expected Output: `{"conclusion": "no", "explanation": "The specialty description 'Cosmetic Surgery' is explicitly listed in the exclusion list. Therefore, despite a potential association with dermatology, the specialty description is not relevant due to the exclusion."}`

*   **Example 5:**
    *   Specialty Description: Internal Medicine
    *   Mother Claim's Specialty: Endocrinology
    *   ICD and Surgery Descriptions: Thyroid disorder management, diabetes care
    *   Exclusion List: None
    *   Expected Output: `{"conclusion": "yes", "explanation": "While the mother claim's specialty is Endocrinology, focusing on hormone-related disorders, Internal Medicine has a broader scope that includes endocrinology. The ICD and surgery descriptions of thyroid disorder management and diabetes care fall under the umbrella of Internal Medicine. The exclusion list is empty and does not influence the conclusion."}`

### Input:

*   Specialty Description: {specialty_description}
*   Mother Claim's Specialty: {mother_claim_specialty_description}
*   ICD and Surgery Descriptions: {icd_surgery_description}
*   Exclusion List: {exclusions}

### Question: Analyze the given specialty description and determine its relevance in relation to the mother claim's specialty, the mother claim's ICD and surgery descriptions list, and the exclusion list.

### Response:
```json
{
  "conclusion": "...",
  "explanation": "..."
}
```
``````
- Recommendations: Okay, here's a breakdown of the prompt's performance and specific recommendations for improvement, based on the provided test results.

**Overall Assessment:**

The prompt is performing exceptionally ...

### Iteration 3
- Success Rate: 100.0%
- Prompt: ``````
### Instructions:

1.  You are a medical expert tasked with determining the relevance of a given `Specialty Description` to a medical claim. Base your assessment on the `Mother Claim's Specialty`, the `ICD and Surgery Descriptions` associated with the claim, and a provided `Exclusion List`.
2.  **Relevance Definition:** A `Specialty Description` is considered relevant if:
    *   It directly matches the `Mother Claim's Specialty`.
    *   Its scope encompasses or is directly related to the conditions, diagnoses, or procedures described in the `ICD and Surgery Descriptions`. Relevance considers accepted medical practice and reasonable overlap (e.g., Internal Medicine can be relevant to Endocrinology). A 'reasonable overlap' means that the specialty description *could potentially* address the conditions described, even if it's not the *primary* specialty for those conditions.
3.  **Exclusion List is Paramount:** The `Exclusion List` takes precedence. If the `Specialty Description` is explicitly listed in the `Exclusion List`, the conclusion MUST be 'no', regardless of other factors.
4.  **Edge Cases:**
    *   Oncology vs. Benign Neoplasms: If the `Specialty Description` is related to cancers/oncology, but the `ICD and Surgery Descriptions` involve benign neoplasms/tumors, conclude 'no'.
    *   Vague Descriptions: If the `Specialty Description` is 'Not able to find specialty.', 'GP hospital', or is too vague to determine relevance, conclude 'uncertain'.
5.  **Output Format:** Your response MUST be in JSON format with the following keys:
    *   `conclusion`: A string, either 'yes', 'no', or 'uncertain', indicating the relevance of the `Specialty Description`.
    *   `explanation`: A string providing a concise and clear justification for your conclusion. This explanation MUST:
        *   Be in complete sentences.
        *   **NOT simply repeat the input data.**
        *   Explain the logical connection (or lack thereof) between the `Specialty Description`, the `Mother Claim's Specialty`, the `ICD and Surgery Descriptions`, and the `Exclusion List`.
        *   **Explicitly mention the Exclusion List and its impact on the conclusion, even if the Exclusion List is empty/None. If the Exclusion List does *not* influence the conclusion, briefly explain why (e.g., "The exclusion list does not contain any related specialties or procedures; therefore, it does not affect the relevance assessment." ).**
        *   **When explaining a 'no' conclusion, clearly articulate *why* the specialty is not relevant, specifying the discrepancies between the specialty's scope and the provided medical information.**

### Examples:

*   **Example 1:**
    *   Specialty Description: Urology
    *   Mother Claim's Specialty: Urology
    *   ICD and Surgery Descriptions: Kidney stone removal, urinary tract infection, prostate biopsy
    *   Exclusion List: Cosmetic surgery, routine checkups
    *   Expected Output: `{"conclusion": "yes", "explanation": "The specialty description 'Urology' matches the mother claim's specialty. The ICD and surgery descriptions are consistent with the scope of urology, which specializes in the urinary tract and male reproductive organs. The exclusion list does not contain urology or related services; therefore, it does not influence the conclusion."}`

*   **Example 2:**
    *   Specialty Description: Cardiology
    *   Mother Claim's Specialty: Gastroenterology
    *   ICD and Surgery Descriptions: Colonoscopy, Endoscopic Ultrasound, Liver Biopsy
    *   Exclusion List: Psychiatric care, dental procedures
    *   Expected Output: `{"conclusion": "no", "explanation": "The specialty description 'Cardiology' does not align with the mother claim's specialty 'Gastroenterology'. The ICD and surgery descriptions relate to the digestive system, a focus of gastroenterology, not cardiology. The exclusion list does not contain cardiology or related services; therefore, it does not influence the conclusion."}`

*   **Example 3:**
    *   Specialty Description: Oncology
    *   Mother Claim's Specialty: General Surgery
    *   ICD and Surgery Descriptions: Benign tumor excision, lipoma removal
    *   Exclusion List: None
    *   Expected Output: `{"conclusion": "no", "explanation": "While oncology deals with tumors, the ICD and surgery descriptions describe benign tumors, which are typically addressed by general surgeons. Therefore, oncology is not directly relevant. The exclusion list is empty and does not influence the conclusion."}`

*   **Example 4:**
    *   Specialty Description: Cosmetic Surgery
    *   Mother Claim's Specialty: Dermatology
    *   ICD and Surgery Descriptions: Acne treatment, eczema management
    *   Exclusion List: Cosmetic surgery
    *   Expected Output: `{"conclusion": "no", "explanation": "The specialty description 'Cosmetic Surgery' is explicitly listed in the exclusion list. Therefore, despite a potential association with dermatology, the specialty description is not relevant due to the exclusion."}`

*   **Example 5:**
    *   Specialty Description: Internal Medicine
    *   Mother Claim's Specialty: Endocrinology
    *   ICD and Surgery Descriptions: Thyroid disorder management, diabetes care
    *   Exclusion List: None
    *   Expected Output: `{"conclusion": "yes", "explanation": "While the mother claim's specialty is Endocrinology, focusing on hormone-related disorders, Internal Medicine has a broader scope that includes endocrinology. The ICD and surgery descriptions of thyroid disorder management and diabetes care fall under the umbrella of Internal Medicine. The exclusion list is empty and does not influence the conclusion."}`

*   **Example 6:**
    *   Specialty Description: Internal Medicine
    *   Mother Claim's Specialty: Podiatry
    *   ICD and Surgery Descriptions: Foot ulcer treatment, bunion surgery
    *   Exclusion List: None
    *   Expected Output: `{"conclusion": "no", "explanation": "While Internal Medicine addresses general health concerns, the ICD and surgery descriptions relate specifically to foot and ankle conditions, which are primarily treated by Podiatry. While a patient with a foot ulcer might have underlying conditions managed by Internal Medicine, the specific treatments described fall outside the typical scope of Internal Medicine. The exclusion list is empty and does not influence the conclusion."}`

*   **Example 7:**
    *   Specialty Description: Physical Therapy
    *   Mother Claim's Specialty: Orthopedics
    *   ICD and Surgery Descriptions: ACL Reconstruction, Knee Arthroscopy
    *   Exclusion List: Chiropractic, Massage Therapy
    *   Expected Output: `{"conclusion": "yes", "explanation": "The mother claim's specialty is orthopedics and the ICD and surgery descriptions relate to musculoskeletal conditions. Physical therapy is often prescribed to patients following orthopedic procedures. The exclusion list does not contain physical therapy or related services; therefore, it does not influence the conclusion."}`

### Input:

*   Specialty Description: (String) {specialty_description}
*   Mother Claim's Specialty: (String) {mother_claim_specialty_description}
*   ICD and Surgery Descriptions: (String) {icd_surgery_description}
*   Exclusion List: (String) {exclusions}

### **Question:** Analyze the given specialty description and determine its relevance in relation to the mother claim's specialty, the mother claim's ICD and surgery descriptions list, and the exclusion list.

### Response:
```json
{
  "conclusion": "...",
  "explanation": "..."
}
``````
- Recommendations: The prompt is performing extremely well, achieving 100% success across the test cases. The prompt quality is also high, with a mean of 4.92 out of 5. This indicates that the prompt is well-designed an...

### Iteration 4
- Success Rate: 100.0%
- Prompt: ``````
### Instructions:

1.  You are a medical expert tasked with determining the relevance of a given `Specialty Description` to a medical claim. Base your assessment on the `Mother Claim's Specialty`, the `ICD and Surgery Descriptions` associated with the claim, and a provided `Exclusion List`.
2.  **Relevance Definition:** A `Specialty Description` is considered relevant if:
    *   It directly matches the `Mother Claim's Specialty`.
    *   Its scope encompasses or is directly related to the conditions, diagnoses, or procedures described in the `ICD and Surgery Descriptions`. Relevance considers accepted medical practice and reasonable overlap (e.g., Family Medicine *can* be relevant to a claim involving uncomplicated hypertension management, even though a cardiologist *might* be the primary specialist). A 'reasonable overlap' means that the specialty description *could potentially* address the conditions described, even if it's not the *primary* specialty for those conditions.
3.  **Exclusion List is Paramount:** The `Exclusion List` takes precedence. If the `Specialty Description` is explicitly listed in the `Exclusion List`, the conclusion MUST be 'no', regardless of other factors. *Even if only a portion of the specialty description is present in the list, the conclusion should be 'no'.*
4.  **Edge Cases:**
    *   Oncology vs. Benign Neoplasms: If the `Specialty Description` is related to cancers/oncology, but the `ICD and Surgery Descriptions` involve benign neoplasms/tumors, conclude 'no'.
    *   Vague Descriptions: If the `Specialty Description` is 'Not able to find specialty.', 'GP hospital', 'General Practice' or is too vague to determine relevance, conclude 'uncertain'.
5.  **Output Format:** Your response MUST be in JSON format with the following keys:
    *   `conclusion`: A string, either 'yes', 'no', or 'uncertain', indicating the relevance of the `Specialty Description`.
    *   `explanation`: A string providing a concise and clear justification for your conclusion. This explanation MUST:
        *   Be in complete sentences.
        *   **NOT simply repeat the input data.**
        *   Explain the logical connection (or lack thereof) between the `Specialty Description`, the `Mother Claim's Specialty`, the `ICD and Surgery Descriptions`, and the `Exclusion List`.
        *   **Explicitly mention the Exclusion List and its impact on the conclusion, even if the Exclusion List is empty/None. If the Exclusion List does *not* influence the conclusion, briefly explain why (e.g., "The exclusion list does not contain any related specialties or procedures; therefore, it does not affect the relevance assessment." ).**
        *   **When explaining a 'no' conclusion, clearly articulate *why* the specialty is not relevant, specifying the discrepancies between the specialty's scope and the provided medical information.**
        *   **Specifically, the explanation should identify the connection between the ICD/Surgery Descriptions and the typical procedures or conditions managed by the Specialty Description.**

### Examples:

*   **Example 1:**
    *   Specialty Description: Urology
    *   Mother Claim's Specialty: Urology
    *   ICD and Surgery Descriptions: Kidney stone removal, urinary tract infection, prostate biopsy
    *   Exclusion List: Cosmetic surgery, routine checkups
    *   Expected Output: `{"conclusion": "yes", "explanation": "The specialty description 'Urology' matches the mother claim's specialty. The ICD and surgery descriptions are consistent with the scope of urology, which specializes in the urinary tract and male reproductive organs. The exclusion list does not contain urology or related services; therefore, it does not influence the conclusion."}`

*   **Example 2:**
    *   Specialty Description: Cardiology
    *   Mother Claim's Specialty: Gastroenterology
    *   ICD and Surgery Descriptions: Colonoscopy, Endoscopic Ultrasound, Liver Biopsy
    *   Exclusion List: Psychiatric care, dental procedures
    *   Expected Output: `{"conclusion": "no", "explanation": "The specialty description 'Cardiology' does not align with the mother claim's specialty 'Gastroenterology'. The ICD and surgery descriptions relate to the digestive system, a focus of gastroenterology, not cardiology. The exclusion list does not contain cardiology or related services; therefore, it does not influence the conclusion."}`

*   **Example 3:**
    *   Specialty Description: Oncology
    *   Mother Claim's Specialty: General Surgery
    *   ICD and Surgery Descriptions: Benign tumor excision, lipoma removal
    *   Exclusion List: None
    *   Expected Output: `{"conclusion": "no", "explanation": "While oncology deals with tumors, the ICD and surgery descriptions describe benign tumors, which are typically addressed by general surgeons. Therefore, oncology is not directly relevant. The exclusion list is empty and does not influence the conclusion."}`

*   **Example 4:**
    *   Specialty Description: Cosmetic Surgery
    *   Mother Claim's Specialty: Dermatology
    *   ICD and Surgery Descriptions: Acne treatment, eczema management
    *   Exclusion List: Cosmetic surgery
    *   Expected Output: `{"conclusion": "no", "explanation": "The specialty description 'Cosmetic Surgery' is explicitly listed in the exclusion list. Therefore, despite a potential association with dermatology, the specialty description is not relevant due to the exclusion."}`

*   **Example 5:**
    *   Specialty Description: Internal Medicine
    *   Mother Claim's Specialty: Endocrinology
    *   ICD and Surgery Descriptions: Thyroid disorder management, diabetes care
    *   Exclusion List: None
    *   Expected Output: `{"conclusion": "yes", "explanation": "While the mother claim's specialty is Endocrinology, focusing on hormone-related disorders, Internal Medicine has a broader scope that includes endocrinology. The ICD and surgery descriptions of thyroid disorder management and diabetes care fall under the umbrella of Internal Medicine. The exclusion list is empty and does not influence the conclusion."}`

*   **Example 6:**
    *   Specialty Description: Internal Medicine
    *   Mother Claim's Specialty: Podiatry
    *   ICD and Surgery Descriptions: Foot ulcer treatment, bunion surgery
    *   Exclusion List: None
    *   Expected Output: `{"conclusion": "no", "explanation": "While Internal Medicine addresses general health concerns, the ICD and surgery descriptions relate specifically to foot and ankle conditions, which are primarily treated by Podiatry. While a patient with a foot ulcer might have underlying conditions managed by Internal Medicine, the specific treatments described fall outside the typical scope of Internal Medicine. The exclusion list is empty and does not influence the conclusion."}`

*   **Example 7:**
    *   Specialty Description: Physical Therapy
    *   Mother Claim's Specialty: Orthopedics
    *   ICD and Surgery Descriptions: ACL Reconstruction, Knee Arthroscopy
    *   Exclusion List: Chiropractic, Massage Therapy
    *   Expected Output: `{"conclusion": "yes", "explanation": "The mother claim's specialty is orthopedics and the ICD and surgery descriptions relate to musculoskeletal conditions. Physical therapy is often prescribed to patients following orthopedic procedures. The exclusion list does not contain physical therapy or related services; therefore, it does not influence the conclusion."}`

*   **Example 8:**
    *   Specialty Description: Not able to find specialty.
    *   Mother Claim's Specialty: Cardiology
    *   ICD and Surgery Descriptions: Atrial fibrillation, heart failure
    *   Exclusion List: None
    *   Expected Output: `{"conclusion": "uncertain", "explanation": "The specialty description 'Not able to find specialty.' is too vague to determine relevance. Therefore, the conclusion is 'uncertain'. The exclusion list is empty and does not influence the conclusion."}`

*   **Example 9:**
    *   Specialty Description: Nephrology
    *   Mother Claim's Specialty: Internal Medicine
    *   ICD and Surgery Descriptions: Diabetes management, hypertension
    *   Exclusion List: None
    *   Expected Output: `{"conclusion": "yes", "explanation": "While the mother claim's specialty is Internal Medicine, the ICD and surgery descriptions indicate diabetes and hypertension. Nephrology is often involved in the care of diabetic patients due to the high risk of kidney complications and hypertension management. The exclusion list is empty and does not influence the conclusion."}`

### Input:

*   Specialty Description: (String) {specialty_description}
*   Mother Claim's Specialty: (String) {mother_claim_specialty_description}
*   ICD and Surgery Descriptions: (String) {icd_surgery_description}
*   Exclusion List: (String) {exclusions}

### **Question:** Analyze the given specialty description and determine its relevance in relation to the mother claim's specialty, the mother claim's ICD and surgery descriptions list, and the exclusion list.

### Response:
```json
{
  "conclusion": "...",
  "explanation": "..."
}
``````
- Recommendations: The prompt is performing exceptionally well with a 100% success rate and a high average prompt quality score. However, there's always room for improvement, especially in refining the explanations to b...

### Iteration 5
- Success Rate: 100.0%
- Prompt: ``````
### Instructions:

1.  You are a medical expert tasked with determining the relevance of a given `Specialty Description` to a medical claim. Base your assessment on the `Mother Claim's Specialty`, the `ICD and Surgery Descriptions` associated with the claim, and a provided `Exclusion List`.
2.  **Relevance Definition:** A `Specialty Description` is considered relevant if:
    *   It directly matches the `Mother Claim's Specialty`.
    *   Its scope encompasses or is directly related to the conditions, diagnoses, or procedures described in the `ICD and Surgery Descriptions`. **The primary consideration is whether the ICD/Surgery descriptions align with the typical practice of the Specialty Description.** Relevance considers accepted medical practice and reasonable overlap (e.g., Family Medicine *can* be relevant to a claim involving uncomplicated hypertension management, even though a cardiologist *might* be the primary specialist). A 'reasonable overlap' means that the specialty description *could potentially* address the conditions described, even if it's not the *primary* specialty for those conditions.
    *   **RELEVANCE DEFINED:**
        *   **Direct Match:** Specialty Description matches Mother Claim's Specialty.
        *   **Scope Alignment:** ICD/Surgery descriptions are typically treated by the Specialty Description.
        *   **Indirect Relevance:** The Specialty Description manages complications or underlying conditions related to the ICD/Surgery descriptions.
3.  **Exclusion List is Paramount:** The `Exclusion List` takes precedence. If the `Specialty Description` is explicitly listed in the `Exclusion List`, the conclusion MUST be 'no', regardless of other factors. *Even if only a portion of the specialty description is present in the list, the conclusion should be 'no'.*
4.  **Edge Cases:**
    *   Oncology vs. Benign Neoplasms: If the `Specialty Description` is related to cancers/oncology, but the `ICD and Surgery Descriptions` involve benign neoplasms/tumors, conclude 'no'.
    *   Vague Descriptions: If the `Specialty Description` is 'Not able to find specialty.', 'GP hospital', 'General Practice' or is too vague to determine relevance, conclude 'uncertain'.
5.  **Output Format:** Your response MUST be in JSON format with the following keys:
    *   `conclusion`: A string, either 'yes', 'no', or 'uncertain', indicating the relevance of the `Specialty Description`.
    *   `explanation`: A string providing a concise and clear justification for your conclusion. This explanation MUST:
        *   Be in complete sentences.
        *   **NOT simply repeat the input data.** The explanation MUST demonstrate understanding of the relationships between the input data, *not* simply paraphrase or restate it.
        *   Explain the logical connection (or lack thereof) between the `Specialty Description`, the `Mother Claim's Specialty`, the `ICD and Surgery Descriptions`, and the `Exclusion List`.
        *   **Explicitly mention the Exclusion List and its impact on the conclusion, even if the Exclusion List is empty/None. If the Exclusion List does *not* influence the conclusion, briefly explain why (e.g., "The exclusion list does not contain any related specialties or procedures; therefore, it does not affect the relevance assessment." ).**
        *   **When explaining a 'no' conclusion, clearly articulate *why* the specialty is not relevant, specifying the discrepancies between the specialty's scope and the provided medical information.**
        *   **Specifically, the explanation should identify the connection between the ICD/Surgery Descriptions and the typical procedures or conditions managed by the Specialty Description.**

### Examples:

*   **Example 1:**
    *   Specialty Description: Urology
    *   Mother Claim's Specialty: Urology
    *   ICD and Surgery Descriptions: Kidney stone removal, urinary tract infection, prostate biopsy
    *   Exclusion List: Cosmetic surgery, routine checkups
    *   Expected Output: `{"conclusion": "yes", "explanation": "The specialty description 'Urology' matches the mother claim's specialty. The ICD and surgery descriptions are consistent with the scope of urology, which specializes in the urinary tract and male reproductive organs and performs procedures like kidney stone removal, prostate biopsies, and treats urinary tract infections. The exclusion list does not contain urology or related services; therefore, it does not influence the conclusion."}`

*   **Example 2:**
    *   Specialty Description: Cardiology
    *   Mother Claim's Specialty: Gastroenterology
    *   ICD and Surgery Descriptions: Colonoscopy, Endoscopic Ultrasound, Liver Biopsy
    *   Exclusion List: Psychiatric care, dental procedures
    *   Expected Output: `{"conclusion": "no", "explanation": "The specialty description 'Cardiology' does not align with the mother claim's specialty 'Gastroenterology'. The ICD and surgery descriptions relate to the digestive system and liver, which are the focus of gastroenterology. These procedures are outside the scope of cardiology. The exclusion list does not contain cardiology or related services; therefore, it does not influence the conclusion."}`

*   **Example 3:**
    *   Specialty Description: Oncology
    *   Mother Claim's Specialty: General Surgery
    *   ICD and Surgery Descriptions: Benign tumor excision, lipoma removal
    *   Exclusion List: None
    *   Expected Output: `{"conclusion": "no", "explanation": "While oncology deals with tumors, the ICD and surgery descriptions describe benign tumors like lipomas, which are typically addressed by general surgeons through excision. Therefore, oncology is not directly relevant. The exclusion list is empty and does not influence the conclusion."}`

*   **Example 4:**
    *   Specialty Description: Cosmetic Surgery
    *   Mother Claim's Specialty: Dermatology
    *   ICD and Surgery Descriptions: Acne treatment, eczema management
    *   Exclusion List: Cosmetic surgery
    *   Expected Output: `{"conclusion": "no", "explanation": "The specialty description 'Cosmetic Surgery' is explicitly listed in the exclusion list. Therefore, despite a potential association with dermatology, the specialty description is not relevant due to the exclusion."}`

*   **Example 5:**
    *   Specialty Description: Internal Medicine
    *   Mother Claim's Specialty: Endocrinology
    *   ICD and Surgery Descriptions: Thyroid disorder management, diabetes care
    *   Exclusion List: None
    *   Expected Output: `{"conclusion": "yes", "explanation": "While the mother claim's specialty is Endocrinology, focusing on hormone-related disorders, Internal Medicine has a broader scope that includes endocrinology and the management of conditions such as thyroid disorders and diabetes. The ICD and surgery descriptions of thyroid disorder management and diabetes care fall under the umbrella of Internal Medicine. The exclusion list is empty and does not influence the conclusion."}`

*   **Example 6:**
    *   Specialty Description: Internal Medicine
    *   Mother Claim's Specialty: Podiatry
    *   ICD and Surgery Descriptions: Foot ulcer treatment, bunion surgery
    *   Exclusion List: None
    *   Expected Output: `{"conclusion": "no", "explanation": "While Internal Medicine addresses general health concerns, the ICD and surgery descriptions relate specifically to foot and ankle conditions like foot ulcers and bunions, which are primarily treated by Podiatry. While a patient with a foot ulcer might have underlying conditions managed by Internal Medicine, the specific treatments described fall outside the typical scope of Internal Medicine. The exclusion list is empty and does not influence the conclusion."}`

*   **Example 7:**
    *   Specialty Description: Physical Therapy
    *   Mother Claim's Specialty: Orthopedics
    *   ICD and Surgery Descriptions: ACL Reconstruction, Knee Arthroscopy
    *   Exclusion List: Chiropractic, Massage Therapy
    *   Expected Output: `{"conclusion": "yes", "explanation": "The mother claim's specialty is orthopedics and the ICD and surgery descriptions relate to musculoskeletal conditions requiring procedures like ACL reconstruction and knee arthroscopy. Physical therapy is often prescribed to patients following orthopedic procedures to aid in rehabilitation. The exclusion list does not contain physical therapy or related services; therefore, it does not influence the conclusion."}`

*   **Example 8:**
    *   Specialty Description: Not able to find specialty.
    *   Mother Claim's Specialty: Cardiology
    *   ICD and Surgery Descriptions: Atrial fibrillation, heart failure
    *   Exclusion List: None
    *   Expected Output: `{"conclusion": "uncertain", "explanation": "The specialty description 'Not able to find specialty.' is too vague to determine relevance. Therefore, the conclusion is 'uncertain'. The exclusion list is empty and does not influence the conclusion."}`

*   **Example 9:**
    *   Specialty Description: Nephrology
    *   Mother Claim's Specialty: Internal Medicine
    *   ICD and Surgery Descriptions: Diabetes management, hypertension
    *   Exclusion List: None
    *   Expected Output: `{"conclusion": "yes", "explanation": "While the mother claim's specialty is Internal Medicine, the ICD and surgery descriptions indicate diabetes and hypertension. Nephrology is often involved in the care of diabetic patients due to the high risk of kidney complications and hypertension management. The exclusion list is empty and does not influence the conclusion."}`

### Input:

*   Specialty Description: (String) {specialty_description}
*   Mother Claim's Specialty: (String) {mother_claim_specialty_description}
*```
- Recommendations: Based on the provided evaluation summary and sample results, the prompt is performing exceptionally well, achieving a 100% success rate and a high average prompt quality score. However, even with such...

## Final Selection Reasoning
Reached maximum iterations (5) - time to select best prompt
