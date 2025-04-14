from resume_extract.resume_reader import read_resume
from resume_extract.main import chunk_resume , extract_info


read_resume(["data/kr.pdf"])


chunk_resume("scratch/kr.md", "data/kr.json")

res = extract_info('data1/mr.json')

print(res)

