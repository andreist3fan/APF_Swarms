"""
This is the main file for running the Level 4 simulations from our paper
"Multi-agent Path Planning using Artificial Potential Fields in Cluttered Environments".

This file contains the main function that runs the simulations and stores the results in a CSV file.
Furthermore, it generates histograms and plots for the minimum communication distance
and the average minimum communication distance for different obstacle densities.

"""


from Setup import Setup
import Environment as e
import Agent as a
import Evaluation as ev
import pygame as pg
import time
import math
from tqdm import tqdm
import logging
from communication import min_communication_distance
import matplotlib.pyplot as plt
import csv



logger = logging.getLogger(__name__)


def run_sim(setup):
    """
    Run the simulation for a given setup.
    Args:
        setup (Setup): The setup object containing the parameters for the simulation.
    
    """


    # Create environment and obstacles according to setup
    env = e.Environment(setup)
    logger.info("Environment created")

    # Create agent according to setup
    agents = []
    pos_agents = []
    agents_stuck = []

    # Create rest of the swarm
    for i in range((setup.nr_agents)):
        agents.append(a.Agent(setup, pos_agents, env.obstacles, False))
        pos_agents.append((agents[-1].x, agents[-1].y))
    logger.info("Agents created")

    agents_all = agents.copy()

    # Start simulation
    start_time = time.time()
    steps = 0
    running = True

    while not setup.target and running:

        ind = 0

        # Update posiiton of agents
        for i in agents:

            agent_positions = [
                (j.x, j.y) for j in agents if not j == i
            ]  # Used for Level 3: agent-agent collision avoidance

            # Update position
            i.update_position(env, setup, agent_positions)

            # Check whether agent has reached target
            i.target_check(env)

            # Check whether agent hit an obstacle
            i.obs_check(env)

            # Consequences if agent reached target
            if i.target:

                end_time = time.time()

                # Performance matrix
                setup.target = True


                # If a swarm is employed but only one agent hasn't crashed, the run is
                # not taken into account for minimum communication distance
                # (Since the communication distance is zero in this case)

                if len(agents) == 1:
                    logger.info("Target is reached. No other agents left.")
                    return
                
                # Compute various metrics (Stub from previous levels)
                setup.computational_complexity = round((end_time - start_time), 5)
                setup.path_length = len(i.pos_lst)
                setup.min_distance_target = ev.safety(i, env)

                
                
                # Compute minimum communication distance such that all agents know that
                # this one has reached the target
                min_d = min_communication_distance(agents + agents_stuck)
                # insert into Setup
                setup.min_communication_distance = min_d

                # Log data
                logger.info(
                    f"Target is reached. Minimum communication distance:{min_d}"
                )

            # Consequences if agent in trouble (hit obstacle, local minimum)
            if i.hit:
                logger.info("Agent hit an obstacle :(")
                del agents[ind]
                setup.nr_hit_agents += 1
            elif i.local_minimum:  # Check whether agent has reached a local minimum
                logger.info("Agent is stuck in a local minimum")
                # delete stuck agent
                if setup.delete_stuck:
                    agents_stuck.append(agents[ind])
                    del agents[ind]
                setup.nr_stuck_agents += 1

            ind += 1

        steps += 1

        # If too many steps required, run ends
        if steps > setup.step_limit:
            running = False
            logger.info("Run took to long and was stopped.")

        # If all agents are stuck, run failed
        if ind == 0:
            running = False


if __name__ == "__main__":
    """
    Main function to run the simulations and store the results.
    """

    # Set up the simulation parameters

    # Number of obstacles
    obs_nums = [75, 125, 175, 225, 275]
    
    # Number of Monte Carlo trials
    trials = 1000

    # Create a dictionary to store the minimum communication distances for each obstacle number
    comm_dists = {}
    for obs_num in obs_nums:
        comm_dists[obs_num] = []

    # Set up the logger
    logging.basicConfig(filename="level_4_simulations.log", level=logging.INFO)

    # Use the RAPF-T algorithm (8) or BAPF (1)
    algorithm = 8

    # Set up the simulation
    setup = Setup(algorithm)

    # Use default simulation parameters
    setup.nr_agents = 5
    setup.start_radius = 3

    setup.visual = False  # Do not display runs as we are running many trials
    setup.name = "Level_4"  

    # Run simulation
    for obs_num in obs_nums:
        print(f"Running simulations with {obs_num} obstacles.")
        setup.obstacle_number = obs_num
        ct = 0
        while ct < trials:
            # Reset setup for each trial
            setup.min_communication_distance = -1
            run_sim(setup)

            # Check if the simulation was successful
            # If not, rerun the simulation
            if setup.min_communication_distance != -1:
                logger.info(
                    f"Finished simulation #{ct+1}/{trials} with {obs_num} obstacles."
                )
                ct += 1
                comm_dists[obs_num].append(setup.min_communication_distance)
            logger.info(f"Trial finished.")
            # Reset setup for next trial
            setup.target = False
            setup.computational_complexity = 0
            setup.path_length = 0
            setup.min_distance_target = 0
            setup.nr_stuck_agents = 0
            setup.nr_hit_agents = 0

    # Plot a histogram for each obstacle number
    for obs_num in obs_nums:
        plt.clf()
        plt.hist(
            comm_dists[obs_num],
            bins=30,
            edgecolor="black",
            density=True,
            label=f"{obs_num} obstacles",
        )
        plt.title(f"Minimum communication distance for {obs_num} obstacles")
        plt.xlabel("Minimum communication distance")
        plt.ylabel("Density")
        plt.legend()
        plt.savefig(f"min_comm_dist_{obs_num}.png")

    plt.clf()

    # Plot the average minimum communication distance for each obstacle number
    plt.plot(
        obs_nums,
        [sum(comm_dists[obs_num]) / len(comm_dists[obs_num]) for obs_num in obs_nums],
        marker="x",
    )
    plt.title("Average minimum communication distance")
    plt.xlabel("Number of obstacles")
    plt.ylabel("Average minimum communication distance")
    plt.savefig("avg_min_comm_dist.png")


    # Save run results to a CSV file
    with open("results.csv", "w", newline="") as csvfile:

        writer = csv.writer(csvfile)
        header = ""
        for obs_num in obs_nums:
            header += f"obs_{obs_num},"
        writer.writerow(header[:-1].split(","))
        for i in range(trials):
            row = []
            for obs_num in obs_nums:
                if i < len(comm_dists[obs_num]):
                    row.append(comm_dists[obs_num][i])
                else:
                    row.append("")
            writer.writerow(row)
        print("Results saved to results.csv")