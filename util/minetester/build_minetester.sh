mkdir -p build/package
cp setup.py build/package/
cp -r minetester build/package/
mkdir build/package/minetester/minetest

#Copy minetest data
cp -r bin build/package/minetester/minetest
cp -r builtin build/package/minetester/minetest
cp -r client build/package/minetester/minetest
cp -r clientmods build/package/minetester/minetest
cp -r cursors build/package/minetester/minetest
cp -r fonts build/package/minetester/minetest
cp -r games build/package/minetester/minetest
cp -r misc build/package/minetester/minetest
cp -r mods build/package/minetester/minetest
cp -r po build/package/minetester/minetest
cp -r textures build/package/minetester/minetest

#Make wheel
cd build/package
python -m build

#Update RPATHS and add relevant libraries to wheel
cd dist
auditwheel repair minetester-*.*.*-py3-none-any.whl --plat manylinux_2_35_x86_64

cd ../../..

mkdir build/package/wheel

cp build/package/dist/wheelhouse/minetester-*.*.*-py3-none-manylinux_2_35_x86_64.whl build/package/wheel

