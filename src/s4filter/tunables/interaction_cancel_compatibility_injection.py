from interactions.interaction_cancel_compatibility import (
    InteractionCancelCompatibility,
    InteractionCancelReason,
)
from lot51_core.tunables.base_injection import BaseTunableInjection
from lot51_core.utils.injection import inject_dict, merge_affordance_filter
from services import get_instance_manager
from sims4.resources import Types
from sims4.tuning.tunable import TunableEnumEntry, TunableList, TunableReference


class InteractionCancelCompatibilityInjection(BaseTunableInjection):
    """Certain services will clear a Sim's queue/control the pie menu based on the cancel compatibility whitelisting.

    For example, when there is a fire on the lot, the pie menus are limited to putting out the fire, calling the
    fire department, or panicking. Including an affordance with the FIRE cancel reason would allow the interaction to
    display in the pie menu.
    """

    FACTORY_TUNABLES = {
        "reason": TunableEnumEntry(
            InteractionCancelReason, default=InteractionCancelReason.FIRE,
        ),
        "include_affordances": TunableList(
            tunable=TunableReference(
                manager=get_instance_manager(Types.INTERACTION), pack_safe=True,
            ),
        ),
    }

    __slots__ = (
        "include_affordances",
        "reason",
    )

    def inject(self):
        if self.include_affordances is not None:
            filter = (
                InteractionCancelCompatibility.INTERACTION_CANCEL_COMPATIBILITY.get(
                    self.reason, None,
                )
            )
            if filter is not None:
                new_filter = merge_affordance_filter(
                    filter, include_affordances=self.include_affordances,
                )
                inject_dict(
                    InteractionCancelCompatibility,
                    "INTERACTION_CANCEL_COMPATIBILITY",
                    new_items={self.reason: new_filter},
                )
