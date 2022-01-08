

from ursina import Entity,color,floor


lookBlock=Entity(model='cube',color=color.rgba(1,1,0,0.4))
lookBlock.scale*=1.001

def higlight(pos,cam,td):
    for i in range(1,15):
        wp=pos+cam.forward*i
        x=floor(wp.x)
        y=floor(wp.y+3)
        z=floor(wp.z)
        lookBlock.x=x
        lookBlock.y=y+0.5
        lookBlock.z=z

        if td.get((x,y,z))=='t':
            lookBlock.visible=True
            break
        else:
            lookBlock.visible=False