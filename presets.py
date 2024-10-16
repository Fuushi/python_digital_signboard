from classes import *

class Presets:
    def homeV2(render):
        render.presetID="homeV2"
        debug=False
        render.scene=Scene()

        render.createElement(
            id="bg_video_player",
            element_type="video",
            source="assets/girlV2.mp4",
            size=(1280,720),
            position=(0,-300),
            zoffset=-0.5,
            verbose=False,
            interval=3,
            framesInMemory=100,
            scripts=[]
        )

        return
    
    def bangboo(render):
        render.presetID="bangboo"
        debug=False
        render.scene=Scene()

        ipd=400

        render.createElement(
            id="eye_left",
            element_type="svg",
            source="assets/circle.json",
            size=(870,0),
            position=(ipd,200),
            zoffset=4,
            scripts=[]
        )

        render.createElement(
            id="eye_right",
            element_type="svg",
            source="assets/circle.json",
            size=(870,0),
            position=(1280-ipd,200),
            zoffset=4,
            scripts=[]
        )



    def home(render):
        render.presetID="home"
        debug=False
        render.scene=Scene()

        render.createElement(
            id="bg_video_player",
            element_type="video",
            source="assets/scenery.mp4",
            size=(1280,720),
            position=(0,-100),
            zoffset=-0.5,
            verbose=False,
            interval=3,
            framesInMemory=100,
            scripts=[]
        )

        render.createElement(
            id="spotify_thumbnail",
            element_type="raster",
            source="assets/img.jpg",
            size=(300,300),
            position=(50,50),
            zoffset=1,
            crop=True,
            verbose=True,
            scripts=["pullDownV2"]
        )
        thumbnail=render.scene.getElement("spotify_thumbnail")
        thumbnail.renderBevel=True
        thumbnail.bevelRadius=50

        render.createElement(
            id="song_name",
            element_type="text",
            source="InvalidKey",
            size=(800,200),
            position=(380,80),
            text="CHECK_TEMPLATE",
            text_template="{song}",
            font="Arial",
            font_size=55,
            text_color=(255,255,255),
            scripts=["accessGlobals", "pullDownV2", "textScroll"],
            verbose=True
        )

        render.createElement(
            id="artist_name",
            element_type="text",
            source="InvalidKey",
            size=(800,200),
            position=(385,140),
            text="CHECK_TEMPLATE",
            text_template="{artist}",
            font="Arial",
            font_size=22,
            text_color=(255,255,255),
            scripts=["accessGlobals", "pullDownV2"],
            verbose=False
        )

        render.createElement(
            id="progress_clock",
            element_type="text",
            source="InvalidKey",
            size=(800,200),
            position=(385,210),
            text="CHECK_TEMPLATE",
            text_template="{progressStrfTime}",
            font="Arial",
            font_size=20,
            text_color=(255,255,255),
            scripts=["accessGlobals", "pullDownV2"],
            verbose=False
        )

        render.createElement(
            id="duration_clock",
            element_type="text",
            source="InvalidKey",
            size=(800,200),
            position=(1210,210),
            text="CHECK_TEMPLATE",
            text_template="{durationStrfTime}",
            font="Arial",
            font_size=20,
            text_color=(255,255,255),
            scripts=["accessGlobals", "pullDownV2"],
            verbose=False
        )

        render.createElement(
            id="clock",
            element_type="text",
            source="InvalidKey",
            position=(600,85-400),
            size=(100,100),
            text="CHECK_TEMPLATE",
            text_template="{clock}",
            font="Arial",
            font_size=200,
            text_color=(255,255,255),
            scripts=["accessGlobals", "pullDownV2", "centreDivX"],
            verbose=False
        )
        songName=render.scene.getElement("clock")
        songName.stateMachine.dropShadow=True

        render.createElement(
            element_type="svg",
            source="assets/progressBar.json",
            size=(870,0),
            position=(0,0),
            zoffset=4,
            scripts=["accessGlobals", "progressBar", "pullDownV2"]
        )



        #######################################################################
        #######################################################################
        #######################################################################
        #######################################################################
 

    def debug(render):
        render.presetID="debug"
        render.scene=Scene()
        render.createElement(
            element_type="raster",
            source="assets/img.JPG",
            size=(100,100),
            position=(400,100),
            zoffset=2,
            scripts=["sinWobble"]
        )

        render.createElement(
            element_type="raster",
            source="assets/shitman.jpg",
            size=(100,100),
            position=(400,250),
            zoffset=2,
            scripts=["parallaxX", "parallaxY", "mouseHoverFlag", "expand", "onClickFlag"]
        )

        render.createElement(
            element_type="svg",
            source="assets/divider.json",
            size=(800,800),
            position=(0,0),
            zoffset=4,
            scripts=["vertexWobble"]
        )

        render.createElement(
            element_type="text",
            source="InvalidKey",
            size=(700,100),
            position=(1,-1),
            zoffset=3,
            text="CHECK_TEMPLATE",
            text_template="{f}",
            font="Arial",
            font_size=10,
            text_color=(150,150,150),
            scripts=["accessGlobals"],
            verbose=False
        )
        return

    def lowPowerMode(render):
        render.presetID="lowPowerMode"
        render.scene=Scene()


        
        #fill white
        fill=render.createElement(
            id="low_power_bg",
            element_type="svg",
            source="assets/square.json",
            size=(800,800),
            position=(0,0),
            zoffset=4,
            scripts=[]
        )
        #fill.assets['assets/square.json']['polys'][0]['color']=c1

        #clock module
        render.createElement(
            id="clock",
            element_type="text",
            source="InvalidKey",
            position=(600,90),
            size=(100,100),
            text="CHECK_TEMPLATE",
            text_template="{clock}",
            font="Arial",
            font_size=200,
            text_color=(0,0,0),
            scripts=["accessGlobals", "centreDivX"],
            verbose=True
        )


        #TODO display anti-burnin noise (legacy)
        """noise = render.createElement(
            id="noise_element",
            element_type="svg",
            source="assets/square.json",
            size=(800,800),
            position=(0,0),
            zoffset=4,
            scripts=[]
        )"""


        songName=render.scene.getElement("clock")#??
        return
            
    def empty(render):
        render.presetID="empty"
        render.scene=Scene()
        return



    