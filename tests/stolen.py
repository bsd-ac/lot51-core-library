from event_testing.resolver import RESOLVER_PARTICIPANT
from event_testing.results import TestResult
from event_testing.test_base import BaseTest
from interactions import ParticipantTypeSingle
from objects.components.types import STOLEN_COMPONENT
from sims4.tuning.tunable import (
    AutoFactoryInit,
    HasTunableSingletonFactory,
    Tunable,
    TunableEnumEntry,
)


class ObjectStolenTest(HasTunableSingletonFactory, AutoFactoryInit, BaseTest):
    """Tests if the subject has a stolen component
    """

    FACTORY_TUNABLES = {
        "is_stolen": Tunable(tunable_type=bool, default=True),
        "subject": TunableEnumEntry(
            tunable_type=ParticipantTypeSingle, default=ParticipantTypeSingle.Object,
        ),
    }

    __slots__ = (
        "is_stolen",
        "subject",
    )

    def get_expected_args(self):
        return {"subjects": self.subject, "resolver": RESOLVER_PARTICIPANT}

    def __call__(self, subjects=(), resolver=None, **kwargs):
        subject = next(iter(subjects))

        is_stolen = subject.get_component(STOLEN_COMPONENT) is not None
        if is_stolen == self.is_stolen:
            return TestResult.TRUE

        return TestResult(
            False,
            f"Subject does not match required stolen value: {is_stolen}",
            tooltip=self.tooltip,
        )
