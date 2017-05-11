import sys
# sys.path.extend(['./copct-master','./dananau-pyhop-195ab6320571'])

from load_facility_demo import load_demo
from facility_domain import causes, M
import math


def toXML(state, xml_file_path):
    with open(xml_file_path,'w') as xml:
        xml.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        xml.write('<tabletop xmlns="http://synapse.cs.umd.edu/tabletop-xml" xspan="20" yspan="12">\n')
        xml.write('<include file="tablesetup/def-room.xml"/>\n')
        # xml.write('<include file="tablesetup/def-forklift.xml"/>\n')
        # xml.write('<include file="tablesetup/teapot.xml"/>\n')
        xml.write('<instance def="room">\n')  
        # xml.write('<var name="rotation" value="(0,0,%s)"/>\n'%state['room'][4])
        xml.write('<var name="location" value="(%s,%s, 0.5)"/>\n'%(state['room'][1],state['room'][2] ))
        xml.write('<var name="xspan" value="%s"/>\n'%state['room'][5])
        xml.write('<var name="yspan" value="%s"/>\n'%state['room'][6])
        xml.write('</instance>\n')
        # xml.write('<instance def="forklift">\n')
        # xml.write('<var name="rotation" value="(0,0,%s)"/>\n'%state['forklift'][4])
        # print(state['forklift'][1:4])
        # xml.write('<var name="location" value="(%s,%s,%s)"/>\n'%tuple(state['forklift'][1:4]))
        # xml.write('</instance>\n')

        # xml.write('<custom id="teapot" location="(0,0,0)" rotation="(-90,0,0)" color="blue"\nscale="0.1" file="tablesetup/stl/Teapot.stl"/>')
        # xml.write('<custom id="teapot" location="(10,10,0)" rotation="(-90,0,0)" color="blue"\nscale="0.1" file="tablesetup/stl/Teapot.stl"/>')
                # xml.write('<block id="%sBlock%d" '%state[obj][5], k)

        
        for obj in state:
            if state[obj][0] == 'block':
                xml.write('<block xspan=".5" yspan=".5" zspan=".5" id="%s" '%obj)
                xml.write('location="(%s,%s,%s)" '%tuple(state[obj][1:4]))
                xml.write('rotation="(0,0,%s)" '%state[obj][4])
                xml.write('color="%s"/>\n'%state[obj][5])
                # xml.write('</instance>\n')
            # if state[obj][0] == 'teapot':
            #     xml.write('<block xspan=".5" yspan=".5" zspan=".5" id="%s" '%obj)
            #     xml.write('location="(%s,%s,%s)" '%tuple(state[obj][1:4]))
            #     xml.write('rotation="(0,0,%s)"/>\n'%state[obj][4])   
                
        xml.write('</tabletop>\n')

### Dynamic set up
def room_builder(room, state):
    blockId = 0
    numOfblocks = room[1]/1000
    for i in numOfblocks:
        state[room[0]+i] = "['block',-2.5, 1.5, .25, 0, '%S']"%(room[2])


if __name__ == '__main__':

    # Infer intentions from demo
    demo = load_demo(demo_directory='./SMILE-1.1.0/room_demo/')
    
    # Make new state with room rotated and more crates
    
    ### Dynamic set up
    setupStr = "paintRoom,4000,blue:machineRoom,2000,green"

    state = {
        'room': ['room', 4,0,0.25, 370]
    }

    roomBuilder = {}
    rooms = setupStr.split(':')
    k = 0
    for i in rooms:
        roomBuilder[k] = i.split(',')
        k = k+1





    # facility name: [room tag, x-coor, y-coor, z-coor, rotation, x-span, y-span]
    # room name: [block tag, x-coor, y-coor, z-coor, rotation, color]
    state = {
        'room': ['room', 4,0,0.25,0,10,10],
        'paintRoom1': ['block', -2.5, 1.5, .25, 0, 'blue'],
        'crate2': ['block', -3.5, 1.5, .25, 0, 'blue'],
        'crate3': ['block', -2.5, 0.5, .25, 0, 'blue'],
        'crate4': ['block', -3.5, 0.5, .25, 0, 'blue'],
        'crate5': ['block', -2.5, -1.5, .25, 0, 'green'],
        'crate6': ['block', -3.5, -1.5, .25, 0, 'green'],
        'crate7': ['block', -2.5, -0.5, .25, 0, 'green'],
        'crate8': ['block', -3.5, -0.5, .25, 0, 'green'],
    }

    coords = {
        'room': ['room', 4,0,0.25, 370],
        1: [-2.5, 1.5, .25],
        'crate2': ['block', -3.5, 1.5, .25, 0, 'blue'],
        'crate3': ['block', -2.5, 0.5, .25, 0, 'blue'],
        'crate4': ['block', -3.5, 0.5, .25, 0, 'blue'],
        'crate5': ['block', -2.5, -1.5, .25, 0, 'green'],
        'crate6': ['block', -3.5, -1.5, .25, 0, 'green'],
        'crate7': ['block', -2.5, -0.5, .25, 0, 'green'],
        'crate8': ['block', -3.5, -0.5, .25, 0, 'green'],
    }
    
    # export to xml for smile viewing
    toXML(state,'./SMILE-1.1.0/tablesetup/room8.xml')
    

