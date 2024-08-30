import pytest
from lifts.model import Person, World

@pytest.mark.parametrize("floors, lifts", [(2, 1), (4, 4)])
def test_world_creation(floors, lifts):
  sut = World(floors, lifts)
  assert floors == len(sut.floors)
  assert lifts == len(sut.lifts)


def test_pressing_button_up():
  world = World(3, 2)
  person = Person()
  person.go_to(2)
  world.floors[0].add_person(person)
  world.advance()
  assert 0 < len(world.lifts[0].messages)
