import os
import math
import sys

# Takes a list of files paths, the first one is the 0.txt and the rest are 1-x, x is how many txt files there are.
def load_demo(demo_directory):
    files = demo_directory
    # populate the initial state
    state = {}
    # state[object_id] = [object_type, x, y, z, angle]
    with open(files[0]) as step_file:
        for line in step_file:
            fields = line.rstrip().split(',')
            action = fields[1]
            if action == 'create':
                object_id, object_type = fields[2], fields[4]
                state[object_id] = [object_type, 0, 0, 0, 0] # type, x, y, z, angle
            if action == 'move':
                object_id, x, y, z, angle = fields[2:6] + [fields[8]]
                state[object_id][1:] = [float(_) for _ in [x,y,z,angle]]
    # populate steps recorded in the demo
    # the steps are parsed into one of these:
    # grasp, object_id
    # release, object_id, destination_id, dx, dy, dz, da
    # dx, dy, dz, da are the relative geometric transformation between object and destination
    demo = []
    grasped_object = None # track currently grasped object
    for step in range(1,len(files)):
        with open(files[step],'r') as step_file:
            for line in step_file:
                fields = line.rstrip().split(',')
                action = fields[1]
                if action == 'grasp':
                    step_action = 'grasp'
                    grasped_object = fields[3]
                if action == 'release':
                    step_action = 'release'
                if action == 'move':
                    object_id, x, y, z, angle = fields[2:6] + [fields[8]]
                    state[object_id][1:] = [float(_) for _ in [x,y,z,angle]]
            if step_action == 'grasp':
                args = [grasped_object]
            if step_action == 'release':
                # compute relative transformation to destination
                dest = find_destination(state, grasped_object)
                dest_x, dest_y, dest_z, dest_angle = state[dest][1:5]
                x, y, z, a = state[grasped_object][1:5]
                rx, ry, dz, da = x - dest_x, y - dest_y, z - dest_z, a - dest_angle
                radians = dest_angle*math.pi/180
                dx = rx*math.cos(-radians) - ry*math.sin(-radians)
                dy = rx*math.sin(-radians) + ry*math.cos(-radians)
                args = [grasped_object, dest, dx, dy, dz, da]
                grasped_object = None
        # convert everything to tuple so that it's hashable for copct
        step_state = tuple((object_id,)+tuple(state[object_id]) for object_id in state)
        step_args = tuple(args)
        demo.append((step_state, step_action, step_args))
    return demo

def find_destination(state, object_id):
    # find the destination object on which an object was just placed
    x, y, z = state[object_id][1:4]
    dest_id = 'room' # defaults to the entire room
    dz = -1 # closest vertical distance found so far
    for other_object_id in state:
        if other_object_id == object_id: continue
        # check if other object is nearby in x,y, and closest underneath in z
        ox, oy, oz = state[other_object_id][1:4]
        if abs(x-ox) < .25 and abs(y-oy) < .25 and dz < oz < z:
            dz = oz
            dest_id = other_object_id
    return dest_id

if __name__=='__main__':
    x = sys.argv[1].split(',')
    z = os.path.normpath(sys.argv[2])
    y = []
    for word in x:
       y.append(os.path.normpath(word))
    demo = load_demo(y)
    #for d in demo:
    #    print(d[1:])
    #with open("test.txt",'w') as xml:
     #   xml.write(z)