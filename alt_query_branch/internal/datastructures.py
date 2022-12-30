from dataclasses import dataclass, asdict

from .constants import ORDERED_ARCHES

@dataclass(frozen=True, eq=True)
class BinaryPackage:
    name: str
    epoch: int
    version: str
    release: str
    arch: str
    disttag: str
    buildtime: int

class SourcePackage:
    def __init__(self, source: str):
        self._source: str = source
        self._binaries: list[BinaryPackage] = []

    def add_bin(self, package: BinaryPackage):
        if package not in self._binaries:
            self._binaries.append(package)

    def _ordered_arches(self):
        arches = list({bin.arch for bin in self._binaries})
        return [arch for arch in ORDERED_ARCHES if arch in arches]

    def _order_binaries(self):
        ordered_binaries = []
        for arch in self._ordered_arches():
            one_arch_binaries = filter(lambda x: x.arch == arch, self._binaries)
            ordered_one_arch_binaries = sorted(one_arch_binaries, key=lambda bin: bin.name)
            ordered_binaries.extend(ordered_one_arch_binaries)
        self._binaries = ordered_binaries

    def to_dict(self):
        self._order_binaries()
        return {
            "source": self._source,
            "binaries": [asdict(b) for b in self._binaries]
        }

class Result:
    def __init__(self, expression: str, exact: bool, branch: str, arches: list[str], packages: list[SourcePackage]):
        self._asked = expression
        self._exactness = "exact" if exact else "inexact"
        self._branch = branch
        self._arches = arches
        self._packages = packages

    def prepare(self):
        return {
            "expression": self._asked,
            "exactness": self._exactness,
            "branch": self._branch,
            "arches": self._arches,
            "packages": [p.to_dict() for p in self._packages]
        }
