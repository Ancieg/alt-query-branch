from typing import Any, Union

from jq import jq

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
        expr += f' | select("\(.source) \(.name)" | match("{match}"))'
    else:
        expr += f' | select(.source == "{match}" or .name == "{match}")'

    return jq(expr).transform(packages, multiple_output=True)
