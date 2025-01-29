#this Nearest Neighbor algorithm determines truck route for deliveries (delivery graphs)

'''
Nearest-Neighbor Algorithm:
INITIALIZE unvisited vertices list = truck’s package delivery locations.
Select a starting vertex – the packaging company’s hub warehouse’s address.
ASSIGN this starting vertex as current-visited, C-V.
	ASSIGN variable min_distance to 25.
Look for the shortest edge that connects C-V to an unvisited vertex:
	GET the first unvisited vertex from the list of packages.
		ASSIGN this as working vertex, W-V.
	LOOP through the list of unvisited vertices:
	WHILE there are still vertices in the unvisited list:
LOOKUP the distance from W-V to C-V.
COMPARE to variable min_distance
IF this result < min_distance
	UPDATE W-V to be next visited, N-V.
UPDATE min_distance = result
ELSE
GET next unvisited vertex from list as W-V.
		END WHILE LOOP
ASSIGN N-V (next visited) as current visited, C-V. (Truck goes here.)
MOVE N-V from the list of unvisited vertices to a queue/list of visited vertices.
	STORE tuple (vertex, min_distance) in the Visited queue.
REPEAT until unvisited vertices list size = 0.


'''