import setuptools

setuptools.setup(
    name="airgym",
    version="1.0",
    author="ZZW",
    author_email="zzheng17@126.com",
    description="Airsim library",
    packages=setuptools.find_packages(),
	license='QY',
    classifiers=(
        "Programming Language :: Python :: 3",
    ),
    install_requires=[
          'msgpack-rpc-python', 'numpy', 'opencv-contrib-python'
    ]
)
