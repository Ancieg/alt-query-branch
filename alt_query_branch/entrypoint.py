import json
import sys

from .cli import argparser, args
from .core_algorithms import search_binary_packages, sort_with_order
from .datastructures import Result

def main():
    match  = args['expression']
    exact  = args['exact']
    branch = args['branch']
    arches = args['arches']
    file   = args['file']
    stdout = args['stdout']

    if not stdout and not file:
        argparser.print_usage(file=sys.stderr)
        print("you should provide '-o/--file FILE' or '-s/--stdout' or both", file=sys.stderr)
        argparser.exit(1)

    try:
        result = search_binary_packages(match, exact, branch, arches)
        result = sort_with_order(result)
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
