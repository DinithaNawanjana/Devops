# Project Tasks

Write `/root/usermgr.sh` operating on `/root/users.db` (created empty by setup).
Support these subcommands:

1. **`add <user> <fullname>`** — append `user:fullname` **only if the user
   doesn't already exist** (idempotent).
2. **`del <user>`** — remove that user's line.
3. **`list`** — print the database.
4. **`count`** — print the number of users (just the number).

Example: `./usermgr.sh add alice "Alice A"`. Then click **Check**.
