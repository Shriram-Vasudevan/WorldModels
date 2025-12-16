from setuptools import setup, find_packages

setup(
    name="semantic-memory",
    version="0.1.0",
    description="Universal semantic memory layer for the physical world",
    author="Your Name",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        "numpy>=1.24.0",
        "pillow>=10.0.0",
        "networkx>=3.0",
        "torch>=2.0.0",
        "torchvision>=0.15.0",
        "transformers>=4.30.0",
        "sentence-transformers>=2.2.0",
        "opencv-python>=4.8.0",
        "pydantic>=2.0.0",
        "tqdm>=4.65.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "mypy>=1.4.0",
            "jupyter>=1.0.0",
        ],
    },
)
