from PIL import Image

from fastapi import UploadFile

from io import BytesIO


def jail(av: bytes) -> BytesIO:
    """
    This function adds a jail overlay to the uploaded image.
    :param av: The uploaded image
    :return: The image with the jail overlay
    """
    # Create BytesIO stream from contents
    image_stream = BytesIO(av)

    # Open the avatar and overlay images
    avatar = Image.open(image_stream).convert("RGBA")
    overlay = Image.open("templates/jail/overlay.png").convert("RGBA")

    # Resize overlay to the same size as the avatar
    x, y = avatar.size
    overlay = overlay.resize((x, y))

    # Paste the overlay on the avatar and return the image
    avatar.paste(overlay, (0, 0), overlay)

    # Save the image to a BytesIO stream
    output = BytesIO()
    avatar.save(output, format="PNG")
    output.seek(0)

    return output
