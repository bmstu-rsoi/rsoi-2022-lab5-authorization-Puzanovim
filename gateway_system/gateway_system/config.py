from pydantic import BaseSettings, Field


class RatingConfig(BaseSettings):
    host: str = Field(env='RATING_SYSTEM_HOST', default='rating')
    port: int = Field(env='RATING_SYSTEM_PORT', default=8050)

    class Config:
        validate_assignment = True


class LibraryConfig(BaseSettings):
    host: str = Field(env='LIBRARY_SYSTEM_HOST', default='library')
    port: int = Field(env='LIBRARY_SYSTEM_PORT', default=8060)

    class Config:
        validate_assignment = True


class ReservationConfig(BaseSettings):
    host: str = Field(env='RESERVATION_SYSTEM_HOST', default='reservation')
    port: int = Field(env='RESERVATION_SYSTEM_PORT', default=8070)

    class Config:
        validate_assignment = True


class CircuitBreakerConfig(BaseSettings):
    failure_threshold: int = Field(env='CIRCUIT_BREAKER_FAILURE_THRESHOLD', default=2)
    success_threshold: int = Field(env='CIRCUIT_BREAKER_SUCCESS_THRESHOLD', default=1)
    timeout: int = Field(env='CIRCUIT_BREAKER_TIMEOUT', default=15)

    class Config:
        validate_assignment = True


RATING_SYSTEM_CONFIG: RatingConfig = RatingConfig()
LIBRARY_SYSTEM_CONFIG: LibraryConfig = LibraryConfig()
RESERVATION_SYSTEM_CONFIG: ReservationConfig = ReservationConfig()
CIRCUIT_BREAKER_CONFIG: CircuitBreakerConfig = CircuitBreakerConfig()
