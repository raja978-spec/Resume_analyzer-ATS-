import pandas as pd
import docx2txt
import pdfplumber
import os
import numpy as np
import re
def read_doc_resume(file):
    text_in_resume = docx2txt.process(file)
    return text_in_resume

def read_pdf_resume(file):
    text_in_resume = ''
    with pdfplumber.open(file) as text:
         for page in text.pages:
              text_in_resume = text_in_resume + page.extract_text()
    return text_in_resume

def extract_skills(text):
    skillsetregex = r'python|machine\s*learning|recommendation\s*system|pytorch'
    return list(set(re.findall(skillsetregex, text.lower())))

def score(skill_list):
    score = {
        'python':2,
        'machine learning':3,
        'pytorch':2,
        'recommendation system':2
    }
    score_for_skills = [score[skill] for skill in skill_list]
    return sum(score_for_skills)

def form_df_from_extracted_data(with_columns=[]):
    path_to_the_dataset = './dataset'
    df = pd.DataFrame(columns=with_columns)
    for file in os.listdir(path_to_the_dataset):
        applicant_name_and_extension = file.split('.')
        applicant_file_name = applicant_name_and_extension[0]
        extension = applicant_name_and_extension[1] 
        text = ''
        skillsets = []
        is_pdf_file = extension == 'pdf'
        is_docx_file = extension == 'docx'
        resume = os.path.join(path_to_the_dataset,file)
        try:
            if(is_pdf_file):
                text = read_pdf_resume(resume)
            if(is_docx_file):
                text = read_doc_resume(resume)
        except Exception as e:
           print(e)
           text = np.nan
        finally:
            skillsets = extract_skills(text)
            score_for_skills = score(skillsets)
            df.loc[len(df)]=[applicant_file_name, text, skillsets, score_for_skills]
    return df

df = form_df_from_extracted_data(with_columns=['filename','text','skillset','score'])
top_five_score = df.sort_values(by=['score'], ascending=False).head(5)[['filename', 'score']]
highest_score = df[df['score'] == df['score'].max()][['filename', 'score']]
print(top_five_score)
print()
print(highest_score)