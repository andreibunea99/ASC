"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
from threading import Lock, currentThread


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    queue_size_per_producer = 0
    total_producers = 0  # numarul total de producers
    total_carts = 0  # numarul total de cart-uri
    producer_buffers = []  # bufferul cu produse generate de fiecare produser
    consumer_carts = []  # cart-ul fiecarul consumer
    producer_lock = None
    consumer_lock = None
    add_lock = None
    checkout_lock = None
    cart_lock = None

    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer
        self.producer_lock = Lock()
        self.consumer_lock = Lock()
        self.add_lock = Lock()
        self.checkout_lock = Lock()
        self.cart_lock = Lock()

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        # adaug o lista noua care sa reprezinte bufferului producerului inregistrat
        self.producer_buffers.append([])
        # evit posibilitatea de a atribui acelasi id pentru mai multi producatori
        with self.producer_lock:
            my_id = self.total_producers
            self.total_producers += 1
        return my_id

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
        # daca dimensiunea permite, adaug produsul in bufferul producatorului
        self.producer_buffers[producer_id].append(product)
        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        with self.cart_lock:  # evit atribuirea aceluiasi cart pentru mai multi consumatori
            my_id = self.total_carts
            self.consumer_carts.append([])
            self.total_carts += 1
        return my_id

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
        with self.add_lock:  # evit adaugarea aceluiasi produs de catre mai multi consumatori
            # caut primul producator care are acel produs
            for i in range(len(self.producer_buffers)):
                if product in self.producer_buffers[i]:
                    producer = i
                    break

            # daca a fost gasit un producator, adaug produsul in cos
            if producer != -1:
                # adaug o lista de tipul [produs, producer] pentru a retine
                # producatorul de la care am luat produsul
                self.consumer_carts[cart_id].append([product, producer])
                self.producer_buffers[producer].remove(product)
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
        producer = -1
        # caut in cart o pereche produs - producer si retin producatorul
        for entry in self.consumer_carts[cart_id]:
            if entry[0] == product:
                producer = entry[1]
                break

        if producer == -1:
            return

        # daca am gasit o astfel pereche, scot din cart si pun produsul in bufferul producatorului
        self.consumer_carts[cart_id].remove([product, producer])
        self.producer_buffers[producer].append(product)

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        # scot intr-o ista toate produsele din cart
        # produsele se afla pe pozitia 0 din perechile [produs, producator] din cart
        output_list = []
        for pair in self.consumer_carts[cart_id]:
            output_list.append(pair[0])
        for product in output_list:
            with self.checkout_lock:
                print(currentThread().getName() + " bought " + str(product))
        return output_list
