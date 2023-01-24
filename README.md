# alt-query-branch
A simple program to find packages in ALT repositories using [in]exact matching.

---

# Description

The program can do exact/inexact search in ALT branches (supported branches are determined in runtime, but they are `p9, p10, sisyphus` for now). **It searches packages names in both source and binary packages sets.**
You may want to provide some filters - and you can.

Main features:

* check both source and binary packages sets for matches;
* JSON format of output;
* it is fast due to using both `jq` and `requests-cache` packages;
* exact or inexact search (when you use inexact search - which is default - you can write regular expressions);
* branch choosing (however, I decided to allow only one branch per request);
* architectures filtration (just a comma-separated list of architectures to `-a/--arches` option);
* you can write results to `STDOUT` and file both (`tee` says it is useless feature);

# Requirements

You need to install the following Python modules into your P10-based system:

* `python3-module-jq`
* `python3-module-requests-cache`

# Installation (optional)

```bash
$ git clone https://github.com/Ancieg/alt-query-branch && cd alt-query-branch
$ pip install .
```

# Usage

```bash
usage: alt-query-branch [-h] [-b BRANCH] [-a ARCHES] [-e] [-s] [-o FILE] expression

positional arguments:
  expression

options:
  -h, --help            show this help message and exit
  -b BRANCH, --branch BRANCH
  -a ARCHES, --arches ARCHES
  -e, --exact
  -s, --stdout
  -o FILE, --file FILE
```

**Also you can use `alt-query-branch.py` script without package installation.**

# Usage as a module
Example (like inside `alt-query-branch.py` script):
```python
from alt_query_branch.algorithms import search_matching_packages, order_packages
from alt_query_branch.rdb import branch_binary_packages_with_source_package

# Fetch all of the branch binary packages.
branch_packages = branch_binary_packages_with_source_package('p10')

# Find matching packages: search inexact 'fuzz' in arches 'noarch' and 'armh'.
packages = search_matching_packages(branch_packages, 'fuzz', arches=['noarch', 'armh'])

# Group by sources packages and sort (sources and arches).
ordered_packages = order_packages(packages)
```
Also you can manage caching:
```python
# Enable caching with arguments.
alt_query_branch.enable_caching(
    path='~/.cache/alt-query-branch', backend='sqlite', lifetime=300
)

# Disable caching.
alt_query_branch.disable_caching()
```
# Output JSON schema

```json
{
  "expression": "string",                    # your expression
  "exactness": "string",                     # 'exact'/'inexact'
  "branch": "string",                        # 'p9', 'p10' or 'sisyphus'
  "arches": "string | comma-separated list"  # 'all' or, by example, 'armh,i586'
  "packages": [
    {
      "source": "string",       # source package's name
      "binaries": [
        {
          "name": "string",     # binary package's name
          "epoch": int,
          "version": "string",
          "release": "string",
          "arch": "string",
          "disttag": "string",
          "buildtime": int
        }
      ]
    }
  ]
}
```

# Architeсtures order

* `noarch`
* `x86_64`
* `i586`
* `armh`
* `aarch64`
* `ppc64le`

# Examples

Find all fuzzers in `p10` for `ppc64le` and `armh`(`jq` used for more pretty output):
```bash
$ ./alt-query-branch.py -b p10 -s -a ppc64le,armh fuzz | jq .
```
(there are many packages, so I don't show them :) ).

Find all `.*lsp-server.*` packages in `sisyphus` for `noarch`:
```bash
$ ./alt-query-branch.py -b sisyphus -s .*lsp-server.* -a noarch | jq .
```
output:
```json
{
  "expression": ".*lsp-server.*",
  "exactness": "inexact",
  "branch": "sisyphus",
  "arches": [
    "noarch"
  ],
  "packages": [
    {
      "source": "python3-module-python-lsp-server",
      "binaries": [
        {
          "name": "python3-module-python-lsp-server",
          "epoch": 0,
          "version": "1.7.0",
          "release": "alt1",
          "arch": "noarch",
          "disttag": "sisyphus+312866.100.1.1",
          "buildtime": 1672864445
        }
      ]
    }
  ]
}
```

# Authors

* idea: Danil Shein <dshein@altlinux.org>;
* initiator: Anton Farygin <rider@altlinux.org>;
* programmer: Anton Zhukharev <ancieg@altlinux.org>.

# License

The program is distributed under the MIT license.
See `LICENSE` file for more information.
