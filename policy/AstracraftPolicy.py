from tf_agents.policies import py_policy
from tf_agents.policies import tf_policy
from tf_agents.policies import tf_py_policy

class AstracraftPolicy(py_policy.PyPolicy):
    def __init__(self):
        """Implementation of our game's Py Policy"""