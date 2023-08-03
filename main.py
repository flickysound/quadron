import discord
import os
import googleapiclient.discovery
#from discord.ext import commands
from googleapiclient.errors import HttpError
import json

intents = discord.Intents(messages=True, guilds=True)
client = discord.Client(intents=intents)

# Set up the API key and YouTube API service
API_KEY = os.getenv("YOUTUBE_API_KEY")
api_service_name = "youtube"
api_version = "v3"

# Load the discovery document
discovery_document = {
  "kind": "discovery#restDescription",
  "discoveryVersion": "v1",
  "id": "youtube:v3",
  "name": "youtube",
  "version": "v3",
  "title": "YouTube Data API v3",
  "description": "Retrieves and manages YouTube resources",
  "icons": {
    "x16":
    "http://www.gstatic.com/images/branding/product/1x/youtube_16dp.png",
    "x32": "http://www.gstatic.com/images/branding/product/1x/youtube_32dp.png"
  },
  "documentationLink": "https://developers.google.com/youtube/",
  "protocol": "rest",
  "baseUrl": "https://www.googleapis.com/youtube/v3/",
  "basePath": "/youtube/v3/",
  "rootUrl": "https://www.googleapis.com/",
  "servicePath": "youtube/v3/",
  "batchPath": "batch/youtube/v3",
  "resources": {
    "channels": {
      "methods": {
        "list": {
          "id": "youtube.channels.list",
          "path": "channels",
          "httpMethod": "GET",
          "parameters": {
            "part": {
              "type": "string",
              "description":
              "The `part` parameter specifies a comma-separated list of one or more channel resource properties that the API response will include.",
              "location": "query"
            },
            "id": {
              "type": "string",
              "description":
              "The `id` parameter specifies a comma-separated list of the YouTube channel ID(s) for the resource(s) that are being retrieved. In a `channel` resource, the `id` property specifies the channel's YouTube channel ID.",
              "location": "query"
            }
          }
        }
      }
    }
  }
}

# Build the YouTube API service
youtube = googleapiclient.discovery.build_from_document(discovery_document,
                                                        developerKey=API_KEY)


def get_subscriber_count(channel_id):
  try:
    # Call the YouTube API to retrieve channel details
    response = youtube.channels().list(part='statistics',
                                       id=channel_id).execute()

    # Decode the response content to string
    response_content = response.decode("utf-8")

    # Parse the response as JSON
    response_json = json.loads(response_content)

    # Extract the subscriber count from the response
    if 'items' in response_json:
      items = response_json['items']
      if len(items) > 0:
        subscriber_count = int(items[0]['statistics']['subscriberCount'])
        return subscriber_count

    # If the response does not contain the subscriber count, return None
    return None

  except HttpError as e:
    print(f'An HTTP error {e.resp.status} occurred: {e.content}')


# Provide the channel ID for which you want to check the subscriber count
channel_id = "UCv9GI55IkfL_eEOUq9hXbDQ"

# Call the function to get the subscriber count
count = get_subscriber_count(channel_id)

# Print the result
if count is not None:
  print(f'Quadron has {count} subscribers.')
else:
  print('Unable to fetch the subscriber count.')


@client.event
async def on_ready():
  print('We have inloggen in as {0.user}'.format(client))

  # Provide the voice channel ID to update
  channel_id = 930838385000603748

  # Fetch the voice channel by its ID
  voice_channel = client.get_channel(channel_id)

  if voice_channel is not None and isinstance(voice_channel,
                                              discord.VoiceChannel):
    # Update the voice channel's name
    new_name = f'{count} Subscribers'
    await voice_channel.edit(name=new_name)
    print(
      f'Voice channel "{voice_channel.name}" has been renamed to "{new_name}"')
  else:
    print(
      f'Voice channel with ID "{channel_id}" not found or is not a voice channel'
    )


client.run(os.getenv('TOKEN'))