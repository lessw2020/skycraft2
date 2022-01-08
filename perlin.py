from perlin_module import PerlinNoise
class Perlin:
    def __init__(self) -> None:
        self.seed=9989
        self.octaves=3
        self.freq=64
        self.amp=12
        
        
        self.pNoise=PerlinNoise(seed=self.seed,octaves=self.octaves)

    def getHeight(self,x,z):
        y=0
        y=self.pNoise([x/self.freq,z/self.freq])*self.amp
        return y

        