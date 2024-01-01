"""
Write the methods/classes which are being used by the other microservices to communicate with the another
Microservice.
This will help us to migrate the code efficiently and smoothly if we decide to use another inter microservice
communication channel like gRPC or the other better alternative.
"""
from logging import getLogger
from logging import Logger

import aiohttp
import inject
from metagrim_common.base.error import ApplicationError
from metagrim_common.base.settings import CoreSettings
from pydantic import UUID4


logger = getLogger(__name__)


class ServiceCommunication:
    """Class being used to allow communication between the microservices."""

    @inject.autoparams("config")
    def __init__(self, config: CoreSettings, logger_: Logger | None = None):
        self.config = config
        self.logger = logger_ or logger

    async def get_event_data(
        self,
        event_uuid: UUID4,
    ) -> str | None:
        # Prepare the URL
        url = f"{self.config.event_service_base_url}/fareharbor/{event_uuid}"
        headers = {}
        response = {}
        try:
            # Generate and forward the HTTP request
            self.logger.info(f"Fetching data {url}")
            timeout = aiohttp.ClientTimeout(total=self.config.requests_timeout)  # type: ignore[attr-defined]
            async with aiohttp.ClientSession(timeout=timeout, trust_env=True) as session:  # type: ignore[attr-defined]
                async with session.get(
                    url=url,
                    headers=headers,
                ) as r:
                    response = await r.json()
                    # Extract the schedule_id from the request if the request was successful
                    if r.status == 200:
                        event_id = str(response["id"])
                        self.logger.info(f"Fetched data: {event_id}")
                        self.logger.debug(f"Event Data: {response}")
                    else:
                        self.logger.error(f"Error in fetching event data: {url} {r.status} {response}")
                        raise ApplicationError(500, message=f"Unable to get event data {r} {r.status} {response}")
        except aiohttp.ClientConnectionError as connect_err:
            self.logger.error(f"Failed to get event data due to: {connect_err}")
        except aiohttp.ClientResponseError as client_err:
            self.logger.error(f"Failed to get event data due to: {client_err}")
        except Exception as e:
            self.logger.error(f"Failed to get event data due to: {e}")
            raise e
        return response

    async def delete_event(self, event_uuid: UUID4) -> bool:

        # Prepare the URL
        url = f"{self.config.event_service_base_url}/fareharbor/{event_uuid}"
        headers = {}
        try:
            # Generate and forward the HTTP request
            self.logger.info(f"Deleting event {url}")
            timeout = aiohttp.ClientTimeout(total=self.config.requests_timeout)  # type: ignore[attr-defined]
            async with aiohttp.ClientSession(timeout=timeout, trust_env=True) as session:  # type: ignore[attr-defined]
                async with session.delete(url=url, headers=headers) as r:
                    # If the schedule was deleted, then we consider the condition successful
                    if r.status == 200:
                        is_deleted = True
                    # If the schedule isn't found, then we consider the condition successful
                    elif r.status == 404:
                        is_deleted = True
        except Exception as e:
            self.logger.error(f"Failed to delete an event due to: {e}")
            raise e
        return is_deleted
