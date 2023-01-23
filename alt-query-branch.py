#!/usr/bin/env python3

import argparse
import json
import sys

from alt_query_branch.algorithms import search_matching_packages, order_packages
from alt_query_branch.rdb import branch_binary_packages_with_source_package


def perror(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-b', '--branch', type=str, default='sisyphus')
    argparser.add_argument('-a', '--arches', type=str, default='all')
    argparser.add_argument('-e', '--exact', action='store_true')
    argparser.add_argument('-s', '--stdout', action='store_true')
    argparser.add_argument('-o', '--file', type=str)
    argparser.add_argument('expression')

    args = vars(argparser.parse_args())

    match  = args['expression']
    exact  = args['exact']
    branch = args['branch']
    arches = 'all' if args['arches'] == 'all' else args['arches'].split(',')
    file   = args['file']
    stdout = args['stdout']

    if not stdout and not file:
        argparser.print_usage(file=sys.stderr)
        perror("you should provide '-o/--file FILE' or '-s/--stdout' or both")
        argparser.exit(1)

    try:
        packages = branch_binary_packages_with_source_package(branch)
        matching_packages = search_matching_packages(packages, match, exact, arches)
        result = json.dumps(
            {
                "expression": match,
                "exactness": "exact" if exact else "inexact",
                "branch": branch,
                "arches": arches,
                "packages": order_packages(matching_packages)
            }
        )
    except Exception as e:
        perror(e)
        sys.exit(2)

    if stdout:
        print(result)
    
    if file:
        with open(file, 'w') as f:
            print(result, file=f)

if __name__ == '__main__':
    main()
