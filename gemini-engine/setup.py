from setuptools import setup, find_packages

setup(
    name="gemini-engine",
    version="1.0.0",
    description="Python Native Multi-Modal AI Engine (Gemini 3.7 + Needle 2 SLM + SQLite Memory)",
    author="Akash Yadav",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
