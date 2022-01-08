from random import *
from ursina import *
from perlin import Perlin
from perlin_module import PerlinNoise
from infiniteTerrain import swirlEngine
from break_blocks import *

class Meshterrain:
    def __init__(self):
        
        self.subsets=[]
        self.numSubsets=128

        self.subWidth=4
        self.Swirl=swirlEngine(self.subWidth)
        self.currentSubset=0
        self.block=load_model('block.obj')
        self.numVertices=len(self.block.vertices)
        

        self.textureAtlas='texture_atlas_3.png'
        self.td={}
        self.vd={}

        self.perlin=Perlin()
        for i in range(0,self.numSubsets):
            e=Entity(model=Mesh(),
            texture=self.textureAtlas)
            e.texture_scale*=64/e.texture.width

            self.subsets.append(e)
    def update(self, pos,cam):
        higlight(pos,cam,self.td)
    def genBlock(self,x,y,z,subset =-1):
        if subset==-1:
            subset=self.currentSubset
        
        model=self.subsets[subset].model
        model.vertices.extend([Vec3(x,y,z)+v for v in self.block.vertices])
        
        c=random.random()-0.5

        model.colors.extend((Vec4(1-c,1-c,1-c,1),)*self.numVertices)
        uu=8
        uv=7
        if y > 2:
            uu=8
            uv=6
        model.uvs.extend([Vec2(uu,uv)+u for u in self.block.uvs])
        self.td[(floor(x),
                floor(y),
                floor(z)
                )] ='t'
        vob=(subset,len(model.vertices)-37)
        self.vd[(floor(x),
                floor(y),
                floor(z)
                )] = vob
        


    def genTerrain(self):
        x = floor(self.Swirl.pos.x)
        z = floor(self.Swirl.pos.y)
        d = self.subWidth//2
        for k in range(-d,d):
            for j in range(-d,d):
                y=floor(self.perlin.getHeight(x+k,z+j))
                if self.td.get((floor(x+k),floor(y),floor(z+j))) !='t':
                    self.genBlock(x+k,y,z+j)
        self.subsets[self.currentSubset].model.generate()
        if self.currentSubset<self.numSubsets-1:
            self.currentSubset+=1
        else:
            self.currentSubset=0
        self.Swirl.move()