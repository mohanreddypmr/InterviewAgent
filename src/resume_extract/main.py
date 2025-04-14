from resume_extract.prompts import get_resume_chunking_prompt
from llms.providers import llm_google , llm_ollama_model
from resume_extract.prompts import *
from resume_extract.parser_items import *
from typing import List
import json
from langchain_core.output_parsers import JsonOutputParser


def chunk_resume(source,save_path):
    f = open(source, 'r')
    k1 = f.read()
    text_ = ''
    for i in k1.split('\n'):
        j = i
        if j.strip() != '':
            text_ += i +'\n'
    f.close()
    msg = get_resume_chunking_prompt(text_)
    llm_gemini = llm_google()
    res1 = llm_gemini.invoke(msg)
    resume_info_meta = {  'personal_details': 'personal',
                    'education': 'education',
                    'work_experience:': 'work experience',
                    'skills': 'skills',
                    'projects': 'projects',
                    'certifications_awards_achievements': ['certifications' ,'awards','achievements'],
                    'publications_research': ['publications', 'research']}
    resume_info_actual = {}
    for i in res1.content.split('###'):
        meta_ = i.strip().split('\n')[0]
        find = "none"
        for info in resume_info_meta:
            if isinstance(resume_info_meta[info],List) :
                for key_meta in resume_info_meta[info]:
                    if key_meta in meta_.lower():
                        find = info
                        print(find)
                        break
                if find != "none":
                    break
            elif isinstance(resume_info_meta[info],str):
                key_meta = resume_info_meta[info]
                if key_meta in meta_.lower():
                    find = info
            if find != "none":
                break
        if find in resume_info_meta:
            resume_info_actual[find] = i.strip()

    with open(save_path, 'w') as f:
        json.dump(resume_info_actual, f)


def extract_info(file_path):
    result = {}
    with open(file_path, 'r') as f:
        resume_info = json.load(f)

    msg_input = work_experience_prompt.format(resume_content=resume_info['work_experience:']) + '\n' + resume_template_instructions
    llm_ollama = llm_ollama_model()
    res_ollama = llm_ollama.invoke(msg_input)
    print("Work experience LLM output received.")

    parser = JsonOutputParser(pydantic_object=WorkExperience)
    json_out = parser.invoke(res_ollama)
    result['work_experience'] = json_out

    msg_input = projects_prompt.format(resume_content=resume_info['projects']) + '\n' + resume_template_instructions
    res_ollama = llm_ollama.invoke(msg_input)
    print("Projects LLM output received.")

    parser = JsonOutputParser(pydantic_object=Project)
    json_out = parser.invoke(res_ollama)
    result['projects'] = json_out

    msg_input = skills_prompt.format(resume_content=resume_info['skills']) + '\n' + resume_template_instructions
    res_ollama = llm_ollama.invoke(msg_input)
    print("Skills LLM output received.")

    parser = JsonOutputParser(pydantic_object=ResumeSkills)
    json_out = parser.invoke(res_ollama)
    result['skills'] = json_out

    msg_input = education_prompt.format(resume_content=resume_info['education']) + '\n' + resume_template_instructions
    res_ollama = llm_ollama.invoke(msg_input)
    print("Education LLM output received.")

    parser = JsonOutputParser(pydantic_object=Education)
    json_out = parser.invoke(res_ollama)
    result['education'] = json_out

    msg_input = publications_prompt.format(resume_content=resume_info['publications_research'])  # + '\n' + resume_template_instructions
    res_ollama = llm_ollama.invoke(msg_input)
    print("Publications/Research LLM output received.")

    parser = JsonOutputParser(pydantic_object=Publication)
    json_out = parser.invoke(res_ollama)
    result['publications_research'] = json_out

    with open('data/resume_info.json', 'w') as f:
        json.dump(result, f)
    print("All extracted information has been saved to 'data/resume_info.json'.")
    return result

