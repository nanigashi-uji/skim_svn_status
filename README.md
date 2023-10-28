#
# Skim svn status output
#

skim_svn_status: Skim output from `svn status` to supress to deal with unicode filename issue

- Contents:

  1.  README.md:                         This file
  2.  bin/mng_pyenv:                     Symblic link to 'runpyscr' for installing Python modules by pip locally.
  2a. bin/mng_pyenv2:                    Same as above using pip2 as default
  2b. bin/mng_pyenv3:                    Same as above using pip3 as default

  3.  bin/runpyscr:                      Wrapper bash script to invoke Python script. (Entity)

  4.  lib/python/site-packages:          Directory where python modules are stored

  5.  lib/python/skim_svn_status.py:     
  5a. lib/python/skim_svn_status3.py:    Same as above using python3 as default

  6.  bin/skim_svn_status:               Symbolic link to 'runpyscr' to invoke skim_svn_status.py.
  6a. bin/skim_svn_status3:              Same as above using python3 as default

  7.  .gitignore:                        Git-related file
  8.  lib/python/site-packages/.gitkeep: Git-related file to keep modules directory in repository.
  
- Usage (Procedure for adding new script):

  1. Put new script under 'lib/python'.

     Example: 'lib/python/{newscriptname}.py'

  2. Make symbolic link to 'bin/runpyscr' with same basename as the
     basename of new script.

      Example: 'bin/{newscriptname}' --> runpyscr

  3. Download external python module by './bin/mng_pyenv'

      Example: 'lib/python/{newscriptname}.py' uses modules, pytz and tzlocal.

      % ./bin/mng_pyenv pytz tzlocal

      To install python module by specifying python/pip version,
      invoke 'mng_pyenv2' or 'mng_pyenv3'.

  4. Invoke the symbolic link made in step.2 for execute the script.

      % ./bin/{newscriptname}

- Caution:

  - Do not put python scripts/modules that are not managed by pip
    under 'lib/python/site-packages'.

    Otherwise those scripts/modules will be removed by
    `./bin/mng_pyenv distclean`

- Note:

  - Python executable is seeked by the following order.

    1. Environmental variable: PYTHON
    2. Shebang in called python script
    3. python3 in PATH
    4. python  in PATH

    If you want to use python2 in prior instead of python3,
    change the value of shell variable \$\{python_major_version_default\}
    at the beginning of "runpyscr"

    In other examples ({newscriptname}2.py, {newscriptname}3.py) are
    specifying the python version at the shebang (1st-line).
    It can be override by Environmental variable: PYTHON.

  - pip command is seeked by the following order.

    1. Environmental variable: PIP
    2. pip2 in PATH for "mng_pyenv2"
       pip3 in PATH for "mng_pyenv3"
    3. pip3 in PATH
    4. pip  in PATH

    If you want to use pip2 in prior instead of pip3 by "mng_pyenv",
    change the value of shell variable ${python_major_version_default}
    at the beginning of "runpyscr"

- Requirements (Tools used in "runpyscr")

  - bash
  - grep
  - sed
  - awk
  - GNU realpath (in GNU coreutils)
  - Python, PIP

- Author

  - Uji Nanigashi (53845049+nanigashi-uji@users.noreply.github.com)

