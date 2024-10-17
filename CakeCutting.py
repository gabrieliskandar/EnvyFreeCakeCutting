from typing import List, Tuple, Dict
from CakeValuation import CakeValuation, compareImaginaryValues

def core(cutterAgent: int, agents: List[CakeValuation], cake: Tuple[int, int]) -> Dict[Tuple[int, int, Tuple[int]], int]:
    # Set the imaginary values for each agent, note that I'm using significantly less values due to memory constraints
    imaginaryValueSize = pow(len(agents), 3) #pow(len(agents), 3) * pow(pow(len(agents), 2), len(agents))
    offset = 0
    for agent in agents:
        agent.setImaginaryValues([i + offset for i in range(imaginaryValueSize, 0, -1)])
        offset += imaginaryValueSize

    cakeCuts = agents[cutterAgent].divideCakeEqually(len(agents))
    remainingAgents = [agent for i, agent in enumerate(agents) if i != cutterAgent]

    # Add the start and end of the cake to the cuts
    cakeCuts.insert(0, cake[0])
    cakeCuts.insert(len(cakeCuts), cake[1])

    # Create a list of tuples that represent the pieces of cake
    cakePieces = [(cakeCuts[i], cakeCuts[i+1], tuple([agent.getNextImaginaryValue() for agent in agents])) for i in range(0, len(cakeCuts) - 1)]
    print(cakePieces)

    allocation = subCore(cakePieces, remainingAgents, [(0,()) for i in range(0, len(remainingAgents))])

    print(allocation)

    for piece in cakePieces:
        if (piece in allocation and allocation[piece] == -1):
            print("Unallocated piece goes to agent ", agents[cutterAgent].getId())
            allocation[piece] = agents[cutterAgent].getId()
    print("Final allocation: ", allocation)

    return allocation

    
