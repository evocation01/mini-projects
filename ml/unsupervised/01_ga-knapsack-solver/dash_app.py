import os

import plotly.graph_objs as go
from dash import Dash, Input, Output, State, dcc, html
from knapsack import *


def run_ga(values, weights, capacity):
    """
    Executes the Genetic Algorithm to solve the Knapsack problem.

    Parameters:
        values (list of int): The list of item values.
        weights (list of int): The list of item weights.
        capacity (int): The maximum capacity of the knapsack.

    Returns:
        tuple: The best solution (genome) and fitness progression data.
    """

    FITNESS_LIMIT = calculate_max_fitness(values, weights, capacity)
    fitness_history = []  # To store fitness progression

    population, generations = run_evolution(
        populate_func=lambda: generate_population(20, len(values)),
        fitness_func=lambda genome: fitness_func_knapsack(
            genome, values, weights, capacity
        ),
        fitness_limit=FITNESS_LIMIT,
        generation_limit=100,
        printer=lambda pop, gen, fit_func: fitness_history.append(
            max(fit_func(gene) for gene in pop)
        ),  # Track the best fitness of each generation
    )
    return population[0], fitness_history


# Initialize Dash app
app = Dash(__name__)

# Define the layout of the app
app.layout = html.Div(
    [
        html.H1("Knapsack Problem Solver"),  # Title of the application
        html.Div(
            [
                html.Label("Enter Values (comma-separated):"),
                dcc.Input(
                    id="values",
                    type="text",
                    placeholder="e.g., 60,100,120,20,80,40",
                    value="60,100,120,20,80,40",  # Default value
                ),
            ]
        ),
        html.Div(
            [
                html.Label("Enter Weights (comma-separated):"),
                dcc.Input(
                    id="weights",
                    type="text",
                    placeholder="e.g., 10,20,30,10,5,10",
                    value="10,20,30,10,5,10",  # Default weight
                ),
            ]
        ),
        html.Div(
            [
                html.Label("Enter Knapsack Capacity:"),
                dcc.Input(
                    id="capacity", type="number", placeholder="e.g., 50", value=50
                ),
            ]
        ),
        html.Button("Run Algorithm", id="run-btn", n_clicks=0),  # Button to execute GA
        html.Div(id="results"),  # Div to display results
        dcc.Graph(id="fitness-plot"),  # Graph to display fitness progression
    ]
)


@app.callback(
    [
        Output("results", "children"),  # Updates the result display
        Output("fitness-plot", "figure"),  # Updates the fitness graph
    ],
    [Input("run-btn", "n_clicks")],  # Triggered by the button click
    [
        State("values", "value"),
        State("weights", "value"),
        State("capacity", "value"),
    ],
)
def update_output_and_plot(n_clicks, values_input, weights_input, capacity):
    """
    Updates the results and fitness graph based on user inputs and the genetic algorithm.

    Parameters:
        n_clicks (int): Number of clicks on the "Run Algorithm" button.
        values_input (str): User-provided item values (comma-separated).
        weights_input (str): User-provided item weights (comma-separated).
        capacity (int): Knapsack capacity provided by the user.

    Returns:
        tuple: HTML content for results and a Plotly figure for the fitness graph.
    """
    try:
        # Parse inputs
        values = list(map(int, values_input.split(",")))
        weights = list(map(int, weights_input.split(",")))

        # Validate input lengths
        if len(values) != len(weights):
            return (
                [html.P("Error: The number of values and weights must be the same!")],
                go.Figure(),  # Return an empty figure
            )

        # Run Genetic Algorithm
        best_solution, fitness_history = run_ga(values, weights, capacity)
        total_value = fitness_func_knapsack(best_solution, values, weights, capacity)
        total_weight = sum(g * w for g, w in zip(best_solution, weights))

        # Prepare results
        results = [
            html.P(f"Best Solution: {best_solution}"),
            html.P(f"Total Value: {total_value}"),
            html.P(f"Total Weight: {total_weight}"),
        ]

        # Prepare fitness plot
        fig = go.Figure(
            data=[
                go.Scatter(
                    x=list(range(len(fitness_history))),
                    y=fitness_history,
                    mode="lines+markers",
                    name="Fitness",
                )
            ]
        )
        fig.update_layout(
            title="Fitness Over Generations",
            xaxis_title="Generation",
            yaxis_title="Fitness",
        )

        return results, fig
    except Exception as e:
        # Handle errors gracefully
        return (
            [html.P(f"Error: {str(e)}")],
            go.Figure(),  # Return an empty figure on error
        )


if __name__ == "__main__":
    """
    Entry point of the application.
    Starts the Dash server and binds it to a port specified in the environment
    variable `PORT` or defaults to port 8050.
    """
    port = int(
        os.environ.get("PORT", 8050)
    )  # Use the PORT environment variable or default to 8050
    app.run_server(host="0.0.0.0", port=port, debug=True)
