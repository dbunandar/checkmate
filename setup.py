from setuptools import setup

setup(
    name="checkmate",
    version="0.1.0",
    description="Checkmate prevents you from OOMing when training big deep neural nets",
    packages=["checkmate"],  # find_packages()
    python_requires=">=3.5",
    install_requires=[
        "matplotlib",  # this is only used once in the core checkmate package
        "numpy",
        "pandas",
        "toposort",
        "psutil",
    ],
    extras_require={
        "eval": [
            "graphviz",
            "keras_segmentation @ https://github.com/ajayjain/image-segmentation-keras/archive/master.zip#egg=keras_segmentation-0.2.0remat",
            "python-dotenv",
            "ray>=0.7.5",
            "redis",
            "scipy",
            "seaborn",
            "tqdm",
        ],
        "test": ["graphviz", "pytest", "tensorflow>=2.0.0"],
    },
)
