#!/usr/bin/env python3
import sys
from argparse import ArgumentParser
from .atsobjs import loadObjects, AtsObject

gates = [
    "Transwarp Gate MR-01",
    "Transwarp Gate U-02",
    "Transwarp Gate T-08",
    "Zausta VI",
    "Boreth",
    "Latinum Galleria",
    "Elosian City",
    "Clispau IX"
]

def get_best_route(atsdb:str, source:str, dest:str) -> str:
    """ Returns the best route based on distance """
    ats_objects = loadObjects(atsdb)
    dest_obj = None
    source_obj = None
    for k, v in ats_objects.items():
        if source.lower() in k.lower():
            source_obj = v
        elif dest.lower() in k.lower():
            dest_obj = v
    if not dest_obj or not source_obj:
        raise ValueError("Could not find the source {} or the destination {} in the database".format(source, dest))
    gate_objs = [ats_objects.get(k) for k in gates]
    # for obj in ats_objects:
    #     if source.lower() in obj.name.lower():
    #         source_obj = obj
    #     if obj.name in gates:
    #         gate_objs.append(obj)
    if not dest_obj or not source or not gate_objs:
        raise ValueError("Unable to find source: {}, dest: {}, or gates".format(
            source_obj, dest_obj
        ))
    # Straight Distance Calculation
    straight_distance = source_obj.distFromObject(dest_obj)

    # First Leg Gates
    flg_dests = [(x.distFromObject(source_obj), x) for x in gate_objs]
    flg_dests.sort(key=lambda x: x[0])
    shortest_flg = flg_dests[0][1]
    if straight_distance < flg_dests[0][0]:
        # Direct route it best:
        return "DIRECT: {} -> {}".format(source_obj.name, dest_obj.name)
      
  
    # second leg gates
    slg_dests = [(x.distFromObject(dest_obj), x) for x in gate_objs]
    slg_dests.sort(key=lambda x: x[0])
    shortest_slg = slg_dests[0][1]

    if shortest_flg == shortest_slg:
        return "DIRECT: {} -> {}".format(source_obj.name, dest_obj.name)

    return "GATED: {} -> {} <---> {} -> {}".format(
        source_obj.name,
        shortest_flg.name,
        shortest_slg.name,
        dest_obj.name
    )

def best_route():
    parser = ArgumentParser(prog="ATS Flight Planner")
    parser.add_argument("--source", help="Starting Location")
    parser.add_argument("--dest", help="Ending Location")
    args = parser.parse_args()
    if not args.source or not args.dest:
        raise ValueError("This requires both source and dest to be provided, at least one is missing")
    print(get_best_route("data/atsdata.json", args.source, args.dest))
    

if __name__ == "__main__":
    best_route()
