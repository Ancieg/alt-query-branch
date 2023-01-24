from collections import defaultdict
from typing import Any, Union

from jq import jq

from .constants import ORDERED_ARCHES


def group_packages_by_sources(
        packages: list[dict[str, Any]]
        ) -> list[dict[str, Any]]:
    """
    Groups 'packages' by 'source' field.
    """
    def without_keys(d, keys):
        return {x: d[x] for x in d if x not in keys}

    groupped = defaultdict(list)

    for package in packages:
        groupped[package['source']].append(without_keys(package, 'source'))

    return [{'source': k, 'packages': v} for k, v in groupped.items()]


def sort_groupped_packages_by_sources(
        packages: list[dict[str, Any]]
        ) -> list[dict[str, Any]]:
    """
    Sorts 'packages' by 'source' field.
    Requires packages already groupped by group_packages_by_sources().
    """
    return sorted(packages, key=lambda p: p['source'])


def order_groupped_packages_by_arches(
        packages: list[dict[str, Any]]
        ) -> list[dict[str, Any]]:
    """
    Orders 'packages' by 'arch' field according to the order in ORDERED_ARCHES.
    Requires packages already groupped by group_packages_by_sources().
    """
    return [
        {
            'source': package['source'],
            'packages': sorted(
                package['packages'], key=lambda p: ORDERED_ARCHES[p['arch']]
            )
        }
        for package in packages
    ]


def search_matching_packages(
            packages: list[dict[str, Any]],
            match: str,
            exact: bool = False,
            arches: Union[str, list[str]] = 'all'
        ) -> list[dict[str, Any]]:
    """
    Using jq is simple and fast way to process large JSON-content.
    """

    if arches == 'all':
        arches = ORDERED_ARCHES
    arches = ",".join([f'"{a}"' for a in arches])

    expr = f'.[] | select(.arch | IN({arches}))'
    if not exact:
        expr += f' | select("\\(.source) \\(.name)" | match("{match}"))'
    else:
        expr += f' | select(.source == "{match}" or .name == "{match}")'

    return jq(expr).transform(packages, multiple_output=True)
