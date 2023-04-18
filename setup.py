from distutils.core import setup
from setuptools import setup, Extension, distutils, Command, find_packages
import setuptools.command.install
import distutils.command.build
import distutils.command.clean
import os
import shutil

## extending the install command functionality.
class install(setuptools.command.install.install):
    def run(self):
        print ("INFO: Installing hipify_torch")
        setuptools.command.install.install.run(self)
        print ("OK: Successfully installed hipify_torch")

## extending the clean command functionality.
class clean(distutils.command.clean.clean):
    def run(self):
        print ("INFO: cleaning hipify_torch")
        cwd = os.getcwd()
        build_dir = os.path.join(cwd, "build")
        egg_dir = os.path.join(cwd, "hipify_torch.egg-info")
        if os.path.isdir(build_dir):
            shutil.rmtree(build_dir)
            shutil.rmtree(egg_dir)
            print("OK: Deleted the build directory.")

        distutils.command.clean.clean.run(self)

cmd_class = {
    "clean"   : clean,
    "install" : install,
    }

setup(
    name='hipify_torch',
    version='0.1',
    cmdclass=cmd_class,
    packages=['hipify',],
    long_description=open('README.md').read(),
    )
