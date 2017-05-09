# Acceptance Tests Suite 2

These tests are meant to show that functionality from Katz and Reggia's software has been preserved. This is achieved by comparing the results of our generated causes function to the results achieved with the causes function in baxter_experiments.py. The baxter_experiments.py file was slightly modified in order to print out more helpful information but the causes function was not altered.

## Running the Tests

```bash
$ chmod +x run_test_suite_2.sh
$ ./run_test_suite_2.sh
```

## Results

The results should be in comparison.txt once the script is run. They list the test name, followed by the average run time (of 5 trials), followed by the standard deviation (of the same 5 trials). 

## Causal Knowledge

The causal knowledge base for these tests is defined in electron435/python_causal_compiler/compiler/input/acceptance_causes.txt and looks like this:

```
RULES {
	if ((TYPE(obj) != DockCase && TYPE(obj) != DockDrawer)&&arm=1):
		move_unobstructed_object(obj, 'left', NONE, NONE) := move_arm_and_grasp(arm, obj);
	if ((TYPE(obj) != DockCase && TYPE(obj) != DockDrawer)&&arm=2):
		move_unobstructed_object(obj, 'right', NONE, NONE) := move_arm_and_grasp(arm, obj);
	if (arm=1):
		move_unobstructed_object(STATE('gripping', 0), dest, dM, dt) := put_down_grasped_object(arm, dest, dM, dt);
	if (arm=2):
		move_unobstructed_object(STATE('gripping', 1), dest, dM, dt) := put_down_grasped_object(arm, dest, dM, dt);
	if ((TYPE(dest)=DockCase || dest='discard-bin') && (dest != 'left' && dest != 'right')):		
		move_unobstructed_object_to_free_spot(obj, dest) := move_unobstructed_object(obj, dest, dM, dt);
	move_object(obj, dest, dM, dt) := move_unobstructed_object(obj, dest, dM, dt);
	if (dest != 'left' && dest != 'right' && (dest = 'dock_case_6' || dest = 'discard-bin')):
		move_object_to_free_spot(obj, dest) := move_object(obj, dest, dM, dt);		
	if (dest = 'discard-bin'):
		discard_object(obj) := move_object_to_free_spot(obj, dest);
	if (TYPE(STATE('gripping', 0)) != DockCase && TYPE(STATE('gripping', 0)) != DockDrawer && arm1 = 1):
		put_down_grasped_object(arm1, dest, dM, dt) := move_grasped_object(arm1, dest, dM, dt), release(arm2);
	if (TYPE(STATE('gripping', 1)) != DockCase && TYPE(STATE('gripping', 1)) != DockDrawer && arm1 = 2):
		put_down_grasped_object(arm1, dest, dM, dt) := move_grasped_object(arm1, dest, dM, dt), release(arm2);
	if (arm0 = arm1 && TYPE(obj) != DockDrawer):
		move_unobstructed_object(obj, dest, dM, dt) := move_arm_and_grasp(arm0, obj), put_down_grasped_object(arm1, dest, dM, dt);
	if (arm0 = arm1 && arm1 = arm2 && TYPE(obj) = DockDrawer && PYTHON(#if (sum([x**2 for (x,) in $dt$])**0.5) > 1:#)):
		open_dock_drawer(obj, PYTHON(#states[2]#)) := move_arm_and_grasp(arm0, obj), move_grasped_object(arm1, dest, dM, dt), release(arm2);
	if (arm0 = arm1 && arm1 = arm2 && TYPE(obj) = DockDrawer && PYTHON(#if (sum([x**2 for (x,) in $dt$])**0.5) <= 1:#)):
		close_dock_drawer(obj) := move_arm_and_grasp(arm0, obj), move_grasped_object(arm1, dest, dM, dt), release(arm2)	

}
```