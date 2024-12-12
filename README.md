# MLPerf Power

Rapid adoption of machine learning (ML) technologies has led to a surge in power consumption across diverse systems, from tiny IoT devices to massive datacenter clusters. Benchmarking the energy efficiency of these systems is crucial for optimization, but presents novel challenges due to the variety of hardware platforms, workload characteristics, and system-level interactions. This paper introduces MLPerf® Power, a comprehensive benchmarking methodology with capabilities to evaluate the energy efficiency of ML systems at power levels ranging from microwatts to megawatts. Developed by a consortium of industry professionals from more than 20 organizations, coupled with insights from academia, MLPerf Power establishes rules and best practices to ensure comparability across diverse architectures. We use representative workloads from the MLPerf benchmark suite to collect 1,841 reproducible measurements from 60 systems across the entire range of ML deployment scales. Our analysis reveals trade-offs between performance, complexity, and energy efficiency across this wide range of systems, providing actionable insights for designing optimized ML solutions from the smallest edge devices to the largest cloud infrastructures. This work emphasizes the importance of energy efficiency as a key metric in the evaluation and comparison of the ML system, laying the foundation for future research in this critical area. We discuss the implications for developing sustainable AI solutions and standardizing energy efficiency benchmarking for ML systems.

# MLPerf Data

All data (except for Figure 11b) is publicaly accessible on the MLCommons website (https://mlcommons.org/benchmarks/). The data is separated by category, so for example, you can access the inference datacenter submission measurements across all benchmarks and versions at (https://mlcommons.org/benchmarks/inference-datacenter/). To access submissions with power measurements, click on the 'Division/Power' dropdown in the Results table and set it to 'Closed - Power'. Now, you can access every submission with submitted power measurements across every MLPerf version and division benchmark. 

# Figure Descriptions

## Figure 1

Description - Performance trends of MLPerf Inference submissions vs Moore's Law.

Data Source - Performance numbres are from the publicly accessible MLPerf inference data (same data as MLPerf Inference Benchmark paper, ISCA 2020, https://arxiv.org/pdf/1911.02549).

## Figure 2

Description - Minimum and maximum power consumption in submissions across the 4 MLPerf scales (tiny, edge, datacenter, training).

Data Source - Power consumption numbers are from the publicly accessible MLPerf Power offline data. Report the minimum and maximum recorded power from a single submission.

## Figure 5a

Description - Energy efficiency trends of MLPerf Power offline inference datacenter submissions.

Data Source - Energy efficiency numbers are from the publicly accessible MLPerf Power offline inference datacenter submissions. We report the maximum energy efficiency (performance/power) of any single submission at or before the specified version. For example, for the v4.0 BERT-99.0 value, the submission with the highest energy efficiency was from v2.1, so keep reporting this score as the max until a new submission beats this number. This is why you will often see plateaus in trends graphs.

## Figure 5b

Description - Energy efficiency trends of MLPerf Power offline inference edge submissions.

Data Source - Energy efficiency numbers are from the publicly accessible MLPerf Power offline inference edge submissions. Report the maximum energy efficiency (performance/power) of any single submission at or before the specified version. 

## Figure 5c

Description - Energy efficiency trends of MLPerf Power offline inference tiny submissions.

Data Source - Energy efficiency numbers are from the publicly accessible MLPerf Power offline inference tiny submissions. Report the maximum energy efficiency (performance/power) of any single submission at or before the specified version. 

## Figure 6

Description - Energy consumption breakdown and time-to-train for Llama2-70b fine runing across different training system scales.

Data Source - Energy consumption and time-to-train numbers are from the publicly accessible MLPerf Power Training v4.0 data. Specifically, submissions 4.0-0090 - 4.0-0097. Energy breakdown numbers are in the publicly accessible notes for these submissions.

## Figure 7

Description - Same system energy consumption and total computation (measured in MACs) for each MLPerf Inference and MLPerf Tiny benchmark. Note that all blue datacenter system energy consumption numbers are from the same system submission, and all red tiny system energy consumption numbers are from the same system submission. The datacenter and tiny system are different, but are put on the same figure to make a rough comparison across scales.

Data Source - Energy consumption numbers are from publicly accessible MLPerf Power offline data. Specifically, the datacenter submission is from v4.0-0063 and the tiny submission is from v1.2-0004. The MAC numbers are from publicly accessible data about benchmark specifications.

## Figure 8

Description - Histogram of energy efficiency drop when increasing the BERT benchmark target accuracy.

Data Source - Energy efficiency numbers are from publicly accessible MLPerf Power v3,1, v4.0, and v4.1 offline inference datacenter data. Each histogram data point represents one submission with an identical system that submited results to both the BERT-99.0 and BERT-99.9 benchmarks.

## Figure 9

Description - Energy efficiency at low and high accuracy BERT benchmark targets. Between v2.1 and v3.0, more aggressive quantization can be used to achieve the same high accuracy, boosting energy efficiency in the high accuracy benchmark.

Data Source - Energy efficiency numbers are from publicly accessible MLPerf Power Training v1.0 - v4.0 data on comparable NVIDIA DGX 8 accelerator system submissions on the LLama2 benchmark. Specifically, the submissions are:

v1.0 - 1.0-73
v1.1 - 1.1-048
v2.0 - 2.0-095
v2.1 - 2.1-0089
v3.1 - 3.1-0109
v4.0 - 4.0-0063

## Figure 10

Description - Histogram of energy efficiency change when the submission hardware is consistent and software is changed.

Data Source - Energy efficiency numbers are from publicly accessible MLPerf Power offline inference datacenter data. Each histogram data point represents one submission with identical hardware configurations on one benchmark that submited results to 2 consecutive versions on the same benchmark.

## Figure 11a

Description - Energy efficiency from software optimizations on an identical system across 4 MLPerf Inference Edge versions.

Data Source - Energy efficiency numbers are from publicly accessible MLPerf Power offline inference edge v1.1 - v3.1 data on comparable GIGABYTE R282 system submissions on the ResNet benchmark. Specifically, the submissions are:

v1.1 - 1.1-124
v2.0 - 2.0-132
v3.0 - 3.0-0101
v3.1 - 3.1-0127

## Figure 11b

Description - Energy efficiency from hardware optimizations on consecutive versions of the same family of systems.

Data Source - These measurements are proprietary and not verified by MLPerf Power. We report the data and figure to show the trends in energy efficiency improvements from hardware optimizations.