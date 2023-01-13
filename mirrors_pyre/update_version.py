"""
Update new versions of `pyre-check` - modify `.version`, `.pre-commit-hooks.yaml` and
 `setup.py` when new versions are released.
Scripts are based on `pre-commit-mirror-maker` package scripts. See
 https://github.com/pre-commit/pre-commit-mirror-maker for details.
"""
import json
import os
import subprocess
from pre_commit_mirror_maker.languages import ADDITIONAL_DEPENDENCIES
from pre_commit_mirror_maker.languages import LIST_VERSIONS
from pre_commit_mirror_maker.make_repo import format_files


def _commit_version(
        repo: str, *,
        language: str,
        version: str,
        **fmt_vars: str,
) -> None:
    # 'all' writes the .version and .pre-commit-hooks.yaml files
    for lang in ('all', language):
        src = os.path.join(os.path.dirname(__file__), lang)
        format_files(src, repo, language=language, version=version, **fmt_vars)

    hooks_yaml = os.path.join(repo, 'hooks.yaml')
    if os.path.exists(hooks_yaml):
        os.remove(hooks_yaml)

    def git(*cmd: str) -> None:
        subprocess.check_call(('git', '-C', repo) + cmd)

    # Commit and tag
    git('add', '.')
    git('commit', '-m', f'Mirror: {version}')
    git('tag', f'v{version}')


def make_repo(repo: str, *, language: str, name: str, **fmt_vars: str) -> None:
    assert os.path.exists(os.path.join(repo, '.git')), repo

    package_versions = LIST_VERSIONS[language](name)
    version_file = os.path.join(repo, '.version')
    if os.path.exists(version_file):
        previous_version = open(version_file).read().strip()
        previous_version_index = package_versions.index(previous_version)
        versions_to_apply = package_versions[previous_version_index + 1:]
    else:
        versions_to_apply = package_versions

    for version in versions_to_apply:
        if language in ADDITIONAL_DEPENDENCIES:
            additional_dependencies = ADDITIONAL_DEPENDENCIES[language](
                name,
                version,
            )
        else:
            additional_dependencies = []

        _commit_version(
            repo,
            name=name,
            language=language,
            version=version,
            additional_dependencies=json.dumps(additional_dependencies),
            **fmt_vars,
        )
        
if __name__ == "__main__":
    make_repo(
        os.getcwd(),
        name="pyre-check",
        description="Static type checking with `pyre-check`."
    ,
        language="python",
        entry="pyre check",
        id="pyre-check",
        match_key="types_or",
        match_val="[python, pyi]",
        args=json.dumps(()),
        require_serial=json.dumps(False),
        pass_filenames=json.dumps(False),
        minimum_pre_commit_version="2.9.2",
    )