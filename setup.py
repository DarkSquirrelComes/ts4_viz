import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='ts4_viz',
    version='0.0.1',
    author='Vadim Rusakov',
    description='Vizualizer for ts4 logs',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://vcs.modus-ponens.com/ton/ts4_viz',
    packages=['ts4_viz'],
    install_requires=['graphviz', 'tonos_ts4==0.5.0a'],
)