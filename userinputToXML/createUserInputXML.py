import sys
import os

# simple types (all but composite) common attributes : id (default = unique string), location (required), 
# rotation (default 0,0,0), mass (default = 1), color (default gray)

#block : select id, select location, select rotation, select color, select mass, select xspan, select yspan, select zspan (default x,y,z = 1)
#cylinder : select id, select location, select rotation, select color, select mass, select radius (default 0.5), select yspan (default 1)
#sphere : select id, select location, select rotation, select color, select mass, select radius (default 1)
#box : select id, select location, select rotation, select color, select mass, select xspan, select yspan, select zspan, select thickness
#custom : select id, select location, select rotation, select color, select mass, select file (required), select scale (default 1)

#composite : select id (optional, select location (required), select rotation (optional),
#select mass (optional), select child elements of composite or simple type (require 1 or more)



# kwargs allows for non-predefined, variable # of key,value arguments
def simpleTypeXML(xmlfile, obj_type, tabs, **kwargs) :
	# write to xml all attributes present in kwargs; if not present, default values will be inferred by SMILE for attribute
	xml = xmlfile
	obj_type = obj_type
	
	xml.write('\t'*tabs + '<%s location = "(%s,%s,%s)"'%(obj_type, kwargs["location"][0],kwargs["location"][1],kwargs["location"][2]))
	# use tabs counter to indent appropriately in case simpleType object is child of composite object
	# writes type of simple object (block, cylinder, sphere, box, or custom) and location attribute since always present

	# covers common attributes of all simple types
	if "id" in kwargs :
		xml.write(' id="%s"'%kwargs["id"])
	if "rotation" in kwargs :
		xml.write(' rotation="(%s,%s,%s)"'%tuple(kwargs["rotation"]))
	if "mass" in kwargs :
		xml.write(' mass="%s"'%kwargs["mass"])
	if "color" in kwargs :
		xml.write(' color="%s"'%kwargs["color"])

	# covers attributes specific to block
	if "xspan" in kwargs :
		xml.write(' xspan="%s"'%kwargs["xspan"])
	if "yspan" in kwargs :
		xml.write(' yspan="%s"'%kwargs["yspan"])
	if "zspan" in kwargs :
		xml.write(' zspan="%s"'%kwargs["zspan"])

	# covers attributes specific to sphere/cylinder; yspan already covered
	if "radius" in kwargs :
		xml.write(' radius="%s"'%kwargs["radius"])

	#covers attributes specific to box; x/y/zspan already covered
	if "thickness" in kwargs :
		xml.write(' thickness="%s"'%kwargs["thickness"])

	#covers attributes specific to custom
	if "file" in kwargs :
		xml.write(' file="%s"'%kwargs["file"])
	if "scale" in kwargs :
		xml.write(' scale="%s"'%kwargs["scale"])

	xml.write("/>\n")
	# end element and add new line
	return

# kwargs allows for non-predefined, variable # of key,value arguments
def compositeXML(xmlfile, tabs, child_type, **kwargs) :
	xml = xmlfile
	xml.write('\t'*tabs + '<composite location = "(%s,%s,%s)"'%tuple(kwargs["location"]))
	# use tabs counter to indent appropriately in case simpleType object is child of composite object
	# writes location attribute since always present

	# covers attributes of composite parent element
	if "id" in kwargs :
		xml.write(' id="%s"'%kwargs["id"])
	if "rotation" in kwargs :
		xml.write(' rotation="(%s,%s,%s)"'%tuple(kwargs["rotation"]))
	if "mass" in kwargs :
		xml.write(' mass="%s"'%kwargs["mass"])

	xml.write('>\n')
	# end composite parent element and add new line

	# deal with children elements recursively or alone if just simpleType element child
	if child_type == "composite" :
		#print(child_type +"composite recurse")
		new_child_type, kwargs = createCompositeDictionary(kwargs[child_type])
		compositeXML(xmlfile, tabs+1, new_child_type, **kwargs)

	else :
		while child_type is not None :
			temp_child_type = child_type
			#print(child_type + "recursing")
			#print(str(kwargs))
			child_type, kwargs = createCompositeDictionary(kwargs[child_type])
			#print(str(kwargs) + "recursing into simple")
			simpleTypeXML(xmlfile, temp_child_type, tabs+1, **kwargs)
		#print("\n"*2)
		#print(str(kwargs))
		#print("\n"*2)
		#line_dict = createSimpleDictionary(comp_dict)
		#create a simpletype dictionary out of the list at end key of composite object's dictionary
		#simpleTypeXML(xmlfile, child_type, tabs+1, **line_dict)
		# call simpletypexml to convert single element 

	xml.write('\t' * tabs + '</composite>\n')
	return

