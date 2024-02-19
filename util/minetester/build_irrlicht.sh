ROOT=$(pwd)
SDL2_DIR=${ROOT}/lib/SDL/build/lib/cmake/SDL2/
cd lib/irrlichtmt
cmake . -DBUILD_SHARED_LIBS=OFF -DBUILD_HEADLESS=1 -DSDL2_DIR=${SDL2_DIR}
make -j$(nproc)
cd ../..