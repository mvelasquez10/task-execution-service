
import logging
from aiobreaker import CircuitBreaker

logger = logging.getLogger(__name__)

class CircuitBreakerMonitor:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CircuitBreakerMonitor, cls).__new__(cls)
            cls._instance.breakers = {}
        return cls._instance

    def register(self, name: str, breaker: CircuitBreaker):
        logger.info(f"Registering circuit breaker: {name}")
        self.breakers[name] = breaker

    def get_status(self):
        logger.info(f"Getting health status. Breakers: {self.breakers}")
        statuses = {}
        overall_status = "healthy"
        has_half_open = False

        for name, breaker in self.breakers.items():
            state = breaker.current_state.name
            statuses[name] = state
            if state == "open":
                overall_status = "down"
                break
            elif state == "half-open":
                has_half_open = True

        if overall_status != "down" and has_half_open:
            overall_status = "degraded"

        health_status = {"status": overall_status, "dependencies": statuses}
        logger.info(f"Health status: {health_status}")
        return health_status

circuit_breaker_monitor = CircuitBreakerMonitor()
