"""
This python program is responsible for interfacing with the jar program included within this branch of the repository.
"""

print("Hello World")
"""
The executable for the jar should be manually edited so that it is usable by the python program
In particular the executable file at the head of the folder structure should be changed such:
    At the end of the line, the name of the top level file of the java program is listed as such:
        LEDWall "$@"
    The  "$@" should be replaced by the command line arguments:
        LEDWall --image-width 1920 --image-height 1080 --max-power 200000
    These arguments do not have to be in a specified order, but the argument immediately after an argument type will be treated as the value for that type
        e.g. imagewidth is specified as 1920, not 1080, and maxpower is specified as 200,000
    Because an argument must be followed by its value, the first argument must be an argument type
        e.g. "LEDWall 1920 --image-width" may lead to undesired operation, instead one should specify "LEDWall --image-width 1920"

    Currently the supported options are:
        1. --image-width: width of image being sent to the java program
            if unspecified: defaults to 40
        2. --image-height: height of image being sent to the java program
            if unspecified: defaults to 30
    
    Soon to be supported:
        1. --modules-wide: the number of modules that the wall is wide
            if unspecified: defaults to 4
        2. --modules-high: the number of modules that the wall is high
            if unspecified: defaults to 3
"""