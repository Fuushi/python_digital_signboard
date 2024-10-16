#Just for Intellisense, remove in Live
from classes import *
from render import *
from imgLib import stringManupulation
import os, sys, time, json
import Keys
keys=Keys.Keys()


class behavior:
    def __init__(self, state, render) -> None:
        import spotipy
        from spotipy.oauth2 import SpotifyClientCredentials
        from spotipy.oauth2 import SpotifyOAuth
        import spotipy.util as util

        self.interval=1

        self._scopes='user-top-read user-read-playback-state user-modify-playback-state user-read-currently-playing playlist-read-private playlist-read-collaborative user-follow-read user-read-recently-played user-read-playback-position user-library-read'

        try:
            username = "minejjchase"
            token = util.prompt_for_user_token(username,scope = self._scopes,client_id=keys.sp_client_id,client_secret=keys.sp_client_secret,redirect_uri='http://localhost:3002', cache_path="cache/spotifycache.txt")
            if token: self._sp = spotipy.Spotify(auth=token)

        except Exception as error:
            print(f"SPOTIFY: ERROR! FAILED TO OBTAIN TOKEN WITH CODE {error}")
            time.sleep(10)
            return()
        
        print("Connected to spotify.")
        
        pb=self._sp.current_playback()
        
        self.url=None
        self.thumbnail=None
        self.songName=None
        self.artistName=None
        self.progressClock=None
        self.durationClock=None
        self.presetID = "home"

        #get first instance of scope variables
        while (not self.thumbnail) or (not self.songName) or (not self.artistName) or (not self.progressClock) or (not self.durationClock):
            self.thumbnail=render.scene.getElement("spotify_thumbnail")
            self.songName=render.scene.getElement("song_name")
            self.artistName=render.scene.getElement("artist_name")
            self.progressClock=render.scene.getElement("progress_clock")
            self.durationClock=render.scene.getElement("duration_clock")

        time.sleep(3)

        return
    
    def run(self, state, render): 
        import spotipy
        from spotipy.oauth2 import SpotifyClientCredentials
        from spotipy.oauth2 import SpotifyOAuth
        import spotipy.util as util
        #get playback
        

        #handle internal refs
        if (render.presetID != self.presetID):
            resetInternalReferences(self, render)
            self.presetID=render.presetID

        #if not applicable preset, return (save resources when not needed)
        runOnPresets=["home"]
        if not render.presetID in runOnPresets:
            self.interval=8
            return
        else:
            self.interval=1

        try: pb = self._sp.current_playback()
        

        #if get fails, regenerate token
        except:
            username = "minejjchase"
            token = util.prompt_for_user_token(username,scope = self._scopes,client_id=keys.sp_client_id,client_secret=keys.sp_client_secret,redirect_uri='http://localhost:3002', cache_path="cache/spotifycache.txt")
            if token: self._sp = spotipy.Spotify(auth=token)

            #try again on next iteration, (return)
            return 


        pbState=PlaybackHandler.detectPlaybackMode(pb)

        #if playback is defined (music is playing)
        if pbState=="track":
            #MUSIC PLAYING

            #parse information from sources and pass
            try:
                url=pb['item']['album']["images"][0]["url"]
                self.thumbnail.updateSourceRaster(url)
                render.globals['song'] = pb['item']['name']
                render.globals['progress']=(pb['progress_ms'], pb['item']['duration_ms'])
                render.globals["progressStrfTime"]=stringManupulation.strfTime(pb['progress_ms'])
                render.globals["durationStrfTime"]=stringManupulation.strfTime(pb['item']['duration_ms'])
                #compile artist names (string manipulation)
                render.globals['artist'] = stringManupulation.compileNames(pb)

                #set flags
                if not render.playing: 
                    setFlags(render, [self.thumbnail, self.songName, self.artistName, self.progressClock, self.durationClock], True)
            except:
                print("An unknown unpacking error has occured...")
        elif pbState=="episode":
            #treated as nothing playing, not supported
            if render.playing: setFlags(render, [self.thumbnail, self.songName, self.artistName, self.progressClock, self.durationClock], False)


        else:
            #NOTHING PLAYING

            #set flags
            if render.playing: setFlags(render, [self.thumbnail, self.songName, self.artistName, self.progressClock, self.durationClock], False)
        return
    
#sets flags for render, and n elements
def setFlags(render, elements:list, status:bool):
    render.playing=status
    for element in elements:
        element.flag=True
        element.flashTrigger=True

class PlaybackHandler:
    def detectPlaybackMode(pb):
        if not pb:
            return "NoPlayback"
        
        return pb['currently_playing_type']
    
def resetInternalReferences(self, render) -> None:
    print("RESETTING INTERNAL REFS")

    #get first instance of scope variables
    time.sleep(5)#>... may need increase
    try:
        self.thumbnail=render.scene.getElement("spotify_thumbnail")
        self.songName=render.scene.getElement("song_name")
        self.artistName=render.scene.getElement("artist_name")
        self.progressClock=render.scene.getElement("progress_clock")
        self.durationClock=render.scene.getElement("duration_clock")
    except:
        pass
    return 