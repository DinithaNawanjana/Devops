# Project: Multi-stage Pipeline

Real pipelines have ordered jobs. In Actions, `needs:` makes one job wait for
another — `build` → `test` → `deploy`.
