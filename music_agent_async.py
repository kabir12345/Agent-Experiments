import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import random
import asyncio
import agentops
from dotenv import load_dotenv
from langchain import hub
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_structured_chat_agent
from agentops import init, end_session
from agentops.langchain_callback_handler import AsyncLangchainCallbackHandler as AgentOpsAsyncLangchainCallbackHandler

# Load environment variables
load_dotenv()

# Spotify API credentials
client_id = os.environ['Spotify_Client']
client_secret = os.environ['Spotify_Secret']

# AgentOps API Key
agent_ops_keys=os.environ['AGENT_OPS_KEY']

# Initialize the Spotify client
spotify_client = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

# Retrieve artist ID from Spotify
def retrieve_artist_id(artist_name: str) -> str:
    """Retrieve the Spotify ID of an artist given their name."""
    results = spotify_client.search(q='artist:' + artist_name, type='artist')
    items = results['artists']['items']
    if not items:
        raise ValueError(f"No artist found with name {artist_name}")
    return items[0]['id']

# Retrieve tracks from Spotify
def retrieve_tracks(artist_id: str, num_tracks: int) -> list:
    """Retrieve the top tracks of an artist given their Spotify ID."""
    top_tracks = spotify_client.artist_top_tracks(artist_id)
    return [track['name'] for track in top_tracks['tracks'][:num_tracks]]

# Decorate the main function as a LangChain tool
@tool
def get_music_recommendations(artists: list, tracks: int) -> list:
    """Asynchronously get music recommendations based on a list of artists and the number of tracks requested."""
    final_tracks = []
    for artist in artists:
        artist_id = retrieve_artist_id(artist)
        artist_tracks = retrieve_tracks(artist_id, min(tracks, 10))
        final_tracks.extend(artist_tracks)
    random.shuffle(final_tracks)
    return final_tracks


agentops_handler = AgentOpsAsyncLangchainCallbackHandler(api_key=agent_ops_keys, tags=[' New Music Agent Async'])
agentops.init(api_key=agent_ops_keys)

# Initialize LLM with OpenAI's API
llm = ChatOpenAI(temperature=0.0, callbacks=[agentops_handler])
tools = [get_music_recommendations]

# Pull the prompt from LangChain hub
prompt = hub.pull("hwchase17/structured-chat-agent")

# Create the agent with LangChain using the pulled prompt
agent = create_structured_chat_agent(llm, tools, prompt)

# Create the executor with AgentOps tracking
executor = AgentExecutor(agent=agent, tools=tools, verbose=True, callbacks=[agentops_handler])

# Asynchronous function to invoke the agent

input_data = {"input": "I like the following artists: Drake, Future. Can I get 5 song recommendations?"}
response = executor.invoke(input_data)
print(response)



# End the AgentOps session
agentops.end_session('Success')
