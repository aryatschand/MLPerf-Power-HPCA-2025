# MLPerf Power

[Arxiv paper](https://arxiv.org/abs/2410.12032)

Rapid adoption of machine learning (ML) technologies has led to a surge in power consumption across diverse systems, from tiny IoT devices to massive datacenter clusters. Benchmarking the energy efficiency of these systems is crucial for optimization, but presents novel challenges due to the variety of hardware platforms, workload characteristics, and system-level interactions. This paper introduces MLPerf® Power, a comprehensive benchmarking methodology with capabilities to evaluate the energy efficiency of ML systems at power levels ranging from microwatts to megawatts. Developed by a consortium of industry professionals from more than 20 organizations, coupled with insights from academia, MLPerf Power establishes rules and best practices to ensure comparability across diverse architectures. We use representative workloads from the MLPerf benchmark suite to collect 1,841 reproducible measurements from 60 systems across the entire range of ML deployment scales. Our analysis reveals trade-offs between performance, complexity, and energy efficiency across this wide range of systems, providing actionable insights for designing optimized ML solutions from the smallest edge devices to the largest cloud infrastructures. This work emphasizes the importance of energy efficiency as a key metric in the evaluation and comparison of the ML system, laying the foundation for future research in this critical area. We discuss the implications for developing sustainable AI solutions and standardizing energy efficiency benchmarking for ML systems.

# MLPerf Power Data

All data (except for Figure 11b) is publicaly accessible on the [MLCommons benchmarks website](https://mlcommons.org/benchmarks/). The data is separated by category, so for example, you can access the inference datacenter submission measurements across all benchmarks and versions [here](https://mlcommons.org/benchmarks/inference-datacenter/). To access submissions with power measurements, click on the 'Division/Power' dropdown in the Results table and set it to 'Closed - Power'. Now, you can access every submission with submitted power measurements across every MLPerf version and division benchmark.

The raw data dumped from the MLPerf benchmark website can be found in '/raw_data.csv'. This contains all power and performance data from all submission divisions. This raw data is an aggregation from exporting all data directly from the website. Between the public data found on the website and '/raw_data.csv', there is no data processing beyond a simple aggregation.

This data is cleaned, filtered by division, and dumped into '/code/data_cleaned_{division}.csv'. This process only involves filtering our rows that do not fit the division or do not contain power measurements, and filtering our columns that contain data that is not relevant for system identification and evaluation. This data is used to create the figures in the paper, and all pre-processing work to calculate the data displayed in the graph can be found in the figure's corresponding python file in the '/code' directory.

# Reproduce Data and Figures

We have provided a Dockerfile to easily reproduce the derived data and all data-driven figures from the MLPerf Power paper. To run this, you must have docker installed on your machine. Once docker is installed, simply run:

```
./run_docker.sh
```

This will build a docker container with the cleaned MLPerf Power data, figure code, and all required dependencies. It will then run all the code to create each figure in the container, create a new 'figures' directory locally on your machine, and copy all the figures over. Once the script is done executing. You can inspect the post-processed data and generated figures and verify that they match the paper. 

We encourage users to build on our analysis and draw deeper insights from the MLPerf Power submission data. We anticipate that there is still much to learn about energy efficiency optimizations from the data and logs.

Refer to figures.md for a more detailed description of each figure in the paper and the specific MLPerf power data points used for each.

Optionally, you can also run the code for each figure individually. Navigate to the '/code' directory, install the required software packages in 'requirements.txt', change the output figure directory at the end of the file to '../figures/figureX.png' and run it with Python 3.12.

# Measuring Power

[This repo](https://github.com/mlcommons/power-dev) contains the development branch of MLPerf™ power measurement code. Everything is Apache 2.0 code developed by MLCommons™. Access is available to anyone.

MLPerf™ is using [SPEC PTDaemon] tool for measuring power. Please see [this README](https://github.com/mlcommons/power-dev/tree/master/ptd_client_server) for more details on how to use it.

Refer to measurement_tutorial.md for the tutorial. 