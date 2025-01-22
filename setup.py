from setuptools import setup

setup(
    name="nccl_goal_generator",
    version="0.1.0",
    description="A toolchain for NCCL trace capturing and LogGOPSim goal file generation",
    author="Your Name",
    author_email="your_email@example.com",
    # Using py_modules to specify a single-file module packaging method
    py_modules=["run_generator", "get_traced_events", "goal2dot"],
    # Inform setuptools that these modules are located in the src/ directory
    package_dir={"": "src"},
    # Define a command-line entry point
    entry_points={
        "console_scripts": [
            # command_name = module_name:function_name
            "nccl_goal_generator = run_generator:main",
        ],
    },
    python_requires=">=3.6",
)