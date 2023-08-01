from setuptools import setup, find_packages

readme = open("./README.md", "r")

setup(
    name="paucode",
    packages=find_packages,
    version="0.02",
    description="funciones de ayuda en trabajo como economista",
    long_description=readme.read(),
    long_description_content_type="text/markdown",
    author="Javier Choque Paucar",
    author_email="choquepaucarj.social@gmail.com",
    download_url="https://github.com/paucode1/paucode",
    keywords=["example"],
    classifiers=[],
    license="MIT",
    include_package_data=True,
    install_requires=[
        "numpy",
        "matplotlib"
        #agregar todas las dependencias
    ]
)