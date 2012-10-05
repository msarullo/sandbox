'''
Created on Oct 4, 2012

@author: msarullo
'''

import logging
import time
from abc import ABCMeta, abstractmethod
from itertools import count
from threading import Thread, Condition, Semaphore

singletonGenerator = None
singletonLock = Semaphore(1)


def getContentGenerator():
    logger = logging.getLogger(__name__ + ".getContentGenerator")
    global singletonGenerator
    global singletonLock

    if singletonGenerator == None:
        if singletonLock.acquire(True):
            try:
                if singletonGenerator == None:
                    singletonGenerator = ContentGenerator()
            finally:
                singletonLock.release()
        else:
            logger.error("Failed to acquire lock to construct content generator!")

    if singletonGenerator == None:
        raise RuntimeError("Failed to construct content generator!")

    return singletonGenerator
    

class ContentGenerationListener:
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def onGeneration(self, msg):
        raise NotImplemented()
        

class ContentGenerator(Thread):

    lock = Condition()
    shouldRun = True
    loopIntervalSecs = 2
    listeners = []

    def __init__(self):
        global singletonLock
        
        if singletonLock.acquire(False):
            # Hmm, we acquired the lock, this is not good, someone is creating us without
            # using the factory method, we should fail now.
            singletonLock.release()
            raise RuntimeError("An attempt was made to create a ContentGenerator object outside of the factory method getContentGenerator")
        
        super(ContentGenerator, self).__init__(name="ContentGeneratorThread")
        self.daemon = True


    def run(self):
        logger = logging.getLogger(__name__ + ".ContentGenerator.run")
        logger.debug("Content Generator Thread beginning")
        
        for x in count(0):
            time.sleep(self.loopIntervalSecs)
            if self.lock.acquire():
                try:
                    if self.shouldRun:
                        self.generator(logger, x)
                    else:
                        break
                finally:
                    self.lock.release()
            else:
                logger.error("Failed to acquire content generation lock, unable to run generator!")
        
        logger.debug("Content Generator Thread finished")


    def gracefulStop(self):
        if not self.isAlive():
            return
        
        if self.lock.acquire():
            try:
                self.shouldRun = False
                self.join(10)
            finally:
                self.lock.release()
        else:
            logger = logging.getLogger(__name__ + ".ContentGenerator.gracefulStop")
            logger.error("Failed to acquire content generation lock, unable to shut down gracefully!")
            
        
    def addListener(self, newGuy):
        logger = logging.getLogger(__name__ + ".ContentGenerator.addListener")
        if not isinstance(newGuy, ContentGenerationListener):
            logger.error("Attempted to add listener of type:  " + type(newGuy))
            return False
        
        if self.lock.acquire():
            try:
                self.listeners.append(newGuy)
            finally:
                self.lock.release()
                
            logger.info("Successfully added listener:  %d", newGuy.id())
            return True
        else:
            logger.error("Failed to acquire content generation lock, unable to add listener!")
            return False
        
        
    def dropListener(self, guyToDrop):
        logger = logging.getLogger(__name__ + ".ContentGenerator.dropListener")
        
        if self.lock.acquire():
            try:
                self.listeners.remove(guyToDrop)
            finally:
                self.lock.release()
                
            logger.info("Successfully dropped listener:  %d", guyToDrop.id())
            return True
        else:
            logger.error("Failed to acquire content generation lock, unable to drop listener!")
            return False

    
    def generator(self, logger, counter):
        # Assume we already have the lock
        logger.debug("Generated item:  (%d)", counter)
        
        for x in self.listeners:
            x.onGeneration(str(counter))
