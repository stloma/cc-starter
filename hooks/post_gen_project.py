import os
import sys
import shutil
from textwrap import dedent

WORKING = os.path.abspath(os.path.join(os.path.curdir))


def main():
    clean_unused_template_settings()
    clean_unused_backend()
    display_actions_message()


def clean_unused_template_settings():
    selected_lang = '{{ cookiecutter.template_language }}'
    templates = os.path.join(
        WORKING, '{{cookiecutter.repo_name}}', 'base_templates')

    if selected_lang == 'chameleon':
        extension = '.pt'
    else:
        extension = "." + selected_lang
    delete_other_ext(templates, extension)


def delete_other_ext(directory, extension):
    """
    Removes all files not ending with the extension.
    """
    for template_file in os.listdir(directory):
        if not template_file.endswith(extension):
            os.unlink(os.path.join(directory, template_file))


def clean_unused_backend():
    selected_backend = '{{ cookiecutter.backend }}'

    if selected_backend == 'none':
        prefix = None
        rm_prefixes = ['sqlalchemy_', 'zodb_']
    elif selected_backend == 'sqlalchemy':
        prefix = 'sqlalchemy_'
        rm_prefixes = ['zodb_']
    elif selected_backend == 'zodb':
        prefix = 'zodb_'
        rm_prefixes = ['sqlalchemy_']

    scaffold_directory = os.path.join(
                WORKING, '{{cookiecutter.repo_name}}')

    delete_other_files(scaffold_directory, prefix, rm_prefixes)


def delete_other_files(directory, current_prefix, rm_prefixes):
    """
    Each backend has associated files in the cookiecutter, prefixed by it's
    name. Additionally, there is a base_ prefix that gets included no matter
    the selection. Here, we rename or remove these prefixes based on the
    selected backend.
    """
    for filename in os.listdir(directory):
        full_path = os.path.join(directory, filename)

        base_prefix = 'base_'
        if filename.startswith(base_prefix):
            filename = filename[len(base_prefix):]
            os.rename(full_path, os.path.join(directory, filename))

        for rm_prefix in rm_prefixes:

            if filename.startswith(rm_prefix):

                if os.path.isdir(full_path):
                    shutil.rmtree(full_path)
                else:
                    os.unlink(full_path)

            elif current_prefix and filename.startswith(current_prefix):
                filename = filename[len(current_prefix):]
                os.rename(full_path, os.path.join(directory, filename))


def display_actions_message():
    WIN = sys.platform.startswith('win')

    venv = 'env'
    if WIN:
        venv_cmd = 'py -3 -m venv'
        venv_bin = os.path.join(venv, 'Scripts')
    else:
        venv_cmd = 'python3 -m venv'
        venv_bin = os.path.join(venv, 'bin')

    env_setup = dict(
        separator='=' * 79,
        venv=venv,
        venv_cmd=venv_cmd,
        pip_cmd=os.path.join(venv_bin, 'pip'),
        pytest_cmd=os.path.join(venv_bin, 'pytest'),
        pserve_cmd=os.path.join(venv_bin, 'pserve'),
        {%- if cookiecutter.backend == 'sqlalchemy' %}
        alembic_cmd=os.path.join(venv_bin, 'alembic'),
        init_cmd=os.path.join(
            venv_bin, 'initialize_{{ cookiecutter.repo_name }}_db'),
        {% endif %}
    )
    msg = dedent(
        """
        %(separator)s
        Documentation: https://docs.pylonsproject.org/projects/pyramid/en/latest/
        Tutorials:     https://docs.pylonsproject.org/projects/pyramid_tutorials/en/latest/
        Twitter:       https://twitter.com/PylonsProject
        Mailing List:  https://groups.google.com/forum/#!forum/pylons-discuss
        Welcome to Pyramid.  Sorry for the convenience.
        %(separator)s

        Change directory into your newly created project.
            cd {{ cookiecutter.repo_name }}

        Create a Python virtual environment.
            %(venv_cmd)s %(venv)s

        Upgrade packaging tools.
            %(pip_cmd)s install --upgrade pip setuptools

        Install the project in editable mode with its testing requirements.
            %(pip_cmd)s install -e ".[testing]"

        {% if cookiecutter.backend == 'sqlalchemy' -%}
        Migrate the database using Alembic.
            # Generate your first revision.
            %(alembic_cmd)s -c development.ini revision --autogenerate -m "init"
            # Upgrade to that revision.
            %(alembic_cmd)s -c development.ini upgrade head
            # Load default data.
            %(init_cmd)s development.ini

        {% endif -%}
        Run your project's tests.
            %(pytest_cmd)s

        Run your project.
            %(pserve_cmd)s development.ini
        """ % env_setup)
    print(msg)


if __name__ == '__main__':
    main()
