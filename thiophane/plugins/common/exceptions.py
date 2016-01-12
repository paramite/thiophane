
""" Common exceptions for thiophane plugins """

class PluginError(Exception):
    """Base plugin exception"""


class PluginShellRuntimeError(Exception):
    """Signals error state raised during plugin runtime in shell execution."""
    def __init__(self, msg, cmd=None, rc=None, stdout=None, stderr=None):
        self.cmd = cmd
        self.rc = rc
        self.stdout = stdout
        self.stderr = stderr
