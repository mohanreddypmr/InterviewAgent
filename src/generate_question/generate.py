import json
from typing import Dict, List
from llms.providers import llm_google, llm_ollama_model
from .models import Question, SectionQuestions, GeneratedQuestions , ListQuestion
from langchain_core.output_parsers import JsonOutputParser

ollama_model = llm_ollama_model()

def load_resume(file_path: str) -> Dict:
    """Load resume data from JSON file"""
    with open(file_path, 'r') as f:
        return json.load(f)

def generate_questions_for_section(section_data: Dict, section_type: str, num_questions: int = 2) -> List[Question]:
    """Generate questions for a specific section using LLM"""
    
    prompts = {
        'work_experience': """
        Given the following work experience, generate {num_questions} specific and technical interview questions.
        For each question, provide:
        1. The question text
        2. Category (technical/behavioral)
        3. Difficulty level (easy/medium/hard)
        4. Context or explanation
        5. expected_answer_points - 2-3 key points expected in the answer(mention the points in bullet points) 

        Format each question as a JSON object with these fields(question , category , difficulty , context , expected_answer_points).
        Focus on technical challenges, problem-solving approaches, and impact of their work.
        Work details: {details}
        """,
        
        'projects': """
        Based on this project description, generate {num_questions} technical interview questions.
        For each question, provide:
        1. The question text
        2. Category (technical/behavioral)
        3. Difficulty level (easy/medium/hard)
        4. Context or explanation
        5. expected_answer_points - 2-3 key points expected in the answer(mention the points in bullet points) 
        
        Format each question as a JSON object with these fields(question , category , difficulty , context , expected_answer_points).
        Focus on technical implementation, challenges overcome, and design decisions.
        Project details: {details}
        """,
        
        'skills': """
        For the following skills, generate {num_questions} technical interview questions.
        For each question, provide:
        1. The question text
        2. Category (technical/behavioral)
        3. Difficulty level (easy/medium/hard)
        4. Context or explanation
        5. expected_answer_points - 2-3 key points expected in the answer(mention the points in bullet points)
        
        Format each question as a JSON object with these fields(question , category , difficulty , context , expected_answer_points).
        Focus on deep understanding and practical application of these technologies.
        Skills: {details}
        """,
        
        'publications': """
        Based on this publication, generate {num_questions} technical interview questions.
        For each question, provide:
        1. The question text
        2. Category (technical/behavioral)
        3. Difficulty level (easy/medium/hard)
        4. Context or explanation
        5. expected_answer_points - 2-3 key points expected in the answer(mention the points in bullet points) 
        
        Format each question as a JSON object with these fields(question , category , difficulty , context , expected_answer_points).
        Focus on research methodology, findings, contributions to the field, and technical depth.
        Publication details: {details}
        """
    }

    # Construct the appropriate prompt
    prompt = prompts.get(section_type, "Generate {num_questions} interview questions about: {details}")
    formatted_prompt = prompt.format(num_questions=num_questions, details=str(section_data))

    messages = [
        {"role": "system", "content": "You are an expert technical interviewer. Generate specific, "
         "technical questions that assess deep understanding and practical experience. "
         "Return the questions in valid JSON format."},
        {"role": "user", "content": formatted_prompt}
    ]

    # Get response from LLM
    # response = llm_google(messages)  
    response = ollama_model.invoke(messages) #.with_structured_output(ListQuestion)
    parser = JsonOutputParser(pydantic_object=ListQuestion)
    # Parse the response into Question objects
    print(response.content)
    try:
        json_out = parser.invoke(response)
        return json_out
    except json.JSONDecodeError:
        # Fallback to simple question format if JSON parsing fails
        return [Question(
            question=q,
            category="technical",
            difficulty="medium",
            context=None,
            expected_answer_points=[]
        ) for q in response.split('\n') if q.strip()]

def main(meta_info_path: str , output_path: str):
    # Load resume data
    resume_data = load_resume(meta_info_path)
    
    all_sections = []
    total_questions = 0
    
    # Generate questions for work experience
    if 'work_experience' in resume_data:
        for experience in resume_data['work_experience']:
            print(experience)
            print('+++'*100)
            questions = generate_questions_for_section(experience, 'work_experience', 3)
            all_sections.append(SectionQuestions(
                section_name="work_experience",
                section_title=experience.get('company', 'Unknown'),
                questions=questions
            ))
            total_questions += len(questions)
    if True:
        # Generate questions for projects
        if 'projects' in resume_data:
            for project in resume_data['projects']:
                questions = generate_questions_for_section(project, 'projects', 2)
                all_sections.append(SectionQuestions(
                    section_name="projects",
                    section_title=project.get('name', 'Unknown'),
                    questions=questions
                ))
                total_questions += len(questions)
        
        # Generate questions for skills
        if 'skills' in resume_data:
            questions = generate_questions_for_section(resume_data['skills'], 'skills', 3)
            all_sections.append(SectionQuestions(
                section_name="skills",
                section_title="Technical Skills",
                questions=questions
            ))
            total_questions += len(questions)
        
        # Generate questions for publications
        if 'publications_research' in resume_data:
            for publication in resume_data['publications_research']:
                questions = generate_questions_for_section(publication, 'publications', 1)
                all_sections.append(SectionQuestions(
                    section_name="publications",
                    section_title=publication.get('title', 'Unknown'),
                    questions=questions
                ))
                total_questions += len(questions)
    
    # Create the final structured output
    generated_questions = GeneratedQuestions(
        total_questions=total_questions,
        sections=all_sections
    )
    
    # Save generated questions to a JSON file
    with open(output_path, 'w') as f:
        f.write(generated_questions.json())

# if __name__ == "__main__":
#     main()
