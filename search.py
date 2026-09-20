# hill climbing with gradient descent, and perhaps annealing
STEP_SIZE = 0.1
start_point = [0, 0.5] #arbitrary point

# function hill_climbing(f, start) returns a local maximun state
#     current = start
#     loop
#         neighbour = highest-valued successor of current
#         if f(neighbour) <= f(current)
#             return current

# curr is a list of list, with the inner list having 2 or 10 elements (knobs)
def single_steps(curr):
    neigbs = []

    for i, knob in enumerate(curr):
        incr = curr.copy()
        incr[i] = knob + STEP_SIZE
        neigbs.append(incr)

        decr = curr.copy()
        decr[i] = knob - STEP_SIZE
        neigbs.append(decr)

    return neigbs

def sweeping_steps(curr, direction):
    """
    Walk STEP_SIZE in `direction` (+1 or -1) across knobs left to right,
    then partially walk back in the opposite direction over all but the
    last two knobs.

    e.g. direction=+1, curr=[.5, .5, .5]:
        [.5,.5,.5] -> [.6,.6,.5] -> [.6,.6,.6] -> [.5,.6,.6]
    (the starting state is skipped — _perturb_single_knobs already covers it)
    """
    neighbours = []

    primed = curr.copy()
    primed[0] += direction * STEP_SIZE
    for i in range(1, len(primed)):
        primed[i] += direction * STEP_SIZE
        neighbours.append(primed.copy())

    reversed_primed = primed.copy()
    for i in range(0, len(reversed_primed) - 2):
        reversed_primed[i] -= direction * STEP_SIZE
        neighbours.append(reversed_primed.copy())

    return neighbours

def get_neighbours(curr):
    neighbours = []
    neighbours.extend(single_steps(curr))
    neighbours.extend(sweeping_steps(curr, direction=+1))
    neighbours.extend(sweeping_steps(curr, direction=-1))
    return neighbours

neigbs = get_neighbours([0.5, 0.5, 0.5])

for neigb in neigbs:
    print(neigb)

# def hill_climbing(f: function, start: List):
#     """
#     f: scoring function
#     start: the starting parameters
#     """
#     current = start
#     while 1:
#         pass
#         # neighbour = highest-valued successor of current. Need expand function