#!/usr/bin/env python3
import sys
import os
import json
import math
from argparse import ArgumentParser

class AtsObject(object):
  def __init__(self, cochranes: str="", market: int=0, name: str="", x:int=0, y:int=0, z:int=0, **kwargs):
    self.market=market
    self.cochranes=cochranes
    self.name = name
    self.x = x
    self.y = y
    self.z = z
    if cochranes=="" and kwargs['cochrenes']:
      self.cochranes = kwargs.get('cochrenes')
    self.dist = None
    self.type = kwargs.get("otype", "Not Known")
    self.empire = kwargs.get("empire", "Not Known")

  def distFromCoords(self, x:int, y:int, z:int):
    """Calculates distance from an arbitrary object"""
    nx = self.x - x
    ny = self.y - y
    nz = self.z - z
    dist = math.sqrt(nx**2 + ny**2 + nz**2)
    return dist

  def distFromObject(self, obj):
    """ Calculates distance from object """
    return self.distFromCoords(obj.x, obj.y, obj.z)

  def distInRadius(self, obj, r:int):
    """ Returns the distance if the object is within a given radius r """
    d = self.distFromObject(obj)
    if d <= r:
      self.dist = d
      return d

  def tojson(self) -> dict:
    """ Converts the object to a dict for JSON conversion """
    return {
      "name": self.name,
      "empire": self.empire,
      "x": self.x,
      "y": self.y,
      "z": self.z,
      "type": self.type,
      "cochranes": self.cochranes
    }


def loadObjects(fname: str, target: str) -> list:
  """ Loads objects from the 2.18 database """
  if not os.path.isfile(fname):
    raise IOError("ATS Data file {} does not exist".format(fname))
  ats_objects = []
  target_obj = None
  with open(fname, 'r') as f:
    data = json.loads(f.read())
  
  for x in data['ATS_Navcomp_DB']['empires']:
    for z in ['planets', 'stations']:
      for y in x.get(z, []):
        obj = AtsObject(empire=x.get("name"), otype=z, **y)
        if target.lower() in y.get("name", "").lower():
          target_obj = obj
        ats_objects.append(obj)
  
  return ats_objects, target_obj


def loadPlanets(fname: str):
  if not os.path.isfile(fname):
    raise IOError("ATS Data file {} does not exist".format(fname))
  
  planets = []
  with open(fname, 'r') as f:
    data = json.loads(f.read())
  
  for x in data['ATS_Navcomp_DB']['empires']:
    for y in x['planets']:
      planets.append(AtsObject(**y))
  
  return planets


def get_nearby_objects(ats_objects: dict, target: AtsObject, radius: int=200, nres: int=20) -> list:
  """ Does the actual work of getting nearby objects """
  psinr = [x for x in ats_objects if (x.distInRadius(target, radius) is not None) and (x.dist > 0)]
  psinr.sort(key=lambda x: x.dist)
  return psinr[:20]


if __name__ == "__main__":
  parser = ArgumentParser(prog="Object Distance Calculator")
  parser.add_argument("--target", help="Partial name of Source")
  parser.add_argument("--radius", help="Radius to look in", default=100)
  parser.add_argument("--nres", help="Number of results", default=20)
  args = parser.parse_args()
  # planets = loadPlanets('atsdata.json')
  ats_objects, target = loadObjects('/home/kcphysics/tmush_code/atsdata.json', args.target)
  # target = [x for x in planets if args.target.lower() in x.name.lower()][0]
  if not target:
    print("Target {} does not exist".format(args.target))
    sys.exit(1)
  psinr = get_nearby_objects(ats_objects, target)
  print("The {} closest objects to {}".format(args.nres, target.name))
  print("{0:<25s}\t{1:15s}\t{2:10s}\t{3:10s}".format(
    "Name of Object",
    "Empire",
    "Type",
    "Distance (PC)"
  ))
  print("=" * 80)
  for x in psinr:
    print("{0:<25s}\t{1:15s}\t{2:10s}\t[{3:>.2f}]".format(
      x.name,
      x.empire,
      x.type,
      x.dist
    ))
