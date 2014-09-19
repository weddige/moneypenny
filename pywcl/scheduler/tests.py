from __init__ import Scheduler, Task

@Task(interval=5, repeat=3)
def test_function():
    print('Decorating functions works as expected.')

class TestClass:
    @Task(interval=5, repeat=3)
    def print_msg(self):
        print('Decorating class methods works as expected.')

if __name__ == '__main__':
    sched = Scheduler()
    sched.schedule(test_function)
    test = TestClass()
    sched.schedule(test.print_msg)
