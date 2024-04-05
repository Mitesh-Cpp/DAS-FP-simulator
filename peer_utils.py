from block import block
from peer import peer
import random

def initiateBlock(isPublisher, blockSize, failureModel, failureRate, invalidTxnPresent):
    '''0->missing, 1->present and correct, 2->present but incorrect'''
    if not isPublisher:
        return block(blockSize)  # Return a block with all zeros
    else:
        if failureModel == "random":
            total_elements = blockSize * blockSize
            num_failures = total_elements * float(failureRate) / 100  # Calculate number of failures
            indices = list(range(total_elements))  # Get all indices
            random.shuffle(indices)  # Shuffle indices for random selection

            # Set failures and successes based on shuffled indices
            new_block = block(blockSize)
            for i in range(total_elements):
                print(indices[i])
                if i < num_failures:
                    new_block.data[indices[i]] = 0
                else:
                    new_block.data[indices[i]] = 1
            if invalidTxnPresent:
                new_block[random.randrange(0, blockSize * blockSize)] = 2
            return new_block
        else:
            raise ValueError("Unsupported failure model: {}".format(failureModel))
        