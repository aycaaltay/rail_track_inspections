import pandas as pd
from scipy.stats import bernoulli, binom, poisson, randint
import numpy as np
import os

def DefectGeneration(lambda1, horizon):
    defects = poisson.rvs(lambda1, size = horizon)
    cumulative_defects = np.cumsum(defects)
    return defects, cumulative_defects

def InspectionIntervalGeneration(horizon):
    insp_intervals = []
    day = 0
    rand_inspection = randint.rvs(2,10)
    while day < horizon and day+rand_inspection < horizon:
        insp_intervals.append(rand_inspection)
        rand_inspection = randint.rvs(2, 10)
        day = sum(insp_intervals)

    insp_times = np.cumsum(insp_intervals)

    return insp_intervals, insp_times, len(insp_times)

def BinomialInspections(cumulative_defects, insp_intervals, insp_times, p, q):
    num_inspections = len(insp_intervals)
    insp_results = [0]* num_inspections
    num_defects = [0] * num_inspections

    for i in range(num_inspections):
        num_defects[i] = cumulative_defects[insp_times[i]-1] - sum(insp_results)
        w = bernoulli.rvs(p)
        if w==1:
            insp_results[i] = num_defects[i]
        elif w==0 and num_defects[i] >1:
            insp_results[i] = binom.rvs(num_defects[i]-1,q)

    return insp_results, num_defects

def ZeroInflatedInspection(cumulative_defects, insp_intervals, insp_times, p):
    num_inspections = len(insp_intervals)
    insp_results = [0] * num_inspections
    num_defects = [0]*num_inspections

    for i in range(num_inspections):
        num_defects[i] = cumulative_defects[insp_times[i] - 1] - sum(insp_results)
        w = bernoulli.rvs(p)
        if w ==0:
            insp_results[i] = num_defects[i]

    return insp_results, num_defects

def GenerateTrials(lambda1, p, q, track_length):

    defects, cumulative_defects = DefectGeneration(lambda1 * track_length, horizon)
    insp_intervals, insp_times, num_inspections= InspectionIntervalGeneration(horizon)

    if model_type == 1:
        insp_results, num_defects = ZeroInflatedInspection(cumulative_defects, insp_intervals, insp_times, p)
    else:
        insp_results, num_defects = BinomialInspections(cumulative_defects, insp_intervals, insp_times, p, q)
    return insp_intervals, insp_times, num_inspections, num_defects, insp_results

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

if __name__ == "__main__":
    #Assign the list of p and q values
    p_values = np.arange(0.05, 0.96, 0.05)
    q_values = np.arange(0.05, 0.96, 0.05)
    #Define inspection horizon and the number of trials for each scenario
    horizon = 5000
    num_trials = 3
    # Assign track length
    track_length = 10 #km


    # Take the model (analysis) type as a user input
    model_type =0
    print("\nInitiating...\n")
    print("Enter 1 for generating scenarios for complete miss rates (zero-inflated Poisson) ")
    print("Enter 2 for generating scenarios for partial miss rates (Poisson-Binomial)\n")
    while model_type < 1 or model_type > 2:
        model_type = int(input("Enter value: "))
        if model_type< 1 or model_type>2:
            print("You have entered a wrong number. Please enter 1 or 2. ")


    # Take the defect arrival rate as a user input
    lambda1 = 0
    while lambda1<=0:
        lambda1 = float(input("Enter defect arrival rate for simulations: "))
    # Generate folder and file names
    lambda_name = str(lambda1)
    lambda_name = lambda_name.replace(".", "");

    print("\nGenerating inspection results for "+str(len(p_values)*len(q_values))+" scenarios with "+\
          str(num_trials)+ " trials for each scenario...")
    scenario_index= 0

    if model_type == 1:
        dir_name = "ZIPScenarios"+lambda_name
    else:
        dir_name = "BPScenarios" + lambda_name
    os.makedirs(dir_name)

    scenario_information = pd.DataFrame(columns=["Scenario", "lambda", "p", "q"])
    # Initiate simulations
    for p in p_values:
        p = np.round(p,2)
        for q in q_values:
            q = np.round(q,2)
            print("Generating scenario " + str(scenario_index + 1) + "/" + str(len(p_values) * len(q_values)) + "...")
            print("p value:", p, "q value:",q)
            scenario_index += 1
            new_scenario_row = {"Scenario": scenario_index, "lambda": lambda1, "p": p, "q": q}
            scenario_information = scenario_information.append(new_scenario_row, ignore_index=True)
            inspection_data = pd.DataFrame(columns=["Scenario", "Trial", "Inspection", "Interval", "Time", "Accumulation", "Defects", \
                                                    "Rate"])

            for trial in range(num_trials):
                insp_intervals, insp_times, num_inspections, num_defects, insp_results = GenerateTrials(lambda1, p, q, track_length)

                for k in range(num_inspections):
                    new_row = {"Scenario": scenario_index, "Trial": trial+1, "Inspection": k+1, "Interval": \
                        insp_intervals[k], "Time": insp_times[k], "Accumulation": num_defects[k], \
                        "Defects": insp_results[k], "Rate": insp_intervals[k]*track_length}

                    inspection_data = inspection_data.append(new_row, ignore_index = True)

                if model_type ==1:
                    filename = dir_name+"/ZIP_Scenario" + str(scenario_index) + ".csv"
                else:
                    filename =  dir_name + "/BP_Scenario"+str(scenario_index)+".csv"
                inspection_data.to_csv(filename)

    print("Organizing information for scenarios...")
    filename= dir_name + "/Parameters.csv"
    scenario_information.to_csv(filename)

    print("Done!\n")
