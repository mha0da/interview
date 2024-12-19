# Review 1


# The arg my_list=[] might cause unexpected result.
# The function will create an empty list when arg my_list is not provided.
# Then values will be collected to the same default created list if the function is executed without arg my_list.
def add_to_list(value, my_list=None):
    if not my_list:
        my_list = []
    my_list.append(value)
    return my_list


# Review 2


# The arg name and age will not be really populated into the placeholder.
# Could leverage format method or f-string to insert variables into string,
def format_greeting(name, age):

    return f"Hello, my name is {name} and I am {age} years old."


# Review 3


# self.count is instance attribute and count is class attribute.
# Instances would share class attributes but instance attributes.
class Counter:

    count = 0

    def __init__(self):
        Counter.count += 1

    @classmethod
    def get_count(cls):

        return cls.count


# Review 4

# Threads might operate one resource at the same time
# Need a lock to make sure the resource can only be accessed by one thread at one time.
import threading


class SafeCounter:

    def __init__(self):

        self.count = 0
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            self.count += 1


def worker(counter):

    for _ in range(1000):

        counter.increment()


counter = SafeCounter()

threads = []

for _ in range(10):

    t = threading.Thread(target=worker, args=(counter,))

    t.start()

    threads.append(t)


for t in threads:

    t.join()


# Review 5

# The correct increcment expression is += 1
def count_occurrences(lst):

    counts = {}

    for item in lst:

        if item in counts:

            counts[item] += 1

        else:

            counts[item] = 1

    return counts
