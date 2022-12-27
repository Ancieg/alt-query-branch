import jq
import re

from .rdb import RDBExportBranchBinaryPackages
from .datastructures import BinaryPackage, SourcePackage, Result

from .constants import ALL_ARCHES

def _order_packages(packages: dict):
    sorted_packages = sorted(packages, key=lambda d: d['source'])
    source_packages_names = list(set(s['source'] for s in sorted_packages))

    source_packages: list[SourcePackage] = []

    for source_package_name in sorted(source_packages_names):
        binaries = filter(lambda s: s['source'] == source_package_name, sorted_packages)
        source_package = SourcePackage(source_package_name)
        for binary in binaries:
            del binary['source']
            source_package.add_bin(BinaryPackage(**binary))
        source_packages.append(source_package)

    return source_packages

def search_matching_packages(match, exact=False, branch='sisyphus', arches=ALL_ARCHES):
    """
    Using jq is simple and fast way to process large JSON-content.
    """
    full_dump = RDBExportBranchBinaryPackages().execute(branch)

    if exact:
        match = ".{{0}}{}.{{0}}".format(re.escape(match))

    arches_string = ",".join(['"{}"'.format(a) for a in arches])

    expr = '.packages[] | select(.source != "")'
    expr += ' | select(.arch | IN({}))'.format(arches_string)
    expr += ' | select("\(.source) \(.name)" | match("{}"))'.format(match)

    plain_result = jq.compile(expr).input(full_dump).all()
    ordered_result = _order_packages(plain_result)

    return Result(match, exact, branch, arches, ordered_result).prepare()
