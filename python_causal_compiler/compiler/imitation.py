import sys
sys.path.extend(['./copct-master','./dananau-pyhop-195ab6320571'])

from load_facility_demo import load_demo
from facility_domain import causes, M
import copct
import pyhop
import math

# states: same hash-based representation as load_facility_demo:
# state.objs[object_id] = [object_type, x, y, z, angle]
def deep_copy(state):
    new_state = pyhop.State(state.__name__)
    new_state.objs = {obj_id: list(state.objs[obj_id]) for obj_id in state.objs}
    return new_state
def toXML(state, xml_file_path):
    with open(xml_file_path,'w') as xml:
        xml.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        xml.write('<tabletop xmlns="http://synapse.cs.umd.edu/tabletop-xml" xspan="20" yspan="12">\n')
        xml.write('<include file="tablesetup/def-room.xml"/>\n')
        xml.write('<include file="tablesetup/def-forklift.xml"/>\n')
        xml.write('<instance def="room">\n')
        xml.write('<var name="rotation" value="(0,0,%s)"/>\n'%state.objs['room'][4])
        xml.write('</instance>\n')
        xml.write('<instance def="forklift">\n')
        xml.write('<var name="rotation" value="(0,0,%s)"/>\n'%state.objs['forklift'][4])
        print(state.objs['forklift'][1:4])
        xml.write('<var name="location" value="(%s,%s,%s)"/>\n'%tuple(state.objs['forklift'][1:4]))
        xml.write('</instance>\n')
        for obj in state.objs:
            if state.objs[obj][0] == 'block':
                xml.write('<block xspan=".5" yspan=".5" zspan=".5" id="%s" '%obj)
                xml.write('location="(%s,%s,%s)" '%tuple(state.objs[obj][1:4]))
                xml.write('rotation="(0,0,%s)"/>\n'%state.objs[obj][4])
        xml.write('</tabletop>\n')

# primitive operators - these change the state of the environment
def grasp(state, obj):
    return deep_copy(state) # don't actually need to change anything
def release(state, obj, dest, dx, dy, dz, da):
    new_state = deep_copy(state)
    # transform and position object relative to dest's frame of reference
    dest_x, dest_y, dest_z, dest_angle = state.objs[dest][1:5]
    radians = dest_angle*math.pi/180
    rx = dx*math.cos(radians) - dy*math.sin(radians)
    ry = dx*math.sin(radians) + dy*math.cos(radians)
    new_state.objs[obj][1:] = [dest_x + rx, dest_y+ry, dest_z + dz, dest_angle + da]
    return new_state
ops = pyhop.declare_operators(grasp, release)

def move_to(state, obj, dest, dx, dy, dz, da):
    __ret_val = [('grasp',obj),('release',obj,dest,dx,dy,dz,da)]
    return __ret_val
pyhop.declare_methods('move-to',move_to)
def stack(state, dest, dx, dy, dz, da, *obj):
    obj = flatten(obj)
    if state.objs[obj[0]][0] == 'block':
        __ret_val = [('move-to',obj[0],dest,dx,dy,dz,da)]
        __all_args = []
        for __action in __ret_val:
            for __arg in __action:
                __all_args.append(__arg)
        __all_intention_args = [[dest],[dx],[dy],[dz],[da],[__obj for __obj in obj]]
        __all_intention_args = flatten(__all_intention_args)
        __all_args = flatten(__all_args)
        if set(__all_intention_args).issubset(set(__all_args)):
            return __ret_val
    if state.objs[obj[0]][0] == 'block':
        __ret_val = [('move-to',obj[0],dest,dx,dy,dz,da),('stack',obj[0],0,0,0.5,0,)+tuple(obj[1:])]
        __all_args = []
        for __action in __ret_val:
            for __arg in __action:
                __all_args.append(__arg)
        __all_intention_args = [[dest],[dx],[dy],[dz],[da],[__obj for __obj in obj]]
        __all_intention_args = flatten(__all_intention_args)
        __all_args = flatten(__all_args)
        if set(__all_intention_args).issubset(set(__all_args)):
            return __ret_val
pyhop.declare_methods('stack',stack)
def stack_all(state, dx, dy, dz, da):
    all_block = [block_id for block_id in state.objs if state.objs[block_id][0]=='block']
    if True:
        __ret_val = [('stack','room',dx,dy,dz,da,)+tuple(all_block[0:])]
        return __ret_val
pyhop.declare_methods('stack-all',stack_all)


def flatten(l):
    out = []
    for item in l:
        if isinstance(item, (list,tuple)):
            out.extend(flatten(item))
        else:
           out.append(item)
    return out

if __name__ == '__main__':

    # Infer intentions from demo
    demo = load_demo(demo_directory='./SMILE-1.1.0/room_demo/')
    _, tlcovs, _ = copct.explain(causes, demo, M=M)
    pcovs, _ = copct.minCardinalityTLCovers(tlcovs)

    # reformat as pyhop tasks
    tasks = [(u[1],) + u[2] for u in pcovs[0][0]]
    
    # Make new state with room rotated and more crates
    state = pyhop.State('')
    state.objs = {
        'room': ['room', 0,0,.5, 270],
        'forklift': ['forklift', 0,0,.25,0],
        'crate1': ['block', 1.5, 1.5, .25, 0],
        'crate2': ['block', -1.5, 1.5, .25, 0],
        'crate3': ['block', 0.0, 1.5, .25, 0],
        'crate4': ['block', -1.5, 0.0, .25, 0],
    }
    
    # export to xml for smile viewing
    toXML(state,'./SMILE-1.1.0/tablesetup/room2.xml')
    
    # Plan new actions for the new situation
    print(tasks)
    new_actions = pyhop.pyhop(state, tasks,verbose=0)
    
    print('New actions:')
    for action in new_actions: print(action)
    
    # Simulate new actions
    for action in new_actions:
        action_fun = ops[action[0]]
        state = action_fun(state, *action[1:])

    # Print and export final state after new actions are performed
    print('Resulting state:')
    for obj in state.objs:
        print(obj, state.objs[obj])
    toXML(state,'./SMILE-1.1.0/tablesetup/room2_final.xml')
