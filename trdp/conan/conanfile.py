from conan import ConanFile
from conans import CMake


class TcnopenConan(ConanFile):
    name = "tcnopen"
    version = "r2375"

    # Optional metadata
    license = "MPLv2.0 and GPL"
    author = "<Put your name here> <And your email here>"
    url = "https://github.com/Roboauto/TCNopen.git"
    description = "TCNopen TRDP library"
    topics = ("Railway", "TRDP", "Protocol")

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"

    def source(self):
        self.run("git clone {}".format(self.url))
        self.run("cd TCNopen && git checkout master")

    def build(self):
        cmake = CMake(self)
        print(cmake)
        cmake.configure(source_folder="TCNopen/trdp")
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["trdp"]
        self.cpp_info.includedirs = ["include"]
        if (self.settings.os == "Linux"):
            self.cpp_info.defines = ["POSIX=1"]
        # Not sure how to detect VXWORKS. Windows is detected automatically.


