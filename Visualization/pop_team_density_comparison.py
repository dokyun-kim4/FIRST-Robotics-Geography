import pandas as pd


def team_density_helper(year):
    """
    Helper function to gather population and team number data
    for plotting purposes.

    Args:
        year (int): FRC season year to gather data for.

    Returns:
        us_pop_density (dataframe): A dataframe containing various
        US population and FRC team data.

        state_team_count (dataframe): A dataframe containing the number of
        FRC teams per state.


    """
    team_locations = pd.read_csv(f"../FRC{year}.csv")
    state_locations = team_locations[["stateProv"]]
    state_team_count = (
        state_locations["stateProv"]
        .value_counts()
        .rename_axis("Name")
        .reset_index(name="counts")
    )
    state_team_count = state_team_count[state_team_count["Name"] != "Guam"]
    state_team_count = state_team_count[
        state_team_count["Name"] != "Puerto Rico"
    ]
    state_team_count = state_team_count[
        state_team_count["Name"] != "District of Columbia"
    ]

    us_pop_density = pd.read_csv(
        "../Location/PopulationDensity/StatePopulationDensity.csv"
    )
    # add the number of teams per state to the state info dataframe
    us_pop_density["FRC Team Count"] = 0
    us_pop_density.sort_values(by=["Name"], inplace=True)
    us_pop_density = us_pop_density.reset_index(drop=True)
    state_team_count.sort_values(by=["Name"], inplace=True)
    state_team_count = state_team_count.reset_index(drop=True)
    us_pop_density["FRC Team Count"] = state_team_count["counts"]
    us_pop_density.sort_values(by=["Population"], inplace=True, ascending=False)

    us_pop_density["Teams Per 100000 People"] = us_pop_density[
        "FRC Team Count"
    ] / (us_pop_density["Population"] / 100000)

    return us_pop_density, state_team_count


def plot_frc_team_count(year):
    """
    When provided with an input FRC year, will
    generate a graph of FRC teams per state. Additionally, will return a
    dataframe containing number of teams per state.

    Args:
        year (int): FRC year to compare.

    Returns:
        state_team_count plot (Matplotlib plot): A plot of FRC teams per
        state.
        state_team_count (dataframe): A dataframe containing the number of
        FRC teams per state.

    """
    (us_pop_density, state_team_count) = team_density_helper(year)
    state_team_count.sort_values(by=["counts"], inplace=True, ascending=False)
    # Visualze the density of teams per state
    state_team_count.plot(
        x="Name",
        xlabel="State",
        ylabel="Number of Teams",
        kind="bar",
        title="Number of FRC Teams per State",
        figsize=(20, 5),
        legend=False,
    )

    return state_team_count


def plot_density_comparison(year):
    """
    When provided with an input FRC year, will
    generate a graph of FRC teams per 100,000 people
    per state. Additionally, will return a dataframe containing
    state population info with FRC team count and density appended to it.

    Args:
        year (int): FRC year to compare.

    Returns:
        us_pop_density plot (Matplotlib plot): A plot of FRC teams per
        100,000 people per state.
        us_pop_density (dataframe): A dataframe containing various US
        population density information.


    """

    (us_pop_density, state_team_count) = team_density_helper(year)

    us_pop_density.plot(
        x="Name",
        y="Teams Per 100000 People",
        kind="bar",
        figsize=(20, 5),
        title="FRC Teams Per 100000 People",
        xlabel="State",
        ylabel="Number of Teams",
        legend=False,
    )
    return us_pop_density
