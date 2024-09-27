from typing import List, Tuple, Dict
from CakeValuation import CakeValuation

def core(cutterAgent: int, agents: List[CakeValuation], cake: Tuple[int, int]) -> Dict[Tuple[int, int], int]:
    cakeCuts = agents[cutterAgent].divideCakeEqually(len(agents))
    remainingAgents = [agent for i, agent in enumerate(agents) if i != cutterAgent]

    # Add the start and end of the cake to the cuts
    cakeCuts.insert(0, cake[0])
    cakeCuts.insert(len(cakeCuts), cake[1])

    # Create a list of tuples that represent the pieces of cake
    cakePieces = [(cakeCuts[i], cakeCuts[i+1]) for i in range(0, len(cakeCuts) - 1)]
    print(cakePieces)
    allocation = subCore(cakePieces, remainingAgents, [0 for i in range(0, len(remainingAgents))])

    print(allocation)

    for piece in cakePieces:
        if (piece in allocation and allocation[piece] == -1):
            print("Unallocated piece goes to agent ", agents[cutterAgent].getId())
            allocation[piece] = agents[cutterAgent].getId()
    print("Final allocation: ", allocation)

    return allocation

    
def subCore(cakePieces: List[Tuple[int, int]], agents: List[CakeValuation], benchmarks: List[int]) -> Dict[Tuple[int, int], int]:
    print("Enter SubCore")
    agentRankings = [agent.rankPiecesByValue(cakePieces) for agent in agents]
    # Shows what agent owns which piece
    pieceAllocations = {cakePiece: -1 for cakePiece in cakePieces}
    pieceSingleTrim = {cakePiece: cakePiece[0] for cakePiece in cakePieces}
    newBenchmarks = benchmarks.copy()

    for m in range(0, len(agents)):
        # If the agent's highest value piece is unallocated, give it to them
        print(f"New agent {agents[m].getId()} chooses piece {cakePieces.index(agentRankings[m][0]) + 1}")
        if (pieceAllocations[agentRankings[m][0]] == -1):
            pieceAllocations[agentRankings[m][0]] = m
        else:
            # First m agents are contesting for same m-1 pieces, called contested pieces
            # For each agent j, set benchmark[j] to the max of benchmark[j] or value of the uncontested piece with highest value 
            for j in range(0, m+1):
                for piece in agentRankings[j]:
                    if pieceAllocations[piece] == -1:
                        newBenchmarks[j] = max(benchmarks[j], agents[j].evalCakePiece(piece[0], piece[1]))
                        break
            
            # For each piece, store the trims as a list of tuples (agent, trim)
            pieceTrims = {piece: [] for piece in cakePieces}

            # For each agent 0 to m, place a trim on all contested pieces so that contested piece on right has value equal to benchmark[j]
            for j in range(0, m+1):
                for piece in agentRankings[j]:
                    # If the piece is allocated and the agent's value is higher than the benchmark, trim the piece
                    if pieceAllocations[piece] != -1 and agents[j].evalCakePiece(piece[0], piece[1]) > newBenchmarks[j]:
                        trim = agents[j].trimPieceToValue(piece[0], piece[1], newBenchmarks[j])
                        pieceTrims[piece].append((j, trim))
                        print(f"Agent {agents[j].getId()} trims piece {cakePieces.index(piece) + 1} to {trim}")

            agentWithMostTrim = []
            # Let W be list of agents who trimmed most in some piece
            for trims in pieceTrims.values():
                if (len(trims) > 0):
                    maxTrim = max([trim for trim in trims], key=lambda trim: trim[1])
                    if (maxTrim[0] not in agentWithMostTrim):
                        agentWithMostTrim.append(maxTrim[0])
            print("Agents with most trim: ", agentWithMostTrim)

            while (len(agentWithMostTrim) < m):
                # Ignore the previous trims of agents in W, and forget previous allocations
                # Run SubCore on contested pieces with W as target set of agents, and for each contested piece, the part to the left of the right-most trim by an agent not in W is ignored.
                newCakePieces = []
                for piece in cakePieces:
                    if pieceAllocations[piece] != -1:
                        rightMostTrim = piece[0]
                        for trim in pieceTrims[piece]:
                            if trim[0] not in agentWithMostTrim:
                                rightMostTrim = max(rightMostTrim, trim[1])
                        newCakePieces.append((rightMostTrim, piece[1]))

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
                            print(f"Agent {agents[agent].getId()} got piece {cakePieces.index(piece) + 1} from inner subCore")
                            break
                
                # Add an agent whose trim is on an unallocated piece
                newAgentI = -1
                for piece in unallocatedPieces:
                    for trim in pieceTrims[piece]:
                        if (len(trims) > 0):
                            # Get the max trim made by agents not in W
                            trimsByNotWAgents = [trim for trim in trims if trim[0] not in agentWithMostTrim]
                            if (len(trimsByNotWAgents) > 0):
                                maxTrim = max(trimsByNotWAgents, key=lambda trim: trim[1])
                                newAgentI = maxTrim[0]
                                break
                    if (newAgentI != -1):
                        break
                agentWithMostTrim.append(newAgentI)
                if (newAgentI == -1):
                    print("Error: No agent to add to W")
                    return None
                print(f"Agent {agents[newAgentI].getId()} is added to W")
            
            # There can only be 1 agent not in W
            agentNotInW = [i for i in range(0, m+1) if i not in agentWithMostTrim][0]
            newCakePieces = []
            # Get set of contested pieces ignoring the port left of the trim made by agent not in W.
            for piece in cakePieces:
                if pieceAllocations[piece] != -1:
                    rightMostTrim = piece[0]
                    for trim in pieceTrims[piece]:
                        if trim[0] == agentNotInW:
                            rightMostTrim = trim[1]
                            break
                    newCakePieces.append((rightMostTrim, piece[1]))
                    pieceSingleTrim[piece] = rightMostTrim
            
            print("Current cake trims: ", pieceSingleTrim)
            
            # Run SubCore on all agents in W and set of new pieces
            returnedAllocations = subCore(newCakePieces, [agents[i] for i in agentWithMostTrim], [newBenchmarks[i] for i in agentWithMostTrim])
            for (allocatedPiece, agentId) in returnedAllocations.items():
                for piece in cakePieces:
                    # If the piece ends are the same, they are from the same piece
                    if (allocatedPiece[1] == piece[1]):
                        agent = [i for i in range(0, m+1) if agents[i].getId() == agentId][0]
                        pieceAllocations[piece] = agent
                        print(f"Agent {agents[agent].getId()} got piece {cakePieces.index(piece) + 1} from outer subCore")
                        break
            
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
        if (pieceSingleTrim[piece] != piece[0]):
            ignoredPiece = (piece[0], pieceSingleTrim[piece])
            envyFreeAllocation[ignoredPiece] = -1
        newPiece = (pieceSingleTrim[piece], piece[1])
        envyFreeAllocation[newPiece] = agents[agent].getId() if agent != -1 else -1
    
    print(envyFreeAllocation)
    print("Exit SubCore")
    return envyFreeAllocation
            
            
                        
            
        


