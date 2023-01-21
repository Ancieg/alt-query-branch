from collections import namedtuple

from .constants import ORDERED_ARCHES

BinaryPackage = namedtuple(
    'BinaryPackage',
    [
        'name',
        'epoch',
        'version',
        'release',
        'arch',
        'disttag',
        'buildtime'
    ]
)


class SourcePackage:
    def __init__(self, source: str):
        self._source = source
        self._binaries = set()

    def add_bin(self, package: BinaryPackage):
        self._binaries.add(package)

    def _ordered_arches(self):
        arches = list({bin.arch for bin in self._binaries})
        return [arch for arch in ORDERED_ARCHES if arch in arches]

    def _ordered_binaries(self):
        ordered_binaries = []
        for arch in self._ordered_arches():
            one_arch_binaries = filter(lambda x: x.arch == arch, self._binaries)
            ordered_one_arch_binaries = sorted(one_arch_binaries, key=lambda bin: bin.name)
            ordered_binaries.extend(ordered_one_arch_binaries)
        return ordered_binaries

    def to_dict(self):
        return {
            "source": self._source,
            "binaries": [b._asdict() for b in self._ordered_binaries()]
        }
