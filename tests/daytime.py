import services
from event_testing.results import TestResult
from event_testing.test_base import BaseTest
from sims4.tuning.tunable import AutoFactoryInit, HasTunableSingletonFactory, Tunable


class DaytimeTest(HasTunableSingletonFactory, AutoFactoryInit, BaseTest):
    FACTORY_TUNABLES = {
        "is_daytime": Tunable(tunable_type=bool, default=True),
    }

    __slots__ = ("is_daytime",)

    def get_expected_args(self):
        return {}

    def __call__(self, **kwargs):
        is_daytime = services.time_service().is_day_time()
        if is_daytime != self.is_daytime:
            return TestResult(
                False,
                f"Daytime test failed, expecting {self.is_daytime} and is {is_daytime}",
            )
        return TestResult.TRUE
