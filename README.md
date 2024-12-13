# MLPerf Power

[Arxiv paper](https://arxiv.org/abs/2410.12032)

Rapid adoption of machine learning (ML) technologies has led to a surge in power consumption across diverse systems, from tiny IoT devices to massive datacenter clusters. Benchmarking the energy efficiency of these systems is crucial for optimization, but presents novel challenges due to the variety of hardware platforms, workload characteristics, and system-level interactions. This paper introduces MLPerf® Power, a comprehensive benchmarking methodology with capabilities to evaluate the energy efficiency of ML systems at power levels ranging from microwatts to megawatts. Developed by a consortium of industry professionals from more than 20 organizations, coupled with insights from academia, MLPerf Power establishes rules and best practices to ensure comparability across diverse architectures. We use representative workloads from the MLPerf benchmark suite to collect 1,841 reproducible measurements from 60 systems across the entire range of ML deployment scales. Our analysis reveals trade-offs between performance, complexity, and energy efficiency across this wide range of systems, providing actionable insights for designing optimized ML solutions from the smallest edge devices to the largest cloud infrastructures. This work emphasizes the importance of energy efficiency as a key metric in the evaluation and comparison of the ML system, laying the foundation for future research in this critical area. We discuss the implications for developing sustainable AI solutions and standardizing energy efficiency benchmarking for ML systems.

# Measuring Power

[This repo](https://github.com/mlcommons/power-dev) contains the development branch of MLPerf™ power measurement code. Everything is Apache 2.0 code developed by MLCommons™. Access is available to anyone.

MLPerf™ is using [SPEC PTDaemon] tool for measuring power. Please see [this README](https://github.com/mlcommons/power-dev/tree/master/ptd_client_server) for more details on how to use it.

# Power Measurement Tutorial using MLCommons CM

*Prepared by the MLCommons taskforce on automation and reproducibility and [OctoML](https://octoml.ai)*.

## Requirements

1. Power analyzer (anyone [certified by SPEC PTDaemon](https://www.spec.org/power/docs/SPECpower-Device_List.html)). Yokogawa is the one that most submitters have submitted with and a new single-channel model like 310E can cost around 3000$. The MLCommons taskforce on automation and reproducibility is also using the [Yokogawa 310E](https://tmi.yokogawa.com/solutions/products/power-analyzers/digital-power-meter-wt300e/) to automate and simplify MLPerf submissions.

2. SPEC PTDaemon (can be downloaded from [here](https://github.com/mlcommons/power) after signing the EULA which can be requested by sending an email to `support@mlcommons.org`). Once you have GitHub access to the MLCommons power repository then the CM workflow will automatically download and configure the SPEC PTDaemon tool.

3. Access to the [MLCommons power-dev](https://github.com/mlcommons/power-dev) repository which has the `server.py` to be run on the director node and `client.py` to be run on the SUT node. This repository being public will be automatically pulled by the CM workflow.

## Connecting power analyzer to the computer

We need to connect the power analyzer to a director machine via USB and the machine must be running Linux (Ethernet mode is supported only on Windows which this workflow is not supporting yet). The power supply to the SUT is done through the power analyzer (current in series and voltage in parallel). An adapter like [this](https://amzn.to/3Cl2TV5) can help avoid cutting the electrical wires. 

![pages (14)](https://user-images.githubusercontent.com/4791823/210117283-82375460-5b3a-4e8a-bd85-9d33675a5843.png).

The director machine runs the `server.py` script and loads a server process that communicates with the SPEC PTDaemon. When a client connects to it (using `client.py`), it in turn connects to the PTDaemon and initiates a measurement run. Once the measurement ends, the power log files are transferred to the client. 

## Ranging mode and Testing mode

Power analyzers usually have different current and voltage ranges it supports and the exact ranges to be used depends on a given SUT and this needs some empirical data. We can do a ranging run where the current and voltage ranges are set to `Auto` and the power analyzer automatically figures out the correct ranges needed. These determined ranges are then used for a proper testing mode run. Using the 'auto' mode in a testing run is not allowed as it can mess up the measurements.

## Setup using MLCommons CM

## Install CM

Please follow these [instructions](https://github.com/mlcommons/ck/blob/master/docs/installation.md) to install the MLCommons CM automation tool.

## Start Power Server (Power analyzer should be connected to this computer and PTDaemon runs here)

If you are having GitHub access to [MLCommons power](https://github.com/mlcommons/power-dev) repository, PTDaemon should be automatically installed using the following CM command:

PS: The below command will ask for `sudo` permission on Linux and should be run with administrator privilege on Windows (to do NTP time sync).
```bash
cm run script --tags=mlperf,power,server --device_type=49 --device_port=/dev/usbtmc0
```
* ``--interface_flag="-U" and `--device_port=1` (can change as per the USB slot used for connecting) can be used on Windows for USB connection
* `--device_type=49` corresponds to Yokogawa 310E and `ptd -h` should list the device_type for all supported devices. The location of `ptd` can be found using the below command
* `--device_port=20` and `--interface_flag="-g" can be used to connect to GPIB interface (currently supported only on Windows) with the serial address set to 20
```bash
cat `cm find cache --tags=get,spec,ptdaemon`/cm-cached-state.json
```

More configuration options can be found [here](https://github.com/mlcommons/power-dev/tree/master/ptd_client_server).

### Running the power server inside a docker container

```bash
cm docker script --tags=run,mlperf,power,server --docker_gh_token=<GITHUB AUTH_TOKEN> \
--docker_os=ubuntu --docker_os_version=22.04 --device=/dev/usbtmc0
```
* Device address may need to be changed depending on the USB port being used
* The above command uses a host-container port mapping 4950:4950 which can be changed by using `--docker_port_maps,=4950:4950`

## Running a dummy workload with power (on host machine)

```bash
cm run script --tags=mlperf,power,client --power_server=<POWER_SERVER_IP> 
```

### Run a dummy workload with power inside a docker container

```bash
cm run script --tags=run,docker,container --cm_repo=ctuning@mlcommons-ck \
--docker_os=ubuntu --docker_os_version=22.04  \
--run_cmd="cm run script --tags==mlperf,power,client --power_server=<POWER_SERVER_IP>"
```

## Running MLPerf Image Classification with power

```bash
cm run script --tags=app,mlperf,inference,_reference,_power,_resnet50,_onnxruntime,_cpu --mode=performance --power_server=<POWER_SERVER_IP>
```

### Running MLPerf Image Classification with power inside a docker container
```bash
cm run script --tags=run,docker,container --cm_repo=ctuning@mlcommons-ck  \
--docker_os=ubuntu --docker_os_version=22.04  \
--run_cmd="cm run script --tags=app,mlperf,inference,_reference,_power,_resnet50,_onnxruntime,_cpu --mode=performance --power_server=<POWER_SERVER_IP>"
```

### Using CM GUI to run MLPerf inference benchmarks and measure power

[Link](https://access.cknowledge.org/playground/?action=howtorun&bench_uid=39877bb63fb54725)

## Further questions?

If you have further questions, are interested in our development roadmap, or need help to automate, optimize and validate your MLPerf submission, feel free to contact the MLCommons taskforce on automation and reproducibility.

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

We encourage users to build on our analysis and draw deeper insights from the MLPerf Power submission data. We anticipate that there is still much to learn about energy efficiency optimizations from the data and logs

# Figure Descriptions

## Figure 1

Description - Performance trends of MLPerf Inference submissions vs Moore's Law.

Data Source - Performance numbres are from the publicly accessible MLPerf inference data (same data as [MLPerf Inference Benchmark paper](https://arxiv.org/pdf/1911.02549), ISCA 2020).

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

Data Source - Energy consumption and time-to-train numbers are from the publicly accessible MLPerf Power Training v4.0 data. Specifically, submissions v4.0-0090 - v4.0-0097. Energy breakdown numbers are in the publicly accessible notes for these submissions.

## Figure 7

Description - Same system energy consumption and total computation (measured in MACs) for each MLPerf Inference and MLPerf Tiny benchmark. Note that all blue datacenter system energy consumption numbers are from the same system submission, and all red tiny system energy consumption numbers are from the same system submission. The datacenter and tiny system are different, but are put on the same figure to make a rough comparison across scales.

Data Source - Energy consumption numbers are from publicly accessible MLPerf Power offline data. Specifically, the datacenter submission is from v4.0-0063 and the tiny submission is from v1.2-0004. The MAC numbers are from publicly accessible data about benchmark specifications.

## Figure 8

Description - Histogram of energy efficiency drop when increasing the BERT benchmark target accuracy.

Data Source - Energy efficiency numbers are from publicly accessible MLPerf Power v3,1, v4.0, and v4.1 offline inference datacenter data. Each histogram data point represents one submission with an identical system that submited results to both the BERT-99.0 and BERT-99.9 benchmarks.

## Figure 9

Description - Energy efficiency at low and high accuracy BERT benchmark targets. Between v2.1 and v3.0, more aggressive quantization can be used to achieve the same high accuracy, boosting energy efficiency in the high accuracy benchmark.

Data Source - Energy efficiency numbers are from publicly accessible MLPerf Power Training v1.0 - v4.0 data on comparable NVIDIA DGX 8 accelerator system submissions on the LLama2 benchmark. Specifically, the submissions are:

v1.0-73, v1.1-048, v2.0-095, v2.1-0089, v3.1-0109, v4.0-0063

## Figure 10

Description - Histogram of energy efficiency change when the submission hardware is consistent and software is changed.

Data Source - Energy efficiency numbers are from publicly accessible MLPerf Power offline inference datacenter data. Each histogram data point represents one submission with identical hardware configurations on one benchmark that submited results to 2 consecutive versions on the same benchmark.

## Figure 11a

Description - Energy efficiency from software optimizations on an identical system across 4 MLPerf Inference Edge versions.

Data Source - Energy efficiency numbers are from publicly accessible MLPerf Power offline inference edge v1.1 - v3.1 data on comparable GIGABYTE R282 system submissions on the ResNet benchmark. Specifically, the submissions are:

v1.1-124, v2.0-132, v3.0-0101, v3.1-0127

## Figure 11b

Description - Energy efficiency from hardware optimizations on consecutive versions of the same family of systems.

Data Source - These measurements are proprietary and not verified by MLPerf Power. We report the data and figure to show the trends in energy efficiency improvements from hardware optimizations.