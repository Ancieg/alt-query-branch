import jq
import re

from .rdb import RDBExportBranchBinaryPackages
from .datastructures import FoundPackage

from .constants import ALL_ARCHES

def sort_with_order(ans): # 'ans' stands for arch-name-source
    sorted_result_list = sorted(ans, key=lambda d: d['source'])
    sources = sorted(list(set(s['source'] for s in sorted_result_list)))

    result_set = []

    for source in sources:
        binaries = list(filter(lambda s: s['source'] == source, sorted_result_list))
        res = FoundPackage(source)
        for binary in binaries:
            res.add_bin(binary['arch'], binary['name'])
        result_set.append(res.to_dict())

    return result_set

def search_binary_packages(match, exact=False, branch='sisyphus', arches=ALL_ARCHES):
    """
    Using jq is simple and fast way to process large JSON-content.
    """
    full_dump = RDBExportBranchBinaryPackages().execute(branch)

    if exact:
        match = ".{{0}}{}.{{0}}".format(re.escape(match))

    arches = ",".join(['"{}"'.format(a) for a in arches])

    expr = '.packages[] | select(.source != "") | {source,arch,name}'
    expr += ' | select(.arch | IN({}))'.format(arches)
    expr += ' | select("\(.source) \(.name)" | match("{}"))'.format(match)

    plain_result = jq.compile(expr).input(full_dump).all()
 
    return sort_with_order(plain_result)
