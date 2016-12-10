from pkg_resources import resource_filename, resource_string, Requirement
import sys

_LOGO_FILENAME = 'cim.png'
_README_FILENAME = 'README.md'

def icon_path():
    if hasattr(sys, '_MEIPASS'):
        from os.path import join
        return join(sys._MEIPASS, _LOGO_FILENAME)
    return resource_filename(Requirement.parse('tiborcim'), _LOGO_FILENAME)

def readme_path ():
    if hasattr(sys, '_MEIPASS'):
        from os.path import join
        return join(sys._MEIPASS, _README_FILENAME)
    return resource_filename(Requirement.parse('tiborcim'), _README_FILENAME)

def sample_path (name):
    if hasattr(sys, '_MEIPASS'):
        from os.path import join
        return join(sys._MEIPASS, 'samples', name)
    return resource_filename(Requirement.parse('tiborcim'), 'samples/' + name)

def samples_list ():
    if hasattr(sys, '_MEIPASS'):
        from os.path import join
        path = join(sys._MEIPASS, 'samples')
    else:
        path = resource_filename(Requirement.parse('tiborcim'), "samples")
    from os import listdir
    samples = []
    for file in listdir(path):
        if file.endswith(".tibas"):
            samples.append(file)
    return samples
