import random

def make_nwx_point_dict(coord_list, keyname):
    """takes single shape coord list and name returns{key:(x,y), key:(x,y)}"""
    pt_shapes = {}
    count = 0
    number = random.randint(100, 999)
    for coords in coord_list:
        node_name = keyname + "_" + str(count) + "-" + str(number)
        pt_shapes[node_name] = (float(coords[0]), float(coords[1]))
        count += 1

    return pt_shapes
