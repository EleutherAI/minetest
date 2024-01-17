.PHONY: all deps repos sdl2 package zmqpp irrlicht minetester minetest install demo proto clean

MINETESTER_VERSION := 0.0.1
SDL2_CMAKE_FILE := lib/SDL/build/lib/cmake/SDL2/sdl2-config.cmake
ZMQPP_LIB_FILE := lib/zmqpp/build/max-g++/libzmqpp.a
IRRLICHTMT_LIB_FILE := lib/irrlichtmt/lib/Linux/libIrrlichtMt.a
MINETEST_BINARY := bin/minetest
DEBUG_BINARY := bin/debug
MINETESTER_WHEEL := build/package/wheel/minetester-$(MINETESTER_VERSION)-py3-none-manylinux_2_35_x86_64.whl

default: minetest 

linux_deps:
	# Install debian dependencies
	util/minetester/install_deps.sh

python_build_deps:
	# Install python build dependencies
	pip install --upgrade pip
	pip install -r build_requirements.txt

repos:
	# Init all submodules
	git submodule update --init --recursive

$(SDL2_CMAKE_FILE):
	# compile sdl2
	util/minetester/build_sdl2.sh

sdl2: $(SDL2_CMAKE_FILE)

proto:
	#create protobuf c++ and python files
	util/minetester/compile_proto.sh

$(ZMQPP_LIB_FILE):
	#compile zmqpp
	util/minetester/build_zmqpp.sh

zmqpp: $(ZMQPP_LIB_FILE)

$(IRRLICHTMT_LIB_FILE):
	util/minetester/build_irrlicht.sh

irrlicht: $(IRRLICHTMT_LIB_FILE)

$(MINETEST_BINARY):
	#build minetest binary
	util/minetester/build_minetest.sh

minetest: $(MINETEST_BINARY)

$(DEBUG_BINARY): 
	util/minetester/build_debuggable_minetest.sh

debug: $(DEBUG_BINARY)

$(MINETESTER_WHEEL):
	#build minetester python library
	util/minetester/build_minetester.sh

minetester: $(MINETESTER_WHEEL)

install:
	#install python library
	pip install $(MINETESTER_WHEEL) --force-reinstall

demo:
	#install run demo script
	python -m minetester.scripts.test_loop

ctags:
	ctags --extras=+f -R --links=no .

clean:
	#clean up repo
	util/minetester/clean.sh

clean_minetester:
	#clean up minetester, but not minetest
	util/minetester/clean_minetester.sh
