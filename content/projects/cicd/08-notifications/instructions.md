# Project Tasks

Create `/root/repo/.github/workflows/notify.yml` with a step that posts a
**Slack or Discord** notification using a **webhook from `secrets`**
(e.g. `${{ secrets.SLACK_WEBHOOK }}`). Use `if: always()` so it fires on
success or failure.

Click **Check**.
