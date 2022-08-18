# You will need some import statements up here.
import random
from math import sqrt
from multiprocessing import Pool

from timeit import timeit

# Programming Assignment 5
#
# Student Name: Samuel Emmett
#
# What to submit:
# (a) This montecarlo.py file
#     As always, you are not allowed to change the names of
#     py files I've given you, functions, parameters, etc.
# (b) A text file with the output from when you run your
#     generateTable and time functions.  One text file with
#     both output tables is fine.
#
# 1) Implement the function piMonteCarlo to estimate
#    the value of pi using Monte Carlo simulation.
#    See the details of how to do this in Blackboard,
#    which shows the sum that you need to compute.
#    You will need to import the random module.  Take a
#    look at the documentation of the random module to find
#    the function that generates random floating-point
#    values in the interval [0.0, 1.0).
#
# 2) Implement a parallel version of this in the function
#    piParallelMonteCarlo.  The second parameter, processes,
#    indicates how many processes to use.  You should use
#    a Pool (see the parallel examples for the import that you
#    will need).  The easiest ways to do this is to either use
#    the apply_async method of the Pool class or the map method
#    of the Pool class.
#
#    Hint 1: If you use apply_async, you'll start by determining
#           how many samples per process, which you can compute
#           from n and p.  You would then call apply_async p times
#           to have p processes call piMonteCarlo (the sequential
#           version) using the number of samples necessary to spread
#           the n samples across p processes.  Once you call apply_async
#           p times (make sure you store the Future objects that those
#           calls return in a list),
#           you'll call get() on each of those Future objects, and average
#           the p results.
#
#    Hint 2: If you want to use Pool.map, then start the same
#           way by determining how many samples to use for each
#           process.  Create your Pool with p processes.  Generate
#           a list of length p where the elements are the numbers of
#           samples for each process, which should sum to n.
#           Call pool.map (assuming your Pool is named pool) to map
#           your sequential piMonteCarlo to that list.
#           When pool.map returns, compute the average of the p
#           results and return it.
#
#    Hint 3: Make sure you use a with block for your Pool (see examples
#           in video and corresponding sourcecode) to ensure the Pool
#           is closed.
#
# 3) Implement the generateTable function as specified below.
#
# 4) Implement the time function as specified below.
#
# 5) Run your generateTable and time functions from the shell
#    and save the output to a textfile.
#
# 6) Are the results what you expected to see?  If so, why?
#    If not, why do you think your results are different
#    then you expected?  You can just answer in a comment.
#
"""
    ANSWER: The output is more or less what I expected. 
    I was fairly surprised though at just how long it took
    for multiple processes to actually perform better than 
    if the algorithm were to just run sequentially.
    
"""
# 7) Submit the .py file and the textfile with the output.

def piMonteCarlo(n) :
    """Computes and returns an estimation of pi
    using Monte Carlo simulation.

    Keyword arguments:
    n - The number of samples.
    """

    Ui = []
    pi = 0

    for i in range (n) :
        Ui.append(random.uniform(0.0, 1.0))
        pre = (4/n) * sqrt(1-Ui[i]**2)
        pi = pi + pre
    return pi

def piParallelMonteCarlo(n, p=4) :
    """Computes and returns an estimation of pi
    using a parallel Monte Carlo simulation.

    Keyword arguments:
    n - The total number of samples.
    p - The number of processes to use.
    """
    # You can distribute the work across p
    # processes by having each process
    # call the sequential version, where
    # those calls divide the n samples across
    # the p calls.
    # Once those calls return, simply average
    # the p partial results and return that average.

    proc1 = n // p
    proc2 = proc1 + (n % p)
    with Pool(p) as pool:
        vals = [proc2 if i == p - 1 else proc1 for i in range(p)]
        total = sum(pool.map(piMonteCarlo, vals))
        return total / p


def generateTable() :
    """This function should generate and print a table
    of results to demonstrate that both versions
    compute increasingly accurate estimations of pi
    as n is increased.  It should use the following
    values of n = {12, 24, 48, ..., 12582912}. That is,
    the first value of n is 12, and then each subsequent
    n is 2 times the previous.  The reason for starting at 12
    is so that n is always divisible by 1, 2, 3, and 4.
    The first
    column should be n, the second column should
    be the result of calling piMonteCarlo(n), and you
    should then have 4 more columns for the parallel
    version, but with 1, 2, 3, and 4 processes in the Pool."""

    print('{0:^10}\t{1:^10}\t{2:^10}\t{3:^10}\t{4:^10}\t{5:^10}'.format("n", "Sequential", "Parallel 1", "Parallel 2", "Parallel 3", "Parallel 4"))
    n = 12
    nmax = 12582912
    while n <= nmax:
        seq = piMonteCarlo(n)
        p1 = piParallelMonteCarlo(n, 1)
        p2 = piParallelMonteCarlo(n, 2)
        p3 = piParallelMonteCarlo(n, 3)
        p4 = piParallelMonteCarlo(n, 4)
        print('{0:^10}\t{1:.8f}\t{2:.8f}\t{3:.8f}\t{4:.8f}\t{5:.8f}'.format(n, seq, p1, p2, p3, p4))
        n = n*2

def time() :
    """This function should generate a table of runtimes
    using timeit.  Use the same columns and values of
    n as in the generateTable() function.  When you use timeit
    for this, pass number=1 (because the high n values will be slow)."""

    print('{0:^10}\t{1:^10}\t{2:^10}\t{3:^10}\t{4:^10}\t{5:^10}'.format("n", "Sequential", "Parallel 1", "Parallel 2", "Parallel 3", "Parallel 4"))
    n = 12
    num = 1
    nmax = 12582912
    while n <= nmax:
        t_s = timeit(lambda : piMonteCarlo(n), number=num) / num
        t_p1 = timeit(lambda : piParallelMonteCarlo(n, 1), number=num) / num
        t_p2 = timeit(lambda: piParallelMonteCarlo(n, 2), number=num) / num
        t_p3 = timeit(lambda: piParallelMonteCarlo(n, 3), number=num) / num
        t_p4 = timeit(lambda: piParallelMonteCarlo(n, 4), number=num) / num
        print('{0:^10}\t{1:.8f}\t{2:.8f}\t{3:.8f}\t{4:.8f}\t{5:.8f}'.format(n, t_s, t_p1, t_p2, t_p3, t_p4))
        n = n * 2

if __name__ == "__main__" :

    generateTable()
    print()
    time()