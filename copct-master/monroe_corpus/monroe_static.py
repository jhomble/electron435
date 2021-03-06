"""
Static facts that are always true in every Monroe problem instance.
"""

# All possible locations in the domain
locs = ("TEXACO1", "STRONG", "PARK-RIDGE", "ROCHESTER-GENERAL", "BRIGHTON-DUMP", "HENRIETTA-DUMP", "MARKETPLACE", "AIRPORT", "BRIGHTON-HIGH", "MENDON-POND", "12-CORNERS", "PITTSFORD-PLAZA", "ROCHESTER", "BRIGHTON", "MENDON", "HAMLIN", "WEBSTER", "IRONDEQUOIT", "HENRIETTA", "GREECE", "PARMA", "CLARKSON", "SWEEDEN", "OGDEN", "GATES", "RIGA", "CHILI", "WHEATLAND", "PITTSFORD", "SCOTTSVILLE", "RUSH", "PERINTON", "FAIRPORT", "PENFIELD", "EAST-ROCHESTER", "CHURCHVILLE", "BROCKPORT", "SPENCERPORT", "HILTON", "HONEOYE-FALLS")

# Most operator parameters are limited to these locations
poslocs = ("TEXACO1", "STRONG", "PARK-RIDGE", "ROCHESTER-GENERAL", "MARKETPLACE", "AIRPORT", "BRIGHTON-HIGH", "MENDON-POND", "12-CORNERS", "PITTSFORD-PLAZA", "BRIGHTON-DUMP", "HENRIETTA-DUMP")

# Water and power companies.
# Dicts that map companies onto tuples of the locations they service.
watercos = {
    "ROCH-WATER":("TEXACO1","STRONG","ROCHESTER-GENERAL","MARKETPLACE","AIRPORT","BRIGHTON-HIGH","12-CORNERS","BRIGHTON-DUMP","HENRIETTA-DUMP"),
    "MONROE-WATER":("PARK-RIDGE","PITTSFORD-PLAZA"),
    "MENDON-WATER":("MENDON-POND",)}
powercos = {
    "RGE":("TEXACO1","STRONG","PARK-RIDGE","ROCHESTER-GENERAL","MARKETPLACE","AIRPORT","BRIGHTON-HIGH","12-CORNERS","BRIGHTON-DUMP","HENRIETTA-DUMP"),
    "MENDON-GE":("MENDON-POND",),
    "MONROE-GE":("PITTSFORD-PLAZA",)}

# Certain task parameters are drawn from these entities
sleaders = ('SLEADER1','SLEADER2','SLEADER3')
gens = ('GEN1','GEN2')
food = ('FOOD1','FOOD2','FOOD3')
pcrews = ('PCREW1')
