from typing import Any

import jq

import alt_query_branch.rdb as rdb

from .constants import ORDERED_ARCHES
from .datastructures import BinaryPackage, SourcePackage


def order_packages(packages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    def without_keys(d, keys):
        return {x: d[x] for x in d if x not in keys}

    sources_names = list({s['source'] for s in packages})
    sources = {sn: SourcePackage(sn) for sn in sources_names}

    for package in packages:
        sources[package['source']].add_bin(
            BinaryPackage(**without_keys(package, 'source'))
        )

    return [v.to_dict() for k, v in sorted(sources.items())]


def search_matching_packages(match, exact=False, branch='sisyphus', arches='all'):
    """
    Using jq is simple and fast way to process large JSON-content.
    """
    packages = rdb.branch_binary_packages_list_with_source_package_only(branch)

    if arches == 'all':
        arches = ORDERED_ARCHES
    arches = ",".join(['"{}"'.format(a) for a in arches])

    expr = '.[] | select(.arch | IN({}))'.format(arches)
    if not exact:
        expr += ' | select("\(.source) \(.name)" | match("{}"))'.format(match)
    else:
        expr += ' | select(.source == "{}" or .name == "{}")'.format(match, match)

    plain_result = jq.jq(expr).transform(packages, multiple_output=True)

    return order_packages(plain_result)
