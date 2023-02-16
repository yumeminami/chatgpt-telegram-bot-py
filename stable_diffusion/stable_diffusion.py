import replicate
import os
import io
from stability_sdk import client
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation


def predict(prompt):
    model = replicate.models.get("stability-ai/stable-diffusion")
    version = model.versions.get(
        "f178fa7a1ae43a9a9af01b833b9d2ecf97b1bcb0acfd2dc5dd04895e042863f1"
    )
    inputs = {
        # Input prompt
        "prompt": prompt,
        # Specify things to not see in the output
        # 'negative_prompt': ...,
        # Width of output image. Maximum size is 1024x768 or 768x1024 because
        # of memory limits
        "width": 768,
        # Height of output image. Maximum size is 1024x768 or 768x1024 because
        # of memory limits
        "height": 768,
        # Prompt strength when using init image. 1.0 corresponds to full
        # destruction of information in init image
        "prompt_strength": "0.8",
        # Number of images to output.
        # Range: 1 to 4
        "num_outputs": 1,
        # Number of denoising steps
        # Range: 1 to 500
        "num_inference_steps": 50,
        # Scale for classifier-free guidance
        # Range: 1 to 20
        "guidance_scale": 7.5,
        # Choose a scheduler.
        "scheduler": "DPMSolverMultistep",
        # Random seed. Leave blank to randomize the seed
        # 'seed': ...,
    }
    output = version.predict(**inputs)
    return output


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
                img.save("image.png")
    return answers
