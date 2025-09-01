from event_testing.results import TestResult
from event_testing.test_base import BaseTest
from interactions import ParticipantTypeSingle
from sims4.tuning.tunable import (
    AutoFactoryInit,
    HasTunableSingletonFactory,
    Tunable,
    TunableEnumEntry,
    TunableList,
)


class ObjectTuningTest(HasTunableSingletonFactory, AutoFactoryInit, BaseTest):
    """Tests if the subject is using any of the provided tuning IDs
    """

    FACTORY_TUNABLES = {
        "subject": TunableEnumEntry(
            tunable_type=ParticipantTypeSingle, default=ParticipantTypeSingle.Object,
        ),
        "invert": Tunable(tunable_type=bool, default=False),
        "tuning_ids": TunableList(
            tunable=Tunable(tunable_type=int, default=0),
        ),
    }

    __slots__ = ("invert", "subject", "tuning_ids")

    def get_expected_args(self):
        return {"subjects": self.subject}

    def __call__(self, subjects=(), **kwargs):
        subject = next(iter(subjects))
        has_tuning_id = subject and subject.guid64 in self.tuning_ids

        if (has_tuning_id and not self.invert) or (not has_tuning_id and self.invert):
            return TestResult.TRUE

        return TestResult(
            False,
            f"Subject does not use any Object Tuning of {self.tuning_ids}, Invert? {self.invert}",
            tooltip=self.tooltip,
        )
