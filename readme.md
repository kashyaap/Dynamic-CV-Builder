# Resume Generator with Flask and Ollama

This project generates resumes dynamically by leveraging Ollama's LLaMA model to craft clever and keyword-rich bullet points from job descriptions. The generated content is mapped to a LaTeX template to produce a PDF resume.

---

## Prerequisites

Before you start, ensure you have the following installed on your machine:

1. **Python 3.8+**
2. **pip** (Python package manager)
3. **Ollama** (local deployment of LLaMA model)
4. **LaTeX** (for PDF generation from `.tex` files)
5. **Virtualenv** (for environment isolation)

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/resume-generator.git
cd resume-generator
```

---

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

---

### 3. Install Required Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Install Ollama

Ollama is required to run the LLaMA model locally.  
Follow the official [Ollama installation guide](https://ollama.com/docs/installation) for your OS.

- **Linux / macOS**:

```bash
brew install ollama
```

- **Windows**:

```bash
winget install ollama
```

---

### 5. Download the LLaMA Model

```bash
ollama run llama3.2
```

Ensure the model `llama3.2` is available locally. This may take a while to download if it's the first time running the command.

---

### 6. Install LaTeX

LaTeX is needed to generate PDFs from `.tex` files.

- **Linux**:

```bash
sudo apt install texlive-full
```

- **macOS**:

```bash
brew install mactex
```

- **Windows**:
  Download and install [MikTeX](https://miktex.org/download).

---

### 7. Configure Environment Variables (Optional)

Create a `.env` file in the root directory to manage environment variables if needed:

```
OLLAMA_URL=http://localhost:11434/api/generate
LATEX_TEMPLATE=./CV/Default.tex
OUTPUT_LATEX_FILE=updated_resume.tex
OUTPUT_PDF_FILE=updated_resume.pdf
```

---

## Running the Project

1. **Ensure Ollama is running**

```bash
ollama serve
```

2. **Run the Flask App**

```bash
flask run
```

By default, the app will be available at:

```
http://127.0.0.1:5000
```

---

## Generating a Resume

- **Endpoint**: `/generate-resume`
- **Method**: `POST`
- **Parameters**:
  - `jd`: Job description (string)
  - `points`: Additional points as JSON (optional)

**Example Request**:

```bash
curl -X POST http://127.0.0.1:5000/generate-resume \
-F "jd=Full Stack Developer with experience in React, Flask, and AWS." \
-F "points={\"POINT_1\": \"Developed a Flask app...\"}"
```

---

## PDF Output

The generated PDF will be available as:

```
updated_resume.pdf
```

---

## Troubleshooting

1. **Ollama Connection Issues**:  
   Ensure that Ollama is running properly using:

```bash
ollama serve
```

2. **LaTeX Errors**:  
   Ensure LaTeX is correctly installed. Test with:

```bash
pdflatex --version
```

3. **Missing Models**:  
   Run the following to ensure the LLaMA model is available:

```bash
ollama run llama3.2
```

---
