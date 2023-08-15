import time
import uuid


class ARRobot:
    def __init__(self):
        self.id = uuid.uuid4()
        self.current_location = None
        self.target_location = None
        self.battery_level = 100
        self.available = True

    def drive_to_target_location(self):
        # target location is one of shelf location, empty location,
        # work station, charging station, point if current path has to be reset
        if self.target_location:
            print(f"Driving to {self.target_location} location")

    def turn(self):
        # TODO przenieść do Managera
        # right or left
        pass

    def head_direction(self):
        pass

    def stop(self):
        # if on target location, unable to move forward, need to turn, rotate shelf, pullup/down shelf
        pass

    def get_station_location(self):
        # if pull_up_shelve
        pass

    def get_shelve_location(self):
        if self.available:
            # location = db.get_station_location
            self.target_location = "location"
            self.available = False

    def get_empty_shelve_location(self):
        # get empty location of inner floor if there is no prediction for items stored in shelf for next 5 mins,
        # or battery level is low
        pass

    def pull_up_shelve(self):
        # if on target location, available and stop
        pass

    def rotate_shelve(self):
        # robot rotates shelf only to right :)
        pass

    def pull_down_shelve(self):
        # drive to target location, stop, available true
        pass

    def drive_to_charging_station(self):
        while self.battery_level > 10:
            time.sleep(60)
            self.battery_level -= 1
        if self.battery_level <= 10:
            if self.available:
                # drive to charging station
                pass
            else:
                # drive to nearest shelf location and then to charging station
                self.get_empty_shelve_location()
        pass
