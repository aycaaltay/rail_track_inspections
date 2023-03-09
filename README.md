# rail_track_inspections
Rail track inspection simulations with complete (zero-inflated) and partial (binomial) miss rates

--------------------------------

**Step 0.** Install the required python modules given in the requirement.txt file using the line below:

_pip install -r requirements.txt_
--------------------------------

**Step 1.** Generate new simulation data or import the readily available data

You can 
- either generate new simulation data using the file in the Scenario_Generation_For_Simulations directory as specified in Step 1a below. 
- or use the readily available data in the data directory and skip Step 1b.

_Step 1a. Generating inspection scenarios_

_main_scenario_generation.py_ file requires you to enter the analysis type and the defect arrival rate (per day and km) manually. 

For analysis type, please enter 
- enter 1 for generating data that follows a zero-inflated Poisson model, or
- enter 2 for generating data that follows a Poisson-Binomial model.

Then, enter the $\lambda$ rate for daily defect arrival rate per km.

A new folder will be created specifying the analysis type and the defect arrival rate. All simulation information will be saved in this directory.

Please note that this file uses $p$ and $q$ values ranging from 0.05 to 0.95 with an increment of 0.05 (19 unique values for both variables). A total of $19 \cdot 19 = 361$  scenarios will be generated. 
If you would like to change these increments or bounds, you can do so by changing lines 65-66 within the .py file.

Step 1b. Loading available data

You can use one of the folders in the data directory for testing the simulations. 
--------------------------------

**Step 2.** Testing inspection scenarios 

If the folder you want to analyze is starting with "ZIP", it is a file prepared for Zero-Inflated Poisson model with complete miss rates. 

If the folder you want to analyze is starting with "BP", it is a file prepared for Poisson-Binomial model with partial miss rates. 
