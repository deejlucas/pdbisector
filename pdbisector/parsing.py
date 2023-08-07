import os

def extract_vrsts(filenames):
    vrsts = [v[:-4] for v in filenames if v[0] == "v" and v[-4:] == ".rst"]
    return vrsts


def extract_major_versions(vrsts):
    return [int(v.split(".")[0][1:]) for v in vrsts]


def get_max_major(vrsts):
    major_vs = extract_major_versions(vrsts)
    return max(major_vs)


def get_max_minor(vrsts, max_major):
    major_vs = extract_major_versions(vrsts)
    minor_vs = [int(v.split(".")[1]) for v in [vm for i, vm in enumerate(vrsts) if major_vs[i] == max_major]]
    return max(minor_vs)


def get_max_patch(vrsts, max_major, max_minor):
    major_vs = extract_major_versions(vrsts)
    minor_vs = [int(v.split(".")[1]) for v in vrsts]
    patch_vs = [int(v.split(".")[2]) for v in [vm for i, vm in enumerate(vrsts) if major_vs[i] == max_major and minor_vs[i] == max_minor]]
    return max(patch_vs)


def get_version_number(install_path):
    """
    Ignores patches
    """
    whatsnew_filenames = os.listdir(os.path.join(install_path, "doc", "source", "whatsnew"))
    vrsts = extract_vrsts(whatsnew_filenames)
    max_major = get_max_major(vrsts)
    max_minor = get_max_minor(vrsts, max_major=max_major)
    max_patch = get_max_patch(vrsts, max_major=max_major, max_minor=max_minor)
    return f"v{max_major}.{max_minor}.{max_patch}"