def subCore(cakePieces: List[Tuple[int, int, Tuple[int]]], agents: List[CakeValuation], benchmarks: List[Tuple[int,Tuple[int]]]) -> Dict[Tuple[int, int, Tuple[int]], int]:
    print(f"Enter SubCore with cake pieces: {cakePieces}, agents: {[agent.getId() for agent in agents]}, benchmarks: {benchmarks}")
    agentRankings = [agent.rankPiecesByValue(cakePieces) for agent in agents]
    # Shows what agent owns which piece
    pieceAllocations = {cakePiece: -1 for cakePiece in cakePieces}
    pieceSingleTrim = {cakePiece: (cakePiece[0], cakePiece[2]) for cakePiece in cakePieces}
    newBenchmarks = benchmarks.copy()

    for m in range(0, len(agents)):
        # If the agent's highest value piece is unallocated, give it to them
        print(f"New agent {agents[m].getId()} chooses piece {cakePieces.index(agentRankings[m][0]) + 1}")
        if (pieceAllocations[agentRankings[m][0]] == -1):
            pieceAllocations[agentRankings[m][0]] = m
        else:
            # First m agents are contesting for same m-1 pieces, called contested pieces
            # For each agent j, set newBenchmarks[j] to the max of benchmark[j] or value of the uncontested piece with highest value 
            for j in range(0, m+1):
                for piece in agentRankings[j]:
                    if pieceAllocations[piece] == -1:
                        if agents[j].evalCakePiece(piece[0], piece[1]) > benchmarks[j][0]:
                            newBenchmarks[j] = (agents[j].evalCakePiece(piece[0], piece[1]), piece[2])
                        break
            
            # For each piece, store the trims as a list of tuples (agent, trim, (imaginary values))
            pieceTrims = {piece: [] for piece in cakePieces}

            # For each agent 0 to m, place a trim on all contested pieces so that contested piece on right has value equal to benchmark[j]
            for j in range(0, m+1):
                for piece in agentRankings[j]:
                    # If the piece is allocated and the agent's value is higher than the benchmark, trim the piece
                    if pieceAllocations[piece] != -1 and agents[j].evalCakePiece(piece[0], piece[1]) > newBenchmarks[j][0]:
                        trim = agents[j].trimPieceToValue(piece[0], piece[1], newBenchmarks[j][0])
                        imaginaryValues = newBenchmarks[j][1] + (agents[j].getNextImaginaryValue(), )
                        pieceTrims[piece].append((j, trim, imaginaryValues))
                        print(f"Agent {agents[j].getId()} trims piece {cakePieces.index(piece) + 1} to {trim} with imaginary values {imaginaryValues}")

            agentWithMostTrim = []
            # Let W be list of agents who trimmed most in some piece
            for (piece, trims) in pieceTrims.items():
                if (len(trims) > 0):
                    # Find the max trim made by an agent
                    maxTrim = trims[0]
                    for trim in trims:
                        if (trim[1] > maxTrim[1]):
                            maxTrim = trim
                        elif (trim[1] == maxTrim[1] and trim[0] != maxTrim[0]):
                            print("Tie between ", agents[maxTrim[0]].getId(), " and ", agents[trim[0]].getId())
                            # If the current max has a smaller imaginary value (aka a bigger imaginary piece), then the competing agent cut smaller
                            if (compareImaginaryValues(maxTrim[2], trim[2])):
                                maxTrim = trim

                    if (maxTrim[0] not in agentWithMostTrim):
                        agentWithMostTrim.append(maxTrim[0])
            print("Agents with most trim: ", [agents[agent].getId() for agent in agentWithMostTrim])

            while (len(agentWithMostTrim) < m):
                # Ignore the previous trims of agents in W, and forget previous allocations
                # Run SubCore on contested pieces with W as target set of agents, and for each contested piece, the part to the left of the right-most trim by an agent not in W is ignored.
                newCakePieces = []
                for piece in cakePieces:
                    if pieceAllocations[piece] != -1:
                        # Current most right is the left end of the piece
                        maxTrim = (-1, piece[0], piece[2])
                        for trim in pieceTrims[piece]:
                            if trim[0] not in agentWithMostTrim:
                                if (trim[1] > maxTrim[1] or (trim[1] == maxTrim[1] and maxTrim[0] == -1)):
                                    maxTrim = trim
                                elif (trim[1] == maxTrim[1]):
                                    # Handle tie with imaginary values
                                    print("Tie between ", agents[maxTrim[0]].getId(), " and ", agents[trim[0]].getId())

                                    # If the current max has a smaller imaginary value (aka a bigger imaginary piece), then the competing agent cut smaller
                                    if (compareImaginaryValues(maxTrim[2], trim[2])):
                                        maxTrim = trim

                        newCakePieces.append((maxTrim[1], piece[1], maxTrim[2]))

                returnedAllocations = subCore(newCakePieces, [agents[i] for i in agentWithMostTrim], [newBenchmarks[i] for i in agentWithMostTrim])
                unallocatedPieces = []
                for (allocatedPiece, agentId) in returnedAllocations.items():
                    for piece in cakePieces:
                        # If the piece ends are the same, they are from the same piece
                        if (allocatedPiece[1] == piece[1]):
                            if (agentId == -1):
                                unallocatedPieces.append(piece)
                                pieceAllocations[piece] = -1
                                break
                            agent = [i for i in range(0, m+1) if agents[i].getId() == agentId][0]
                            pieceAllocations[piece] = agent
                            newBenchmarks[agent] = (agents[agent].evalCakePiece(allocatedPiece[0], allocatedPiece[1]), allocatedPiece[2])
                            print(f"Agent {agents[agent].getId()} got piece {cakePieces.index(piece) + 1} from inner subCore")
                            break
                
                # Add an agent whose trim is on an unallocated piece
                newAgentI = -1
                for piece in unallocatedPieces:
                    # Get the max trim made by agents not in W
                    trimsByNotWAgents = [trim for trim in pieceTrims[piece] if trim[0] not in agentWithMostTrim]
                    if (len(trimsByNotWAgents) > 0):
                        maxTrim = trimsByNotWAgents[0]
                        for trim in trimsByNotWAgents:
                            if trim[1] > maxTrim[1]:
                                maxTrim = trim
                            elif trim[1] == maxTrim[1] and trim[0] != maxTrim[0]:
                                # Handle tie with imaginary values
                                print("Tie between ", agents[maxTrim[0]].getId(), " and ", agents[trim[0]].getId())

                                # If the current max has a smaller imaginary value (aka a bigger imaginary piece), then the competing agent cut smaller
                                if (compareImaginaryValues(maxTrim[2], trim[2])):
                                    maxTrim = trim

                        newAgentI = maxTrim[0]
                        pieceAllocations[piece] = newAgentI
                        newBenchmarks[newAgentI] = (agents[newAgentI].evalCakePiece(maxTrim[1], piece[1]), maxTrim[2])
                        break
                agentWithMostTrim.append(newAgentI)
                if (newAgentI == -1):
                    print("Error: No agent to add to W")
                    return None
                print(f"Agent {agents[newAgentI].getId()} is added to W")

            # There can only be 1 agent not in W
            agentNotInW = [i for i in range(0, m+1) if i not in agentWithMostTrim][0]
            newCakePieces = []
            # Get set of contested pieces ignoring the part left of the trim made by agent not in W.
            for piece in cakePieces:
                if pieceAllocations[piece] != -1:
                    rightMostTrim = (-1, piece[0], piece[2])
                    for trim in pieceTrims[piece]:
                        if trim[0] == agentNotInW:
                            rightMostTrim = trim
                            break
                    newCakePieces.append((rightMostTrim[1], piece[1], rightMostTrim[2]))
            
            # Run SubCore on all agents in W and set of new pieces
            returnedAllocations = subCore(newCakePieces, [agents[i] for i in agentWithMostTrim], [newBenchmarks[i] for i in agentWithMostTrim])
            for (allocatedPiece, agentId) in returnedAllocations.items():
                for piece in cakePieces:
                    # If the piece ends are the same, they are from the same piece
                    if (allocatedPiece[1] == piece[1]):
                        agent = [i for i in range(0, m+1) if agents[i].getId() == agentId][0]
                        pieceAllocations[piece] = agent
                        pieceSingleTrim[piece] = (allocatedPiece[0], allocatedPiece[2])
                        print(f"Agent {agents[agent].getId()} got piece {cakePieces.index(piece) + 1} from outer subCore")
                        break
            
            print("Current cake trims: ", pieceSingleTrim)

            # Remaining agent gets their most preferred uncontested piece
            for piece in agentRankings[agentNotInW]:
                if pieceAllocations[piece] == -1:
                    pieceAllocations[piece] = agentNotInW
                    print(f"Agent {agents[agentNotInW].getId()} chooses piece {cakePieces.index(piece) + 1}")
                    break
        print("Current piece allocations: ", pieceAllocations)
    
    # Construct the partial envy-free allocation. If a piece is trimmed, the left trimmed part belongs to no agent.
    envyFreeAllocation = {}
    for (piece, agent) in pieceAllocations.items():
        if (pieceSingleTrim[piece][0] != piece[0]):
            ignoredPiece = (piece[0], pieceSingleTrim[piece][0], piece[2])
            envyFreeAllocation[ignoredPiece] = -1
            newPiece = (pieceSingleTrim[piece][0], piece[1], pieceSingleTrim[piece][1])
        else:
            newPiece = piece
        envyFreeAllocation[newPiece] = agents[agent].getId() if agent != -1 else -1
    
    print("Envy-free allocation", envyFreeAllocation)
    print("Exit SubCore")
    return envyFreeAllocation
            

        


