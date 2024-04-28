import subprocess
import requests

from langchain.document_loaders import YoutubeLoader
from modules.mongodb import get_all_transcripts

from dotenv import find_dotenv, load_dotenv
import os
from openai import OpenAI
load_dotenv(find_dotenv())
api_key  = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
youtube_api_key= os.getenv("YOUTUBE_API_KEY")

from googleapiclient.discovery import build


def get_video_links(channel_url):
     # Replace with your YouTube Data API key
    youtube = build('youtube', 'v3', developerKey=youtube_api_key)
    
    # Extract channel ID from URL
    channel_id = extract_channel_id(channel_url)
    if channel_id:
        # Fetch videos from channel
        request = youtube.search().list(
            part='snippet',
            channelId=channel_id,
            maxResults=5
        )
        response = request.execute()
        # Extract video URLs from response
        video_urls = []
        for item in response['items']:
            if item['id']['kind'] == 'youtube#video':
                video_urls.append(f"https://www.youtube.com/watch?v={item['id']['videoId']}")
        
        return video_urls
    else:
        print("Invalid channel URL")
        return []

def extract_channel_id(channel_url):
    
    try:
        youtube = build('youtube', 'v3', developerKey=youtube_api_key)
        # Extract the username from the URL

        username = channel_url.split('/')[-1]

        # Make a request to the YouTube API to search for channels with the given username
        request = youtube.search().list(part='id',q=username, type='channel')
        response = request.execute()

        # Extract the channel ID from the search results
        channel_id = response['items'][0]['id']['channelId']
        return channel_id
    
    except requests.exceptions.RequestException as e:
        print("Error occurred while making the request:", e)
        return None

# def make_transcript(urls):
    
#     # Directory to save audio files
#     save_dir = "./YouTube"

#     loader = GenericLoader(YoutubeAudioLoader(urls, save_dir), OpenAIWhisperParser())
#     docs = loader.load()
#     combined_docs = [doc.page_content for doc in docs]
#     text = " ".join(combined_docs)

#     return text


def make_transcript(urls):
    try:
        loader = YoutubeLoader.from_youtube_url(urls, add_video_info=True)
        docs = loader.load()
        combined_docs = [doc.page_content for doc in docs]
        text = " ".join(combined_docs)
        return text
    except Exception as e:
        print(f"Error making transcript: {e}")
        return False


def get_all_transcript(user_id,channel_id):
    """Get all transcripts of videos from the target youtube channel"""
    transcripts = get_all_transcripts(user_id,channel_id)
    return transcripts