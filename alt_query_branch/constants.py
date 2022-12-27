RDB_URL = 'https://rdb.altlinux.org/api'
EXPORT_BRANCH_BINARY_PACKAGES = '/export/branch_binary_packages/'
REQUEST_ROUTE = RDB_URL + EXPORT_BRANCH_BINARY_PACKAGES + '{}'

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

ALL_ARCHES = sorted(ORDERED_ARCHES)
