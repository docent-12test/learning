import asyncio
import logging
from datetime import datetime
from random import random as rand
from dataclasses import dataclass, field
from typing import Optional, List

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

CUSTOMER_COUNT = 100
ARRIVAL_DELAY_MAX = 1.0
SERVICE_DELAY_MAX = ARRIVAL_DELAY_MAX * 2


@dataclass
class Customer:
    name: str
    arrival: datetime = field(default_factory=datetime.now)
    leave: Optional[datetime] = None

    def mark_left(self) -> None:
        self.leave = datetime.now()

    def __repr__(self) -> str:
        ret = f"{self.name} arrived at {self.arrival}"
        if self.leave:
            ret += f" and left at {self.leave}: {self.leave - self.arrival}"
        return ret


SENTINEL = object()  # marker om de consument te laten stoppen


# ... existing code ...
async def produce_customers(queue: asyncio.Queue, count: int, customers_log: List[Customer]) -> None:
    for i in range(count):
        logger.debug(f"Customer {i} arrived")
        customer = Customer(f"Customer {i}")
        customers_log.append(customer)
        await queue.put(customer)
        await asyncio.sleep(rand() * ARRIVAL_DELAY_MAX)
    # signaal dat er geen nieuwe klanten meer komen
    await queue.put(SENTINEL)


# ... existing code ...
async def serve_customers(queue: asyncio.Queue) -> None:
    while True:
        item = await queue.get()
        if item is SENTINEL:
            # sentinel terugzetten als je meerdere consumenten hebt
            await queue.put(SENTINEL)
            logger.debug("Service shutting down (no more customers).")
            break
        customer: Customer = item  # type: ignore[assignment]
        # verwerk de klant
        await asyncio.sleep(rand() * SERVICE_DELAY_MAX)
        customer.mark_left()
        logger.debug(f"Customer {customer.name} left")
        queue.task_done()


# ... existing code ...
async def main() -> list[Customer]:
    queue: asyncio.Queue = asyncio.Queue()
    customers: list[Customer] = []
    producer = asyncio.create_task(produce_customers(queue, CUSTOMER_COUNT, customers))
    consumer1 = asyncio.create_task(serve_customers(queue))
    consumer2 = asyncio.create_task(serve_customers(queue))
    await asyncio.gather(producer, consumer1, consumer2)
    return customers


# ... existing code ...
if __name__ == "__main__":
    customers_result = asyncio.run(main())
    for customer in customers_result:
        print(customer)
