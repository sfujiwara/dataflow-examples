from distutils.command.build import build as _build
import subprocess
import setuptools


CUSTOM_COMMANDS = [
    (["sudo", "apt-get", "update"], "."),
    # Install MeCab
    (['sudo', 'apt-get', 'install', '-y', 'mecab'], '.'),
    (['sudo', 'apt-get', 'install', '-y', 'libmecab-dev'], '.'),
    (['sudo', 'apt-get', 'install', '-y', 'mecab-ipadic-utf8'], '.'),
    # Install NEologd
    (['git', 'clone', '--depth', '1', 'https://github.com/neologd/mecab-ipadic-neologd.git'], '.'),
    (['./bin/install-mecab-ipadic-neologd', '-n', '-y'], 'mecab-ipadic-neologd')
]


class build(_build):
    sub_commands = _build.sub_commands + [('CustomCommands', None)]


class CustomCommands(setuptools.Command):

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def RunCustomCommand(self, command_list):
        p = subprocess.Popen(
            command_list[0],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=command_list[1]
        )
        stdout_data, _ = p.communicate()
        if p.returncode != 0:
            raise RuntimeError('Command %s failed: exit code: %s' % (command_list[0], p.returncode))

    def run(self):
        for command in CUSTOM_COMMANDS:
            self.RunCustomCommand(command)


setuptools.setup(
    name='mecab-install-example',
    version='0.0.1',
    packages=setuptools.find_packages(),
    install_requires=[
        'mecab-python3'
    ],
    cmdclass={
        'build': build,
        'CustomCommands': CustomCommands,
    }
)
