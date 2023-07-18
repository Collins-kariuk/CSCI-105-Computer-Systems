from __future__ import with_statement
from threading import Thread, Lock, Condition, Semaphore
from os import _exit as quit
import time, random

####################################################### 
#                      
# Partner 1: Joram Amador
#
# Partner 2: Collins Kariuki
# 
#######################################################


# Modify only the code of the class Club to make the program
# correct.

# Place your synchronization variables inside the Club instance.

# Make sure nobody is holding a Club synchronization variable
# while executing outside the Club code.


def hangout():
    time.sleep(random.randint(0, 2))


class Club:
    def __init__(self, capacity):
        self.goth_count = 0               # num goths in club
        self.hipster_count = 0            # num hipsters in club
        self.capacity = capacity          # only used for optional questions
        self.lock = Lock()
        self.switch = Lock()
        self.cv_goth = Condition(self.lock)
        self.cv_hipster = Condition(self.lock)



    def __sanitycheck(self):
        if self.goth_count > 0 and self.hipster_count > 0:
            print("sync error: bad social mixup! Goths = %d, Hipsters = %d" %  (self.goth_count, self.hipster_count))
            quit(1)
        if self.goth_count>self.capacity or self.hipster_count>self.capacity:
            print("sync error: too many people in the club! Goths = %d, Hipsters = %d" %  (self.goth_count, self.hipster_count))
            quit(1)
        if self.goth_count < 0 or self.hipster_count < 0:
            print("sync error: lost track of people! Goths = %d, Hipsters = %d" %  (self.goth_count, self.hipster_count))
            quit(1)

        
    def goth_enter(self):
        self.switch.acquire()
        self.lock.acquire()

        while self.hipster_count > 0 or self.goth_count >= self.capacity:
            self.cv_goth.wait()
        
        self.goth_count +=1

        self.switch.release()
        self.__sanitycheck()
        self.lock.release()
        


    def goth_exit(self):
        self.lock.acquire()
        self.goth_count -= 1
        self.cv_goth.notify()
        if self.goth_count == 0:
            self.cv_hipster.notify_all()
        self.__sanitycheck()
        self.lock.release()
        


    def hipster_enter(self):
        self.switch.acquire()
        self.lock.acquire()

        while self.goth_count > 0 or self.hipster_count >= self.capacity:
            self.cv_hipster.wait()

        self.hipster_count += 1
        self.switch.release()
        self.__sanitycheck()
        self.lock.release()
        

    def hipster_exit(self):
        self.lock.acquire()
        self.hipster_count -= 1
        self.cv_hipster.notify()
        if self.hipster_count == 0:
            self.cv_goth.notify_all()
        self.__sanitycheck()
        self.lock.release()
        

class Goth(Thread):
    def __init__(self, id):
        Thread.__init__(self)
        self.id = id

    def run(self):
        global daclub

        while True:
            print("goth #%d: wants to enter" % self.id)
            daclub.goth_enter()
            print("goth #%d: in the club" % self.id)
            print("goths in club: %d" % daclub.goth_count)
            hangout()
            daclub.goth_exit()
            print("goth #%d: left club" % self.id)
            print("goths in club: %d" % daclub.goth_count)
            
class Hipster(Thread):
    def __init__(self, id):
        Thread.__init__(self)
        self.id = id

    def run(self):
        global daclub

        while True:
            print("hipster #%d: wants to enter" % self.id)
            daclub.hipster_enter()
            print("hipster #%d: in the club" % self.id)
            print("hipsters in club: %d" % daclub.hipster_count)
            hangout()
            daclub.hipster_exit()
            print("hipster #%d: left club" % self.id)
            print("hipsters in club: %d" % daclub.hipster_count)


NUMGOTH = 6
NUMHIPSTER = 6
CAPACITY = 3
daclub = Club(CAPACITY)


def main():
    for i in range(0, NUMGOTH):
        g = Goth(i)
        g.start()    
    for i in range(0, NUMHIPSTER):
        h = Hipster(i)
        h.start()    

if __name__ == "__main__":
    main()
