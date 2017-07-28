#!/usr/bin/env python2

import sys, copy

dicoPath = './dictionary.txt'

class node :

   def __init__(self, prefix):
      self._sons = {}
      self._isWord = False
      self._prefix = prefix

   def insert(self, suffix):
      if len(suffix) == 0:
         self._isWord = True
         return
      if self._sons.has_key(suffix[0]):
         self._sons[suffix[0]].insert(suffix[1:])
      else:
         self._sons[suffix[0]] = node(suffix[0])
         self._sons[suffix[0]].insert(suffix[1:])

   def contains(self, suffix):
      if not suffix:
         if self._isWord:
            return 'sol'
         else: 
            return 'prefix'
      if not self._sons.has_key(suffix[0]):
         return 'no'
      return self._sons[suffix[0]].contains(suffix[1:])

class openSol :

   def __init__(self, newPos, oldUsed, newPrefix):
      self._pos = newPos
      self._used = oldUsed
      self._used[newPos[0]][newPos[1]] = True
      self._prefix = newPrefix

   def getNextSols(self, grid, solutions, dico):
      nRelPos = [(x,y) for x in [-1,0,1] for y in [-1,0,1]\
            if not (x==0 and y==0)]
      nAbsPos = [(self._pos[0]+x[0], self._pos[1]+x[1]) for x in nRelPos]

      res = []
      for p in nAbsPos:
         # remove position out of the grid
         if p[0] < 0 or p[1] < 0 or p[0] >= 4 or p[1] >= 4:
            continue
         # remove position used for the prefix
         if self._used[p[0]][p[1]]:
            continue
         # remove if no word can be build with the new prefix
         newPrefix = self._prefix + grid[p[0]][p[1]]
         if dico.contains(newPrefix) == 'no':
            continue

         if dico.contains(newPrefix) == 'sol':
            solutions.append(newPrefix)
         res.append(openSol(p, copy.deepcopy(self._used), newPrefix))

      return res

def removeDuplicates(seq):
   seen = set()
   seen_add = seen.add
   return [ x for x in seq if x not in seen and not seen_add(x)]

def main():

   print "Build the game's grid ..."
   line = sys.argv[1]
   grid = [['' for x in range(4)] for y in range(4)]
   for i in range(len(line)):
      grid[i/4][i%4] = line[i]

   print "Load dictionary ..."
   dico = node("")
   with open(dicoPath, 'r+') as f:
      for line in f:
         dico.insert(line[0:len(line)-2])

   print "Initialise open solutions ..."
   openSols = []
   used = [[False for x in range(4)] for y in range(4)]
   for x in range(4):
      for y in range(4):
         openSols.append(openSol((x,y), copy.deepcopy(used), grid[x][y]))

   print "Compute open solutions ..."
   solutions = []
   while openSols:
      openSols.extend(openSols.pop().getNextSols(grid, solutions, dico))

   solutions = removeDuplicates(solutions)
   solutions.sort(key=len, reverse=True)

   print "\n*** Solutions ***"
   print " ".join(solutions)

if __name__ == "__main__":
   main()
