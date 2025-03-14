Some Python scripts in this repository use a complex plane to store the information of a 2-dimensional grid. Instead of representing an $(x, y)$ coordinate using a list of coordinates like `pos = [x, y]`, the position is stored as a complex number where the x-position is represented using the real part, and the y-position using the imaginary part like `pos = x + y*i`. This offers a few advantages over using a list of coordinates.

1. Since complex numbers are immutable, they can be used as keys for a dictionary or as elements in a set. This opens up the possibility of representing the 2-dimensional map as a dictionary, where the keys are the complex coordinates and the values are the corresponding contents of the map at those positions. This makes it much easier - yet very fast - to check for map boundaries, since `if element in dictionary` is an $O(1)$ operation.

2. Changing the position becomes a simple statement. Suppose we want to change some position `pos` by some direction `dir`. In a complex plane, this can be done using `pos = pos + dir`. Using a list of coordinates, this would become `pos = [pos[0] + dir[0], pos[1] + dir[1]]`.

3. If the map contains holes, then these holes do not need to be part of the map if a dictionary of coordinates is used. This cannot be done when nested lists are used.

4. Rotation by 90 degrees is a simple statement. A 90 degrees rotation left or right equals multiplying by -1j or 1j, respectively. For example, a direction pointing east `dir = 1 + 0j` rotated 90 degrees left becomes `dir = (1 + 0j) * -1j = 0 - 1j`, which is indeed north. Doing such a computation using `dir = [1, 0]` would require matrix multiplication.
