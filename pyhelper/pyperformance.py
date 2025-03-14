import cProfile
import pstats
from importlib import import_module

with cProfile.Profile() as pr:
    import_module('') # YYYY.FOLDER...FOLDER.FILE

stats = pstats.Stats(pr)
stats.sort_stats(pstats.SortKey.TIME)
stats.print_stats()