import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="audio-soundwave-generator",
    version="0.0.1",
    author="Witold Wroblewski",
    author_email="witoldwrob@gmail.com",
    description="A package to convert audio file into several waveform images of specific duration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wiwski/audio-soundwave-generator.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
    package_data={
    '': ['bin/*'],
    }

)