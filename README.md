# pre-commit-yamlpolicy
pre-commit hooks to deny commits which don't conform to organizational YAML
usage policies.

See also: <https://github.com/pre-commit/pre-commit>

### Using pre-commit-yamlpolicy with pre-commit

Add this to your `.pre-commit-config.yaml`

```yaml
-   repo: https://github.com/eitrtechnologies/pre-commit-yamlpolicy
    rev: v1.0.0  # Use the ref you want to point to
    hooks:
    -   id: disallowunquoted
```

### Hooks Available

#### `disallowunquoted`
Deny commits where certain YAML values are found but not quoted.
  - `--values` - Specify a comma-separated list of YAML values to disallow.
    Defaults to `on,off,yes,no,y,n`.
  - `--case-sensitive` - Flag to turn off case insensitivity when searching for
    values. Operation defaults to ignore case.
