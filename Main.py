from CakeValuation import DiscreteCakeValuation
from CakeCutting import core

if __name__ == "__main__":
    # Create 5 agents
    # agents = [
    #     DiscreteCakeValuation([1,1,1,1,1,1,2,2,2,3,3,6,6], 0),
    #     DiscreteCakeValuation([4,4,2,1,1,8,0,0,0,0,0,8,0], 1),
    #     DiscreteCakeValuation([1,1,1,1,1,1,1,1,3,0,0,4,0], 2),
    #     DiscreteCakeValuation([1,1,1,1,2,2,4,2,4,2,4,4,0], 3),
    #     DiscreteCakeValuation([1,1,1,1,1,1,0,0,0,0,0,3,0], 4)
    # ]

    agents = [
        DiscreteCakeValuation([1,1,1,1,1,1,2,2,2,3,3,6,6], 0),
        DiscreteCakeValuation([4,4,2,1,1,8,0,0,0,0,0,8,0], 1),
        DiscreteCakeValuation([1,2,1,1,1,1,2,1,3,0,0,4,0], 2),
        DiscreteCakeValuation([1,1,1,1,2,2,4,2,4,2,4,4,0], 3),
        DiscreteCakeValuation([1,1,1,1,1,1,0,0,0,0,0,3,0], 4)
    ]

    # agents = [
    #     DiscreteCakeValuation([1,1,1,1,1,1,2,2,2,3,3,6,6], 10),
    #     DiscreteCakeValuation([4,4,2,1,1,6,1,1,0,0,0,8,0], 11),
    #     DiscreteCakeValuation([1,1,2,1,0,1,1,1,3,0,0,4,0], 12),
    #     DiscreteCakeValuation([1,1,1,4,2,2,4,2,4,2,4,8,0], 13),
    #     DiscreteCakeValuation([1,1,1,1,5,1,1,0,0,0,3,3,12], 14)
    # ]

    # Define the cake as a tuple representing the start and end points
    # We don't normalize the cake, but all results are identical if normalized
    cake = (0, 13)

    # Call the core function with the first agent as the cutter
    core(0, agents, cake)