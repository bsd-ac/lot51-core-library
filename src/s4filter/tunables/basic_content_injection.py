from interactions.base.basic import FlexibleLengthContent
from interactions.utils.statistic_element import (
    PeriodicStatisticChangeElement,
    TunableExitConditionSnippet,
)
from lot51_core import logger
from lot51_core.utils.collections import AttributeDict
from lot51_core.utils.injection import merge_dict, merge_list
from lot51_core.utils.tunables import (
    clone_factory_with_overrides,
    clone_factory_wrapper_with_overrides,
)
from sims4.tuning.tunable import (
    AutoFactoryInit,
    HasTunableSingletonFactory,
    OptionalTunable,
    Tunable,
    TunableList,
)


class TunableBasicContentInjection(HasTunableSingletonFactory, AutoFactoryInit):
    FACTORY_TUNABLES = {
        "conditional_actions": TunableList(
            description="Only used for interactions with a flexible_length basic_content.",
            tunable=TunableExitConditionSnippet(pack_safe=True),
        ),
        "periodic_stat_change": OptionalTunable(
            description="Only used for interactions with a flexible_length basic_content.",
            tunable=PeriodicStatisticChangeElement.TunableFactory(
                locked_args={"show_while_routing": False},
            ),
        ),
        "start_autonomous_inertial_override": OptionalTunable(
            description="Only used for interactions with a flexible_length basic_content.",
            tunable=Tunable(tunable_type=bool, default=True),
        ),
        "start_user_directed_inertial_override": OptionalTunable(
            description="Only used for interactions with a flexible_length basic_content.",
            tunable=Tunable(tunable_type=bool, default=True),
        ),
    }

    __slots__ = (
        "conditional_actions",
        "periodic_stat_change",
        "start_autonomous_inertial_override",
        "start_user_directed_inertial_override",
    )

    def inject_to_affordance(self, affordance):
        overrides = AttributeDict()

        # Periodic Stat Change
        if self.periodic_stat_change is not None:
            if isinstance(affordance.basic_content, FlexibleLengthContent):
                periodic_stat_change = affordance.basic_content.periodic_stat_change
                if periodic_stat_change is not None:
                    overrides.periodic_stat_change = (
                        clone_factory_wrapper_with_overrides(
                            periodic_stat_change,
                            operation_actions=merge_dict(
                                periodic_stat_change.operation_actions,
                                actions=merge_list(
                                    periodic_stat_change.operation_actions.actions,
                                    self.periodic_stat_change.operation_actions.actions,
                                ),
                            ),
                            operations=merge_list(
                                periodic_stat_change.operations,
                                self.periodic_stat_change.operations,
                            ),
                        )
                    )
                else:
                    logger.warn(
                        f"Cannot inject periodic_stat_change to {affordance}. This affordance does not have existing periodic_stat_change content.",
                    )
            else:
                logger.warn(
                    f"Cannot inject periodic_stat_change to {affordance}. This affordance does not use flexible_content basic_content.",
                )

        # Conditional Actions
        if len(self.conditional_actions):
            if isinstance(affordance.basic_content, FlexibleLengthContent):
                overrides.conditional_actions = merge_list(
                    affordance.basic_content.conditional_actions,
                    self.conditional_actions,
                )
            else:
                logger.warn(
                    f"Cannot inject conditional_actions to {affordance}. This affordance does not use flexible_content basic_content.",
                )

        if self.start_autonomous_inertial_override is not None:
            if isinstance(affordance.basic_content, FlexibleLengthContent):
                overrides.start_autonomous_inertial = (
                    self.start_autonomous_inertial_override
                )
            else:
                logger.warn(
                    f"Cannot inject start_autonomous_inertial to {affordance}. This affordance does not use flexible_content basic_content.",
                )

        if self.start_user_directed_inertial_override is not None:
            if isinstance(affordance.basic_content, FlexibleLengthContent):
                overrides.start_user_directed_inertial = (
                    self.start_user_directed_inertial_override
                )
            else:
                logger.warn(
                    f"Cannot inject start_user_directed_inertial to {affordance}. This affordance does not use flexible_content basic_content.",
                )

        # Apply overrides
        if len(overrides):
            affordance.basic_content = clone_factory_with_overrides(
                affordance.basic_content, **overrides,
            )
