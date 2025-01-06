# Single Digit Combinations

This is a number puzzle I saw in a newspaper when I was a kid.
I do not know the official name of the game,
but its objective is to find the _smallest expression_ that produces a value using a single digit.


## Background

It is easier to understand this by looking at a problem.
Say we are asked to find combinations to produce the number `75`.

A simple case is using the digit `3`.

1. The number `75` is divisible by `3`, so we would think `3 * 25`, except we cannot use `25`.
1. So now we need to look for an expression that evaluates to `25`. A good option could be `27 - 2`.
1. The first term is simply `3 ^ 3`.
1. Now we need an expression that produces `2` in terms of `3`. We could use `3 - 1`.
1. And use `3 / 3` to produce that `1`.

Or we can simply say $(3 \times (3^3 - (3 - \frac{3}{3}))$.

We can then try other digits, `6` for example.
Here we can start with `72 + 3`.
The first term is simple, but getting that `3` is a bit tricky.
Eventually we end up with something like $(6 \times (6 + 6) + \frac{6 \times 6}{6 + 6})$.


### Scoring

The cost of a solution is determined by the number of times the digit is used.
So the solution $(3 \times (3^3 - (3 - \frac{3}{3}))$, has a cost of `6`.
Likewise the solution using the digit `6` has a cost of `7`.

We can improve both solutions.
One solution for the digit `3` would be $(3 \times 3^3 - 3!)$, which is `81 - 6`, and has a cost of `4`.
And an improvement on the solution with the digit `6` could be $(\frac{666}{6} - 6 \times 6)$, with a cost of `6`.


### Operations

The operations allowed also impact the difficulty of the game.
Allowing only additions is the most limiting case.
For example, if the digit `5` is available, we can only do:

```
10 = 5 + 5
15 = 5 + 5 + 5
20 = 5 + 5 + 5 + 5
25 = 5 + 5 + 5 + 5 + 5
...
```

Expanding the operations to allow multiplication results in smaller solutions:

```
25 = 5 * 5
```

And adding subtraction and division can both generate smaller solutions, and generate numbers we couldn't produce before.

```
20 = 5 * 5 - 5
4 = 5 - 5/5
```

The game gets more interesting as we increase the number of operations.
For example adding exponentiation (`^`), factorial (`!`) and square root (`sqrt`) helps reduce the cost of some combinations.



## Solver

For the solver, I am using monotonic operations at first.
That allows us to have a _directed acyclic graph_ (DAG).

## Usage

The script `calculate.py` is a CLI to the solver.
The syntax is:

```txt
calculate.py [OPTIONS]

Options:
  --digit <number>          digit to use for expressions
  --upper <number>          largest number to report
  --steps <number>          number of iterations
  --full                    show combinations in terms of the digit, otherwise use expanded values
  --format <text | json>    format for the output
  --help                    this information
```


```sh
python3 calculate.py --digit 3
```

木
