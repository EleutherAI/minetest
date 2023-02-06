# syntax=docker/dockerfile:1
FROM ubuntu:focal
ARG ENABLE_SDL2
ENV DEBIAN_FRONTEND=noninteractive

RUN <<EOF
# build SDL2
# define installation directory
mkdir SDL2
export SDL2_INSTALLATION=/SDL2
# clone SDL
apt-get update -y
apt install -y git build-essential
if [ -n "$ENABLE_SDL2" ];then
	# build SDL2
	# define installation directory
	mkdir SDL2
	# clone SDL
	git clone https://github.com/libsdl-org/SDL.git -b SDL2 && cd SDL && git checkout tags/release-2.26.2
	# build
	mkdir build && cd build
	../configure --prefix=/SDL2 --enable-video-offscreen && make && make install
fi
EOF

RUN <<EOF
# build Irrlicht
# install missing dependency
apt-get update -y
apt install -y zlib1g-dev libjpeg-dev libpng-dev libxi-dev cmake
# clone irrlicht
git clone https://github.com/EleutherAI/irrlicht && cd irrlicht && git checkout disable-x11
# define lib paths
if [ -n "$ENABLE_SDL2" ];then
	cmake . -DBUILD_SHARED_LIBS=OFF -DBUILD_HEADLESS=1 -DSDL2_DIR=/SDL2/lib/cmake/SDL2
else
	cmake . -DBUILD_SHARED_LIBS=OFF -DBUILD_HEADLESS=1
fi
# build
make -j8
EOF

RUN <<EOF
# build minetest
# install dependencies
apt-get update -y
apt install -y libzmqpp-dev libgmp3-dev protobuf-compiler libprotobuf-dev libzstd-dev libfreetype-dev libsqlite3-dev
# clone minetest fork
git clone https://github.com/EleutherAI/minetest
git clone --depth 1 https://github.com/minetest/minetest_game.git minetest/games/minetest_game
cd minetest
git checkout cmake-SDL2-target-fix
# compile protobuf
cd hacking_testing
./compile_proto.sh
cd ..
# define lib paths
export SDL2_INSTALLATION=/SDL2
export IRRLICHT_REPO=/irrlicht
# build
if [ -n "$ENABLE_SDL2" ];then
	cmake . -B build_headless_render -DCMAKE_BUILD_TYPE=Debug -DSDL2_DIR=/SDL2/lib/cmake/SDL2 -DIRRLICHTMT_BUILD_DIR=$IRRLICHT_REPO -DBUILD_HEADLESS=1 -DENABLE_SOUND=OFF -DRUN_IN_PLACE=1
else
	cmake . -B build_headless_render -DCMAKE_BUILD_TYPE=Debug -DIRRLICHTMT_BUILD_DIR=$IRRLICHT_REPO -DBUILD_HEADLESS=1 -DENABLE_SOUND=OFF -DRUN_IN_PLACE=1
fi
cmake --build build_headless_render
EOF

RUN <<EOF
# Install Python packages and Xvfb
apt-get install -y python3 python3-pip xvfb
pip install numpy matplotlib gym zmq protobuf
EOF

WORKDIR minetest
EXPOSE 30000
CMD ["hacking_testing/server.sh"]
