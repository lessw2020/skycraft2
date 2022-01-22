from perlin import Perlin
from ursina import *
from random import random
from swirl_engine import SwirlEngine
from mining_system import *
from building_system import *

# This is the block texture atlas made faster :)

textureMap = [
              ('soil', 10, 7),
              ('grass', 8, 7),
              ('stone', 8, 5),
              ('ice', 9,7),
              ('snow', 8,6),
]

#load blockStyles
g_blockStyles = {}
for name, uu, uv in textureMap:
  g_blockStyles[name] = (uu, uv)

print(f"--> Loaded:  block styles = {g_blockStyles}")

g_snowHeight = 2  # control height where snow begins...



class MeshTerrain:
    def __init__(this):
        
        this.block = load_model('block.obj')
        this.textureAtlas = 'texture_atlas_3.png'
        this.numVertices = len(this.block.vertices)

        this.subsets = []
        this.numSubsets = 1024
        
        # Must be even number! See genTerrain()
        this.subWidth = 6 
        this.swirlEngine = SwirlEngine(this.subWidth)
        this.currentSubset = 0

        # Our terrain dictionary :D
        this.td = {}

        # Our vertex dictionary -- for mining.
        this.vd = {}

        this.perlin = Perlin()

        for i in range(0,this.numSubsets):
            e = Entity( model=Mesh(),
                        texture=this.textureAtlas)
            e.texture_scale*=64/e.texture.width
            this.subsets.append(e)

    def do_mining(this):
        epi = mine(this.td,this.vd,this.subsets)
        if epi != None:
            this.genWalls(epi[0],epi[1])
            this.subsets[epi[1]].model.generate()

    # Highlight looked-at block :)
    def update(this,pos,cam):
        highlight(pos,cam,this.td)
        # Blister-mining!
        if bte.visible==True:
            for key, value in held_keys.items():
                if key=='left mouse' and value==1:
                    this.do_mining()

    
    def input(this,key):
        if key=='left mouse up' and bte.visible==True:
            this.do_mining()
        # Building :)
        if key=='right mouse up' and bte.visible==True:
            bsite = checkBuild(bte.position,this.td)
            if bsite!=None:
                this.genBlock(floor(bsite.x),floor(bsite.y),floor(bsite.z),subset=0,blockType='grass')
                gapShell(this.td,bsite)
                this.subsets[0].model.generate()
    
    # I.e. after mining, to create illusion of depth.
    def genWalls(this,epi,subset):
        if epi==None: return
        # Refactor this -- place in mining_system 
        # except for cal to genBlock?
        wp =    [   Vec3(0,1,0),
                    Vec3(0,-1,0),
                    Vec3(-1,0,0),
                    Vec3(1,0,0),
                    Vec3(0,0,-1),
                    Vec3(0,0,1)]
        for i in range(0,6):
            np = epi + wp[i]
            if this.td.get( (floor(np.x),
                            floor(np.y),
                            floor(np.z)))==None:
                this.genBlock(np.x,np.y,np.z,subset,gap=False,blockType='soil')


    def genBlock(this,x,y,z,subset=-1,gap=True,blockType='grass'):
        if subset==-1: subset=this.currentSubset
        # Extend or add to the vertices of our model.
        model = this.subsets[subset].model

        model.vertices.extend([ Vec3(x,y,z) + v for v in 
                                this.block.vertices])
        # Record terrain in dictionary :)
        this.td[(floor(x),floor(y),floor(z))] = 't'
        # Also, record gap above this position to
        # correct for spawning walls after mining.
        if gap==True:
            key=((floor(x),floor(y+1),floor(z)))
            if this.td.get(key)==None:
                this.td[key]='g'

        # Record subset index and first vertex of this block.
        vob = (subset, len(model.vertices)-37)
        this.vd[(floor(x),
                floor(y),
                floor(z))] = vob

        # Decide random tint for colour of block :)
        c = random()-0.5
        model.colors.extend( (Vec4(1-c,1-c,1-c,1),)*
                                this.numVertices)

        # get texture mapping for block style (with randomization and env input)
        uu, uv = self.getTexture(blockType)

        if uu is not None:
          model.uvs.extend([Vec2(uu,uv) + u for u in this.block.uvs])


    def getTexture(self, blockType):
      """ determine block style for current block based on block type and environment """

      # If high enough, cap with snow blocks :D
        if y > g_snowHeight:
           uu, uv = g_blockStyles.get('snow', (None, None))

        # else randomly insert stone blocks
        elif random() > 0.86:
          uu, uv = g_blockStyles.get('stone', (None, None))
        
        # else load requested block style
        else:
          # get block texture based on block type...return None if not available
          uu, uv = g_blockStyles.get(blockType, (None, None))
        
        return uu, uv
    

    def genTerrain(this):
        # Get current position as we swirl around world.
        x = floor(this.swirlEngine.pos.x)
        z = floor(this.swirlEngine.pos.y)

        d = int(this.subWidth*0.5)

        for k in range(-d,d):
            for j in range(-d,d):

                y = floor(this.perlin.getHeight(x+k,z+j))
                if this.td.get( (floor(x+k),
                                floor(y),
                                floor(z+j)))==None:
                    this.genBlock(x+k,y,z+j,blockType='grass')

        this.subsets[this.currentSubset].model.generate()
        # Current subset hack ;)
        if this.currentSubset<this.numSubsets-1:
            this.currentSubset+=1
        else: this.currentSubset=0
        this.swirlEngine.move()
