###############################################################################
# Copyright 2019 StarkWare Industries Ltd.                                    #
#                                                                             #
# Licensed under the Apache License, Version 2.0 (the "License").             #
# You may not use this file except in compliance with the License.            #
# You may obtain a copy of the License at                                     #
#                                                                             #
# https://www.starkware.co/open-source-license/                               #
#                                                                             #
# Unless required by applicable law or agreed to in writing,                  #
# software distributed under the License is distributed on an "AS IS" BASIS,  #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.    #
# See the License for the specific language governing permissions             #
# and limitations under the License.                                          #
###############################################################################


from hashlib import sha256
from math import log2, ceil

from field import FieldElement


class MerkleTree(object):
    """
    A simple and naive implementation of an immutable Merkle tree.
    """

    def __init__(self, data):
        assert isinstance(data, list)
        assert len(data) > 0, 'Cannot construct an empty Merkle Tree.'
        num_leaves = 2 ** ceil(log2(len(data)))
        self.data = data + [FieldElement(0)] * (num_leaves - len(data))
        self.height = int(log2(num_leaves))
        self.facts = {}
        self.root = self.build_tree()

    def get_authentication_path(self, leaf_id):
        assert 0 <= leaf_id < len(self.data)
        node_id = leaf_id + len(self.data) #why this? 
        cur = self.root
        decommitment = []
        # In a Merkle Tree, the path from the root to a leaf, corresponds to the the leaf id's
        # binary representation, starting from the second-MSB, where '0' means 'left', and '1' means
        # 'right'.
        # We therefore iterate over the bits of the binary representation - skipping the '0b'
        # prefix, as well as the MSB.
        for bit in bin(node_id)[3:]:
            cur, auth = self.facts[cur]
            if bit == '1':
                auth, cur = cur, auth
            decommitment.append(auth)
        return decommitment

    def build_tree(self):
        return self.recursive_build_tree(1)

    def recursive_build_tree(self, node_id):
        if node_id >= len(self.data):
            # A leaf.
            id_in_data = node_id - len(self.data)
            leaf_data = str(self.data[id_in_data])
            h = sha256(leaf_data.encode()).hexdigest()
            self.facts[h] = leaf_data
            return h
        else:
            # An internal node.
            left = self.recursive_build_tree(node_id * 2)
            right = self.recursive_build_tree(node_id * 2 + 1)
            h = sha256((left + right).encode()).hexdigest()
            self.facts[h] = (left, right)
            return h


def verify_decommitment(leaf_id, leaf_data, decommitment, root):
    leaf_num = 2 ** len(decommitment)
    node_id = leaf_id + leaf_num
    cur = sha256(str(leaf_data).encode()).hexdigest()
    for bit, auth in zip(bin(node_id)[3:][::-1], decommitment[::-1]):
        if bit == '0':
            h = cur + auth
        else:
            h = auth + cur
        cur = sha256(h.encode()).hexdigest()
    return cur == root



"""

MERKLETREE CLASS 

The class MerkleTree is used to create a Merkle tree from a list of data. A Merkle tree is a data structure that is used to verify the authenticity of a piece of data in a larger set of data. The class has several methods:

The init method initializes the Merkle tree by taking a list of data as input. It adds trailing zeroes to the data to make the number of leaves a power of 2. It also sets the height of the tree and initializes an empty dictionary called facts. The method also calls the build_tree method to construct the Merkle tree and sets the root attribute of the class to the root of the constructed tree.

The get_authentication_path method takes a leaf_id as input and returns the authentication path for that leaf. An authentication path is a list of hashes that allows a verifier to check the authenticity of a leaf node.

The build_tree method calls the recursive_build_tree method to construct the Merkle tree

The recursive_build_tree method is a recursive method that is used to construct the Merkle tree. It takes a node_id as input and returns the hash of the node. If the node is a leaf node, it returns the hash of the leaf data, otherwise it computes the hash of the left and right child of the node and returns the concatenation of those hashes.

The verify_decommitment method is a function that takes leaf_id, leaf_data, decommitment and root as input and returns a Boolean indicating whether the decommitment is valid or not. It verifies the authenticity of a piece of data in a larger set of data using the decommitment and the root of the Merkle tree.
"""

"""

WHY ADDING TRAILING ZEROS?

In a Merkle Tree, each leaf node represents a piece of data and each non-leaf node represents the hash of its child nodes. The tree is constructed by recursively calculating the hash of the child nodes and combining them to form the hash of the parent node. To ensure that the tree is a complete binary tree, it is necessary to have the number of leaf nodes to be a power of 2. This is because in a complete binary tree, all levels are fully filled except possibly the last level and all nodes are as far left as possible.

By adding trailing zeroes to the data, it ensures that the number of leaf nodes is a power of 2, so that the tree can be made a complete binary tree. This makes the tree structure simple and efficient for authentication and verification.
"""

"""
WHY DO WE SET THE 'HEIGHT' AND CREATE AN EMPTY DICTIONARY CALLED 'FACTS'?


The height of the tree is set because it is used later in the code to determine the number of elements in the binary representation of the leaf node id, which is used to determine the path of the node in the tree.

The facts dictionary is used to store the parent-child relationship of the nodes in the tree, where the key is the hash of a node and the value is the hash of its children. This is used later in the get_authentication_path method to determine the path of a leaf node in the tree, and in the verify_decommitment function to reconstruct the tree and check the root hash of the tree.

"""

"""
Let's say we have a Merkle tree with the following structure:

        H(H(a) + H(b))
         /          \
    H(a)             H(b)
    /   \           /   \
  a      b       c      d

The root of this Merkle tree is the hash of the concatenation of the hashes of the two children of the root.

Let's say we want to verify if the leaf node with value "c" is in the tree. To do this, we would take the hash of "c" and use it to construct the authentication path by following the tree from the leaf node to the root.

First, we would start at the leaf node "c" and find its parent. The parent is H(b) and it's sibling is H(a). So, we would take the hash of "c" and concatenate it with H(a) to form a new hash H(c+H(a))

We would then move up one level to the root and find the parent node which is H(H(a) + H(b)) and it's sibling is None. So, we would take the hash of H(c+H(a)) and concatenate it with None to form a new hash H(H(c+H(a))

At this point we reach the root of the tree and compare it with the given root of the tree. If they match then we know that the leaf node "c" is in the tree.
"""