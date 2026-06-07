"""
Setup script for Biomedical Waste Segregation System

Run: pip install -e .

Author: AI-Based Medical Waste Segregation System
Version: 1.0
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="biomedical-waste-detection",
    version="1.0.0",
    author="AI-Based Medical Waste Project",
    description="AI-Based Medical Waste Segregation Monitoring System for Multi-Speciality Hospitals",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "biomedical-waste-quickstart=quickstart:main",
            "biomedical-waste-train=train_model:main",
            "biomedical-waste-infer=inference:main",
            "biomedical-waste-analyze=analyze_csv:main",
        ],
    },
    include_package_data=True,
)
