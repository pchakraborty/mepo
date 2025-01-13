# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

### Added

### Changed

## [2.3.0] - 2025-01-12

### Changed

- Moved `mepo status` and `mepo restore-state` to default to their serial variants rather than parallel by default. At the same time, we remove the `--serial` option from these commands and add a `--parallel` option if users want to run them in parallel.

- `mepo init` is deprecated. Running `mepo init` will issue the warning "init will be removed in version 3, use clone instead"

## [2.2.1] - 2025-01-03

### Fixed

- Fixed bugs in the lesser used options of `mepo clone`, `allrepos` and `registry`

### Added

- Added tests for `mepo clone --allrepos` and `mepo clone --registry`

## [2.2.0] - 2024-12-24

### Added

- Hidden option `--location` for mepo that returns the path to the mepo directory
- Added ability to print number of stashes in `mepo status`
- Added new tests for `mepo clone`

### Changed

- Removed legacy `bin` directory
- Checked out branches are no longer in 'detached head' state

## [2.1.0] - 2024-10-02

### Fixed

- Fixed mepo completion

### Added

- Added ability to print version info via `mepo --version`
- Added install instructions for spack and brew tap
- Added tests for Registry and MepoComponent classes

### Changed

- Full path of remote url is now stored in the state file
- Some refactor of component.py
- Removed MepoState dependency in git.py

## [2.0.0] - 2024-08-12

### Fixed

### Added

- Added `pyproject.toml` to aid with `pip` installation.

- Engineering
  -- Formatting with Black
  -- Linting with Pylint
  -- Dependency management and packaging with Rye

- Added tests to cover more `mepo` commands

- Add new command `update-state` to permanently convert mepo1 style state to mepo2

### Changed

- Converted `mepo` to a Python project via the following renaming
  -- Added `src/mepo/__init__.py`
  -- Renamed `mepo.d` -> `src/mepo`
  -- Renamed `mepo.d/utest` -> `tests`
  -- Renamed `doc` --> `docs`
  -- A `mepo` config file is now called a `mepo` registry
  -- More code reorganization

- Helper script `mepo`, used for development, moved to the `bin` directory.
- Added README for `docs/make_md_docs.py` script

- State: pickle format (mepo1 style) to json format (mepo2 style)
  -- If mepo1 style state is detected, print warning and suggest running `mepo update-state`

## [1.52.0] - 2024-01-10

### Added

- Added new `--partial` option to `mepo clone` with two settings: `off`, `blobless`, and `treeless`. If you set, `--partial=blobless` then
  the clone will not download blobs by using `--filter=blob:none`. If you set `--partial=treeless` then the clone will not download
  trees by using `--filter=tree:0`. The `blobless` option is useful for large repos that have a lot of binary files that you don't
  need. The `treeless` option is even more aggressive and *SHOULD NOT* be used unless you know what you are doing. The
  `--partial=off` option allows a user to override the default behavior of `--partial` in `.mepoconfig` and turn it off for a
  run of `mepo clone`.
- Add a new section for `.mepoconfig` to allow users to set `--partial` as a default for `mepo clone`.

## [1.51.1] - 2023-08-25

### Fixed

- Fixes to allow mepo to work on older mepo clones that don't have ignore_submodules in their state

## [1.51.0] - 2023-08-25

### Added

- Added new `ignore_submodules` field in `components.yaml` to allow ignoring submodules in a repo. Currently used for `status` and
  `diff` commands.

## [1.50.0] - 2023-08-17

### Added

- Command `status` has now a `--hashes` option that list current HEAD hash for each component.

## [1.49.0] - 2023-01-25

### Changed

- When running `compare` in default mode, size columns based on the longest branch name of a repo that has changed. This prevents
  odd column widths based on long branch names in repos that haven't changed

## [1.48.0] - 2022-12-09

### Added

- Added new `reset` command to reset a mepo clone

### Changed

- Updated GitHub Actions

## [1.47.0] - 2022-11-14

### Added

- Added ability to do `mepo tag push --delete` so you can delete a tag on the remote

## [1.46.0] - 2022-10-18

### Added

- Add new `changed-files` command to list all changed files vs original state

## [1.45.0] - 2022-08-10

### Changed

- Allow `checkout-if-exists` to work on tags or branches

## [1.44.0] - 2022-04-28

### Fixed

- Add support for typechange in `mepo status`

## [1.43.0] - 2022-04-18

### Fixed

