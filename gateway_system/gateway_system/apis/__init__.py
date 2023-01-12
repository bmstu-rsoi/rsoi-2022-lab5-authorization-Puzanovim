from gateway_system.apis.library_system_api.api import LibrarySystemAPI
from gateway_system.apis.rating_system_api.api import RatingSystemAPI
from gateway_system.apis.reservation_system.api import ReservationSystemAPI

library_system_api: LibrarySystemAPI = LibrarySystemAPI()
reservation_system_api: ReservationSystemAPI = ReservationSystemAPI()
rating_system_api: RatingSystemAPI = RatingSystemAPI()


async def get_library_system_api() -> LibrarySystemAPI:
    return library_system_api


async def get_reservation_system_api() -> ReservationSystemAPI:
    return reservation_system_api


async def get_rating_system_api() -> RatingSystemAPI:
    return rating_system_api
