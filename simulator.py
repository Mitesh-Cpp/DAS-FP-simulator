import argparse
import random
import csv
import heapq
from peer import peer
from block import block
import uuid
from connect_graph import connect_graph
import copy

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

    for peerId in peersSet:
        '''PeerId 0 would be block publisher'''
        isLight = peerId in lightPercentSet # interpret 0 as slow and 1 as fast
        isHonest = peerId in honestPercentSet  # interpret 0 as low and 1 as high
        allPeers.append(peer(peerId, (peerId == 0), isLight, isHonest))

    connect_graph(allPeers)

    # for peerId in peersSet:
    #     for nbr in allPeers[peerId].connected_nodes:
    #         if not allPeers[nbr].isLight and allPeers[nbr].isHonest:
    #             print(peerId, " connected to ", nbr)
    #             break

if __name__ == "__main__":
    main()