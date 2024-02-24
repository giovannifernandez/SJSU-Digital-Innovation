# Uninstall Colab's preinstalled modules which have dependency conflicts with
# the OpenAI Python library.
!pip uninstall tensorflow-probability -y
!pip uninstall llmx -y
# Install the OpenAI Python library.
!pip install --upgrade openai

from openai import OpenAI
client = OpenAI(api_key='your-api-key-here')

# Given the path to an audio file, transcribes the audio using Whisper.
def transcribe_audio(audio_file_path):
    audio_file = open(audio_file_path, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )
    return transcription.text

# Takes the transcription of the meeting and returns a summary of it via text completions
def abstract_summary_extraction(transcription):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "You are a highly skilled AI trained in language comprehension and summarization. I would like you to read the following text and summarize it into a concise abstract paragraph. Aim to retain the most important points, providing a coherent and readable summary that could help a person understand the main points of the discussion without needing to read the entire text. Please avoid unnecessary details or tangential points."
            },
            {
                "role": "user",
                "content": transcription
            }
        ]
    )
    return response.choices[0].message.content

# Takes the transcription of the meeting and returns the key points in it via text completions
def key_points_extraction(transcription):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "You are a proficient AI with a specialty in distilling information into key points. Based on the following text, identify and list the main points that were discussed or brought up. These should be the most important ideas, findings, or topics that are crucial to the essence of the discussion. Your goal is to provide a list that someone could read to quickly understand what was talked about."
            },
            {
                "role": "user",
                "content": transcription
            }
        ]
    )
    return response.choices[0].message.content

# Takes the transcription of the meeting and returns the action items from it via text completions
def action_item_extraction(transcription):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "You are an AI expert in analyzing conversations and extracting action items. Please review the text and identify any tasks, assignments, or actions that were agreed upon or mentioned as needing to be done. These could be tasks assigned to specific individuals, or general actions that the group has decided to take. Please list these action items clearly and concisely."
            },
            {
                "role": "user",
                "content": transcription
            }
        ]
    )
    return response.choices[0].message.content

# Takes the transcription of the meeting and returns the sentiment of it via text completions
def sentiment_analysis(transcription):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "As an AI with expertise in language and emotion analysis, your task is to analyze the sentiment of the following text. Please consider the overall tone of the discussion, the emotion conveyed by the language used, and the context in which words and phrases are used. Indicate whether the sentiment is generally positive, negative, or neutral, and provide brief explanations for your analysis where possible. Please keep it to fewer than 5 sentences."
            },
            {
                "role": "user",
                "content": transcription
            }
        ]
    )
    return response.choices[0].message.content

# Taken directly from OpenAI's documentation for a meeting minutes generator.
def meeting_minutes(transcription):
    abstract_summary = abstract_summary_extraction(transcription)
    key_points = key_points_extraction(transcription) 
    action_items = action_item_extraction(transcription)
    sentiment = sentiment_analysis(transcription)
    return {
        'abstract_summary': abstract_summary,
        'key_points': key_points,
        'action_items': action_items,
        'sentiment': sentiment
    }

# Saves a string to a txt file.
def makeTxt(filename, string):
    file = open(filename, "w")
    file.write(string)
    file.close()

audio_file_path = input("Enter the path to an audio file with size <25MB: ")
transcription = transcribe_audio(audio_file_path)
minutes = meeting_minutes(transcription)

minutes_filename = "minutes/" + audio_file_path.split("/")[-1].split(".")[0] + ".txt"
title = "MEETING MINUTES for " + audio_file_path.split("/")[-1].split(".")[0] + "\n\n"

abstract_summary = "ABSTRACT SUMMARY\n" + minutes["abstract_summary"] + "\n\n"
key_points = "KEY POINTS\n" + minutes["key_points"] + "\n\n"
action_items = "ACTION ITEMS\n" + minutes["action_items"] + "\n\n"
sentiment = "SENTIMENT\n" + minutes["sentiment"] + "\n\n"

#makeTxt(minutes_filename, title + abstract_summary + key_points + action_items + sentiment)

print("----------------------------------------------")
print(title + abstract_summary + key_points + action_items + sentiment)

# Feedback message
print("----------------------------------------------")
print("Meeting minutes saved to", minutes_filename + "!")
