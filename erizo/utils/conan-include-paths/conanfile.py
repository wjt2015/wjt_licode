from conans.model import Generator
from conans import ConanFile

from conans.client.build.compiler_flags import (architecture_flag, build_type_define,
                                                build_type_flags, format_defines,
                                                format_include_paths, format_libraries,
                                                format_library_paths, libcxx_define, libcxx_flag,
                                                rpath_flags, sysroot_flag,
                                                visual_linker_option_separator, visual_runtime)
from conans.client.build.cppstd_flags import cppstd_flag
from conans.paths import BUILD_INFO_COMPILER_ARGS


class IncludePathsGenerator(Generator):

    @property
    def filename(self):
        print("BUILD_INFO_COMPILER_ARGS={};".format(BUILD_INFO_COMPILER_ARGS))
        return BUILD_INFO_COMPILER_ARGS

    @property
    def compiler(self):
        r=self.conanfile.settings.get_safe("compiler")
        print("r={};self.conanfile.settings={};".format(r,self.conanfile.settings))
        return self.conanfile.settings

    @property
    def content(self):
        """With compiler_args you can invoke your compiler:
        $ gcc main.c @conanbuildinfo.args -o main
        $ clang main.c @conanbuildinfo.args -o main
        $ cl /EHsc main.c @conanbuildinfo.args
        """
        flags = []

        print("include_paths={};compiler={};".format(self._deps_build_info.include_paths,self.compiler))

        #flags.extend(format_defines(self._deps_build_info.defines))
        #flags.extend(format_include_paths(self._deps_build_info.include_paths,compiler=self.compiler))

        ##include_paths=format_include_paths(self._deps_build_info.include_paths,{"compiler":"gcc"})
        include_paths=format_include_paths(self._deps_build_info.include_paths,self.compiler)
        print("before_flags.extend_flags={};include_paths={};".format(flags,include_paths))
        flags.extend(include_paths)

        print("after_flags.extend_flags={};".format(flags))
        #flags.extend(self._deps_build_info.cxxflags)
        #flags.extend(self._deps_build_info.cflags)

        #arch_flag = architecture_flag(arch=self.conanfile.settings.get_safe("arch"),
        #                              compiler=self.compiler)
        #if arch_flag:
        #    flags.append(arch_flag)

        #build_type = self.conanfile.settings.get_safe("build_type")
        #btfs = build_type_flags(compiler=self.compiler, build_type=build_type,
        #                        vs_toolset=self.conanfile.settings.get_safe("compiler.toolset"))
        #if btfs:
        #    flags.extend(btfs)
        #btd = build_type_define(build_type=build_type)
        #if btd:
        #    flags.extend(format_defines([btd]))

        #if self.compiler == "Visual Studio":
        #    runtime = visual_runtime(self.conanfile.settings.get_safe("compiler.runtime"))
        #    if runtime:
        #        flags.append(runtime)
        #    # Necessary in the "cl" invocation before specify the rest of linker flags
        #    flags.append(visual_linker_option_separator)

        #the_os = (self.conanfile.settings.get_safe("os_build") or
        #          self.conanfile.settings.get_safe("os"))
        #flags.extend(rpath_flags(the_os, self.compiler, self._deps_build_info.lib_paths))
        #flags.extend(format_library_paths(self._deps_build_info.lib_paths, compiler=self.compiler))
        #flags.extend(format_libraries(self._deps_build_info.libs, compiler=self.compiler))
        #flags.extend(self._deps_build_info.sharedlinkflags)
        #flags.extend(self._deps_build_info.exelinkflags)
        #flags.extend(self._libcxx_flags())
        #flags.append(cppstd_flag(self.conanfile.settings.get_safe("compiler"),
        #                         self.conanfile.settings.get_safe("compiler.version"),
        #                         self.conanfile.settings.get_safe("cppstd")))
        #sysrf = sysroot_flag(self._deps_build_info.sysroot, compiler=self.compiler)
        #if sysrf:
        #    flags.append(sysrf)

        s=" ".join(flag for flag in flags if flag)
        print("s={};".format(s))
        return s

    def _libcxx_flags(self):
        print("_libcxx_flags;self={};".format(self))
        libcxx = self.conanfile.settings.get_safe("compiler.libcxx")
        compiler = self.conanfile.settings.get_safe("compiler")

        print("libcxx={};compiler={};".format(libcxx,compiler))

        lib_flags = []
        if libcxx:
            stdlib_define = libcxx_define(compiler=compiler, libcxx=libcxx)
            lib_flags.extend(format_defines([stdlib_define]))
            cxxf = libcxx_flag(compiler=compiler, libcxx=libcxx)
            if cxxf:
                lib_flags.append(cxxf)

        return lib_flags


class MyCustomGeneratorPackage(ConanFile):
    name = "IncludePathsGenerator"
    version = "0.1"
    url = "https://github.com/lynckia/include-paths-generator"
    license = "MIT"

    def build(self):
        pass

    def package_info(self):
        self.cpp_info.includedirs = []
        self.cpp_info.libdirs = []
        self.cpp_info.bindirs = []