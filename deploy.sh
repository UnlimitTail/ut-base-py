#! /bin/bash
rm -rf build dist utailBase.egg-info
python setup.py bdist_wheel
twine upload dist/*