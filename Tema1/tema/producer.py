"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
from time import sleep


class Producer(Thread):
    """
    Class that represents a producer.
    """
    products = []  # lista de produse ale producatorului
    marketplace = None  # marketplace-ul asociat
    republish_wait_time = 0

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time

    def run(self):
        producer_id = self.marketplace.register_producer()  # inregistrez producerul
        while True:
            # pentru fiecare produs retin cantitatea si timpul de asteptare
            for product in self.products:
                count = product[1]
                waiting_time = product[2]
                for i in range(count):
                    while True:
                        # daca s-a putut face publicarea, trec la urmatoarea publicare
                        if self.marketplace.publish(producer_id, product[0]):
                            break
                        sleep(self.republish_wait_time)
                    sleep(waiting_time)
