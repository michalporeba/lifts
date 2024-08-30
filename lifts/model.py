class Event:
  def __init__(self, message):
    self.message = message

class FloorEvent(Event):
  def __init__(self, floor, message):
    super().__init__(message)
    self.floor = floor


class Floor:
  def __init__(self, world, level):
    self.world = world
    self.world.subscribe(self)
    self.level = level
    self.queue = []
    self.upIndicator = False
    self.downIndicator = False

  def add_person(self, person) -> None:
    self.queue.append(person)
    if (not self.downIndicator and person.destination > self.level):
      self._press_down_button()
    elif (not self.upIndicator and person.destination < self.level):
      self._press_up_button()

  def receive(self, event):
    pass

  def _press_down_button(self):
    self.world.send(FloorEvent(self.level, "down"))
    self.downIndicator = True

  def _press_up_button(self):
    self.world.send(FloorEvent(self.level, "up"))
    self.upIndicator = True


class Lift:
  def __init__(self, world):
    self.world = world
    self.world.subscribe(self)
    self.messages = []

  def receive(self, event):
    print("receiving")
    self.messages.append(event)


class Person:
  def go_to(self, floor: int) -> None:
    self.destination = floor


class World:
  def __init__(self, floors, lifts):
    self.events = []
    self.subscribers = []
    self.floors = [Floor(self, x) for x in range(floors)]
    self.lifts = [Lift(self) for _ in range(lifts)]

  def advance(self):
    self._pump_events()

  def send(self, event):
    self.events.append(event)

  def subscribe(self, subscriber):
    self.subscribers.append(subscriber)

  def _pump_events(self):
    for event in self.events:
      for subscriber in self.subscribers:
        subscriber.receive(event)
