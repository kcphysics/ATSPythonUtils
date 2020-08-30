#!/usr/bin/env python3
import sys
import os
import json
import math
from argparse import ArgumentParser
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y', 'z'])

PARSEC = 3085659622.014257
LIGHTSPEED = 29.979246
AVG_COCHRANE_DENSITY = 1298.737508

class AtsObject(object):
  def __init__(self, cochranes: str="", market:float=0, name: str="", x:float=0, y:float=0, z:float=0, **kwargs):
    self.market=market
    self.cochranes=cochranes
    self.name = name
    self.location = Point(x, y, z)
    self.x = x
    self.y = y
    self.z = z
    if cochranes=="" and kwargs['cochrenes']:
      self.cochranes = float(kwargs.get('cochrenes', COCHRANES))
    self.dist = None
    self.type = kwargs.get("otype", "Not Known")
    self.empire = kwargs.get("empire", "Not Known")

  def timeToObject(self, target, speed:float, dist:float = None):
    """ Calculates the average cocharanges then converts to parsecs/s """
    avg_cochranes = (self.cochranes + target.cochranes) / 2.0
    velocity = speed ** 3.3333 * avg_cochranes * LIGHTSPEED / PARSEC 
    if not dist:
      dist = self.distFromObject(target)
    return dist / velocity 

  def distFromCoords(self, x:float, y:float, z:float):
    """Calculates distance from an arbitrary object"""
    nx = self.x - x
    ny = self.y - y
    nz = self.z - z
    dist = math.sqrt(nx**2 + ny**2 + nz**2)
    return dist

  def distFromObject(self, obj):
    """ Calculates distance from object """
    return self.distFromCoords(obj.x, obj.y, obj.z)

  def distInRadius(self, obj, r:float):
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


def loadObjects(fname: str) -> dict:
  """ Loads objects from the 2.18 database """
  if not os.path.isfile(fname):
    raise IOError("ATS Data file {} does not exist".format(fname))
  ats_objects = {}
  with open(fname, 'r') as f:
    data = json.loads(f.read())
  
  for x in data['ATS_Navcomp_DB']['empires']:
    for z in ['planets', 'stations']:
      for y in x.get(z, []):
        obj = AtsObject(empire=x.get("name"), otype=z, **y)
        ats_objects[obj.name] = obj
  
  return ats_objects

def loadBorders(fname: str) -> dict:
  """ Loads borders, which also are the basis of coord frames """
  if not os.path.isfile(fname):
    raise IOError("ATS Data file {} does not exist".format(fname))
  ats_objects = {}
  with open(fname, 'r') as f:
    data = json.loads(f.read())
  
  for x in data['ATS_Navcomp_DB']['empires']:
    for z in ['borders']:
      for y in x.get(z, []):
        ats_objects[y.get('name')] = Point(y.get('x'), y.get('y'), y.get('z'))
  
  return ats_objects


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






