import os
import time
import building_recognition.mask_conversion as mc
import building_recognition.predict as prd
import visualization
from Simulation import Simulation
import FileWrite
import Paramaters as Par
from image_processing import process_image


# runs a simple simulation with the specified number of trials.
def run_simple_test():
    print("Running Simulation")
    start = time.time()
    sim = Simulation(Par.DESIRED_STATS, Par.OBJECTS)
    sim.run_simulation(Par.FIRES_TO_SIMULATE)
    FileWrite.write_simple_stats(Par.CSV_file, sim.get_statistics(), Par.FIRES_TO_SIMULATE, Par.HEATMAP_TITLE)
    end = time.time()
    print(f"Took {end - start} seconds to run.")
    return


# This simulation runs a simple simulation on a list of specified mitigation levels. Use without Heatmap!
def run_mitigation_levels_test(mitigation_levels, csv_name=Par.CSV_file):
    data = [["Mitigation Level"] + Par.DESIRED_STATS]
    print("Running Simulation", flush=True)
    start = time.time()
    for m_level in mitigation_levels:
        # m_level = mitigation_levels[int(os.getenv("SGE_TASK_ID")) - 1]
        Par.MITIGATION_LEVEL = m_level  # I might be tweaking but this doesn't sound right
        start_level = time.time()
        data_row = [m_level]
        sim = Simulation(Par.DESIRED_STATS, Par.OBJECTS)
        sim.run_simulation(Par.FIRES_TO_SIMULATE)
        sim_stats = sim.get_statistics()
        for stat in sim_stats.keys():
            if stat != "Heatmap":
                data_row.append(sim_stats.get(stat))
        data.append(data_row)
        end_level = time.time()
        print(f"{m_level} finished in {end_level - start_level}", flush=True)
    FileWrite.write_2d_stats(csv_name, data)
    end = time.time()
    print(f"Took {end - start} seconds to run.", flush=True)
    return


def test_heatmap():
    sim = Simulation(["Heatmap"], Par.OBJECTS)
    sim.run_simulation(1000)
    data = sim.get_statistics()["Heatmap"]
    visualization.visualize_aftermath(data, 1000, "WestCountyHawkWatchTest")
    return


def run_prob_iteration_test(prob_levels, mitigation_levels):
    start = time.time()
    for prob in prob_levels:
        #prob = prob_levels[int(os.getenv("SGE_TASK_ID")) - 1]
        print(f"Running {prob} probability.", flush=True)
        run_mitigation_levels_test(mitigation_levels, "results_" + str(prob) + ".csv")
    end = time.time()
    print(f"Total took {end - start} seconds to run.", flush=True)
    return


""" 
    This is the main function for the fire spread model simulation. It will run through simulations with
        varied parameters and calculate some statistics from the results.
    """
if __name__ == '__main__':
    # Par.OBJECTS = mc.get_center_coordinates(prd.predict())
    run_simple_test()
