# what packages are needed and install them

import importlib.metadata, subprocess, sys
required  = {'liffile[all]'}
installed = {pkg.metadata['Name'] for pkg in importlib.metadata.distributions()}
missing   = required - installed

if missing:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing])

import liffile

>>> with LifFile('data/Project.lif') as lif:
    for image in lif.images:
        name = image.name
        image = lif.images['Fast Flim']
        assert image.shape == (1024, 1024)
        assert image.dims == ('Y', 'X')
        lifetimes = image.asxarray()
