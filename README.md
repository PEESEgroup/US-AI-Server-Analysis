# US-AI-Server-Analysis
This study unveils the energy/water/climate impact of AI servers in the U.S. from 2024 to 2030 and highlight the emergent actions required from both the governmental and industrial bodies. The following contents are included in this repository to support our key findings:
1. Codes: include major codes to conduct the estimation process.
2. Data: include all data used during the analysis.

## Requirements
To run the codes in this repository, the following Python and core packages must be installed (version is given for refenrence):
- Python 3.9.13
- numpy 1.21.5
- pyomo 6.5.0 with ipopt solver
- csv 1.0
- cyipopt 1.1.0
- ReEDs 2.0 (specific settings,installations and computing resource requirements can be found in https://github.com/NREL/ReEDS-2.0)

The above packages can be conveniently downloaded through open-source library within a few hours on a normal computer. There is no specific computing resource requirements to run the main codes, which can be runned on normal computer within a few seconds.

## Codes
- **Best&Worst PUE and WUE.py**: This file contains the calculation process for generating the best and worst PUE and WUE cases for AI data centers.
- **simulation_funs_DC_i.py**: This file defines the basic functions for evaluating the PUE and WUE values of AI data centers.
- **LoadFile.py**: This file edit the baseline load file provided by the ReEDs 2.0 model (specific settings can be found in https://github.com/NREL/ReEDS-2.0) by involving AI server loads.
- **Main_Base_Scenario.py**: This file runs a base case for estimating the energy/water/carbon footprints of AI servers in the U.S. from 2024 to 2030.
- **Main_Best_Carbon_Scenario.py**: This file runs best carbon emission practice scenarios for AI servers in the U.S. from 2024 to 2030.
- **Main_Worst_Carbon_Scenario.py**: This file runs worst carbon emission practice scenarios for AI servers in the U.S. from 2024 to 2030.
- **Main_Best_Water_Scenario.py**: This file runs a best water footprint practice scenarios for AI servers in the U.S. from 2024 to 2030.
- **Main_Worst_Water_Scenario.py**: This file runs a worst water footprint practice scenarios for AI servers in the U.S. from 2024 to 2030.

## Data
- **PUE and WUE values of each state in the U.S.**: Best_PUE.csv, Best_WUE.csv, Baseline_PUEWUE.csv, Worst_PUE.csv, Worst_WUE.csv
- **Carbon emission per unit of electricity data of each U.S. region from 2024 to 2030**: txt files with CF notation in the Grid Factor folder
- **Water usage per unit of electricity data of each U.S. region from 2024 to 2030**: txt files with WF notation in the Grid Factor folder
- **Spatial allocation ratio of each U.S. states**: txt files with spatial notation in the Spatial Distribution folder
- **Settings for generating the grid factors through the ReEDs model**: cases_R3.csv in the Grid Factor folder
- **Collected AI data center locations**: csv file with AI data center notation
- **Example files of ReEDS model output**: emit_r.csv, gen_ann.csv, water_consumption_ivrt.csv in the Grid Factor folder

## Running the code
### Running the base case
The file **Main_Base_Scenario.py** can be used to run a base case for estimating the energy/water/carbon footprints of AI servers in the U.S. from 2024 to 2030. After download the codes and data, simply replace the "FILE PATH" used in the code file with the install path of our data folder to run the simulation.
### Running the best/worst cases
The other "Main" files can be used to run the best and worst practices considering carbon emission and water footprint. After download the codes and data, simply replace the "FILE PATH" used in the code file with the install path of our data folder to run the simulation.

## Citation
Please use the following citation when using the data, methods or results of this work:

Xiao, T., Fuso-Nerini, F., Matthews, D., Tavoni, M., You, F., Environmental impact and net-zero pathways for sustainable artificial intelligence servers in the USA. Accepted by Nature Sustainability. doi:10.1038/s41893-025-01681-y 

## License
This project is covered under the **Apache 2.0 License**.


