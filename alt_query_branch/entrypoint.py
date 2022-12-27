import json
import sys
import argparse

from .core_algorithms import search_binary_packages, sort_with_order
from .datastructures import Result
from .constants import ORDERED_ARCHES

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-b', '--branch', type=str, default='sisyphus')
    argparser.add_argument('-a', '--arches', type=str, default=','.join(ORDERED_ARCHES))
    argparser.add_argument('-e', '--exact', action='store_true')
    argparser.add_argument('-s', '--stdout', action='store_true')
    argparser.add_argument('-o', '--file', type=str)
    argparser.add_argument('expression')

    args = vars(argparser.parse_args())

    match  = args['expression']
    exact  = args['exact']
    branch = args['branch']
    arches = args['arches'].split(',')
    file   = args['file']
    stdout = args['stdout']

    if not stdout and not file:
        argparser.print_usage(file=sys.stderr)
        print("you should provide '-o/--file FILE' or '-s/--stdout' or both", file=sys.stderr)
        argparser.exit(1)

    try:
        result = search_binary_packages(match, exact, branch, arches)
        result = Result(match, "exact" if exact else "inexact", branch, arches, result).to_dict()
        result = json.dumps(result)
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(2)

    if stdout:
        print(result)
    
    if file:
        with open(file, 'w') as f:
            print(result, file=f)

if __name__ == '__main__':
    main()
