"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    queue_size_per_producer = 0
    total_producers = 0
    total_carts = 0
    producer_buffers = []
    consumer_carts = []

    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer
        pass

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        self.total_producers += 1
        return self.total_producers - 1

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        if len(self.producer_buffers[producer_id]) == self.queue_size_per_producer:
            return False
        self.producer_buffers[producer_id].append(product)
        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        self.consumer_carts[self.total_carts] = {}
        self.total_carts += 1
        return self.total_carts - 1

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        producer = -1
        for i in range(len(self.producer_buffers)):
            if product in self.producer_buffers[i]:
                producer = i
                break
        if producer != -1:
            self.consumer_carts[cart_id][product] = producer
            return True
        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        producer = self.consumer_carts[cart_id][product]
        self.consumer_carts[cart_id].pop(product)
        self.producer_buffers[producer].append(product)

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        products = self.consumer_carts[cart_id].keys()
        return products
