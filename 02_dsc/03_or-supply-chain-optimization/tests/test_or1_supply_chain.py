import numpy as np
import pandas as pd
import pytest
from scipy.optimize import linprog


@pytest.fixture
def synthetic_data():
    """Fixture to provide synthetic datasets for testing."""
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

    return order_list, wh_capacities, plant_ports, freight_rates


def test_total_supply_vs_demand(synthetic_data):
    """Test if total supply meets demand correctly."""
    order_list, wh_capacities, _, _ = synthetic_data
    total_supply = wh_capacities["Daily Capacity "].sum()
    total_demand = order_list["Unit quantity"].sum()
    assert (
        total_supply < total_demand
    ), "Supply is intentionally less than demand for this test case."


def test_valid_freight_pairs(synthetic_data):
    """Test if valid freight pairs are correctly identified."""
    _, _, plant_ports, freight_rates = synthetic_data
    plant_to_port = plant_ports.set_index("Plant Code")["Port"].to_dict()
    valid_pairs = [
        (plant, "PORT09")
        for plant, port in plant_to_port.items()
        if port in freight_rates["orig_port_cd"].values
    ]
    assert len(valid_pairs) > 0, "There should be valid freight pairs."


def test_optimization_result(synthetic_data):
    """Test if optimization returns a valid solution."""
    _, wh_capacities, _, _ = synthetic_data
    cost_vector = [1.5, 2.0]
    A_ub = [[1, 0], [0, 1]]
    b_ub = wh_capacities["Daily Capacity "].tolist()
    A_eq = [[1, 1]]
    b_eq = [3500]
    result = linprog(
        cost_vector, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, method="highs"
    )
    assert (
        not result.success
    ), "Optimization should correctly report infeasibility when supply is insufficient."
    if result.success:
        assert (
            abs(sum(result.x) - 3500) < 1e-6
        ), "Total transported quantity should match demand."
