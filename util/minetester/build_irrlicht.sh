cd lib/irrlichtmt
cmake . -DBUILD_SHARED_LIBS=OFF
make -j$(nproc)
cd ../..