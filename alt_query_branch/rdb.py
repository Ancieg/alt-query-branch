import re
import requests
import requests_cache

# global cache
requests_cache.install_cache('~/.cache/alt-query-branch')

class RDBNoSuchBranchError(RuntimeError):
    pass

class RDB:
    def __init__(self):
        self._api_route = 'https://rdb.altlinux.org/api/export/branch_binary_packages/{}'
        self._headers = {'Accept': 'application/json'}

    def _do_api_request(self, request):
        return requests.get(request, headers=self._headers)

    def _export_branch_binary_packages(self, branch):
        return self._do_api_request(self._api_route.format(branch)).json()

    def _allowed_packages_sets(self):
        """
        A tricky way to get allowed branches. It returns the following for now:

        -----BEGIN RESPONSE-----
        {
            "args": {
            "arch": null
        },
        "validation_message": [
            "unknown package set name : invalid-branch",
            "allowed package set names are : ['sisyphus', 'p9', 'p10']"
        ],
        "message": "Request parameters validation error"
        }
        -----END RESPONSE-----
        """
        response = self._export_branch_binary_packages('invalid-branch')
        allowed_package_set_names = response['validation_message'][1]
        allowed_packages_set_names_list_as_str = re.findall("'[a-zA-Z0-9]*'", allowed_package_set_names)
        return [m.strip("'") for m in allowed_packages_set_names_list_as_str]

    def available_branches(self):
        return self._allowed_packages_sets()

    def branch_binary_packages(self, branch='sisyphus'):
        if branch not in self.available_branches():
            raise RDBNoSuchBranchError('Branch {} is not available'.format(branch))
        return self._export_branch_binary_packages(branch)

