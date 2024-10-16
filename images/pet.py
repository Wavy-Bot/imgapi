from petpetgif import petpet

from fastapi import UploadFile

from io import BytesIO


def pet(av: bytes) -> BytesIO:
    """
    This function adds a pet overlay to the uploaded image.
    Yes, I am using a library for this. Sue me.
    :param av: The uploaded image
    :return: The image with the pet overlay
    """
    # Create BytesIO stream from contents
    image_stream = BytesIO(av)

    # Create a BytesIO stream for the output
    output = BytesIO()

    # Make the gif
    petpet.make(image_stream, output)
    output.seek(0)

    return output
