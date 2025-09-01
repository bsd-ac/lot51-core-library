import services
from caches import cached_test
from event_testing.results import TestResult
from event_testing.test_base import BaseTest
from sims4.resources import Types, get_resource_key
from sims4.tuning.tunable import (
    AutoFactoryInit,
    HasTunableSingletonFactory,
    Tunable,
    TunableEnumEntry,
    TunableVariant,
)


class GetDefinitionResource(HasTunableSingletonFactory, AutoFactoryInit):
    FACTORY_TUNABLES = {
        "definition_id": Tunable(tunable_type=int, default=0),
    }

    __slots__ = ("definition_id",)

    def __repr__(self):
        return f"<DefinitionResource> id: {self.definition_id}"

    def get_resource(self):
        manager = services.definition_manager()
        if manager is not None:
            return manager.get(self.definition_id)


class GetTuningResource(HasTunableSingletonFactory, AutoFactoryInit):
    FACTORY_TUNABLES = {
        "instance_type": TunableEnumEntry(tunable_type=Types, default=Types.TUNING),
        "instance_id": Tunable(tunable_type=int, default=0),
    }

    __slots__ = (
        "instance_id",
        "instance_type",
    )

    def __repr__(self):
        return f"<TuningResource> type: {self.instance_type} id: {self.instance_id}"

    def get_resource(self):
        manager = services.get_instance_manager(self.instance_type)
        if manager is not None:
            return manager.types.get(
                get_resource_key(self.instance_id, self.instance_type),
            )


class ResourceExistenceTest(HasTunableSingletonFactory, AutoFactoryInit, BaseTest):
    """Check if a tuning type or object definition is available,
    useful to check for the existence of other custom content
    """

    FACTORY_TUNABLES = {
        "resource_type": TunableVariant(
            tuning=GetTuningResource.TunableFactory(),
            definition=GetDefinitionResource.TunableFactory(),
        ),
    }

    __slots__ = ("resource_type",)

    def get_expected_args(self):
        return {}

    @cached_test
    def __call__(self, **kwargs):
        if self.resource_type is not None:
            if self.resource_type.get_resource() is not None:
                return TestResult.TRUE
        return TestResult(
            False,
            f"Could not find resource: {self.resource_type}",
            tooltip=self.tooltip,
        )
