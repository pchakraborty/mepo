import os
import io
import shutil
import contextlib
from types import SimpleNamespace

try:
    from contextlib import chdir as contextlib_chdir
except ImportError:
    from mepo.utilities.chdir import chdir as contextlib_chdir

import mepo.command.clone as mepo_clone
import mepo.command.status as mepo_status


FIXTURE_NAME = "GEOSfvdycore-mepo-testing"
FIXTURE_URL = f"https://github.com/pchakraborty/{FIXTURE_NAME}.git"
TEST_DIR = os.path.dirname(os.path.realpath(__file__))


def get_mepo_status():
    args = SimpleNamespace(
        ignore_permissions=False,
        nocolor=True,
        hashes=False,
        parallel=False,
    )
    with contextlib.redirect_stdout(io.StringIO()) as output:
        mepo_status.run(args)
    return output.getvalue()


def test_mepo_clone_url():
    if os.path.isdir(FIXTURE_NAME):
        shutil.rmtree(FIXTURE_NAME)
    args = SimpleNamespace(
        style="prefix",
        registry=None,
        url=FIXTURE_URL,
        branch=None,
        directory=None,
        partial="blobless",
        allrepos=False,
    )
    mepo_clone.run(args)
    saved_output = """Checking status...
GEOSfvdycore           | (b) main
env                    | (t) v4.29.1 (DH)
cmake                  | (t) v3.55.0 (DH)
ecbuild                | (t) geos/v1.4.0 (DH)
GMAO_Shared            | (t) v1.9.9 (DH)
GEOS_Util              | (t) v2.1.3 (DH)
FMS                    | (t) geos/2019.01.02+noaff.10 (DH)
FVdycoreCubed_GridComp | (t) v2.12.0 (DH)
fvdycore               | (t) geos/v2.9.1 (DH)
mom6                   | (t) geos/v3.3 (DH)
"""
    with contextlib_chdir(FIXTURE_NAME):
        status_output = get_mepo_status()
    assert status_output == saved_output
    shutil.rmtree(FIXTURE_NAME)


def test_mepo_clone_url_branch_directory():
    DIRECTORY = "clone_url_branch_directory"
    if os.path.isdir(DIRECTORY):
        shutil.rmtree(DIRECTORY)
    args = SimpleNamespace(
        style="postfix",
        registry=None,
        url=FIXTURE_URL,
        branch="fvdycore-develop",
        directory=DIRECTORY,
        partial="blobless",
        allrepos=False,
    )
    mepo_clone.run(args)
    saved_output = """Checking status...
GEOSfvdycore           | (b) fvdycore-develop
env                    | (t) v4.29.1 (DH)
cmake                  | (t) v3.55.0 (DH)
ecbuild                | (t) geos/v1.4.0 (DH)
GMAO_Shared            | (t) v1.9.9 (DH)
GEOS_Util              | (t) v2.1.3 (DH)
FMS                    | (t) geos/2019.01.02+noaff.10 (DH)
FVdycoreCubed_GridComp | (b) develop
fvdycore               | (b) geos/develop
"""
    with contextlib_chdir(DIRECTORY):
        status_output = get_mepo_status()
    assert status_output == saved_output
    shutil.rmtree(DIRECTORY)


def test_mepo_clone_url_branch_allrepos():
    if os.path.isdir(FIXTURE_NAME):
        shutil.rmtree(FIXTURE_NAME)
    args = SimpleNamespace(
        style="prefix",
        registry=None,
        url=FIXTURE_URL,
        branch="mepo-testing-do-not-delete",
        directory=None,
        partial="blobless",
        allrepos=True,
    )
    mepo_clone.run(args)
    saved_output = """Checking status...
GEOSfvdycore           | (b) mepo-testing-do-not-delete
env                    | (b) mepo-testing-do-not-delete
cmake                  | (b) mepo-testing-do-not-delete
ecbuild                | (b) mepo-testing-do-not-delete
GMAO_Shared            | (b) mepo-testing-do-not-delete
GEOS_Util              | (b) mepo-testing-do-not-delete
FMS                    | (b) mepo-testing-do-not-delete
FVdycoreCubed_GridComp | (b) mepo-testing-do-not-delete
fvdycore               | (b) mepo-testing-do-not-delete
"""
    with contextlib_chdir(FIXTURE_NAME):
        status_output = get_mepo_status()
    assert status_output == saved_output
    shutil.rmtree(FIXTURE_NAME)


def test_mepo_clone_url_external_registry():
    if os.path.isdir(FIXTURE_NAME):
        shutil.rmtree(FIXTURE_NAME)
    args = SimpleNamespace(
        style="prefix",
        registry=os.path.join(TEST_DIR, "input/external-components.yaml"),
        url=FIXTURE_URL,
        branch="mepo-testing-do-not-delete",
        directory=None,
        partial="blobless",
        allrepos=False,
    )
    mepo_clone.run(args)
    saved_output = """Checking status...
GEOSfvdycore           | (b) mepo-testing-do-not-delete
   | components.yaml: \x1b[31mmodified, not staged\x1b[0m
env                    | (t) v4.29.1 (DH)
cmake                  | (t) v3.55.0 (DH)
ecbuild                | (t) geos/v1.4.0 (DH)
GMAO_Shared            | (b) mepo-testing-do-not-delete
GEOS_Util              | (t) v2.1.3 (DH)
FMS                    | (t) geos/2019.01.02+noaff.10 (DH)
FVdycoreCubed_GridComp | (b) develop
fvdycore               | (b) geos/develop
"""
    with contextlib_chdir(FIXTURE_NAME):
        status_output = get_mepo_status()
    assert status_output == saved_output
    shutil.rmtree(FIXTURE_NAME)
