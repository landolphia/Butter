from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [], 'excludes': []}

base = 'Console'

executables = [
    Executable('main.py', base=base, targetName = 'Butter')
]

setup(name='Butter',
      version = '0.9',
      description = 'An ad posting/scraping tool.',
      options = {'build_exe': build_options},
      executables = executables)
