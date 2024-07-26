import spacy

nlp = spacy.load('en_core_web_sm')

sample_txt = nlp('Recently started a course of counselling with the Employee Assistance Programme, they were excellent. I had a detailed consultant call to establish what I needed and how urgently. Incredible safe guarding on any immediate support that might have been required. On the same day, I had a call from the counsellor to book my first session, these are via Zoom or telephone with appointments weekdays, evenings or weekends. Could not have been easier and the sessions so far have been super helpful.')

def keyword_chunks(sample):
    spacy_doc = nlp(sample)

    keywords = []

    # Extracting keyphrases 
    for chunk in spacy_doc.noun_chunks: 
        if chunk.text.lower() not in nlp.Defaults.stop_words: 
            keywords.append(chunk.text)

    return keywords
  

if __name__ == '__main__':
    
    # Displaying the keywords 
    print(keyword_chunks(sample_txt))



