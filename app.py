from flask import Flask, request, jsonify
import requests
import os
from jsonschema import validate, ValidationError
import json
import re

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"
LATEX_TEMPLATE = "./CV/Default.tex"
OUTPUT_LATEX_FILE = "updated_resume.tex"
OUTPUT_PDF_FILE = "updated_resume.pdf"

# Define the schema for the LLaMA response
LLAMA_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "points": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 11,
            "maxItems": 11
        }
    },
    "required": ["points"]
}

@app.route('/generate-resume', methods=['POST'])
def generate_resume():
    data = request.json
    jd = data.get('jd', '')
    points = data.get('points', {})
    print(jd, "jd here")
    print(points, "points here")

    if not jd:
        return jsonify({"error": "Job description is required"}), 400

    if not points:
        print("or is it here:?")
        return jsonify({"error": "Points data is required"}), 400


    # Construct the prompt for the LLaMA model
    prompt = (
        f"Create exactly 11 bullet points for a resume based on the following job description (JD). "
        f"The points should be witty and cleverly incorporate the JD's keywords and themes in such a way "
        f"that it would be challenging for anyone to determine if the experience is real or inferred from the JD. "
        f"Format each bullet point like the examples provided below and ensure the response is structured in JSON. "
        f"Here is the JD:\n\n"
        f"{jd}\n\n"
        f"Here are examples of the format for the bullet points:\n"
        f"- Engineered a scalable GenAI powered transcription microservice with dynamic prompting and audio "
        f"  segmentation, overcoming token restrictions in long-form audio processing, reducing manual efforts by 80%.\n"
        f"- Architected a Notification Service Engine using Django, SNS, and Celery, as a centralized endpoint to "
        f"  orchestrate notifications across channels like SMS and email, boosting user engagement by 45%.\n\n"
        f"Create exactly 11 bullet points ... Return only the final answer in the following JSON format:"
        f'{{"points": ["point1", "point2", ..., "point11"]}}'
    )
    print("is the prompt forming ?")
    try:
        # Send the prompt to the LLaMA model via Ollama
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "llama3.2:latest",
                "prompt": prompt,
                "stream": False
            }
        )
        response.raise_for_status()
        llama_raw_response = response

        # Use a regex to find the JSON object in the response text
        match = re.search(r'{"points"\s*:\s*\[.*?\]}', llama_raw_response, re.DOTALL)
        if not match:
            return jsonify({"error": "No valid JSON found in response"}), 500

        points_json_str = match.group(0)
        points_extracted = json.loads(points_json_str)

        # Now validate against the schema
        validate(instance=points_data, schema=LLAMA_RESPONSE_SCHEMA)

        # Replace placeholders in the LaTeX template with the new points
        with open(LATEX_TEMPLATE, 'r') as file:
            latex_content = file.read()

        for placeholder, value in points.items():
            latex_content = latex_content.replace(f"%{placeholder}%", value)

        with open(OUTPUT_LATEX_FILE, 'w') as file:
            file.write(latex_content)

        # Generate the PDF
        os.system(f"pdflatex -output-directory . {OUTPUT_LATEX_FILE}")

        return jsonify({"message": "Resume updated successfully", "pdf_path": OUTPUT_PDF_FILE, "points": points_extracted}), 200
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
