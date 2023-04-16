Interaction.py - Proof of Interaction

This Python module contains the Interaction class, which is the core component of the Proof of Interaction (PoI) system. It represents an interaction between nodes in the PoI network and provides functionality to create, sign, and verify interactions.

**Features**


**Interaction Creation**


The Interaction class allows you to create a new interaction with a timestamp, data, and a public key of the sender node.

**Interaction Signing**


Signing an interaction is performed using the private key of the sender node. This ensures that only the node that created the interaction can sign it. The signed interaction is then added to the network, and other nodes can verify its authenticity.

**Interaction Verification**

The Interaction class also provides the ability to verify an interaction's signature. This feature allows other nodes in the network to confirm that the interaction was created by the node that claims to have created it, ensuring the integrity of the PoI system.

**Limitations:**

This current version of the Interaction.py module focuses solely on creating, signing, and verifying interactions. It does not include features such as:

- Interaction management and storage (e.g., handling and storing multiple interactions in a data structure like a blockchain)
- Networking and communication between nodes (sending/receiving interactions and propagating them throughout the network)
- Reputation or consensus mechanism (determining node reputations, selecting valid interactions, or establishing rules for participation in the PoI system)
- Token or reward distribution (calculating and distributing rewards for participating in the PoI system)
- These additional features would be required to build a complete PoI system, and should be implemented in separate classes or modules to keep the system modular and maintainable.

**Usage**


To use the Interaction.py module in your project, make sure to install the required dependency:


`pip install pycryptodome`


After installing pycryptodome, you can import the Interaction class in your code and use its methods to create, sign, and verify interactions as shown in the provided examples.
