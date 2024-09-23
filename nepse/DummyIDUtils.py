import asyncio
from datetime import datetime


class _DummyIDManager:
    def __init__(self, market_status_function=None, date_function=datetime.now):
        self.data = None
        self.dummy_id = None
        self.date_stamp = None

        self.setDateFunction(date_function)
        self.setMarketStatusFunction(market_status_function)

    def setDateFunction(self, func):
        self.date_function = func

    def setMarketStatusFunction(self, func):
        self.market_status_function = func
        self.data = None

    def convertToDateTime(self, date_time_str):
        return datetime.strptime(date_time_str, "%Y-%m-%dT%H:%M:%S")

    def __repr__(self):
        return f"<Dummy ID: {self.dummy_id}, Date: {self.date_stamp}>"


class AsyncDummyIDManager(_DummyIDManager):
    def __init__(self, market_status_function=None, date_function=datetime.now):
        super().__init__(market_status_function, date_function)

        self.update_started = asyncio.Event()
        self.update_completed = asyncio.Event()

    async def populateData(self, force=False):
        today = self.date_function()

        # executes only if self.data is not initialized or force flag set to True is passed
        if self.data is None or force:
            if not self.update_started.is_set():
                self.update_started.set()
                self.update_completed.clear()

                self.data = await self.market_status_function()
                self.dummy_id = self.data["id"]
                self.date_stamp = today

                self.update_completed.set()
                self.update_started.clear()
                return
            await self.update_completed.wait()

        # check if day has already passed and another co-routine to update it is already started
        # if that's the case then just wait for that coroutine to complete itself.
        if self.date_stamp.date() < today.date():
            if self.update_started.is_set():
                await self.update_completed.wait()
            else:
                # set event
                self.update_started.set()
                self.update_completed.clear()

                new_data = await self.market_status_function()

                new_converted_date = self.convertToDateTime(new_data["asOf"])

                # check if nepse date is equal to current date
                if new_converted_date.date() == today.date():
                    self.data = new_data
                    self.dummy_id = self.data["id"]
                    self.date_stamp = new_converted_date

                # nepse date is not equal to current date which means nepse is closed
                # in such case we set the date stamp to today so that we dont have to check it everytime
                else:
                    self.data = new_data
                    self.dummy_id = self.data["id"]
                    self.date_stamp = today

                # clear event
                self.update_completed.set()
                self.update_started.clear()

    async def getDummyID(self):
        await self.populateData()
        return self.dummy_id


class DummyIDManager(_DummyIDManager):
    def __init__(self, market_status_function=None, date_function=datetime.now):
        super().__init__(market_status_function, date_function)

    def populateData(self, force=False):
        today = self.date_function()

        if self.data is None or force:
            self.data = self.market_status_function()
            self.dummy_id = self.data["id"]
            self.date_stamp = today
            return

        if self.date_stamp.date() < today.date():
            new_data = self.market_status_function()
            new_converted_date = self.convertToDateTime(new_data["asOf"])

            # check if nepse date is equal to current date
            if new_converted_date.date() == today.date():
                self.data = new_data
                self.dummy_id = self.data["id"]
                self.date_stamp = new_converted_date

            # nepse date is not equal to current date which means nepse is closed
            # in such case we set the date stamp to today so that we dont have to check it everytime
            else:
                self.data = new_data
                self.dummy_id = self.data["id"]
                self.date_stamp = today

    def getDummyID(self):
        self.populateData()
        return self.dummy_id


def testDummyManager():
    def friday():
        print("friday_called")
        return {
            "isOpen": "Pre Open CLOSE",
            "asOf": "2023-09-27T10:45:00",
            "id": 80,
        }

    def saturday():
        print("saturday_called")
        return {
            "isOpen": "Pre Open CLOSE",
            "asOf": "2023-09-27T10:45:00",
            "id": 81,
        }

    def sunday():
        print("sunday_called")
        return {
            "isOpen": "Pre Open CLOSE",
            "asOf": "2023-10-01T10:45:00",
            "id": 82,
        }

    def monday():
        print("monday called")
        return {
            "isOpen": "Pre Open CLOSE",
            "asOf": "2023-10-02T10:45:00",
            "id": 82,
        }

    today_friday = lambda: datetime(2023, 9, 28)
    today_saturday = lambda: datetime(2023, 9, 29)
    today_sunday = lambda: datetime(2023, 10, 1)
    today_monday = lambda: datetime(2023, 10, 2)

    dummy_manager = DummyIDManager()

    dummy_manager.setDateFunction(today_friday)
    dummy_manager.setMarketStatusFunction(friday)
    dummy_manager.getDummyID()
    print(dummy_manager)

    dummy_manager.setMarketStatusFunction(friday)
    dummy_manager.getDummyID()
    print(dummy_manager)

    dummy_manager.setMarketStatusFunction(friday)
    dummy_manager.getDummyID()
    print(dummy_manager)

    dummy_manager.setDateFunction(today_saturday)
    dummy_manager.setMarketStatusFunction(saturday)
    dummy_manager.getDummyID()
    print(dummy_manager)

    dummy_manager.setDateFunction(today_saturday)
    dummy_manager.setMarketStatusFunction(saturday)

    dummy_manager.getDummyID()
    print(dummy_manager)
    dummy_manager.getDummyID()
    print(dummy_manager)
    dummy_manager.getDummyID()
    print(dummy_manager)

    dummy_manager.setDateFunction(today_sunday)
    dummy_manager.setMarketStatusFunction(saturday)

    dummy_manager.getDummyID()
    print(dummy_manager)
    dummy_manager.getDummyID()
    print(dummy_manager)

    dummy_manager.setDateFunction(today_sunday)
    dummy_manager.setMarketStatusFunction(sunday)

    dummy_manager.getDummyID()
    print(dummy_manager)
    dummy_manager.getDummyID()
    print(dummy_manager)

    dummy_manager.setDateFunction(today_monday)
    dummy_manager.setMarketStatusFunction(monday)

    dummy_manager.getDummyID()
    print(dummy_manager)
    dummy_manager.getDummyID()
    print(dummy_manager)
