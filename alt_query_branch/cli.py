import argparse

from .constants import ORDERED_ARCHES

argparser = argparse.ArgumentParser()
argparser.add_argument('-b', '--branch', type=str, default='sisyphus')
argparser.add_argument('-a', '--arches', type=str, default=','.join(ORDERED_ARCHES))
argparser.add_argument('-e', '--exact', action='store_true')
argparser.add_argument('-s', '--stdout', action='store_true')
argparser.add_argument('-o', '--file', type=str)
argparser.add_argument('expression')

args = vars(argparser.parse_args())
args['arches'] = args['arches'].split(',')
