#!/usr/bin/env python3
import sys
import os
from datetime import timedelta
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

def get_best_route(ats_objects:dict, source:str, dest:str, speed:float = 16) -> str:
    """ Returns the best route based on distance """
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
    direct_time = source_obj.timeToObject(dest_obj, speed=speed, dist=straight_distance)

    # First Leg Gates
    flg_dests = [(x.distFromObject(source_obj), x) for x in gate_objs]
    flg_dests.sort(key=lambda x: x[0])
    shortest_flg = flg_dests[0][1]
    shortest_flg_time = source_obj.timeToObject(shortest_flg, speed=speed, dist=flg_dests[0][0]) 
    if straight_distance < flg_dests[0][0]:
        # Direct route it best:
        return "DIRECT: {} -> {} Time: {}".format(source_obj.name, dest_obj.name, str(timedelta(seconds=direct_time)))
      
  
    # second leg gates
    slg_dests = [(x.distFromObject(dest_obj), x) for x in gate_objs]
    slg_dests.sort(key=lambda x: x[0])
    shortest_slg = slg_dests[0][1]
    shortest_slg_time = source_obj.timeToObject(shortest_slg, speed=speed, dist=slg_dests[0][0]) 
    if shortest_flg == shortest_slg:
        return "DIRECT: {} -> {} Time: {}".format(source_obj.name, dest_obj.name, str(timedelta(seconds=direct_time)))
        #return "DIRECT: {} -> {}".format(source_obj.name, dest_obj.name)

    return "GATED: {} -> {} Time: {} <---> {} -> {} Time: {}".format(
        source_obj.name,
        shortest_flg.name,
        str(timedelta(seconds=shortest_flg_time)),
        shortest_slg.name,
        dest_obj.name,
        str(timedelta(seconds=shortest_slg_time))
    )

def best_route():
    parser = ArgumentParser(prog="ATS Flight Planner")
    parser.add_argument("--source", help="Starting Location")
    parser.add_argument("--dest", help="Ending Location")
    parser.add_argument("--speed", help="Speed that you are going", default=16, type=float)
    args = parser.parse_args()
    if not args.source or not args.dest:
        raise ValueError("This requires both source and dest to be provided, at least one is missing")
    fpath = os.path.dirname(os.path.abspath(__file__))
    dbpath = os.path.join(fpath, "data/atsdata.json")
    ats_objects = loadObjects(dbpath)
    print(get_best_route(ats_objects, args.source, args.dest, args.speed))
    

if __name__ == "__main__":
    best_route()
