import google.generativeai as genai

def generate_mom(transcription, prompt=None, api_key=None):
    if api_key:
        genai.configure(api_key=api_key)
    else:
        return "API Key required"

    model = genai.GenerativeModel(model_name="gemini-1.5-pro")

    input_text = transcription
    if prompt:
        input_text = f"{prompt}\n{transcription}"

    try:
        response = model.generate_content(input_text)
        mom_text = response.text.strip()
        mom_content = mom_text.split("Minutes of Meeting (MoM)", 1)[-1].strip()
        return mom_content
    except Exception as e:
        return f"Gemini error: {e}"

