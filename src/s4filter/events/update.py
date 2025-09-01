from clock import ServerClock
from lot51_core.services.events import CoreEvent, event_service
from lot51_core.utils.context import Context
from lot51_core.utils.injection import inject_to


@inject_to(ServerClock, "tick_server_clock")
def _on_update(original, *args, **kwargs):
    original(*args, **kwargs)
    try:
        context = Context.get_current_context()
        event_service.process_event(CoreEvent.GAME_TICK, context=context)
    except:
        pass
