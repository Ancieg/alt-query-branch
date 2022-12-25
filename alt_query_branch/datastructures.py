from . import ordered_arches

class FoundPackage:
    def __init__(self, source):
        self._source = source
        self._binaries = []

    def add_bin(self, arch, bin):
        if {'arch': arch, 'name': bin} not in self._binaries:
            self._binaries.append({'arch': arch, 'name': bin})

    def _sorted_arches(self):
        arches = set()
        for bin in self._binaries:
            arches.add(bin['arch'])
        arches = list(arches)

        ordered_arches_sub = []
        for arch in ordered_arches:
            if arch in arches:
                ordered_arches_sub.append(arch)
        return ordered_arches_sub

    def _sort_binaries(self):
        sorted_bin_packages = []
        for arch in self._sorted_arches():
            for bin in sorted(filter(lambda x: x['arch'] == arch, self._binaries), key=lambda bin: bin['name']):
                sorted_bin_packages.append({'arch': arch, 'name': bin['name']})
        self._binaries = sorted_bin_packages

    def to_dict(self):
        self._sort_binaries()
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
