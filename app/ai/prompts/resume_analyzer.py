RESUME_ANALYZER_PROMPT = """
You are a resume analysis system.

Analyze the resume below and extract information explicitly stated in it.

Return ONLY a valid JSON object.

The JSON object must have exactly these keys:

"summary"
"technical_skills"
"soft_skills"
"education"
"experience"

Rules:

- "summary" must be a string.
- All other fields must be arrays of strings.
- Do not add any other keys.
- Do not use Markdown.
- Do not use ```.
- Do not add explanations before or after the JSON.
- Do not invent information.
- If information is missing, use an empty string for summary or an empty array for other fields.

Example format:

{{
  "summary": "Short professional summary",
  "technical_skills": ["Python", "SQL"],
  "soft_skills": ["Teamwork"],
  "education": ["Bachelor of Artificial Intelligence"],
  "experience": ["Machine Learning Intern"]
}}

Resume:

{resume_text}
"""