# -*- coding: utf-8 -*-
import random


first_primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                     31, 37, 41, 43, 47, 53, 59, 61, 67,
                     71, 73, 79, 83, 89, 97, 101, 103,
                     107, 109, 113, 127, 131, 137, 139,
                     149, 151, 157, 163, 167, 173, 179,
                     181, 191, 193, 197, 199, 211, 223,
                     227, 229, 233, 239, 241, 251, 257,
                     263, 269, 271, 277, 281, 283, 293,
                     307, 311, 313, 317, 331, 337, 347, 349]


def random_odd(n_bits: int) -> int:
    """
    Generates random odd number in range [2 ^ (n_bits - 1), 2 ^ (n_bits) - 1]
    Odd number probably is prime number
    """
    assert n_bits > 0
    value = random.getrandbits(n_bits)
    value |= (1 << n_bits) | 1
    return value


def is_low_level_test_passed(value: int) -> bool:
    """
    Returns True if low level tests has been passed
    """
    for prime in first_primes_list:
        if prime**2 > value:
            break

        if value % prime == 0:
            return False

    return True


TESTS_COUNT = 20


def is_composite_value(value: int, a: int, ec: int, max_pow_2: int) -> bool:
    """
    Returns True if value is composite. otherwise false
    """
    b0 = pow(a, ec, value)

    if b0 == 1 or b0 == value - 1:
        return False
    b_prev = b0

    for _ in range(max_pow_2):
        bi = pow(b_prev, 2, value)

        if bi == 1:
            break
        elif bi == value - 1:
            return False

        b_prev = bi

    return True


def is_miller_rabin_passed(value: int) -> bool:
    """
    Checks is value a prime number with Fermat theorem
    and Miller Rabin algorithm
    """
    ec = value - 1
    max_pow_2 = 0
    while ec % 2 == 0:
        ec >>= 1
        max_pow_2 += 1

    for i in range(TESTS_COUNT):
        a = random.randint(2, ec)

        if is_composite_value(value, a, ec, max_pow_2):
            return False

    return True


def random_prime(n_bits: int) -> int:
    """
    Returns random primary number
    """
    while True:
        possible_prime = random_odd(n_bits)

        if (
                is_low_level_test_passed(possible_prime) and
                is_miller_rabin_passed(possible_prime)
        ):
            return possible_prime
