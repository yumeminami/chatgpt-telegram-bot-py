import os
import io
import uuid
from PIL import Image

# from stability_sdk import client

from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation


def generate(prompt):
    stability_api = client.StabilityInference(
        key=os.environ["STABILITY_KEY"],
        verbose=True,
    )
    answers = stability_api.generate(prompt, samples=1)
    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))
                img_path = uuid.uuid4().hex + ".png"
                img.save(img_path)
                return img_path
    return None
