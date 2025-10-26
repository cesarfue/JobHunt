def clean_json(input):
    cleaned_result = input.strip()
    if cleaned_result.startswith("```json"):
        cleaned_result = cleaned_result[7:]
    if cleaned_result.startswith("```"):
        cleaned_result = cleaned_result[3:]
    if cleaned_result.endswith("```"):
        cleaned_result = cleaned_result[:-3]
    cleaned_result = cleaned_result.strip()
    return cleaned_result
