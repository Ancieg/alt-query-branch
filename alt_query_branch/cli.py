import argparse

from . import sorted_arches

argparser = argparse.ArgumentParser()
argparser.add_argument('-b', '--branch', type=str, default='sisyphus')
argparser.add_argument('-a', '--arches', type=str, default='noarch,x86_64,i586,armh,aarch64,ppc64le')
argparser.add_argument('-e', '--exact', action='store_true')
argparser.add_argument('-s', '--stdout', action='store_true')
argparser.add_argument('-o', '--file', type=str)
argparser.add_argument('expression')

args = vars(argparser.parse_args())
args['arches'] = args['arches'].split(',')
