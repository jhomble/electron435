#!/usr/bin/env python

import time
import sys
sys.path.append('../../copct-master')
import copct

M = 3
def causes(v):
    """
    Causal relation for the robotic imitation learning domain.
    v is a sequence of intentions or actions.
    Each element v[i] is of the form (state, task name, parameter values).
    Returns the set of all possible causes of v.
    """
    g = set() # set of possible causes
    arm_ids = ("left","right")
    clear_ids = ("discard-bin")
    states, tasks, args = zip(*v)

    # print('ACTS: '+str(tasks))

    if len(v) == 1:
        if tasks == ("move arm and grasp",):
            arm, object_id = args[0]
            dest_id = arm_ids[int(arm)-1]
            asm_type = dict(states[0])[object_id]
            if asm_type not in ("DockCase","DockDrawer"):
                print('move unobstructed object')                
                g.add((states[0], "move unobstructed object",(object_id, dest_id, (), ())))
        if tasks == ("put down grasped object",):
            arm, dest_id, dM, dt = args[0]
            object_id = dict(states[0])["gripping"][int(arm)-1]
            print('move unobstructed object')                            
            g.add((states[0], "move unobstructed object", (object_id, dest_id, dM, dt)))
        if tasks == ("move unobstructed object",):
            object_id, dest_id, dM, dt = args[0]
            if dest_id in arm_ids:
                print('move object')                
                g.add((states[0], "move object", args[0]))
            else:
                asm_type = dict(states[0])[dest_id]
                if (asm_type=="DockCase") or (dest_id in clear_ids):
                    print('move unobstructed object to free spot')                
                    g.add((states[0],"move unobstructed object to free spot", (object_id, dest_id)))
                print('move object')
                g.add((states[0],"move object", args[0]))
        if tasks == ("move object",):
            object_id, dest_id, dM, dt = args[0]
            if dest_id not in arm_ids:
                if (dest_id=="dock-case_6") or (dest_id in clear_ids):
                    print('move object to free spot')                
                    g.add((states[0],"move object to free spot", (object_id, dest_id)))
        if tasks == ("move object to free spot",):
            object_id, dest_id = args[0]
            if dest_id=="discard-bin":
                print('discard object')                                
                g.add((states[0],"discard object",(object_id,)))
    if len(v)==2:
        if tasks == ("move grasped object","release"):
            arm, dest_id, dM, dt = args[0]
            object_id = dict(states[0])["gripping"][int(arm)-1]
            asm_type = dict(states[0])[object_id]
            if asm_type not in ("DockCase","DockDrawer"):
                print('put down grasped object')                
                g.add((states[0], "put down grasped object", args[0]))
        if tasks == ("move arm and grasp","put down grasped object"):
            arm_0, object_id = args[0]
            arm_1, dest_id, dM, dt = args[1]
            asm_type = dict(states[0])[object_id]
            if (arm_0==arm_1) and not (asm_type=="DockDrawer"):
                print('move unobstructed object')                
                g.add((states[0],"move unobstructed object",(object_id, dest_id, dM, dt)))
    if len(v)==3:
        if tasks == ("move arm and grasp","move grasped object","release"):
            arm_0, object_id = args[0]
            arm_1, _, _, dt = args[1]
            arm_2, = args[2]
            asm_type = dict(states[0])[object_id]
            if (arm_0==arm_1) and (arm_1==arm_2) and (asm_type=="DockDrawer"):
                distance = sum([x**2 for (x,) in dt])**0.5
                if distance > 1:
                    print('open dock drawer')                
                    g.add((states[0],"open dock drawer",(object_id, states[2])))
                else:
                    print('close dock drawer')                
                    g.add((states[0],"close dock drawer",(object_id,)))
    return g

