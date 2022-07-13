import setuptools

with open("requirements.txt") as f:
    all_reqs = f.read().splitlines()
    requirements = [r for r in all_reqs if not r.startswith("http")]

setuptools.setup(
    name="atlas_queue_api",
    version="0.0.1",
    author="jbuehlz",
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
    install_requires=requirements,
    include_package_data=True
)