- Fixed issue where you could issue `mepo clone` in already cloned multirepos (#224)

### Changed

- Changed StateDoesNotExistError and StateAlreadyInitializedError to be subclasses of `SystemExit`
- Changed some git subcommands to use full local path

## [1.42.0] - 2022-03-29

### Added

- Added `-b/--ignore-space-change` option to `mepo diff`

## [1.41.0] - 2022-03-25

### Changed

- Changed the default behavior of `compare` to only show differing repos. Use `--all` to see all repos
- Add `--nocolor` option to `status` and `compare` (for unit testing)
- Add `--wrap` option to `compare` (for unit testing)
- Updated unit tests for new `compare` behavior

## [1.40.0] - 2022-01-12

### Fixed

- Fixed the output of `mepo compare` to handle detached branch hashes

### Added

- Added `--ignore-case` option to `mepo whereis`

### Changed

- Updated `mepo-cd` functions and aliases to use ignore-case variant of `mepo whereis --ignore-case` by default
  - This allows for simpler use of `mepo-cd` as you don't have to exactly match the name of a component

## [1.39.0] - 2022-01-07

### Added

- Added `--ignore-permissions` flag to `status` and `diff` to allow the commands to ignore permissions changes
- Add `--name-status` flag to `mepo diff`

### Changed

- When running `mepo compare` and `mepo status`, detatched branches will also display the commit id:

  ```
  GEOSgcm_GridComp       | (b) feature/aogcm (DH, 0793f7b2)
  ```

- GitHub Actions updates
  - Uses `pypy-3.8` specifically
  - Have `pip` install from `requirements.txt`

## [1.38.0] - 2021-09-10

### Added

- Added `CHANGELOG.md`
- Added changelog enforcer

### Changed

- Detach branches on clone

## [1.37.1] - 2021-09-02

### Fixed

- Fix for `mepo save`

## [1.37.0] - 2021-08-19

### Added

- Allows `mepo checkout -b <branch>` to run on all repos rather than requiring one to be specified

### Fixed

- Fixes a bug in handling paths with spaces in folder names

## [1.36.1] - 2021-08-19

### Changed

- Make the `mepo pull` and `mepo pull-all` commands verbose by default
  - The older, quieter behavior can be gotten by adding the new `--quiet` option to `pull` and `pull-all`

## [1.36.0] - 2021-06-23

### Fixed

- Fix bug in `mepo save`

### Added

- Allow use of `hash:` key in `components.yaml`

## [1.35.0] - 2021-06-10

### Changed

- Allow `checkout` on all repos

## [1.34.1] - 2021-06-10

### Fixed

- Fix bug in `tag` subcommand

## [1.34.0] - 2021-05-27

### Changed

- The `fetch-all` command is removed and "subsumed" into the `fetch` command.

- The `push-all` command was removed

### Added

- Add script that aids in making the [Mepo Commands](https://github.com/GEOS-ESM/mepo/wiki/Mepo-Commands) wiki page. For Markdown reasons, some of the Argparse parsers had to be changed to better work with Markdown syntax.

## [1.33.0] - 2021-05-26

### Fixed

- Obey config file for no style. Previously, if no style was passed into mepo, by default it chose prefix. This is fine for GEOSgcm, etc. but broke MAPL which uses naked.  For now, if no style is found passed in on the command line or in `.mepoconfig` assume what is in `components.yaml` is the correct sytle.

## [1.32.0] - 2021-05-25

### Changes

- Changes to tag subcommand
  - `mepo tag push` instead of `mepo push --tags`

## [1.31.0] - 2021-05-25

### Added

- Add mepo style support
- Add support for `.mepoconfig` file
- Created `mepo push-all`

### Changed

- Allow `mepo tag create` and `mepo tag delete` to work on all components

### Fixed

- Fixes to `mepo status`

## [1.30.1] - 2021-03-30

### Added

- Added `-q` flag for commands with `--quiet`

## [1.30.0] - 2021-03-30

### Changed

- Detect illegal `components.yaml`
- Added useful prints to `checkout` and `develop`

## [1.29.1] - 2021-03-19

### Changed

- Clean up for `mepo save`

## [1.29.0] - 2021-03-16

### Fixed

- Fix for `mepo clone`
- Fixes for `status` and `compare`

## [1.28.1] - 2021-01-05

### Fixed

- Fix bug in `mepo status`
- Clean up odd `save` issue

## [1.28.0] - 2020-11-20

### Added

- Add `mepo commit -a`

## [1.27.1] - 2020-11-20

### Fixed

- Fixed bug when doing `mepo clone URL` *without* `--config`.

## [1.27.0] - 2020-11-20

### Fixed

- Fix for using `config` with "all-in-one" clone

## [1.26.0] - 2020-11-17

### Added

- Added `--force` flag for `fetch` and `fetch-all`

## [1.25.0] - 2020-11-12

### Added

- Add `--staged` option to `mepo diff`

## [1.24.0] - 2020-11-09

### Fixed

- Fix for fixture initialization

## [1.23.1] - 2020-10-30

### Fixed

- Fixed bug for CI systems

## [1.23.0] - 2020-10-30

### Added

- Add ability to see fixture (see release notes for more)

## [1.22.0] - 2020-10-30

### Added

- Add `mepo-cd.csh`

## [1.21.1] - 2020-10-30

### Fixed

- Fixes for `whereis` and `diff`

## [1.21.0] - 2020-10-28

### Fixed

- Updates to allow mepo clones to be moved (#106)
- A bit of nicety on `mepo status` for detatched HEAD states
- Adds `mepo-cd.zsh` as I couldn't figure out how to get the bash script to work in zsh

## [1.20.1] - 2020-10-07

### Fixed

- Bug fixes for `mepo save`
  - The command would save the new yaml file in `pwd` rather than at the "root" directory where the original was. This was a bit confusing, so the command now saves at root level
  - `mepo save` did not handle hashes well. There is no reason it couldn't save to a hash, but it labeled it as a `branch` in the yaml file which, while not broken, was in consistent.

## [1.20.0] - 2020-09-01

### Added

- Add `dry-run` for `checkout-if-exists`

## [1.19.0] - 2020-08-26

### Added

- Add per-repo diff

## [1.18.0] - 2020-08-19

### Added

- Added `mepo tag` commands
- Added `.zenodo.json` file

### Changed

- Update `mepo branch list` to work on one or more repos

## [1.17.0] - 2020-08-18

### Added

- Add `restore-state` command
  - Note: at present this will restore *EVERYTHING* to the previous state. Not a repo here or there.

## [1.16.0] - 2020-07-17

### Added

- Add `pull`, `pull-all` and `fetch-all`

### Fixed

- Fix `.mepo` file on Darwin

## [1.15.0] - 2020-07-14

### Changed

- Updates to `clone` command

## [1.14.1] - 2020-07-08

### Fixed

- Fix for `mepo push`

## [1.14.0] - 2020-06-23

### Added

- Add `mepo stash`

## [1.13.0] - 2020-06-15

### Changed

- Updates for `clone` and `fetch` commands

### Fixes

- `mepo status` won't crash if a repo is not on a tag or branch

## [1.12.0] - 2020-06-01

### Changed

- Update the CI to use a matrix on Linux and macOS of python3.x and pypy3

### Fixed

- Fix the unit tests

## [1.11.0] - 2020-05-28

### Added

- Add license

## [1.10.1] - 2020-05-27

### Fixed

- Fix bad shebang

## [1.10.0] - 2020-05-27

### Changed

- Add to `mepo-cd` functionality

## [1.9.0] - 2020-04-07

### Added

- Add `mepo fetch` and `mepo fetch --all` ability.

## [1.8.0] - 2020-03-04

### Changed

- Add ability for single editor for multi-repo commit

## [1.7.0] - 2020-03-03

### Added

- Add `--name-only` to `mepo diff`
- Add colors to `mepo status` for non-original branches
- Make `checkout-if-exists` more verbose
- Make `mepo commit` act more like `git commit`

## [1.6.0] - 2020-02-19

### Added

- Add `checkout-if-exists` capability

## [1.5.0] - 2020-02-07

### Added

- Add ability to work with symlinks

## [1.4.0] - 2020-01-28

### Added

- Add the ability to have `recurse_submodules:` in the YAML file.

## [1.3.0] - 2020-01-16

### Added

- Add `mepo diff` command
- Add `CODEOWNERS`

## [1.2.0] - 2020-01-09

### Changed

- Updates to `status` and `compare`

### Added

- Add `mepo-cd` bash function

## [1.1.0] - 2019-12-19

### Added

- Add GitHub Action for unit tests
- Add README
- Add `develop` command

### Changed

- Lots of updates to internals

## [1.0.0] - 2019-12-08

### Changed

- Initial release of mepo

## [0.4] - 2019-11-12

### Added

- Add stage and unstage

## [0.3] - 2019-11-06

### Added

- Add init, clone, status, checkout, branch, diff, where, whereis, history, stage

## [0.2] - 2019-11-01

### Added

- Add init, clone, status, checkout, branch, diff, where

## [0.1] - 2019-10-28

### Added

- Add checkout and status
