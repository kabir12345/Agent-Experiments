import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import random
import os
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
from langchain_community.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from typing import Optional, Type
import agentops
from agentops import track_agent
from agentops import record_function
from agentops.langchain_callback_handler import LangchainCallbackHandler as AgentOpsLangchainCallbackHandler
from dotenv import load_dotenv
load_dotenv()



agent_ops_keys=os.environ['AGENT_OPS_KEY']
agentops_handler = AgentOpsLangchainCallbackHandler(api_key=agent_ops_keys, tags=['Music Agent'])

client_id = os.environ['Spotify_Client']

client_secret = os.environ['Spotify_Secret']


sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=client_id,
                                                                             client_secret=client_secret))

class MusicInput(BaseModel):
    artists: list = Field(description="A list of artists that they'd like to see music from")
    tracks: int = Field(description="The number of tracks/songs they want returned.")

class SpotifyTool(BaseTool):
    
    name = "Spotify Music Recommender"
    description = "Use this tool when asked music recommendations."
    args_schema: Type[BaseModel] = MusicInput
    
    # utils
    @staticmethod
    def retrieve_id(artist_name: str) -> str:
        results = sp.search(q='artist:' + artist_name, type='artist')
        if len(results) > 0:
            artist_id = results['artists']['items'][0]['id']
        else:
            raise ValueError(f"No artists found with this name: {artist_name}")
        return artist_id

    @staticmethod
    def retrieve_tracks(artist_id: str, num_tracks: int) -> list:
        if num_tracks > 10:
            raise ValueError("Can only provide up to 10 tracks per artist")
        tracks = []
        top_tracks = sp.artist_top_tracks(artist_id)
        for track in top_tracks['tracks'][:num_tracks]:
            tracks.append(track['name'])
        return tracks

    @staticmethod
    def all_top_tracks(artist_array: list) -> list:
        complete_track_arr = []
        for artist in artist_array:
            artist_id = SpotifyTool.retrieve_id(artist)
            all_tracks = {artist: SpotifyTool.retrieve_tracks(artist_id, 10)}
            complete_track_arr.append(all_tracks)
        return complete_track_arr


    def _run(self, artists: list, tracks: int) -> list:
        """
        A tool to provide music recommendations based on artists provided.
        """
        num_artists = len(artists)
        max_tracks = num_artists * 10
        print("---------------")
        print(artists)
        print(type(artists))
        print("---------------")
        all_tracks_map = SpotifyTool.all_top_tracks(artists) # map for artists with top 10 tracks
        all_tracks = [track for artist_map in all_tracks_map for artist, tracks in artist_map.items() for track in tracks] #complete list of tracks

        if tracks > max_tracks:
            raise ValueError(f"Only 10 tracks per artist, max tracks for this many artists is: {max_tracks}")
        final_tracks = random.sample(all_tracks, tracks)
        return final_tracks

    def _arun(self):
        raise NotImplementedError("Spotify Music Recommender does not support ")
        
tools = [SpotifyTool()]
llm = ChatOpenAI(temperature=0.0,callbacks=[agentops_handler])
for t in tools:
    t.callbacks = [agentops_handler]

# @track_agent(name='MusicAgent')
# class MyAgent:
#     def __init__(self):
#         self.agent = initialize_agent(tools, llm, agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose = True,callbacks=[agentops_handler],handle_parsing_errors=True)
#         return self.agent
#     # def run(self, query,callbacks):
#     #     return self.agent.run(query)
# agent_new = MyAgent()

# agent_new.run("""I like the following artists:  [Future]
#                 can I get 6 song recommendations with them in it.""" , callbacks=[agentops_handler])
agent = initialize_agent(tools,
                         llm,
                         agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
                         verbose=True,
                         callbacks=[agentops_handler], # You must pass in a callback handler to record your agent
                         handle_parsing_errors=True)
agent.run("""I like the following artists:  [Future]
#                 can I get 6 song recommendations with them in it.""" , callbacks=[agentops_handler])


agentops.end_session('Success')