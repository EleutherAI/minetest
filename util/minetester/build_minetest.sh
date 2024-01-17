ROOT=$(pwd)

mkdir -p build/normal
mkdir -p build/headless

cd build/headless


SDL2_DIR=${ROOT}/lib/SDL/build/lib/cmake/SDL2/
IRRLICHTMT_DIR=${ROOT}/lib/irrlichtmt

echo ${SDL2_DIR}

cmake ../.. -DRUN_IN_PLACE=TRUE -DBUILD_HEADLESS=1 -DSDL2_DIR=${SDL2_DIR} -DIRRLICHTMT_BUILD_DIR=${IRRLICHTMT_DIR}
make -j$(( $(nproc) > 1 ? $(nproc) - 1 : 1 )) #use max(nproc - 1,1) threads

cd ../..

mv bin/minetest bin/minetest_headless

cd build/normal
cmake ../.. -DRUN_IN_PLACE=TRUE -DBUILD_HEADLESS=0 -DSDL2_DIR= -DIRRLICHTMT_BUILD_DIR=${IRRLICHTMT_DIR}
make -j$(( $(nproc) > 1 ? $(nproc) - 1 : 1 )) #use max(nproc - 1,1) threads

cd ../..


