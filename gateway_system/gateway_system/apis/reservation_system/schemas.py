from datetime import date
from enum import Enum
from uuid import UUID

from pydantic import BaseModel

from gateway_system.apis.library_system_api.schemas import BookModel, Condition, LibraryModel
from gateway_system.apis.rating_system_api.schemas import UserRating


class Status(Enum):
    RENTED = 'RENTED'
    RETURNED = 'RETURNED'
    EXPIRED = 'EXPIRED'


class Reservation(BaseModel):
    reservationUid: UUID
    status: Status
    startDate: date
    tillDate: date


class ReservationModel(Reservation):
    bookUid: UUID
    libraryUid: UUID


class ReservationResponse(Reservation):
    book: BookModel
    library: LibraryModel


class ReservationBookInput(BaseModel):
    bookUid: UUID
    libraryUid: UUID
    tillDate: date


class ReturnBookInput(BaseModel):
    condition: Condition
    date: date


class ReservationBookResponse(ReservationResponse):
    rating: UserRating


class ReservationUpdate(BaseModel):
    status: Status


class RentedBooks(BaseModel):
    count: int
