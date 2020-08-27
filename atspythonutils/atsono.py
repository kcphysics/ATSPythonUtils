import sys
import os
from argparse import ArgumentParser
from .atsobjs import loadObjects, AtsObject

def get_nearby_objects(ats_objects: dict, target: AtsObject, radius: int=200, nres: int=20) -> list:
    """ Does the actual work of getting nearby objects """
    dists = [(x.distInRadius(target, radius), x) for k,x in ats_objects.items() if target.name != k]
    psinr = [(d, x) for d,x in dists if d is not None and d > 0]
    psinr.sort(key=lambda x: x[0])
    #psinr = [x for x in ats_objects if (x.distInRadius(target, radius) is not None) and (x.dist > 0)]
    #psinr.sort(key=lambda x: x.dist)
    return psinr[:20]


def get_ono():
    parser = ArgumentParser(prog="Object Distance Calculator")
    parser.add_argument("--target", help="Partial name of Source")
    parser.add_argument("--radius", help="Radius to look in", default=100)
    parser.add_argument("--nres", help="Number of results", default=20)
    args = parser.parse_args()
    if not args.target:
        raise ValueError("No target was given")
    fpath = os.path.dirname(os.path.abspath(__file__))
    dbpath = os.path.join(fpath, "data/atsdata.json")
    ats_objects = loadObjects(dbpath)
    target_key = [v for k,v in ats_objects.items() if args.target.lower() in k.lower()]
    if len(target_key) > 1:
        raise ValueError("Found more then one candidate for {}, please specify more of the name".format(args.target))
    elif len(target_key) < 1:
        raise ValueError("Target {} does not exist in the objects database".format(args.target))
    target = target_key[0]
    # target = [x for x in planets if args.target.lower() in x.name.lower()][0]
    psinr = get_nearby_objects(ats_objects, target)
    print("The {} closest objects to {}".format(args.nres, target.name))
    print("{0:<25s}\t{1:15s}\t{2:10s}\t{3:10s}".format(
        "Name of Object",
        "Empire",
        "Type",
        "Distance (PC)"
    ))
    print("=" * 80)
    for _,x in psinr:
        print("{0:<25s}\t{1:15s}\t{2:10s}\t[{3:>.2f}]".format(
        x.name,
        x.empire,
        x.type,
        x.dist
        ))
  
if __name__ == "__main__":
    get_ono()