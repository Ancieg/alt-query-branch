REQUEST_ROUTE = 'https://rdb.altlinux.org/api/export/branch_binary_packages'

ALLOWED_BRANCHES = [
    'sisyphus',
    'p10',
    'p9'
]

ORDERED_ARCHES = {
    'noarch': 0,
    'x86_64': 1,
    'i586': 2,
    'armh': 3,
    'aarch64': 4,
    'ppc64le': 5
}

CACHING = {
    'enabled': True,
    'lifetime': 900,
    'backend': 'sqlite',
    'path': '~/.cache/alt-query-branch'
}
