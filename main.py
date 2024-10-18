# Griffin King
# Unit 2 Project
# Bear, Fish, River

from os import system
from ecosystem import *
from time import sleep

DAYS_SIMULATED = 30
RIVER_SIZE = 10
START_BEARS = 5
START_FISH = 10

def BearFishRiver():

  r = River(RIVER_SIZE, START_BEARS, START_FISH)
  day = 0
  done = False
  message = "Sean is a poop doody"

  for day in range(DAYS_SIMULATED):
    print(f"\n\nDay: {day+1}")
    print(r)
    print(f"\nStarting Poplation: {r.population} animals")
    done, message = r.new_day()
    print(f"Ending Poplation: {r.population} animals")
    print(r)
    day += 1
    sleep(5)
    if done:
      break
  if done == True:
    print(f"\nThe simulations has ended because {message}")
  else:
    print("\nThe simulation has reached the desired days")
if __name__ == "__main__":
  system("clear")
  BearFishRiver()