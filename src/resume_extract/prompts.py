personal_details_prompt = """You are provided with a resume document in plain text format. Your task is to extract structured candidate details from the resume.
Resume Content:
{resume_content}
Extract Personal Details:
You are provided with the resume text. Please extract the candidate’s personal details, including their full name, email address, and mobile phone number (including country code if available).
 - Name: The candidate's complete name.
 - Email: The candidate’s primary email address.
 - Mobile: The candidate’s contact number (ensure to extract any country code included).
Format your output as a JSON object following this structure. If any detail is missing, use null."""


work_experience_prompt = """You are provided with a resume document in plain text format. Your task is to extract structured candidate details from the resume.
Resume Content:
{resume_content}
Extract Work Experience:
Review the provided resume text and extract information about the candidate’s work experience. For each position, capture the following details:
 - Company: Name of the organization.
 - Title: Job title held by the candidate.
 - Duration: Employment period (for example, "Jan 2018 - Dec 2020").
 - Responsibilities: A brief description of the candidate’s responsibilities or achievements for that role.
 - Projects: extract the details of projects the candidate has worked on the company. For each project, capture:
     - title: The project's name.
     - description: A short summary of the project.
     - technologies: A list of technologies, tools, or frameworks used.
Return the details as a JSON array of work experience objects. If no work experience is listed, return an empty array."""

projects_prompt = """You are provided with a resume document in plain text format. Your task is to extract structured candidate details from the resume.
Resume Content:
{resume_content}
Extract Projects:
From the resume text, extract the details of projects the candidate has worked on. For each project, capture:
 - title: The project's name.
 - description: A short summary of the project.
 - technologies: A list of technologies, tools, or frameworks used.
Present your findings as a JSON array. If the candidate has no projects listed, return an empty array.
use this format for json keys title , description , technologies
Now extract this information from the resume above:"""

skills_prompt = """You are a professional resume analyzer.
Your task is to extract all **skills** mentioned in the given resume. Group them into the following categories:

1. **Technical Skills** – programming languages, frameworks, libraries, dev tools, databases, cloud services, etc.
2. **Soft Skills** – communication, leadership, time management, problem-solving, etc.
3. **Domain-Specific Skills** – subject matter expertise or industry-specific knowledge (e.g., fintech, robotics, bioinformatics).
4. **Tools & Platforms** – IDEs, productivity tools, software platforms (e.g., Git, JIRA, Figma).
5. **Languages** – spoken languages (e.g., English, Spanish, German).

Return the output as a structured JSON object with each skill category containing a list of strings. Do not include explanations or extra formatting — only valid JSON.
use these names for json keys technical_skills , soft_skills , domain_specific_skills , tools_and_platforms , languages
If a skill category is not present, return an empty list for that category.
Now extract the skills from the following resume:
{resume_content}
"""

education_prompt = """You are provided with a resume document in plain text format. Your task is to extract structured candidate details from the resume.
Resume Content:
{resume_content}
Extract Education Details:
Please extract the candidate’s educational background from the resume text. For each entry, include:
 - Institution: The name of the school, college, or university.
 - Degree: The degree or certification earned.
 - Year: The time period of attendance or the graduation year.
Return these details as a JSON array. If the candidate provides no education details, return an empty array.
use this format for json keys institution , degree , year
Now extract this information from the resume above:"""

resume_template_instructions = """Instructions:
Read the resume content provided below.
 - Extract the information for each section, even if one or more sections are missing. For missing sections, return an empty list or null (as applicable).
 - Format your output as a JSON object that follows the structure defined by the attached Pydantic model.
 - Do not include any additional keys outside of those specified in the model."""


resume_template_prompt= """You are provided with a resume document in plain text format. Your task is to extract structured candidate details from the resume. Please extract and output the following information:

1.Personal Information
 - Name: Full name of the candidate.
 - Email: All email addresses.
 - Mobile Number: Contact number, ensuring to include country code if available.
2.Professional Summary and Achievements
 - Work Experience: A chronological list including companies, job titles, duration of employment, and key responsibilities or accomplishments.
 - Projects: Titles, descriptions, technologies used, and any results or outcomes related to the projects.
3.Education Details
 - Institutions: Names of schools, colleges, or universities attended.
 - Degrees/Certifications: Degrees earned or certifications completed.
 - Years: Attendance period or graduation years.
4.Skills
 - Technical and Soft Skills: A list of programming languages, tools, and relevant soft skills.
5.Additional Achievements
 - Awards & Honors: Any relevant awards, recognitions, or notable achievements.

The extracted information should be formatted in JSON using key-value pairs. If any section is not present in the resume, denote its value as null or an empty list where appropriate.
resume:{resume_document}"""

publications_prompt = """You are an expert resume parser. Your task is to extract all **publications and research** mentioned in the resume and return the result as a **JSON array** of structured objects.
Each item should include the following fields (if available):
- **title**: Title of the paper or research work
- **authors**: List of authors (including the resume owner if named)
- **publication_venue**: Journal, conference, or platform where it was published
- **year**: Year of publication (integer)
- **doi_or_link**: DOI or a direct link to the publication (if available)
- **description**: A short summary or abstract (if present)

Return only valid JSON. If no publications or research work is found, return an empty list.
Now extract this information from the resume below:
{resume_content}
"""


def get_resume_chunking_prompt(resume_text: str) -> str:
    prompt = f"""
You are an intelligent document parser designed to preprocess resumes for a Retrieval-Augmented Generation (RAG) system.
Your task is to intelligently chunk the given raw resume content into well-defined sections for semantic retrieval. Focus on structuring the data meaningfully and consistently so that downstream models can retrieve relevant information efficiently.
Specifically, divide the resume into the following labeled sections:
1. Personal Details
   - Full name, email, phone number, LinkedIn, GitHub, portfolio links, address (if present).
2. Education
   - Degrees, institutions, years of study, relevant coursework or achievements.
3. Work Experience
   - Job titles, company names, duration, responsibilities, technologies used, accomplishments.
4. Skills
   - List of technical, soft, or domain-specific skills.
5. Projects
   - Project titles, descriptions, tech stack, roles played, outcomes.
6. Certifications / Awards / Achievements (optional section)
   - Any notable recognitions, certificates, honors.
7. Publications / Research (optional section)
   - Any academic publications or relevant research contributions.
---
🔍 Guidelines for Output Formatting:
- Label each section clearly with headers.
- Preserve bullet points, dates, and formatting that help maintain semantic meaning.
- If a section is missing or not clearly identifiable, note it as "Not Found".
- Ensure each chunk is semantically meaningful and self-contained for downstream use in retrieval.
- Prefer consistent formatting, such as bullet points or structured lists where appropriate.
---
✅ Output Format Example:
### Personal Details:
Name: Jane Doe  
Email: jane.doe@email.com  
Phone: +1-123-456-7890  
LinkedIn: linkedin.com/in/janedoe  
GitHub: github.com/janedoe
### Education:
- B.Sc. in Computer Science, MIT (2016–2020)  
  Relevant Coursework: Algorithms, Machine Learning  
### Work Experience:
- Software Engineer at Google (2021–Present)  
  • Built scalable microservices in Go and Python  
  • Improved system latency by 30%
### Skills:
Python, Java, Docker, AWS, SQL, Leadership, Agile
### Projects:
- Resume Parser App  
  • Built using Python and spaCy  
  • Extracted structured data from raw resume PDFs
### Certifications / Awards / Achievements:
- AWS Certified Solutions Architect  
- Winner, HackMIT 2019
### Publications / Research:
Not Found
---
Now parse the following resume content accordingly:
{resume_text} 
"""
    return prompt
