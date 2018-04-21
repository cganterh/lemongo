"""Provide a general lemongo TestCase."""


from unittest import TestCase

from lemongo import _reset_module_state


class LeMongoTestCase(TestCase):
    """Generic lemongo test case.

    This class has a custom tearDown method that ensures the lemongo
    module is cleaned after each execution. This is necessary mainly
    because ``lemongo.get_client()`` has side effects over the module.
    """

    def tearDown(self):
        """Call ``lemongo._reset_module_state()``."""
        _reset_module_state()