def run_experiments(check_irr=True):
    results = {}
    # Dock maintenance demos
    demos = ["demo_%s_%d"%(skill, di) for di in [1,2] for skill in ["remove_red_drive","replace_red_with_green","replace_red_with_spare","swap_red_with_green"]]
    # demos = ["demo_%s_%d"%(skill, di) for di in [1,2] for skill in ["remove_red_drive"]]
    # Block stacking demos
    demos += ["demo_il", "demo_ai", "demo_um"]
    # Cover demos
    print("Covering demos...")
    for demo_name in demos:
        results[demo_name] = {}        
        results[demo_name]["run_time"] = 0.0
        results[demo_name]["run_times"] = []        
        for i in range(0,5):
            print(demo_name)
            # import demo and ground truth
            exec_str = "from baxter_corpus.%s import demo"%demo_name
            exec(exec_str, globals())
            exec_str = "from baxter_corpus.%s_ground_truth import ground_truth"%demo_name
            exec(exec_str, globals())
            # Cover and prune by each parsimony criterion
            start_time = time.clock()
            status, tlcovs, g = copct.explain(causes, demo, M=M)

            # I ADDED THIS!!
            print('copct status: %s'%status)
            print('%d covers'%len(tlcovs))

            # get most parsimonious covers
            pcovs, length = copct.minCardinalityTLCovers(tlcovs)
            print('%d covers of length %d'%(len(pcovs), length))
            
            # Show the first one
            print('First cover of length %d:'%length)
            for intention in pcovs[0][0]:
               print(intention[1:])

            results[demo_name]["run_times"].append(time.clock()-start_time)
            results[demo_name]["run_time"] += time.clock()-start_time
            results[demo_name]["tlcovs"], results[demo_name]["g"] = tlcovs, g
            results[demo_name]["tlcovs_mc"] = [u for (u,_,_,_,_) in copct.minCardinalityTLCovers(tlcovs)[0]]
            results[demo_name]["tlcovs_md"] = [u for (u,_,_,_,_) in copct.maxDepthTLCovers(tlcovs)[0]]
            results[demo_name]["tlcovs_xd"] = [u for (u,_,_,_,_) in copct.minimaxDepthTLCovers(tlcovs)[0]]
            results[demo_name]["tlcovs_mp"] = [u for (u,_,_,_,_) in copct.minParametersTLCovers(tlcovs)[0]]
            results[demo_name]["tlcovs_fsn"] = [u for (u,_,_,_,_) in copct.minForestSizeTLCovers(tlcovs)[0]]
            results[demo_name]["tlcovs_fsx"] = [u for (u,_,_,_,_) in copct.maxForestSizeTLCovers(tlcovs)[0]]
            start_time = time.clock()
            if check_irr:
                status, tlcovs_irr = copct.irredundantTLCovers(tlcovs, timeout=1000)
                if status == False: print("IRR timeout")
            else:
                tlcovs_irr = tlcovs
            results[demo_name]["run_time_irr"] = time.clock()-start_time
            results[demo_name]["tlcovs_irr"] = [u for (u,_,_,_,_) in tlcovs_irr]
            results[demo_name]["u in tlcovs"] = ground_truth in [u for (u,_,_,_,_) in tlcovs]
            results[demo_name]["u in tlcovs_mc"] = ground_truth in results[demo_name]["tlcovs_mc"]
            results[demo_name]["u in tlcovs_md"] = ground_truth in results[demo_name]["tlcovs_md"]
            results[demo_name]["u in tlcovs_xd"] = ground_truth in results[demo_name]["tlcovs_xd"]
            results[demo_name]["u in tlcovs_mp"] = ground_truth in results[demo_name]["tlcovs_mp"]
            results[demo_name]["u in tlcovs_fsn"] = ground_truth in results[demo_name]["tlcovs_fsn"]
            results[demo_name]["u in tlcovs_fsx"] = ground_truth in results[demo_name]["tlcovs_fsx"]
            results[demo_name]["u in tlcovs_irr"] = ground_truth in results[demo_name]["tlcovs_irr"]
    # display results
    criteria = ["_mc", "_irr", "_md", "_xd", "_mp", "_fsn", "_fsx"]
    # print("Accuracy:")
    # for crit in criteria:
    #     correct_demos = [d for d in results if results[d]["u in tlcovs%s"%crit]]
    #     print('%s: %f%%'%(crit, 1.0*len(correct_demos)/len(demos)))
    # print("# of covers found:")
    # print(["Demo","Runtime (explain)", "Runtime (irr)"]+criteria)
    print("BAXTER Demo: Average Runtime, Standard Deviation")    
    for demo_name in demos:
        num_tlcovs = [len(results[demo_name]["tlcovs%s"%crit]) for crit in criteria]
        # print([demo_name, results[demo_name]["run_time"], results[demo_name]["run_time_irr"]]+num_tlcovs)
        avg = str(results[demo_name]["run_time"]/5.0)
        std_dev = str(calc_std_dev(results[demo_name]["run_times"], float(avg)))
        print(str(demo_name)+': '+avg+', '+std_dev)
    return results

def calc_std_dev(lst,avg):
    summ = 0.0
    for i in lst:
        summ += (i - avg)**2.0
    return (summ/float(len(lst)))**0.5

if __name__ == "__main__":

    check_irr = raw_input("Run irredundancy checks?  May take several minutes. [y/n]")
    results = run_experiments(check_irr == "y")
