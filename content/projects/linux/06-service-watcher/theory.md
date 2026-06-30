# Project: Service Health Watcher

A watchdog that checks whether a service is up and restarts it if not. Here the
"service" is represented by the marker file `/root/run/service.up`. Practises
existence checks, recreating state, and event logging.
