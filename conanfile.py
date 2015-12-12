from conans import CMake
from conans import ConanFile

class GitMixin(object):
    def source(self):
        self.__clone(self.GIT_REPO, self.GIT_TAG)

    def __git(self, *args):
        self.run('git {}'.format(' '.join(args)))

    def __clone(self, repo, tag):
        self.__git('init .')
        self.__git('remote add -t \* -f origin', '{}'.format(repo))
        self.__git('checkout {}'.format(tag))
        self.__git('submodule update --recursive')

class CMakeMixin(object):
    INSTALL_PREFIX = '/'
    INSTALL_DIR = 'root'

    def build(self):
        self.__configure(
            CMake(self.settings),
            '-DCMAKE_INSTALL_PREFIX:PATH={}'.format(self.INSTALL_PREFIX),
            *getattr(self, 'CMAKE_CONFIGURE_ARGS', ())
        )
        self.__build(
            CMake(self.settings),
            *getattr(self, 'CMAKE_BUILD_ARGS', ())
        )

        if getattr(self, 'CMAKE_RUN_TESTS', False):
            self.run('ctest')

    def package(self):
        self.__cmake(
            '--build . --target install',
            '-- DESTDIR={}'.format(self.INSTALL_DIR)
        )
        self.copy(pattern='*', dst='', src=self.INSTALL_DIR)

    def __cmake(self, *args):
        self.run('cmake {}'.format(' '.join(args)))

    def __configure(self, cmake, *args):
        self.__cmake('.', cmake.command_line, *args)

    def __build(self, cmake, *args):
        self.__cmake('--build .', cmake.build_config, *args)

class CppFormatConan(GitMixin, CMakeMixin, ConanFile):
    name = 'cppformat'
    version = '2.0.0'
    url = 'https://github.com/owbone/conan-cppformat.git'
    settings = 'os', 'compiler', 'build_type', 'arch'

    # GitMixin settings
    GIT_REPO = 'https://github.com/cppformat/cppformat.git'
    GIT_TAG = 'tags/{}'.format(version)

    # CMakeMixin settings
    CMAKE_RUN_TESTS = True
