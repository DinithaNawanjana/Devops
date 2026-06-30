# Docker-in-Docker sandbox for the Docker track.
#   docker build -t lab-docker:latest lab-images/lab-docker
#
# Runs an isolated dockerd inside the sandbox so learners can build/run
# containers without touching the host engine. Requires the sandbox to run
# with elevated privileges — see README §Security (the manager's cap_drop /
# no-new-privileges defaults must be relaxed for this image, e.g. via Sysbox
# or a privileged override).
FROM docker:27-dind

RUN apk add --no-cache bash curl wget vim nano less procps

WORKDIR /root

# entrypoint.sh starts dockerd in the background, then idles.
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["sleep", "infinity"]
