from pkg_resources import resource_filename, resource_string


def path(name, resource_dir="images/"):
    """Return the filename for the referenced file."""
    return resource_filename(__name__, resource_dir + name)
