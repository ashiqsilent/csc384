from bicycle import *

a = [
    ['loc0', 'loc1', 'loc2', 'loc3', 'loc4', 'loc5', 'loc6',
     'loc7', 'loc8', 'loc9', 'loc10', 'loc11', 'loc12', 
     'loc13', 'loc14'],
     [['loc0', 'loc1', 30], ['loc0', 'loc2', 30], ['loc0', 'loc3', 30],
      ['loc0', 'loc4', 30], ['loc0', 'loc5', 30], ['loc0', 'loc6', 30],
      ['loc0', 'loc7', 30], ['loc0', 'loc8', 30], ['loc0', 'loc9', 30],
      ['loc0', 'loc10', 30], ['loc0', 'loc11', 30], ['loc0', 'loc12', 30],
      ['loc0', 'loc13', 30], ['loc0', 'loc14', 30], ['loc1', 'loc2', 30],
      ['loc1', 'loc3', 30], ['loc1', 'loc4', 30], ['loc1', 'loc5', 30],
      ['loc1', 'loc6', 30], ['loc1', 'loc7', 30], ['loc1', 'loc8', 30],
      ['loc1', 'loc9', 30], ['loc1', 'loc10', 30], ['loc1', 'loc11', 30],
      ['loc1', 'loc12', 30], ['loc1', 'loc13', 30], ['loc1', 'loc14', 30],
      ['loc2', 'loc3', 30], ['loc2', 'loc4', 30], ['loc2', 'loc5', 30],
      ['loc2', 'loc6', 30], ['loc2', 'loc7', 30], ['loc2', 'loc8', 30],
      ['loc2', 'loc9', 30], ['loc2', 'loc10', 30], ['loc2', 'loc11', 30],
      ['loc2', 'loc12', 30], ['loc2', 'loc13', 30], ['loc2', 'loc14', 30],
      ['loc3', 'loc4', 30], ['loc3', 'loc5', 30], ['loc3', 'loc6', 30],
      ['loc3', 'loc7', 30], ['loc3', 'loc8', 30], ['loc3', 'loc9', 30],
      ['loc3', 'loc10', 30], ['loc3', 'loc11', 30], ['loc3', 'loc12', 30],
      ['loc3', 'loc13', 30], ['loc3', 'loc14', 30], ['loc4', 'loc5', 30],
      ['loc4', 'loc6', 30], ['loc4', 'loc7', 30], ['loc4', 'loc8', 30],
      ['loc4', 'loc9', 30], ['loc4', 'loc10', 30], ['loc4', 'loc11', 30],
      ['loc4', 'loc12', 30], ['loc4', 'loc13', 30], ['loc4', 'loc14', 30],
      ['loc5', 'loc6', 30], ['loc5', 'loc7', 30], ['loc5', 'loc8', 30],
      ['loc5', 'loc9', 30], ['loc5', 'loc10', 30], ['loc5', 'loc11', 30],
      ['loc5', 'loc12', 30], ['loc5', 'loc13', 30], ['loc5', 'loc14', 30],
      ['loc6', 'loc7', 30], ['loc6', 'loc8', 30], ['loc6', 'loc9', 30],
      ['loc6', 'loc10', 30], ['loc6', 'loc11', 30], ['loc6', 'loc12', 30],
      ['loc6', 'loc13', 30], ['loc6', 'loc14', 30], ['loc7', 'loc8', 30],
      ['loc7', 'loc9', 30], ['loc7', 'loc10', 30], ['loc7', 'loc11', 30],
      ['loc7', 'loc12', 30], ['loc7', 'loc13', 30], ['loc7', 'loc14', 30],
      ['loc8', 'loc9', 30], ['loc8', 'loc10', 30], ['loc8', 'loc11', 30],
      ['loc8', 'loc12', 30], ['loc8', 'loc13', 30], ['loc8', 'loc14', 30],
      ['loc9', 'loc10', 30], ['loc9', 'loc11', 30], ['loc9', 'loc12', 30],
      ['loc9', 'loc13', 30], ['loc9', 'loc14', 30], ['loc10', 'loc11', 30],
      ['loc10', 'loc12', 30], ['loc10', 'loc13', 30], ['loc10', 'loc14', 30],
      ['loc11', 'loc12', 30], ['loc11', 'loc13', 30], ['loc11', 'loc14', 30],
      ['loc12', 'loc13', 30], ['loc12', 'loc14', 30], ['loc13', 'loc14', 30]]]

s = [['Job4', 'loc14', 8.15, 'loc6', [8.30, 480], [8.45, 240]]]

y = solve(make_start_state(a, s))
print y