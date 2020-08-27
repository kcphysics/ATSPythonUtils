#!/usr/bin/env python3
import sys
from argparse import ArgumentParser
from atsobjs import loadObjects, AtsObject

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
  ats_objects, dest_obj = loadObjects(atsdb, dest)
  source_obj = None
  gate_objs = []
  for obj in ats_objects:
      if source.lower() in obj.name.lower():
          source_obj = obj
      if obj.name in gates:
          gate_objs.append(obj)
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

if __name__ == "__main__":
    parser = ArgumentParser(prog="ATS Flight Planner")
    parser.add_argument("--source", help="Starting Location")
    parser.add_argument("--dest", help="Ending Location")
    args = parser.parse_args()
    print(get_best_route("/home/kcphysics/tmush_code/atsdata.json", args.source, args.dest))
    
