# pre-commit-yamlpolicy
pre-commit hooks to deny commits which don't conform to organizational YAML
usage policies.

See also: <https://github.com/pre-commit/pre-commit>

### Using pre-commit-yamlpolicy with pre-commit

Add this to your `.pre-commit-config.yaml`

```yaml
repos:
- repo: https://github.com/eitrtechnologies/pre-commit-yamlpolicy
  rev: v1.2.0  # Use the ref you want to point to
  hooks:
    - id: bannedk8skinds
    - id: disallowunquoted
    - id: valueregex
      jmespath: '*.matchers[].match'
      regex: '\([^ ]|[^ ]\)'
```

### Hooks Available

#### `bannedk8skinds`
Deny commits of certain Kubernetes object types.
  - `--allow-multiple-documents` - allow yaml files which use the
    [multi-document syntax](http://www.yaml.org/spec/1.2/spec.html#YAML)
  - `--kinds` - Specify a comma-separated list of
    [Kubernetes object types](https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds)
    which will be denied in a commit to the repo. Defaults to `Secret`

#### `disallowunquoted`
Deny commits where certain YAML values are found but not quoted.
  - `--values` - Specify a comma-separated list of YAML values to disallow.
    Defaults to `on,off,yes,no,y,n`.
  - `--case-sensitive` - Flag to turn off case insensitivity when searching for
    values. Operation defaults to ignore case.

#### `valueregex`
Deny commits where certain YAML values are found and match a given regex. A
JMESPath query is used in conjunction with a regular expression to match string
values in YAML.
  - `--jmespath` - [JMESPath expression](https://jmespath.org/) which returns
    the values to run a regex against. *REQUIRED*
  - `--regex` - Regex which will cause the hook to fail if it matches any of the
    values returned by the JMESPath query. *REQUIRED*
  - `--allow-multiple-documents` - Allow YAML files which use the
    [multi-document syntax](http://www.yaml.org/spec/1.2/spec.html#YAML)
