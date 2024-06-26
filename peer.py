import random
import uuid
import numpy as np
from block import block
import copy
from peer_utils import *

class peer:
    def __init__(self, id, isPublisher, isLight, isHonest, blockSize = 32, failureModel = "random", failureRate = "30", invalidTxnPresent = False):
        '''if the peer is not publisher, then it doesn't have any use for failureModel, failureRate and invalidTxnPresent'''
        self.id = id
        self.isPublisher = isPublisher
        self.isLight = isLight
        self.isHonest = isHonest
        self.connected_nodes = [] # Adjecent peers of the current peer
        self.block = initiateBlock(isPublisher, blockSize, failureModel, failureRate, invalidTxnPresent)
        self.blockRowsNeeded = [] if isPublisher else random.shuffle(list(range(blockSize)))  # Create shuffled list
        self.blockRowsToPropogate = [] if not isPublisher else random.shuffle(list(range(blockSize)))  # Create shuffled list
        self.blockRowsReceived = []
        self.fraudProofReceived = False
        self.numValidations = 2 if isLight else blockSize
        self.validationQueue = [] # full node request missing chunks only after getting/validating random chunks which are present in their validation queue

