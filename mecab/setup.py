from distutils.command.build import build as _build
import subprocess
import setuptools


class build(_build):
    sub_commands = _build.sub_commands + [('CustomCommands', None)]


CUSTOM_COMMANDS = [
    (["sudo", "apt-get", "update"], "."),
    (["sudo", "apt-get", "install", "git", "build-essential", "libatlas-base-dev", "-y"], "."),
]


class CustomCommands(setuptools.Command):

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def RunCustomCommand(self, command_list):
        p = subprocess.Popen(command_list[0], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=command_list[1])
        stdout_data, _ = p.communicate()
        if p.returncode != 0:
            raise RuntimeError('Command %s failed: exit code: %s' % (command_list[0], p.returncode))

    def run(self):
        for command in CUSTOM_COMMANDS:
            self.RunCustomCommand(command)


REQUIRED_PACKAGES = []

setuptools.setup(
    name='mecab-install-example',
    version='0.0.1',
    packages=setuptools.find_packages(),
    #install_requires=REQUIRED_PACKAGES,
    cmdclass={
        'build': build,
        'CustomCommands': CustomCommands,
    }
)
