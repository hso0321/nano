# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.10

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/nano/jetson-inference

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/nano/jetson-inference/build

# Include any dependencies generated for this target.
include examples/imagenet-console/CMakeFiles/imagenet-console.dir/depend.make

# Include the progress variables for this target.
include examples/imagenet-console/CMakeFiles/imagenet-console.dir/progress.make

# Include the compile flags for this target's objects.
include examples/imagenet-console/CMakeFiles/imagenet-console.dir/flags.make

examples/imagenet-console/CMakeFiles/imagenet-console.dir/imagenet-console.cpp.o: examples/imagenet-console/CMakeFiles/imagenet-console.dir/flags.make
examples/imagenet-console/CMakeFiles/imagenet-console.dir/imagenet-console.cpp.o: ../examples/imagenet-console/imagenet-console.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/nano/jetson-inference/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object examples/imagenet-console/CMakeFiles/imagenet-console.dir/imagenet-console.cpp.o"
	cd /home/nano/jetson-inference/build/examples/imagenet-console && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/imagenet-console.dir/imagenet-console.cpp.o -c /home/nano/jetson-inference/examples/imagenet-console/imagenet-console.cpp

examples/imagenet-console/CMakeFiles/imagenet-console.dir/imagenet-console.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/imagenet-console.dir/imagenet-console.cpp.i"
	cd /home/nano/jetson-inference/build/examples/imagenet-console && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/nano/jetson-inference/examples/imagenet-console/imagenet-console.cpp > CMakeFiles/imagenet-console.dir/imagenet-console.cpp.i

examples/imagenet-console/CMakeFiles/imagenet-console.dir/imagenet-console.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/imagenet-console.dir/imagenet-console.cpp.s"
	cd /home/nano/jetson-inference/build/examples/imagenet-console && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/nano/jetson-inference/examples/imagenet-console/imagenet-console.cpp -o CMakeFiles/imagenet-console.dir/imagenet-console.cpp.s

examples/imagenet-console/CMakeFiles/imagenet-console.dir/imagenet-console.cpp.o.requires:

.PHONY : examples/imagenet-console/CMakeFiles/imagenet-console.dir/imagenet-console.cpp.o.requires

examples/imagenet-console/CMakeFiles/imagenet-console.dir/imagenet-console.cpp.o.provides: examples/imagenet-console/CMakeFiles/imagenet-console.dir/imagenet-console.cpp.o.requires
	$(MAKE) -f examples/imagenet-console/CMakeFiles/imagenet-console.dir/build.make examples/imagenet-console/CMakeFiles/imagenet-console.dir/imagenet-console.cpp.o.provides.build
.PHONY : examples/imagenet-console/CMakeFiles/imagenet-console.dir/imagenet-console.cpp.o.provides

examples/imagenet-console/CMakeFiles/imagenet-console.dir/imagenet-console.cpp.o.provides.build: examples/imagenet-console/CMakeFiles/imagenet-console.dir/imagenet-console.cpp.o


# Object files for target imagenet-console
imagenet__console_OBJECTS = \
"CMakeFiles/imagenet-console.dir/imagenet-console.cpp.o"

# External object files for target imagenet-console
imagenet__console_EXTERNAL_OBJECTS =

aarch64/bin/imagenet-console: examples/imagenet-console/CMakeFiles/imagenet-console.dir/imagenet-console.cpp.o
aarch64/bin/imagenet-console: examples/imagenet-console/CMakeFiles/imagenet-console.dir/build.make
aarch64/bin/imagenet-console: /usr/local/cuda/lib64/libcudart_static.a
aarch64/bin/imagenet-console: /usr/lib/aarch64-linux-gnu/librt.so
aarch64/bin/imagenet-console: aarch64/lib/libjetson-inference.so
aarch64/bin/imagenet-console: aarch64/lib/libjetson-utils.so
aarch64/bin/imagenet-console: /usr/local/cuda/lib64/libcudart_static.a
aarch64/bin/imagenet-console: /usr/lib/aarch64-linux-gnu/librt.so
aarch64/bin/imagenet-console: /usr/local/lib/libopencv_calib3d.so.4.1.1
aarch64/bin/imagenet-console: /usr/local/lib/libopencv_features2d.so.4.1.1
aarch64/bin/imagenet-console: /usr/local/lib/libopencv_flann.so.4.1.1
aarch64/bin/imagenet-console: /usr/local/lib/libopencv_imgproc.so.4.1.1
aarch64/bin/imagenet-console: /usr/local/lib/libopencv_core.so.4.1.1
aarch64/bin/imagenet-console: /usr/local/lib/libopencv_cudev.so.4.1.1
aarch64/bin/imagenet-console: examples/imagenet-console/CMakeFiles/imagenet-console.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/nano/jetson-inference/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable ../../aarch64/bin/imagenet-console"
	cd /home/nano/jetson-inference/build/examples/imagenet-console && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/imagenet-console.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
examples/imagenet-console/CMakeFiles/imagenet-console.dir/build: aarch64/bin/imagenet-console

.PHONY : examples/imagenet-console/CMakeFiles/imagenet-console.dir/build

examples/imagenet-console/CMakeFiles/imagenet-console.dir/requires: examples/imagenet-console/CMakeFiles/imagenet-console.dir/imagenet-console.cpp.o.requires

.PHONY : examples/imagenet-console/CMakeFiles/imagenet-console.dir/requires

examples/imagenet-console/CMakeFiles/imagenet-console.dir/clean:
	cd /home/nano/jetson-inference/build/examples/imagenet-console && $(CMAKE_COMMAND) -P CMakeFiles/imagenet-console.dir/cmake_clean.cmake
.PHONY : examples/imagenet-console/CMakeFiles/imagenet-console.dir/clean

examples/imagenet-console/CMakeFiles/imagenet-console.dir/depend:
	cd /home/nano/jetson-inference/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/nano/jetson-inference /home/nano/jetson-inference/examples/imagenet-console /home/nano/jetson-inference/build /home/nano/jetson-inference/build/examples/imagenet-console /home/nano/jetson-inference/build/examples/imagenet-console/CMakeFiles/imagenet-console.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : examples/imagenet-console/CMakeFiles/imagenet-console.dir/depend

