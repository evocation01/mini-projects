import os

import pandas as pd
import pytest
from supply_chain import optimize_supply_chain


@pytest.fixture
def synthetic_filepath_no_demand(tmp_path):
    """Fixture for a synthetic dataset with zero demand."""
    filepath = tmp_path / "synthetic_no_demand.xlsx"

    order_list = pd.DataFrame({"Destination Port": ["PORT09"], "Unit quantity": [0]})

    wh_capacities = pd.DataFrame(
        {"Plant ID": ["PLANT01", "PLANT02"], "Daily Capacity ": [1000, 2000]}
    )

    plant_ports = pd.DataFrame(
        {"Plant Code": ["PLANT01", "PLANT02"], "Port": ["PORT01", "PORT02"]}
    )

    freight_rates = pd.DataFrame(
        {
            "orig_port_cd": ["PORT01", "PORT02"],
            "dest_port_cd": ["PORT09", "PORT09"],
            "minimum cost": [1.5, 2.0],
        }
    )

    wh_costs = pd.DataFrame({"WH": ["PLANT01", "PLANT02"], "Cost/unit": [1.0, 1.5]})

    products_per_plant = pd.DataFrame(
        {"Plant Code": ["PLANT01", "PLANT02"], "Product ID": [101, 102]}
    )

    with pd.ExcelWriter(filepath) as writer:
        order_list.to_excel(writer, sheet_name="OrderList", index=False)
        wh_capacities.to_excel(writer, sheet_name="WhCapacities", index=False)
        plant_ports.to_excel(writer, sheet_name="PlantPorts", index=False)
        freight_rates.to_excel(writer, sheet_name="FreightRates", index=False)
        wh_costs.to_excel(writer, sheet_name="WhCosts", index=False)
        products_per_plant.to_excel(writer, sheet_name="ProductsPerPlant", index=False)

    return str(filepath)


@pytest.fixture
def synthetic_filepath(tmp_path):
    """Fixture to create a temporary synthetic Excel file for testing."""
    filepath = tmp_path / "synthetic_supply_chain.xlsx"

    order_list = pd.DataFrame(
        {"Destination Port": ["PORT09", "PORT09"], "Unit quantity": [1500, 2000]}
    )

    wh_capacities = pd.DataFrame(
        {"Plant ID": ["PLANT01", "PLANT02"], "Daily Capacity ": [1000, 2000]}
    )

    plant_ports = pd.DataFrame(
        {"Plant Code": ["PLANT01", "PLANT02"], "Port": ["PORT01", "PORT02"]}
    )

    freight_rates = pd.DataFrame(
        {
            "orig_port_cd": ["PORT01", "PORT02"],
            "dest_port_cd": ["PORT09", "PORT09"],
            "minimum cost": [1.5, 2.0],
        }
    )

    wh_costs = pd.DataFrame({"WH": ["PLANT01", "PLANT02"], "Cost/unit": [1.0, 1.5]})

    products_per_plant = pd.DataFrame(
        {"Plant Code": ["PLANT01", "PLANT02"], "Product ID": [101, 102]}
    )

    with pd.ExcelWriter(filepath) as writer:
        order_list.to_excel(writer, sheet_name="OrderList", index=False)
        wh_capacities.to_excel(writer, sheet_name="WhCapacities", index=False)
        plant_ports.to_excel(writer, sheet_name="PlantPorts", index=False)
        freight_rates.to_excel(writer, sheet_name="FreightRates", index=False)
        wh_costs.to_excel(writer, sheet_name="WhCosts", index=False)
        products_per_plant.to_excel(writer, sheet_name="ProductsPerPlant", index=False)

    return str(filepath)


def test_optimize_supply_chain_with_no_demand(synthetic_filepath_no_demand):
    """Test optimize_supply_chain with zero demand."""
    optimal_solution, total_cost = optimize_supply_chain(synthetic_filepath_no_demand)
    assert isinstance(
        optimal_solution, dict
    ), "Optimal solution should be a dictionary."
    assert (
        sum(optimal_solution.values()) == 0
    ), "No quantities should be transported when demand is zero."
    assert total_cost == 0, "Total cost should be zero when demand is zero."


def test_optimize_supply_chain_with_synthetic_data(synthetic_filepath):
    """Test optimize_supply_chain with synthetic data."""
    optimal_solution, total_cost = optimize_supply_chain(synthetic_filepath)
    assert isinstance(
        optimal_solution, dict
    ), "Optimal solution should be a dictionary."
    assert total_cost > 0, "Total cost should be greater than zero."
    assert (
        sum(optimal_solution.values()) == 3000
    ), "Total transported quantity should match the demand."


def test_optimize_supply_chain_with_real_data():
    """Test optimize_supply_chain with real data file (if available)."""
    real_filepath = "data/Supply chain logistics problem.xlsx"
    if os.path.exists(real_filepath):
        optimal_solution, total_cost = optimize_supply_chain(real_filepath)
        assert isinstance(
            optimal_solution, dict
        ), "Optimal solution should be a dictionary."
        assert total_cost > 0, "Total cost should be greater than zero."
    else:
        pytest.skip("Real data file not found.")


if __name__ == "__main__":
    import os
    import sys

    # Ensure the project root is in sys.path for absolute imports
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    pytest.main()
