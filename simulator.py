import argparse
import random
import csv
import heapq
from peer import peer
from block import block
import uuid
from connect_graph import connect_graph
import copy

'''assuming one chunk is of 1Kb including proofs and all'''

bwupfull = 50000 # 50 Mbps
bwdownfull = 200000 # 200 Mbps
bwuplight = 10000 # 10 Mbps
bwdownlight = 10000 # 10 Mbps
blockSize = 32


def generatePeerSet(totalPeers, lightPercent, HonestPercent):
    peersSet = [i for i in range(0, totalPeers)]
    lightPercentSet = random.sample(peersSet, int(lightPercent * totalPeers / 100))
    honestPercentSet = random.sample(peersSet, int(HonestPercent * totalPeers / 100))
    return peersSet, lightPercentSet, honestPercentSet

def main():
    parser = argparse.ArgumentParser(description='DAS-FP-Simulator')
    parser.add_argument('--totalPeers', type=int, default=100, help='Total number of peers')
    parser.add_argument('--lightPercent', type=float, default=70.0, help='lightPercent (Light Client %)')
    parser.add_argument('--HonestPercent', type=float, default=80.0, help='HonestPercent (Honest Nodes %)') 
    
    args = parser.parse_args()
    peersSet, lightPercentSet, honestPercentSet = generatePeerSet(args.totalPeers, args.lightPercent, args.HonestPercent)

    # print("Light Percent Set")
    # print(lightPercentSet)
    # print("Honest Percent Set")
    # print(honestPercentSet)

    allPeers = [] 
    lightAndHonest = []

    for peerId in peersSet:
        '''PeerId 0 would be block publisher'''
        isLight = peerId in lightPercentSet # interpret 0 as slow and 1 as fast
        isHonest = peerId in honestPercentSet  # interpret 0 as low and 1 as high
        if isLight and isHonest:
            lightAndHonest.append(peerId)
        allPeers.append(peer(peerId, (peerId == 0), isLight, isHonest, blockSize))
        print("This is peer: ", peerId, "'s block")
        allPeers[-1].block.print()
    connect_graph(allPeers)

    # for peerId in peersSet:
    #     for nbr in allPeers[peerId].connected_nodes:
    #         if not allPeers[nbr].isLight and allPeers[nbr].isHonest:
    #             print(peerId, " connected to ", nbr)
    #             break

    time_step = 0
    targetLightClient = random.choice(lightAndHonest)
    globalRowsUnavailable = []
    globalRowsUnavailable.append(set([i for i in range(blockSize)]))
    # invalid block chunk will be always counted as unavailable
    while not globalRowsUnavailable[-1] == [] or not allPeers[targetLightClient].fraudProofReceived:
        if len(globalRowsUnavailable) >= 7 and globalRowsUnavailable[-7] == globalRowsUnavailable[-1]:
            print("Unable to reconstruct the block, not available in the network..!! Exiting..!!")
            break
        for peerId in peersSet:
            # full nodes will ask for all the rows and honest full nodes will propogate them as well in the network
            processQueues(peerId, allPeers, globalRowsUnavailable)
        time_step += 1

    if globalRowsUnavailable[-1] == []:
        print("Block valid and available in ", time_step, " steps.")
    if allPeers[targetLightClient].fraudProofReceived:
        print("Light client (idx = ", targetLightClient, ") received fraud proof after ", time_step, " time steps.")


if __name__ == "__main__":
    main()