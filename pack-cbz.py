#!/usr/bin/env python


import os
import glob
import zipfile


z = zipfile.ZipFile('Nimona.cbz', 'w')
for f in glob.glob('nimona/*.*'):
  z.write(f, os.path.basename(f)) # Saves minimal megs... , zipfile.ZIP_DEFLATED)
