from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd

in_videos_path = "/home/anvay/COEP/sem6/DSci/project/trending_videos/USvideos.csv"

in_df = pd.read_csv(in_videos_path)

print(in_df.columns)

documents = {}

i = 0
for vid in in_df['video_id']:
    print(vid)
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(vid)
        transcript_text = ' '.join([item['text'] for item in transcript_list])
        documents[i] = transcript_text

        i = i + 1
        if i > 4:
            break
    except:
        print("Subtitles are turned off")
    print("")

for item in documents:
    print(documents[item])
    print("")
    

