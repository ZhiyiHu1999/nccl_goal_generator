from setuptools import setup, find_packages

setup(
    name="nccl_goal_generator",
    version="0.1.0",
    description="A toolchain for NCCL trace capturing and LogGOPSim goal file generation",
    # author="Your Name",
    # author_email="your_email@example.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "nccl_goal_generator": ["npkit_data_summary_Simple.json", "npkit_data_summary_LL.json"],
    },
    include_package_data=True,  # include npkit_data_summary_Simple.json and npkit_data_summary_LL.json
    entry_points={
        "console_scripts": [
            "nccl_goal_generator = nccl_goal_generator.run_generator:main",
        ],
    },
    python_requires=">=3.6",
)