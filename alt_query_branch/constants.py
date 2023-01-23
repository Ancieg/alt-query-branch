REQUEST_ROUTE = 'https://rdb.altlinux.org/api/export/branch_binary_packages'

ALLOWED_BRANCHES = [
    'sisyphus',
    'p10',
    'p9'
]

ORDERED_ARCHES = [
    'noarch',
    'x86_64',
    'i586',
    'armh',
    'aarch64',
    'ppc64le'
]

CACHING = {
    'enabled': True,
    'lifetime': 900,
    'backend': 'sqlite',
    'path': '~/.cache/alt-query-branch'
}
