from pprint import pprint

HOUSE_AREA = [113, 169, 221, 254, 287, 323,352, 360]
HOUSE_TYPE = [0.80, 0.97, 1.04,  1.17]

user_list = []

for type_val in HOUSE_AREA:
	
	temp_list = []
	for area_val in HOUSE_TYPE:
		val = "%.2f"%(type_val/30.0 * area_val)
		temp_list.append( val) 
	user_list.append(temp_list)

pprint(user_list)