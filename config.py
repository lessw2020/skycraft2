# central location for all global type settings

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

g_sixAxis = [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1),]



