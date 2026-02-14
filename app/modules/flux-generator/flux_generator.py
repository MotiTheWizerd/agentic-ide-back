import time
import requests


class FluxGenerator:
    BASE_URL = "https://api.fireworks.ai/inference/v1/workflows"

    def __init__(self, api_key: str, model: str = "flux-kontext-pro"):
        self.model = model
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def generate(
        self,
        prompt: str,
        output_path: str = "output.png",
        aspect_ratio: str = "1:1",
        output_format: str = "png",
        safety_tolerance: int = 6,
        poll_interval: float = 2,
    ) -> str:
        """Generate an image from a text prompt and save it to disk.

        Returns the output file path.
        """
        url = f"{self.BASE_URL}/accounts/fireworks/models/{self.model}"

        # Submit request
        resp = requests.post(
            url,
            headers=self.headers,
            json={
                "prompt": prompt,
                "output_format": output_format,
                "aspect_ratio": aspect_ratio,
                "safety_tolerance": safety_tolerance,
            },
        )
        if resp.status_code != 200:
            raise RuntimeError(f"Submit failed ({resp.status_code}): {resp.text}")

        request_id = resp.json()["request_id"]

        # Poll for result
        while True:
            result = requests.post(
                f"{url}/get_result",
                headers=self.headers,
                json={"id": request_id},
            )
            data = result.json()
            status = data.get("status")

            if status == "Ready":
                image_url = data["result"]["sample"]
                img_resp = requests.get(image_url)
                if img_resp.status_code != 200:
                    raise RuntimeError(f"Download failed ({img_resp.status_code})")
                with open(output_path, "wb") as f:
                    f.write(img_resp.content)
                return output_path

            if status in ("Error", "Content Moderated", "Request Moderated"):
                raise RuntimeError(f"Generation failed: {status} - {data}")

            time.sleep(poll_interval)
