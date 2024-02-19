from setuptools import setup, find_packages

DEV = ["pre-commit", "black", "isort", "flake8", "pytest", "pytest-asyncio"]
DOCS = [
    "sphinx==6.2.1",
    "sphinx_rtd_theme==1.2.2",
    "sphinx-autobuild",
    "sphinx_autodoc_typehints",
    "sphinx_copybutton",
    "myst_parser",
]

setup(
    name='minetester',
    version='0.0.1',
    description='Complex environments based on Minetest.',
    author='EleutherAI',
    python_requires=">=3.8.0",
    packages=find_packages(),
    install_requires=[
        'gymnasium',
        'numpy',
        'matplotlib',
        'zmq',
        'protobuf==3.20.1',
        'patchelf',
    ],
    extras_require={"dev": DEV, "docs": DOCS},
    package_data={
        'minetester': [
             'minetest/bin/minetest',
             'minetest/bin/minetest_headless',
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
