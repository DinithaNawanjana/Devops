# Project: Scheduled Report Generator

Generate a dated report and define the cron schedule that would run it. A cron
line is five time fields plus a command:

```
0 6 * * *  /root/genreport.sh    # every day at 06:00
```
