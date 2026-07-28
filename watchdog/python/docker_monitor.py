"""
docker_monitor.py — Checks the status of monitored containers.
"""
import logging
import docker

logger = logging.getLogger("watchdog.monitor")


def get_client() -> docker.DockerClient:
    return docker.from_env()


def check_container_status(client: docker.DockerClient, container_name: str):
    """
    Returns the current container status ('running', 'exited', 'restarting', etc.)
    or None if the container does not exist.
    """
    try:
        container = client.containers.get(container_name)
        return container.status
    except docker.errors.NotFound:
        logger.warning("Container %s not found", container_name)
        return None
    except docker.errors.APIError as e:
        logger.error("Error checking status of %s: %s", container_name, e)
        return None


def is_healthy(client: docker.DockerClient, container_name: str) -> bool:
    """
    True if the container is 'running'. If it has a healthcheck defined,
    also requires the health status to not be 'unhealthy'.
    """
    try:
        container = client.containers.get(container_name)
        if container.status != "running":
            return False

        health = container.attrs.get("State", {}).get("Health", {}).get("Status")
        if health and health == "unhealthy":
            return False

        return True
    except docker.errors.NotFound:
        return False
    except docker.errors.APIError as e:
        logger.error("Error checking health of %s: %s", container_name, e)
        return False
