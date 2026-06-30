# Your Task

Work in your home directory (`/root`). Complete each step, then click **Check**.

1. **Create a project tree**

   Make the nested directory structure `project/src` and `project/docs`.

   ```bash
   mkdir -p project/src project/docs
   ```

2. **Create a README**

   Inside `project/`, create a file `README.md` containing the word `hello`.

   ```bash
   echo "hello" > project/README.md
   ```

3. **Create and mark a script executable**

   Create `project/src/run.sh`, then make it executable for the owner so its
   mode is `755`.

   ```bash
   echo '#!/bin/bash' > project/src/run.sh
   chmod 755 project/src/run.sh
   ```

4. **Restrict a secrets file**

   Create `project/secret.txt` and set its permissions so only the owner can
   read and write it (mode `600`).

When all four steps pass, you've earned 100 XP. 🎉
