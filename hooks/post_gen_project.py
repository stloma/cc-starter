import os
import sys
import shutil
from textwrap import dedent

working = os.path.abspath(os.path.join(os.path.curdir))


def main():
    clean_unused_template_settings()
    clean_unused_backend()
    display_actions_message()


def clean_unused_template_settings():
    selected_lang = '{{ cookiecutter.template_language }}'
    templates = os.path.join(
        working, '{{cookiecutter.repo_name}}', 'base_templates')

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
    base_prefix = 'base_'

    if selected_backend == 'none':
        prefix = None
        rm_prefixes = ['sqlalchemy_', 'zodb_']
    elif selected_backend == 'sqlalchemy':
        prefix = 'sqlalchemy_'
        rm_prefixes = ['zodb_']
    elif selected_backend == 'zodb':
        prefix = 'zodb_'
        rm_prefixes = ['sqlalchemy_']

    w_dir = os.path.join(
                working, '{{cookiecutter.repo_name}}')

    for folder in os.listdir(w_dir):
        full_path = os.path.join(w_dir, folder)
        if folder.startswith(base_prefix):
            folder = folder[len(base_prefix):]
            os.rename(full_path, os.path.join(w_dir, folder))
        for rm_prefix in rm_prefixes:
            if folder.startswith(rm_prefix):
                shutil.rmtree(full_path)
            elif prefix and folder.startswith(prefix):
                folder = folder[len(prefix):]
                os.rename(full_path, os.path.join(w_dir, folder))


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
        {% if cookiecutter.backend == 'sqlalchemy' %}
        Configure the database:
            %(init_cmd)s development.ini
        {% endif %}
        Run your project's tests.
            %(pytest_cmd)s

        Run your project.
            %(pserve_cmd)s development.ini
        """ % env_setup)
    print(msg)


if __name__ == '__main__':
    main()
