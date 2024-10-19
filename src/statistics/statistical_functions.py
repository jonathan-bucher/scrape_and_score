import numpy as np
import pandas as pd

def condition_indices(df, event: tuple) -> set:
    """
    Returns the indices where an event occurs as a set

    Args:
        df (pd.DataFrame): the dataframe containing the data.
        event (tuple): A three tuple where:
            - The first element is the column name(str).
            - the second element is the operator (e.g., 'geq', 'eq', 'leq', etc.).
            - the third element is the value for the condition
            only takes one event

    Returns:
        set: The set of indices where the event occured
    """

    if df[event[0]].isnull().any():
        raise ValueError(f"Null values detected in the column {event[0]}")

    if event[1] == 'geq':
        condition_occurs = df.index[df[event[0]] >= event[2]]
    elif event[1] == 'g':
        condition_occurs = df.index[df[event[0]] > event[2]]
    elif event[1] == 'eq':
        condition_occurs = df.index[df[event[0]] == event[2]]
    elif event[1] == 'l':
        condition_occurs = df.index[df[event[0]] < event[2]]
    elif event[1] == 'leq':
        condition_occurs = df.index[df[event[0]] <= event[2]]
    elif event[1] == 'in_range':
        condition_occurs = df.index[
            (df[event[0]] >= event[2][0]) & (df[event[0]] <= event[2][1])
            ]
    else:
        raise ValueError("Invalid operator. Use one of: 'geq', 'g', 'eq', 'l', 'leq', 'in_range'.")
    
    return set(condition_occurs)


def probability(df, event: tuple, null = False) -> float:
    """
    Calculate the probability of an event occuring

    Args:
        df (pd.DataFrame): the dataframe containing the data.
        event (tuple): A three tuple where:
            - The first element is the column name(str).
            - the second element is the operator (e.g., 'geq', 'eq', 'leq', etc.).
            - the third element is the value for the condition
            only takes one event

    Returns:
        float: The probability
    """

    if null != False:
        df = df.dropna()

    total_count = len(df[event[0]])     # changed this from .count()
    event_count = len(condition_indices(df, event))
    return event_count / total_count


def joint_probability(df, events: list[tuple]) -> float:
    """
    Calculate the probability of two events happening together

    Args:
        df (pd.DataFrame): the dataframe containing the data.
        events (list[tuple]): A list of three tuples where:
            - The first element is the column name(str).
            - the second element is the operator (e.g., 'geq', 'eq', 'leq', etc.).
            - the third element is the value for the condition
            takes only two events

    Returns:
        float: The joint probability
    """

    # Get the total number of rows
    total_count = len(df)
    
    # Find the indices where both conditions hold
    condition_1_indices = condition_indices(df, events[0])
    condition_2_indices = condition_indices(df, events[1])
    
    # Find the intersection of both conditions
    joint_indices = condition_1_indices & condition_2_indices
    
    # Calculate joint probability
    joint_prob = len(joint_indices) / total_count if total_count > 0 else 0
    
    return joint_prob

    
def conditional_probability(df, conditions: list[tuple], null = False) -> float:
    """
    Calculates the probability of an event occurring given that conditions have been met.
    
    Args:
        df (pd.DataFrame): The dataframe containing the data.
        conditions (list[tuple]): A list of three-tuples where:
            - The first element is the column name (str).
            - The second element is the operator (e.g., 'geq', 'eq', 'leq', etc.).
            - The third element is the value for the condition.
            The event is the first tuple, and the conditions are the subsequent tuples.
            
    Returns:
        float: The conditional probability.
    """

    if null != False:
        df = df.dropna()

    # put in an option to print the number of rows that met the condition
    
    # Step 1: Get the indices where the event occurs (first condition in the list)
    event_indices = condition_indices(df, conditions[0])

    # Step 2: Create a set for condition indices based on the first condition after the event
    condition_indices_set = condition_indices(df, conditions[1])

    # Step 3: Check for additional conditions and find intersection of indices
    for i in range(2, len(conditions)):
        condition_indices_set &= condition_indices(df, conditions[i])

    # Step 4: Calculate the number of rows where the condition occurs (event space)
    event_space_size = len(condition_indices_set)

    # Step 5: Find the rows where both the event and conditions occur
    joint_indices = condition_indices_set & event_indices

    # Step 6: Calculate the conditional probability
    conditional_prob = len(joint_indices) / event_space_size if event_space_size > 0 else 0

    return conditional_prob


def bayes(df, conditions: list[tuple]) -> float:
    """
    Calculate the reverse conditional probability

    Args:
        df (pd.DataFrame): the dataframe containing the data.
        events (list[tuple]): A list of two three-tuples where:
            - The first element is the column name(str).
            - the second element is the operator (e.g., 'geq', 'eq', 'leq', etc.).
            - the third element is the value for the condition
            The first tuple is the event, the second tuple is the condition         

    Returns:
        float: The conditional probability
    """
    numerator = conditional_probability(df, list(reversed(conditions))) * (probability(df, conditions[0]))
    # denominator is the overall chance of rain
    denominator = probability(df, conditions[1])

    return (numerator / denominator)