import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="NR_Color_IQA", # Replace with your own username
    version="0.0.1",
    author="John Park",
    author_email="",
    description="NR Color Image Quality Assessments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/johnypark/NR-Color-IQA",
    packages=setuptools.find_packages(),
    install_requires = ['tensorflow',
                       'opencv-python',
                       'scikit-image',
                       'scipy',
                        'typeguard'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

