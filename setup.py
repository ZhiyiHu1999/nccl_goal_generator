from setuptools import setup

setup(
    name="nccl_goal_generator",
    version="0.1.0",
    description="A toolchain for NCCL trace capturing and LogGOPSim goal file generation",
    author="Your Name",
    author_email="your_email@example.com",
    # 这里使用 py_modules 指定单文件模块的打包方式
    py_modules=["run_generator", "get_traced_events", "goal2dot"],
    # 告诉 setuptools，这些模块都在 src/ 目录下
    package_dir={"": "src"},
    # 设置一个命令行入口点
    entry_points={
        "console_scripts": [
            # 命令名 = 模块名:函数名
            "nccl_goal_generator = run_generator:main",
        ],
    },
    python_requires=">=3.6",
)