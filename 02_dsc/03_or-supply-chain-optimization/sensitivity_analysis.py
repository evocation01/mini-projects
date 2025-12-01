import logging

import pandas as pd
from supply_chain import optimize_supply_chain

logging.basicConfig(level=logging.INFO)


def perform_sensitivity_analysis(filepath):
    """Perform sensitivity analysis on transportation costs, capacities, and demand."""

    # Load original data
    order_list = pd.read_excel(filepath, sheet_name="OrderList")
    freight_rates = pd.read_excel(filepath, sheet_name="FreightRates")
    wh_capacities = pd.read_excel(filepath, sheet_name="WhCapacities")
    wh_costs = pd.read_excel(filepath, sheet_name="WhCosts")
    products_per_plant = pd.read_excel(filepath, sheet_name="ProductsPerPlant")
    plant_ports = pd.read_excel(filepath, sheet_name="PlantPorts")

    variations = [-0.2, -0.1, 0.1, 0.2]
    results = []

    # Vary transportation costs
    for variation in variations:
        modified_freight_rates = freight_rates.copy()
        modified_freight_rates["minimum cost"] *= 1 + variation
        modified_filepath = "temp_modified_costs.xlsx"
        with pd.ExcelWriter(modified_filepath) as writer:
            order_list.to_excel(writer, sheet_name="OrderList", index=False)
            modified_freight_rates.to_excel(
                writer, sheet_name="FreightRates", index=False
            )
            wh_capacities.to_excel(writer, sheet_name="WhCapacities", index=False)
            wh_costs.to_excel(writer, sheet_name="WhCosts", index=False)
            products_per_plant.to_excel(
                writer, sheet_name="ProductsPerPlant", index=False
            )
            plant_ports.to_excel(writer, sheet_name="PlantPorts", index=False)

        solution, total_cost = optimize_supply_chain(modified_filepath)
        total_quantity = sum(solution.values())
        results.append(
            {
                "Parameter": "Transportation Cost",
                "Variation": f"{variation*100:+.0f}%",
                "Total Cost": total_cost,
                "Total Quantity": total_quantity,
                "Num Plants Used": len(solution),
            }
        )

    # Vary plant capacities
    for variation in variations:
        modified_capacities = wh_capacities.copy()
        modified_capacities["Daily Capacity "] *= 1 + variation
        modified_filepath = "temp_modified_capacities.xlsx"
        with pd.ExcelWriter(modified_filepath) as writer:
            order_list.to_excel(writer, sheet_name="OrderList", index=False)
            freight_rates.to_excel(writer, sheet_name="FreightRates", index=False)
            modified_capacities.to_excel(writer, sheet_name="WhCapacities", index=False)
            wh_costs.to_excel(writer, sheet_name="WhCosts", index=False)
            products_per_plant.to_excel(
                writer, sheet_name="ProductsPerPlant", index=False
            )
            plant_ports.to_excel(writer, sheet_name="PlantPorts", index=False)

        solution, total_cost = optimize_supply_chain(modified_filepath)
        total_quantity = sum(solution.values())
        results.append(
            {
                "Parameter": "Plant Capacity",
                "Variation": f"{variation*100:+.0f}%",
                "Total Cost": total_cost,
                "Total Quantity": total_quantity,
                "Num Plants Used": len(solution),
            }
        )

    # Vary demand
    for variation in variations:
        modified_order_list = order_list.copy()
        modified_order_list["Unit quantity"] *= 1 + variation
        modified_filepath = "temp_modified_demand.xlsx"
        with pd.ExcelWriter(modified_filepath) as writer:
            modified_order_list.to_excel(writer, sheet_name="OrderList", index=False)
            freight_rates.to_excel(writer, sheet_name="FreightRates", index=False)
            wh_capacities.to_excel(writer, sheet_name="WhCapacities", index=False)
            wh_costs.to_excel(writer, sheet_name="WhCosts", index=False)
            products_per_plant.to_excel(
                writer, sheet_name="ProductsPerPlant", index=False
            )
            plant_ports.to_excel(writer, sheet_name="PlantPorts", index=False)

        solution, total_cost = optimize_supply_chain(modified_filepath)
        total_quantity = sum(solution.values())
        results.append(
            {
                "Parameter": "Demand",
                "Variation": f"{variation*100:+.0f}%",
                "Total Cost": total_cost,
                "Total Quantity": total_quantity,
                "Num Plants Used": len(solution),
            }
        )

    # Convert results to a DataFrame and save to CSV
    results_df = pd.DataFrame(results)
    results_df.to_csv("sensitivity_analysis_results.csv", index=False)
    print("Sensitivity analysis results saved to sensitivity_analysis_results.csv")
    return results_df


if __name__ == "__main__":
    path = "Projects/python/or1-project/data/Supply chain logistics problem.xlsx"
    perform_sensitivity_analysis(path)
