# Your Task

Write `/root/fizzbuzz.sh` — the classic FizzBuzz, parameterized.

Requirements:

1. **Executable** `/root/fizzbuzz.sh` (mode `755`, `#!/bin/bash` shebang).

2. **Takes a number `N`** as its first argument and prints the numbers
   `1` through `N`, one per line, **except**:
   - multiples of 3 → print `fizz`
   - multiples of 5 → print `buzz`
   - multiples of both 3 and 5 → print `fizzbuzz`

   So `./fizzbuzz.sh 15` prints: `1 2 fizz 4 buzz fizz 7 8 fizz buzz 11 fizz 13 14 fizzbuzz` (each on its own line).

3. **Use a function** named `classify` that decides what to print for a given
   number (keep your loop clean).

4. **No-argument guard** — running `./fizzbuzz.sh` with no argument must print a
   message containing `usage` and exit with a **non-zero** status.

Test with `./fizzbuzz.sh 15`, then click **Check**.
