from setuptools import setup, find_packages

setup(
    name='minetester',
    version='0.0.1',
    description='Complex environments based on Minetest.',
    author='EleutherAI',
    author_email='',
    packages=find_packages(),
    install_requires=[
        'opencv-python',
        'gymnasium',
        'numpy',
        'matplotlib',
        'zmq',
        'protobuf==3.20.1',
        'psutil',
    ],
    package_data={
        'minetester': [
             'minetest/bin/minetest',
             'minetest/client/**/*',
             'minetest/clientmods/**/*',
             'minetest/cursors/**/*',
             'minetest/games/**/*',
             'minetest/mods/**/*',
             'minetest/textures/**/*',
             'minetest/po/**/*',
             'minetest/builtin/**/*',
             'minetest/misc/**/*',
             'minetest/fonts/**/*'
            ],
    },

)
