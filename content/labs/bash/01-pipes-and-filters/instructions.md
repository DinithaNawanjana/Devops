# Your Task

We've placed a sample web log at `/root/access.log`. Analyze it using pipes
and filters. Work in `/root`.

1. **Count total requests**

   Write the total number of lines in `access.log` to `/root/total.txt`.

   ```bash
   wc -l < access.log > total.txt
   ```

2. **Count errors**

   Count how many lines contain the string `ERROR` and write just the number
   to `/root/errors.txt`.

3. **Top IP addresses**

   The first field of each line is an IP address. Produce the **top 3** IPs by
   request count into `/root/top_ips.txt`, one `count ip` pair per line, most
   frequent first.

   _Hint:_ `awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -3`

Click **Check** when done.
