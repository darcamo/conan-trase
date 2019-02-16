from conans import ConanFile, CMake, tools
import shutil
import os


class TraseConan(ConanFile):
    name = "trase"
    version = "2019-02-05-c1d09b7"
    license = "BSD 3-Clause License"
    author = "Darlan Cavalcante Moreira (darcamo@gmail.com)"
    url = "https://github.com/darcamo/conan-trase"
    description = "A lightweight plotting library"
    topics = ("plotting", "scientific", "svg", "opengl")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    homepage = "https://github.com/trase-cpp/trase.git"
    requires = "glfw/3.2.1@bincrafters/stable"

    def source(self):
        git = tools.Git(folder="sources")
        commit_sha1 = self.version.split("-")[-1]
        git.clone(self.homepage)
        git.checkout(commit_sha1)

        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("sources/CMakeLists.txt", "project (trase)",
                              '''project (trase)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

        tools.replace_in_file("sources/CMakeLists.txt", "find_package (glfw3 3.2 REQUIRED)",
                              '''''')

        tools.replace_in_file("sources/CMakeLists.txt", "target_link_libraries (nanovg PUBLIC ${OPENGL_gl_LIBRARY} glfw dl)",
                              "target_link_libraries (nanovg PUBLIC ${OPENGL_gl_LIBRARY} ${CONAN_LIBS} dl)")

    def build(self):
        os.mkdir("build")
        shutil.move("conanbuildinfo.cmake", "build/")

        cmake = CMake(self)
        cmake.configure(source_folder="sources", build_folder="build")
        cmake.build()
        # cmake.install()  # Does not copy include paths correctly

    def package(self):
        self.copy("*.a", src="build")
        self.copy("*.so", src="build")
        self.copy("*.hpp", src="sources/src", dst="include")
        self.copy("*.tcc", src="sources/src", dst="include")


    def package_info(self):
        self.cpp_info.libs = ["trase", "nanovg"]
