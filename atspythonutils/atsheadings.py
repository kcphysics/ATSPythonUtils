"""
I have badly stolen this from mar'Qon, and am not too ashamed about it.

I have worked most of the math out on my own, but I will maintain parity with the implmentation already set
"""
import pdb
import os
import math
from datetime import timedelta
from argparse import ArgumentParser
from collections import namedtuple
from .atsobjs import Point, loadObjects, loadBorders

Heading = namedtuple('Heading', ['yaw', 'pitch'])


def rads(angle:float):
    return angle * math.pi / 180.0

def converttogrc(p: Point, frame:str, ats_borders: dict) -> Point:
    """ Searches the dictionary for a border name, and if it is found,
    converts the point from that frame -> GRC """
    for frame_name, frame_point in ats_borders.items():
        if frame.lower() in frame_name.lower():
            return Point(p.x + frame_point.x, p.y + frame_point.y, p.z + frame_point.z)
    raise ValueError("Frame '{}' could not be found, valid frames are {}".format(frame, ats_borders.keys()))

def projectheading(heading: Heading, spoint: Point, d:float=1000) -> Point:
    nx = d * math.cos(rads(heading.yaw)) * math.cos(rads(heading.pitch))
    ny = d * math.sin(rads(heading.yaw)) * math.cos(rads(heading.pitch))
    nz = d * math.sin(rads(heading.pitch))
    return Point(spoint.x + nx, spoint.y + ny,spoint.z +  nz)


def bourkian_determinant(p1: Point, p2: Point, s: Point, sd:float=1.0) -> bool:
    """ Does the math to determine if a line intersects a sphere, from here http://paulbourke.net/geometry/circlesphere
    Returns true if it intersects, even once, false otherwise"""
    a = (p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2 + (p2.z - p1.z) ** 2
    b = 2 * ( (p2.x - p1.x) * (p1.x - s.x) + (p2.y - p1.y) * (p1.y - s.y) + (p2.z - p1.z) * (p1.z - s.z) )
    c = s.x ** 2 + s.y **2 + s.z ** 2 + p1.x ** 2 + p1.y ** 2 + p1.z ** 2 - 2 * (s.x * p1.x + s.y * p1.y + s.z * p1.z) - sd ** 2
    bourke = (b ** 2) - 4 * a * c
    return bourke >= 0

def findobjectsalongline(x:float, y:float, z:float, yaw:float, pitch:float, atsobjects:dict, atsborders:dict , frame:str = None, speed:float = 16, distance:float = 1000.0, sdist:float = 50) -> list:
    """ Returns a list of objects along a line """
    source = Point(x, y, z)
    if frame:
        source = converttogrc(source, frame, atsborders)
    heading = Heading(yaw, pitch)
    projected = projectheading(heading, source, d=distance)
    for crad in range(1, 12, 2):
        objs = [obj for _, obj in atsobjects.items() if bourkian_determinant(source, projected, obj.location, crad) and obj.distFromCoords(source.x, source.y, source.z) > sdist ]
        if objs:
            break
    returns = []
    for obj in objs:
        d = obj.distFromCoords(source.x, source.y, source.z) 
        if d < 10:
            continue
        t = str(timedelta(seconds=obj.timeToDist(speed, d)))
        returns.append((d, t, crad, obj))
    returns.sort(key=lambda x: x[0])
    return returns

def findobjectbyplanet(atsdb: dict, target:str, **kwargs) -> list:
    """ Finds objects by a planet name instead of by using coords """
    target_obj = None
    if target in atsdb:
        target_obj = atsdb.get(target)
    else:
        for k, v in atsdb.items():
            if target.lower() in k.lower():
                target_obj = v
                break
    if not target_obj:
        raise ValueError("Unable to locate target object {} in the database".format(target))
    return findobjectsalongline(target_obj.x, target_obj.y, target_obj.z, **kwargs)


def get_objects_on_line():
    parser = ArgumentParser(prog="Get Objects along Line")
    parser.add_argument("x", type=float, help="X Value in the Galactic Coordinate Frame")
    parser.add_argument("y", type=float, help="Y Value in the Galactic Coordinate Frame")
    parser.add_argument("z", type=float, help="Z Value in the Galactic Coordinate Frame")
    parser.add_argument("yaw", type=float, help="Yaw value of heading")
    parser.add_argument("pitch", type=float, help="Pitch value of heading")
    parser.add_argument("--speed", type=float, help="Speed at which the object was moving", default=16)
    parser.add_argument("--frame", help="Frame, should be one of these (as of v2.18 of the db)", choices=["Cardassian", "CU-Iure", "CU-Kakra", "Federation", "Talos Exclusion Zone", "Bajoran", "Breen", "Klingon", "KE-Beeble", "KE-Narendra", "KE-QIT", "KE-Hunt", "Romulan", "GFA", "Orion", "Dominion", "Tholian", "Qvarne", "Gorn"])
    args = parser.parse_args()
    fpath = os.path.dirname(os.path.abspath(__file__))
    dbpath = os.path.join(fpath, "data/atsdata.json")
    ats_objects = loadObjects(dbpath)
    ats_borders = loadBorders(dbpath)
    print("Objects along line defined by Point {}, {}, {} and heading {}, {}:".format(
        args.x, args.y, args.z,
        args.yaw, args.pitch
    ))
    for d, t, r, obj in findobjectsalongline(args.x, args.y, args.z, args.yaw, args.pitch, ats_objects, ats_borders, speed=args.speed, frame=args.frame):
        print("{0:20s}\t{1:20s}\t[{2:<.2f}]".format(obj.name, t, d))
    print("Complete")

def get_objects_on_line_from_object():
    # from pudb import set_trace
    # set_trace()
    parser = ArgumentParser(prog="Get potential destinations via an object and a heading")
    parser.add_argument("name", type=str, help="Name of object in the objects database")
    parser.add_argument("yaw", type=float, help="Yaw value of heading")
    parser.add_argument("pitch", type=float, help="Pitch value of heading")
    parser.add_argument("--speed", type=float, help="Speed at which the object was moving", default=16)
    parser.add_argument("--frame", help="Frame, should be one of these (as of v2.18 of the db)", choices=["Cardassian", "CU-Iure", "CU-Kakra", "Federation", "Talos Exclusion Zone", "Bajoran", "Breen", "Klingon", "KE-Beeble", "KE-Narendra", "KE-QIT", "KE-Hunt", "Romulan", "GFA", "Orion", "Dominion", "Tholian", "Qvarne", "Gorn"])
    args = parser.parse_args()
    fpath = os.path.dirname(os.path.abspath(__file__))
    dbpath = os.path.join(fpath, "data/atsdata.json")
    ats_objects = loadObjects(dbpath)
    ats_borders = loadBorders(dbpath)
    target_obj = None
    for k, v in ats_objects.items():
        if args.name.lower() in k.lower():
            target_obj = v
            break
    if not target_obj:
        raise ValueError("Target {} could not be found in the database".format(args.name))
    potential_dests = [x for x in findobjectsalongline(
        target_obj.x, target_obj.y, target_obj.z,
        args.yaw, args.pitch, ats_objects, ats_borders, speed=args.speed, frame=args.frame)
    ]
    potential_dests.sort(key=lambda x: x[0])
    print("Objects along line defined by Object {} and heading {}, {}:".format(
        target_obj.name,
        args.yaw, args.pitch
    ))
    for d, t, x in potential_dests:
         print("{0:20s}\t{1:20s}\t[{2:<.2f}]".format(x.name, t, d))
    print("Complete")

if __name__ == "__main__":
    get_objects_on_line()


