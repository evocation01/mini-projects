import pandas as pd
from pulp import LpMinimize, LpProblem, LpStatus, LpVariable, lpSum, value

# Load datasets
warehouse_capabilities = pd.read_csv(
    "Projects/python/or1-project/data/Supply chain logistics problem - WhCapabilities.csv"
)
freight_rates = pd.read_csv(
    "Projects/python/or1-project/data/Supply chain logistics problem - FreightRates.csv"
)
plant_ports = pd.read_csv(
    "Projects/python/or1-project/data/Supply chain logistics problem - PlantPorts.csv"
)
products_per_plant = pd.read_csv(
    "Projects/python/or1-project/data/Supply chain logistics problem - ProductsPerPlant.csv"
)
order_list = pd.read_csv(
    "Projects/python/or1-project/data/Supply chain logistics problem - OrderList.csv"
)
vmi_customers = pd.read_csv(
    "Projects/python/or1-project/data/Supply chain logistics problem - VmiCustomers.csv"
)
wh_costs = pd.read_csv(
    "Projects/python/or1-project/data/Supply chain logistics problem - WhCosts.csv"
)


# Convert 'rate' column to numeric by removing '$' and converting to float
freight_rates["minimum cost"] = (
    freight_rates["minimum cost"].replace("[\$,]", "", regex=True).astype(float)  # type: ignore
)

# Aggregate demand by destination port
demand_by_port = order_list.groupby("Destination Port")["Unit quantity"].sum().to_dict()
total_demand = sum(demand_by_port.values())

# Extract plant capacities
plant_capacities = warehouse_capabilities.set_index("Plant ID")[
    "Daily Capacity "
].to_dict()
total_supply = sum(
    plant_capacities.values()
)  # Calculate total supply from plant capacities

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

# Initialize model
model = LpProblem("Supply_Chain_Optimization_Simple", LpMinimize)

# Define decision variables for shipments (for all plants)
ship_vars = {
    (plant, "PORT09"): LpVariable(f"Ship_{plant}_PORT09", lowBound=0, cat="Continuous")
    for plant in plant_capacities.keys()
}

# Objective function: Minimize transport cost
model += (
    lpSum(
        ship_vars[(plant, "PORT09")]
        * freight_costs.get((plant_to_port[plant], "PORT09"), 1e6)
        for plant in plant_capacities.keys()
    ),
    "Total_Transport_Cost",
)

# Supply constraints: Ensure total shipments from each plant do not exceed capacity
for plant in plant_capacities.keys():
    model += (
        ship_vars[(plant, "PORT09")] <= plant_capacities[plant],
        f"Supply_Constraint_{plant}",
    )

# Demand constraint: Ensure total shipments meet total available supply
model += (
    lpSum(ship_vars[(plant, "PORT09")] for plant in plant_capacities.keys())
    == total_supply,
    "Adjusted_Demand_Constraint",
)


# Solve the model
model.solve()

# Print results
print("Status:", LpStatus[model.status])
print("Total Cost:", value(model.objective))

# Print shipment decisions
for (plant, destination), var in ship_vars.items():
    if var.varValue > 0:  # type: ignore
        print(f"{plant} -> {destination}: {var.varValue}")
