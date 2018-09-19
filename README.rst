============================
pyramid-cookiecutter-starter
============================

.. image:: https://travis-ci.org/Pylons/pyramid-cookiecutter-starter.png?branch=master
        :target: https://travis-ci.org/Pylons/pyramid-cookiecutter-starter
        :alt: Master Travis CI Status

A Cookiecutter (project template) for creating a Pyramid starter project using URL dispatch. Customizable options upon install are Jinja2, Chameleon, or Mako for templating and memory, SQLAlchemy, or ZODB for a persistent backend.

Requirements
------------

* Python 2.7 or 3.4+
* `cookiecutter <https://cookiecutter.readthedocs.io/en/latest/installation.html>`_

Versions
--------

This cookiecutter has several branches to support new features in Pyramid or avoid incompatibilities.

* ``latest`` aligns with the latest stable release of Pyramid, and is the default branch on GitHub.
* ``master`` aligns with the ``master`` branch of Pyramid, and is where development takes place.
* ``x.y-branch`` aligns with the ``x.y-branch`` branch of Pyramid.


Usage
-----

1.  Generate a Pyramid project, following the prompts from the command.

    .. code-block:: bash

        $ cookiecutter gh:Pylons/pyramid-cookiecutter-starter

    Optionally append a specific branch checkout to the command:

    .. code-block:: bash

        $ cookiecutter gh:Pylons/pyramid-cookiecutter-starter --checkout master

2.  Finish configuring the project by creating a virtual environment and installing your new project. These steps are output as part of the cookiecutter command above and are slightly different for Windows.

    .. code-block:: bash

        # Change directory into your newly created project.
        $ cd myproj
        # Create a virtual environment...
        $ python3 -m venv env
        # ...where we upgrade packaging tools...
        $ env/bin/pip install --upgrade pip setuptools
        # ...and into which we install our project and its testing requirements.
        $ env/bin/pip install -e ".[testing]"

**Note:** *If you are not running the SQLAlchemy backend, please skip to step 5*

3.  Initialize and upgrade the database using Alembic.

    .. code-block:: bash

        # Generate your first revision.
        $ env/bin/alembic -c development.ini revision --autogenerate -m "init"
        # Upgrade to that revision.
        $ env/bin/alembic -c development.ini upgrade head

4.  Load default data into the database using a script.

    .. code-block:: bash

        $ env/bin/initialize_tutorial_db development.ini

5.  Run your project's tests.

    .. code-block:: bash

        $ env/bin/pytest

6.  Run your project.

    .. code-block:: bash

        $ env/bin/pserve development.ini
