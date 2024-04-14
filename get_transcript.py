import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from gensim import corpora
from gensim.models import LdaModel
from gensim.models import CoherenceModel
import string

# Preprocessing
def preprocess_text(text):
    tokens = word_tokenize(text)
    tokens = [token.lower() for token in tokens]
    tokens = [token for token in tokens if token not in string.punctuation]

    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]

    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]

    preprocessed_text = ' '.join(tokens)
    return tokens

if __name__ == '__main__':
    in_videos_path = "C:/Users/jorve/Desktop/SEM-6/DSci/youtube_search_engine/trending_videos/USvideos.csv"
    in_df = pd.read_csv(in_videos_path)

    # Extracting transcripts and preprocessing 
    documents = []
    i = 0
    for vid in in_df['video_id']:
        print(vid)
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(vid)
            transcript_text = ' '.join([item['text'] for item in transcript_list])
            preprocessed_text = preprocess_text(transcript_text)
            documents.append(preprocessed_text)

            i = i + 1
            # if i > 10:
            #     break
        except:
            print("Subtitles are turned off")
        print("")

    # Create dictionary and corpus
    dictionary = corpora.Dictionary(documents)
    corpus = [dictionary.doc2bow(doc) for doc in documents]

    # Train LDA model
    lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=5, passes=10)

    print("Topics:")
    for idx, topic in lda_model.print_topics():
        print(f"Topic {idx}: {topic}")

    # Compute coherence score
    coherence_model = CoherenceModel(model=lda_model, texts=documents, dictionary=dictionary, coherence='c_v')
    coherence_score = coherence_model.get_coherence()
    print(f"Coherence Score: {coherence_score}")
