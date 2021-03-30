"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
from time import sleep


class Consumer(Thread):
    """
    Class that represents a consumer.
    """
    carts = []  # cart-urile consumatorului
    marketplace = None  # marketplace-ul asociat
    retry_wait_time = 0

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time

    def run(self):
        # pentru fiecare cart obtin un cart nou in marketplace
        for cart in self.carts:
            cart_id = self.marketplace.new_cart()

            # pentru fiecare intrare din cart obtin tipul operatiei, prodsul si cantitatea
            for entry in cart:
                action_type = entry["type"]
                product = entry["product"]
                quantity = entry["quantity"]

                for i in range(quantity):
                    if action_type == "add":
                        while True:
                            # daca adaugarea in cos a avut succes trec la urmatoarea adaugare
                            if self.marketplace.add_to_cart(cart_id, product):
                                break
                        sleep(self.retry_wait_time)
                    else:
                        # scot din cos daca tipul operatiei este remove
                        self.marketplace.remove_from_cart(cart_id, product)

            self.marketplace.place_order(cart_id)
