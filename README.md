# ATSPythonUtils

This project is to create command line, python based utilities that can be used for the game [TrekMUSH: Among the Stars](https://wiki.trekmush.org/index.php/Main_Page).  These are based off of the utilities created by mar'Qon, available [here](https://zen.trekmush.org/ats-navcomp/).  These tools are not commensurate with those that Qon created, but this is a casting so that other clients beside MUSHClient can use those tools (for me, TinTin++).

These are also leveraged via an RESTful API.

## Commands

This will be filled out slowly as the project is updated.

usage: Object Distance Calculator [-h] [--target TARGET] [--radius RADIUS]
                                  [--nres NRES]

optional arguments:
  -h, --help       show this help message and exit
  --target TARGET  Partial name of Source
  --radius RADIUS  Radius to look in
  --nres NRES      Number of results

### atsono

usage: Object Distance Calculator [-h] [--target TARGET] [--radius RADIUS]
                                  [--nres NRES]

optional arguments:
  -h, --help       show this help message and exit
  --target TARGET  Partial name of Source
  --radius RADIUS  Radius to look in
  --nres NRES      Number of results


### atsbestroute

usage: ATS Flight Planner [-h] [--source SOURCE] [--dest DEST]

optional arguments:
  -h, --help       show this help message and exit
  --source SOURCE  Starting Location
  --dest DEST      Ending Location