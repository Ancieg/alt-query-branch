ordered_arches = [
    'noarch',
    'x86_64',
    'i586',
    'armh',
    'aarch64',
    'ppc64le'
]

sorted_arches = sorted(ordered_arches)

CACHE_ENABLED = True
CACHE_LIFETIME = 900
CACHE_PATH = '~/.cache/alt-query-branch'
