"""Service for checking updates from GitHub releases."""

import requests
from packaging import version as pkg_version


class UpdateService:
    """Check for new versions from GitHub API."""

    REPO = "wilkinbarban/normalizador-audio"
    API_URL = f"https://api.github.com/repos/{REPO}/releases/latest"
    GITHUB_RELEASE_URL = f"https://github.com/{REPO}/releases/latest"

    @staticmethod
    def get_latest_version() -> dict | None:
        """
        Fetch latest release info from GitHub API.

        Returns:
            dict with keys: tag_name, name, html_url, or None if error.
        """
        try:
            response = requests.get(UpdateService.API_URL, timeout=5)
            response.raise_for_status()
            data = response.json()

            return {
                "tag_name": data.get("tag_name", ""),
                "name": data.get("name", ""),
                "url": data.get("html_url", UpdateService.GITHUB_RELEASE_URL),
            }
        except (requests.RequestException, ValueError):
            # Network error or JSON parse error
            return None

    @staticmethod
    def compare_versions(current: str, latest: str) -> bool:
        """
        Check if latest version is newer than current.

        Args:
            current: Current version string (e.g., "1.0.0")
            latest: Latest version string (e.g., "1.0.1")

        Returns:
            True if latest > current, False otherwise.
        """
        try:
            # Handle tags like "v1.0.0" by stripping 'v'
            current_clean = current.lstrip("v")
            latest_clean = latest.lstrip("v")
            return pkg_version.parse(latest_clean) > pkg_version.parse(current_clean)
        except Exception:
            return False

    @staticmethod
    def should_update(current_version: str) -> tuple[bool, dict | None]:
        """
        Check if update is available.

        Args:
            current_version: Current app version.

        Returns:
            Tuple of (update_available, release_info).
            release_info contains: tag_name, name, url.
        """
        release_info = UpdateService.get_latest_version()
        if not release_info:
            return False, None

        if UpdateService.compare_versions(current_version, release_info["tag_name"]):
            return True, release_info

        return False, None
