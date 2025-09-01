from event_testing.results import TestResult
from event_testing.test_base import BaseTest
from lot51_core import logger
from services import get_instance_manager
from sims4.resources import Types
from sims4.tuning.tunable import (
    AutoFactoryInit,
    HasTunableSingletonFactory,
    TunableReference,
)


class ValidPickerChoiceTest(HasTunableSingletonFactory, AutoFactoryInit, BaseTest):
    FACTORY_TUNABLES = {
        "affordance": TunableReference(manager=get_instance_manager(Types.INTERACTION)),
    }

    __slots__ = ("affordance",)

    def get_expected_args(self):
        return {}

    def __call__(self, **kwargs):
        if self.affordance is None or not hasattr(self.affordance, "has_valid_choice"):
            return TestResult(
                False, f"Invalid picker interaction: {self.affordance}",
            )

        if not self.affordance.has_valid_choice():
            return TestResult(
                False,
                f"Picker interaction does not have any valid choices: {self.affordance}",
                tooltip=self.tooltip,
            )

        logger.debug(f"Affordance has valid picker choices {self.affordance}")

        return TestResult.TRUE


class ValidPurchasePickerChoiceTest(
    HasTunableSingletonFactory, AutoFactoryInit, BaseTest,
):
    FACTORY_TUNABLES = {
        "snippet": TunableReference(manager=get_instance_manager(Types.SNIPPET)),
    }

    __slots__ = ("snippet",)

    def get_expected_args(self):
        return {}

    def __call__(self, **kwargs):
        if self.snippet is None or not hasattr(self.snippet, "has_valid_choice"):
            return TestResult(False, f"Invalid picker snippet: {self.snippet}")

        if not self.snippet.has_valid_choice():
            return TestResult(
                False,
                f"Picker does not have any valid choices: {self.snippet}",
                tooltip=self.tooltip,
            )

        logger.debug(f"Snippet has valid picker choices {self.snippet}")

        return TestResult.TRUE
