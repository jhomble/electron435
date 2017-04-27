import sys
sys.path.append('./copct-master')

import copct
from load_facility_demo import load_demo

# # Background Causal Knowledge:
# (move-to, obj, dest, dx, dy, dz, da) causes
#     [(grasp, obj), (release, obj, dest, dx, dy, dz, da)]    
# (stack, dest, dx, dy, dz, da, obj1) causes
#     [(move-to, obj1, dest, dx, dy, dz, da)]
#     but only if obj1 is a block.
# (stack, dest, dx, dy, dz, da, obj1, obj2, obj3, ...) causes
#     [(move-to, obj1, dest, dx, dy, dz, da), (stack, obj1, 0, 0, .5, 0, obj2, obj3, ...)]
#     but only if obj1 is a block.
# (stack-all, dx, dy, dz, da) causes
#     [(stack, 'room', dx, dy, dz, da, obj1, obj2, obj3, ...)]
#     where obj1, obj2, obj3, ... are all the blocks in the room.

def lookup_type(object_id, state):
    return [obj_type for (obj_id,obj_type,_,_,_,_) in state if obj_id == object_id][0]

def causes(v):
    # v[i] = the i^th (state, action, arguments)
    # returns g, a set of possible causes of v
    states, actions, arguments = zip(*v)
    g = set()

    if actions == ('grasp','release',):
        g.add((states[0],'move-to',(arguments[1][0], )+(arguments[1][1], )+(arguments[1][2], )+(arguments[1][3], )+(arguments[1][4], )+(arguments[1][5], )))
    if actions == ('move-to',):
        obj_type = lookup_type(arguments[0][0], states[0])
        if obj_type == 'block':
            g.add((states[0],'stack',(arguments[0][1], )+(arguments[0][2], )+(arguments[0][3], )+(arguments[0][4], )+(arguments[0][5], )+(arguments[0][0], )))
    if actions == ('move-to','stack',):
        obj1_type = lookup_type(arguments[1][0], states[0])
        if obj1_type == 'block' and arguments[0][0] == arguments[1][0]:
            g.add((states[0],'stack',(arguments[0][1], )+(arguments[0][2], )+(arguments[0][3], )+(arguments[0][4], )+(arguments[0][5], )+(arguments[1][0], )+(arguments[1][5], )+arguments[1][6:]))
    if actions == ('stack',):
        all_block = [obj_id for (obj_id, obj_type,_,_,_,_) in states[0] if obj_type == 'block']
        if set(all_block) == set(arguments[0][5:]) and arguments[0][0] == 'room':
            g.add((states[0],'stack-all',(arguments[0][1], )+(arguments[0][2], )+(arguments[0][3], )+(arguments[0][4], )))


    return g

M = 2

def main():
    # Load demo
    demo = load_demo(demo_directory='./SMILE-1.1.0/room_demo/')
    
    # interpret demo (fixed-parameter-tractable when M is small and explicitly provided)
    status, tlcovs, g = copct.explain(causes, demo, M=M)
    print('copct status: %s'%status)
    print('%d covers'%len(tlcovs))

    # get most parsimonious covers
    pcovs, length = copct.minCardinalityTLCovers(tlcovs)
    print('%d covers of length %d'%(len(pcovs), length))
    
    # Show the first one
    print('First cover of length %d:'%length)
    for intention in pcovs[0][0]:
        print(intention[1:])

if __name__=='__main__':
    main()
