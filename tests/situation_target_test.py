import services
import tag
from event_testing.results import TestResult
from event_testing.test_base import BaseTest
from interactions import ParticipantTypeSingle
from lot51_core import logger
from sims.sim_info import SimInfo
from sims4.tuning.tunable import (
    AutoFactoryInit,
    HasTunableSingletonFactory,
    TunableEnumEntry,
    TunableEnumSet,
)


class SituationTargetObjectTest(HasTunableSingletonFactory, AutoFactoryInit, BaseTest):
    FACTORY_TUNABLES = {
        "subject": TunableEnumEntry(
            tunable_type=ParticipantTypeSingle, default=ParticipantTypeSingle.Actor,
        ),
        "target": TunableEnumEntry(
            tunable_type=ParticipantTypeSingle, default=ParticipantTypeSingle.Object,
        ),
        "situation_tags": TunableEnumSet(
            enum_type=tag.Tag,
            enum_default=tag.Tag.INVALID,
            invalid_enums=(tag.Tag.INVALID,),
        ),
    }

    __slots__ = (
        "situation_tags",
        "subject",
        "target",
    )

    def get_expected_args(self):
        return {"subjects": self.subject, "targets": self.target}

    def __call__(self, subjects=(), targets=(), **kwargs):
        subject = next(iter(subjects))
        target = next(iter(targets))

        if subject and isinstance(subject, SimInfo):
            subject = subject.get_sim_instance()

        if target and isinstance(target, SimInfo):
            target = target.get_sim_instance()

        if target.is_part:
            target = target.part_owner

        for situation in services.get_zone_situation_manager().get_situations_sim_is_in(
            subject,
        ):
            if self.situation_tags & situation.tags:
                if hasattr(situation, "get_target_object"):
                    situation_target = situation.get_target_object()
                    if situation_target and situation_target == target:
                        logger.debug(
                            f"SITUATION TARGET TEST PASSED. {subject}: {target} == {situation_target}",
                        )
                        return TestResult.TRUE
                    logger.debug(
                        f"SITUATION TARGET TEST FAILED. DOES NOT MATCH TARGET. {subject}: {target} != {situation_target}",
                    )
                    return TestResult(
                        False,
                        "Object does not match situation target object",
                        tooltip=self.tooltip,
                    )
        logger.debug(
            f"SITUATION TARGET TEST FAILED. SIM NOT IN SITUATION WITH TAGS. {subject} {self.situation_tags}",
        )
        return TestResult(
            False,
            f"Sim is not in expected situation with tags: {self.situation_tags}",
            tooltip=self.tooltip,
        )
