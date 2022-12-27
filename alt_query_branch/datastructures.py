from .constants import ORDERED_ARCHES

class FoundPackage:
    def __init__(self, source):
        self._source = source
        self._binaries = []

    def add_bin(self, arch, bin):
        if {'arch': arch, 'name': bin} not in self._binaries:
            self._binaries.append({'arch': arch, 'name': bin})

    def _ordered_arches(self):
        arches = list({bin['arch'] for bin in self._binaries})
        return [arch for arch in arches if arch in ORDERED_ARCHES]

    def _order_binaries(self):
        ordered_binaries = []
        for arch in self._ordered_arches():
            one_arch_binaries = filter(lambda x: x['arch'] == arch, self._binaries)
            ordered_one_arch_binaries = sorted(one_arch_binaries, key=lambda bin: bin['name'])
            ordered_binaries.extend(ordered_one_arch_binaries)
        self._binaries = ordered_binaries

    def to_dict(self):
        self._order_binaries()
        return {
            "source": self._source,
            "binaries": self._binaries
        }

class Result:
    def __init__(self, asked, type, branch, arches, found):
        self._asked = asked
        self._type = type
        self._branch = branch
        self._arches = arches
        self._found = found

    def to_dict(self):
        return {
            "asked": self._asked,
            "type": self._type,
            # "branch": self._branch,
            # "arches": self._arches,
            "found": self._found
        }