def createCompositeDictionary(line_list) :
	i = 0
	comp_dict = dict()
	#print("\n"*2)
	#print('composite list' + str(line_list))
	while i < len(line_list) and line_list[i] not in ["block","box","cylinder","sphere","custom", "composite"]:
		# find point where composite branches to child elements and stop dictionary there so can recurse later
		if line_list[i] == "location" or line_list[i] == "rotation" :
			# if location or rotation attribute, need 3 values for key
			comp_dict[line_list[i]] = (line_list[i+1:i+4])
			i = i + 4
		else :
			# otherwise only need one value
			comp_dict[line_list[i]] = line_list[i+1]
			i = i + 2

	if i < len(line_list) :
		comp_dict[line_list[i]] = line_list[i+1:]
		child_type = line_list[i]
	else :
		child_type = None
	#print(child_type)
	#print(str(comp_dict))
	#print("done with dict create" + "\n" * 2)
	return child_type, comp_dict
	#return the child type as well as dictionary of attributes for composite object 
	#with child's list of values at end key of dict

def createSimpleDictionary(line_list) :
	line_dict = dict()
	try :
		i = 1
		while i < len(line_list):
			#convert list into key,value dictionary to pass to kwargs
			if line_list[i] == "location" or line_list[i] == "rotation" :
			# location and rotation have 3 values (x,y,z)
				line_dict[line_list[i]] = (line_list[i+1:i+4])
				i = i + 4
			else :
			# rest have only 1 value
				line_dict[line_list[i]] = line_list[i+1]
				i = i + 2
	except IndexError :
		# error handling for incorrectly formatted csv/text file, 
		# theres a missing key/value causing faulty indexing
		print("incorrect line format for xml object " + line_list[0])
		print("contents of line are " + str(line_list))
		exit(1)
	return line_dict

def createUserInputXML(string_input, file_path_output) :
	with open(file_path_output,'w') as xml :
		xml.write('<?xml version="1.0" encoding="UTF-8"?>\n')
		xml.write('<tabletop xmlns="http://synapse.cs.umd.edu/tabletop-xml" ')
		text = string_input.split(':')
		for line in text :
			# read string input from command line
			line_list = line.strip().split(',')
			if line_list[0] == 'tabletop' :
				xml.write('xspan="%s" yspan="%s">\n'%(line_list[2],line_list[4]))
				#first line is tabletop specifications, allows user to set size of facility layout; root element of xml
			elif line_list[0] == 'composite' :
				child_type, comp_dict = createCompositeDictionary(line_list[1:])
				compositeXML(xml,1,child_type,**comp_dict)
			elif line_list[0] == 'include' :
				xml.write('\t<%s file="%s"/>\n'%tuple(line_list))
			elif line_list[0] == 'instance' :
				instanceXML(xml,line_list)
			else :
				line_dict = createSimpleDictionary(line_list)
				simpleTypeXML(xml,line_list[0],1,**line_dict)

		xml.write('</tabletop>\n')
		xml.close()

def instanceXML(xmlfile, line_list) :
	# takes care of instance xml lines
	xml = xmlfile
	xml.write('\t<instance def="%s">\n'%line_list[1])
	try :
		i = 2
		while i < len(line_list) :
			if line_list[i] == 'var' :
				# goes thru each var element series in list and prints out corresponding xml line
				if line_list[i+1] == 'location' or line_list[i+1] == 'rotation' :
					print (line_list[i+2:i+5])
					xml.write('\t\t<var name="%s" value="%s"/>\n'%(line_list[i+1],str(tuple([float(line_list[i+2]),float(line_list[i+3]),float(line_list[i+4])]))))
					i = i + 5
				else :
					xml.write('\t\t<var name="%s" value="%s"/>\n'%(line_list[i+1:i+3]))
					i = i + 3
	except IndexError :
		print ('incorrect line format for xml object ' + line_list[0:2])
		print ('contents of line are ' + str(line_list))
	xml.write('\t</instance>\n')
	return


if  __name__ == '__main__' :
	createUserInputXML(sys.argv[1],'./generated_xml.xml')
