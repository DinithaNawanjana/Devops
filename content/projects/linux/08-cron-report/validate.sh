#!/bin/sh
cd /root 2>/dev/null || cd / 2>/dev/null
fail=0
[ -x ./genreport.sh ] || { echo "STEP:genreport.sh exists:FAIL:create executable /root/genreport.sh"; exit 1; }
echo "STEP:genreport.sh exists:PASS"
./genreport.sh >/dev/null 2>&1
rep=$(ls reports/report-*.txt 2>/dev/null | head -1)
if [ -n "$rep" ] && grep -q "Files: 3" "$rep"; then echo "STEP:dated report says Files: 3:PASS"; else echo "STEP:dated report says Files: 3:FAIL:report-<date>.txt should contain 'Files: 3'"; fail=1; fi
if grep -Eq '^[0-9*/,-]+ +[0-9*/,-]+ +[0-9*/,-]+ +[0-9*/,-]+ +[0-9*/,-]+ .*genreport' reports/crontab.txt 2>/dev/null; then
  echo "STEP:valid cron line for genreport:PASS"; else echo "STEP:valid cron line for genreport:FAIL:crontab.txt needs a 5-field schedule + genreport.sh"; fail=1; fi
exit $fail
