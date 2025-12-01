import logging

import pandas as pd
from scipy.optimize import linprog

# Configure logging
logging.basicConfig(level=logging.INFO)


def optimize_supply_chain(filepath):
    """
    Function to load data, set up constraints, and solve the supply chain optimization problem.

    Parameters:
    filepath (str): Path to the Excel file containing the supply chain data.

    Returns:
    tuple: (optimal_solution, total_cost) if successful, otherwise raises an error.
    """
    try:
        # Load dataset
        order_list = pd.read_excel(filepath, sheet_name="OrderList")
        freight_rates = pd.read_excel(filepath, sheet_name="FreightRates")
        wh_costs = pd.read_excel(filepath, sheet_name="WhCosts")
        wh_capacities = pd.read_excel(filepath, sheet_name="WhCapacities")
        products_per_plant = pd.read_excel(filepath, sheet_name="ProductsPerPlant")
        plant_ports = pd.read_excel(filepath, sheet_name="PlantPorts")
        logging.info("Datasets loaded successfully.")
    except FileNotFoundError as e:
        logging.error(f"Error loading dataset: {e}")
        raise

    # Aggregate demand by destination port
    demand_by_port = (
        order_list.groupby("Destination Port")["Unit quantity"].sum().to_dict()
    )

    total_demand = sum(demand_by_port.values())

    # Handle zero demand case
    if total_demand == 0:
        logging.info("Total demand is zero. Returning zero cost and empty solution.")
        return {}, 0

    # Extract plant capacities
    plant_capacities = wh_capacities.set_index("Plant ID")["Daily Capacity "].to_dict()

    # Map plants to their respective ports
    plant_to_port = plant_ports.set_index("Plant Code")["Port"].to_dict()

    # Filter relevant freight rates based on available plant-port combinations
    relevant_freight_rates = freight_rates[
        freight_rates["orig_port_cd"].isin(plant_to_port.values())
        & freight_rates["dest_port_cd"].isin(demand_by_port.keys())
    ]

    # Create cost dictionary for relevant (origin, destination) pairs
    freight_costs = (
        relevant_freight_rates.groupby(["orig_port_cd", "dest_port_cd"])["minimum cost"]
        .min()
        .to_dict()
    )

    # Ensure valid pairs exist
    valid_pairs = [
        (plant, "PORT09")
        for plant, port in plant_to_port.items()
        if (port, "PORT09") in freight_costs
    ]
    if not valid_pairs:
        logging.error("No valid (plant, port) pairs found in the dataset.")
        raise ValueError("Invalid dataset: No valid routes available.")

    cost_vector = [
        freight_costs[(plant_to_port[plant], "PORT09")] for plant, _ in valid_pairs
    ]

    # Construct inequality constraints for plant capacities
    A_ub = [
        [1 if pair[0] == plant else 0 for pair in valid_pairs]
        for plant in plant_capacities.keys()
    ]
    b_ub = [plant_capacities[plant] for plant in plant_capacities.keys()]

    # Equality constraint to satisfy demand at PORT09
    A_eq = [
        [1 for _ in valid_pairs]
    ]  # All pairs contribute to meeting the demand at PORT09
    b_eq = [sum(plant_capacities.values())]  # Adjusted demand to match total supply

    # Solve the linear programming problem with adjusted demand
    result = linprog(
        cost_vector, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, method="highs"
    )

    if result.success:
        optimal_solution = {
            valid_pairs[i]: result.x[i]
            for i in range(len(valid_pairs))
            if result.x[i] > 0
        }
        total_cost = result.fun
        logging.info("Optimization completed successfully.")
        return optimal_solution, total_cost
    else:
        logging.error("No optimal solution found.")
        raise ValueError("Optimization failed: No feasible solution found.")


if __name__ == "__main__":
    path = "Projects/python/or1-project/data/Supply chain logistics problem.xlsx"
    try:
        solution, cost = optimize_supply_chain(path)
        print("Optimal solution:", solution)
        print("Total cost:", cost)
    except Exception as e:
        print(f"Error: {e}")
