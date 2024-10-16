from PIL import Image, ImageSequence

from fastapi import UploadFile

from io import BytesIO


def pet(av: bytes) -> BytesIO:
    """
    This function adds a pet overlay to the uploaded image.
    :param av: The uploaded image
    :return: The image with the pet overlay
    """
    # Temp
    raise NotImplementedError

    # TODO(Robert): Fix this mess because for some reason
    # the GIF is still getting overlapped by itself
    # even though there is a blank composite frame

    # Create BytesIO stream from contents
    image_stream = BytesIO(av)

    # Open the avatar and overlay images
    avatar = Image.open(image_stream).convert("RGBA")
    overlay = Image.open("templates/pet/overlay.gif")

    # Resize avatar
    # TODO(Robert): Make avatar size dynamic
    x, y = overlay.size
    avatar = avatar.resize((80, 80))

    # Get the size of the avatar
    av_x, av_y = avatar.size

    # Calculate the position to paste the avatar
    position = (x - av_x, y - av_y)

    frames = []
    for frame in ImageSequence.Iterator(overlay):
        frame = frame.convert("RGBA")

        # Create a new blank frame
        composite_frame = Image.new("RGBA", (x, y), (0, 0, 0, 0))

        # Paste the images onto the blank frame
        composite_frame.paste(avatar, position, avatar)
        composite_frame.paste(frame, (0, 0), frame)

        frames.append(composite_frame)

    output = BytesIO()
    frames[0].save(
        output,
        save_all=True,
        append_images=frames[1:],
        loop=0,
        duration=overlay.info["duration"],
        format="GIF",
    )
    output.seek(0)

    return output
