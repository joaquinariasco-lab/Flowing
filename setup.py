from setuptools import setup, find_packages

setup(
    name="flowing-os",
    version="0.2.0",  # Increment this if already published
    description="Flowing: The Control Plane for AI Agents",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/flowing-os",  # update with your repo
    author="Your Name",
    author_email="your.email@example.com",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "click>=8.0,<9.0",
        "flask>=2.0,<4.0",
        "flask-socketio>=5.0,<6.0",
        "streamlit>=1.30,<2.0",
        "requests>=2.25,<3.0",
        "networkx>=3.0,<4.0",
        "plotly>=5.0,<6.0"
    ],
    entry_points={
        "console_scripts": [
            "flowing=flowing.cli:main",
        ],
    },
    include_package_data=True,
)
