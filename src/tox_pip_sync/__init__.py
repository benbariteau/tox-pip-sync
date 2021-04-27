import pluggy

from tox_pip_sync._pip_sync import pip_sync

hookimpl = pluggy.HookimplMarker("tox")


@hookimpl
def tox_testenv_install_deps(venv, action):
    """Perform install dependencies action for this venv."""

    # Call our pip sync method instead of the usual way to install dependencies
    pip_sync(venv, action)
    venv.pip_synced = True

    # Let tox know we've handled this case
    return True


@hookimpl
def tox_runtest_pre(venv):
    """Perform arbitrary action after running tests for this venv."""

    # Note: None of this gets called for `.tox/.tox`, so we are using default
    # behavior for the venv tox installs itself into. On the other side, you
    # can't specify anything using versions, referring to files etc. for the
    # direct tox dependencies anyway: they are always plain unpinned
    # dependencies.

    if not getattr(venv, "pip_synced", False):
        # `tox_testenv_install_deps` does not get called every time we run tox
        # so assuming we've not run before, we should make sure we have
        tox_testenv_install_deps(venv=venv, action=venv.new_action("pip-sync"))
