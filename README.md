# pyre mirror

Mirror of `pyre-check` for pre-commit.

For `pre-commit`, see [github.com/pre-commit/pre-commit](https://github.com/pre-commit/pre-commit). For `pyre-check`, see [github.com/facebook/pyre-check](https://github.com/facebook/pyre-check).

## Using pyre with pre-commit

### Pyre configuration

Add this to your project root

```json
{
  "site_package_search_strategy": "pep561",
  "source_directories": [
    "."
  ],
  "ignore_all_errors": [
    ".venv/"  // ignore files from this directory - virtual environments, etc.
  ]
}
```

### Pre-commit configuration

Add this to your `.pre-commit-config.yaml`

```yaml
-   repo: https://github.com/murilo-cunha/mirrors-pyre
    rev: v0.9.17  # Use the sha/tag you want to point at
    hooks:
    -   id: pyre-check
```