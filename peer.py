import random
import uuid
import numpy as np
from block import block
import copy

class peer:
    def __init__(self, id, isPublisher, isLight, isHonest, blockSize = 64, failureModel = "random", failureRate = "30", invalidTxnPresent = False):
        '''if the peer is not publisher, then it doesn't have any use for failureModel, failureRate and invalidTxnPresent'''
        self.id = id
        self.isPublisher = isPublisher
        self.isLight = isLight
        self.isHonest = isHonest
        self.connected_nodes = [] # Adjecent peers of the current peer
        self.block = initiate_block(isPublisher, failureModel, failureRate, invalidTxnPresent)
        self.blockChunksNeeded = [] if isPublisher else randomShuffle([for i in range(blockSize*blockSize)])
        self.blockChunksToSend = [] if not isPublisher else randomShuffle([for i in range(blockSize*blockSize)])
