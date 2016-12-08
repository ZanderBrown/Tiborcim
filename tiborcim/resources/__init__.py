from pkg_resources import resource_filename, resource_string, Requirement


def icon_path():
    return resource_filename(Requirement.parse('tiborcim'), 'cim.png')

def readme_path ():
    return resource_filename(Requirement.parse('tiborcim'), 'README.md')

def sample_path (name):
    return resource_filename(Requirement.parse('tiborcim'), 'samples/' + name)

def samples_list ():
    from os import listdir
    samples = []
    for file in listdir(resource_filename(Requirement.parse('tiborcim'), "samples")):
        if file.endswith(".tibas"):
            samples.append(file)
    return samples
