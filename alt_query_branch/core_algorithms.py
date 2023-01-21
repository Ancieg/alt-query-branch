import jq

import alt_query_branch.rdb as rdb

from .constants import ORDERED_ARCHES
from .datastructures import BinaryPackage, SourcePackage


def _order_packages(packages: dict):
    def without_keys(d, keys):
        return {x: d[x] for x in d if x not in keys}

    sorted_packages = sorted(packages, key=lambda d: d['source'])
    source_packages_names = list(set(s['source'] for s in sorted_packages))

    source_packages: list[SourcePackage] = []

    for source_package_name in sorted(source_packages_names):
        binaries = filter(lambda s: s['source'] == source_package_name, sorted_packages)
        source_package = SourcePackage(source_package_name)
        for binary in binaries:
            source_package.add_bin(BinaryPackage(**without_keys(binary, 'source')))
        source_packages.append(source_package)

    return source_packages

def search_matching_packages(match, exact=False, branch='sisyphus', arches='all'):
    """
    Using jq is simple and fast way to process large JSON-content.
    """
    full_dump = rdb.branch_binary_packages(branch)

    if arches == 'all':
        arches = ORDERED_ARCHES
    arches = ",".join(['"{}"'.format(a) for a in arches])

    expr = '.packages[] | select(.source != "")'
    expr += ' | select(.arch | IN({}))'.format(arches)
    if not exact:
        expr += ' | select("\(.source) \(.name)" | match("{}"))'.format(match)
    else:
        expr += ' | select(.source == "{}" or .name == "{}")'.format(match, match)

    plain_result = jq.jq(expr).transform(full_dump, multiple_output=True)
    ordered_result = _order_packages(plain_result)

    return [p.to_dict() for p in ordered_result]
