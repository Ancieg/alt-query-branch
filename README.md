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

# Installation

```bash
$ git clone https://github.com/Ancieg/alt-query-branch && cd alt-query-branch
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -U pip setuptools
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

# Usage as a module
Example:
```python
import alt_query_branch
alt_query_branch.search_matching_packages('python3-modules', exact=False, branch='p10', arches=['noarch', 'armh'])
```

# Output JSON schema

```json
{
    "expression": "<your request>",
    "exactness": "< exact/inexact >",
    "branch": "< sisyphus/p10/p9 >",
    "arches": "< comma-separated list of queried architectures >",
    "packages": [
    	{
	    "source": "<source package name>",
	    "binaries": [
              {
                "name": "<bin name>",
                "epoch": <epoch>,
                "version": "<version>",
                "release": "<release>",
                "arch": "<architecture>",
                "disttag": "<disttag>",
                "buildtime": <build time>
              },
		    ...
	    ]
	},
        ...
    ]
}
```

# Architetures order

* `noarch`
* `x86_64`
* `i586`
* `armh`
* `aarch64`
* `ppc64le`

# Examples

Find all fuzzers in `p10` for `ppc64le` and `armh`(`jq` used for more pretty output):
```bash
$ alt-query-branch -b p10 -s -a ppc64le,armh fuzz | jq .
```
(there are many packages, so I don't show them :) ).

Find all `.*lsp-server.*` packages in `sisyphus` for `noarch`:
```bash
$ alt-query-branch -b sisyphus -s .*lsp-server.* -a noarch | jq .
```
output:
```json
{
  "asked": ".*lsp-server.*",
  "type": "inexact",
  "found": [
    {
      "source": "python3-module-python-lsp-server",
      "binaries": [
        {
          "arch": "noarch",
          "name": "python3-module-python-lsp-server"
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
