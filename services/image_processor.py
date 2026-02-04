from PIL import Image
import io
import rembg
import os

class ImageProcessor:
    @staticmethod
    def load_image(path: str) -> Image.Image:
        """Loads an image from the specified path."""
        try:
            return Image.open(path)
        except Exception as e:
            raise RuntimeError(f"Failed to load image: {e}")

    @staticmethod
    def save_image(image: Image.Image, path: str, format: str = None):
        """Saves the image to the specified path."""
        try:
            if format:
                # Handle simpler formats/modes if necessary, but PIL usually handles it
                if format.upper() == "JPEG" or format.upper() == "JPG":
                     if image.mode in ("RGBA", "P"):
                        image = image.convert("RGB")

            image.save(path, format=format)
        except Exception as e:
            raise RuntimeError(f"Failed to save image: {e}")

    @staticmethod
    def convert_format(image: Image.Image, target_format: str) -> Image.Image:
        """Converts image to target format (returning the image object, mostly checks mode compatibility)."""
        target_format = target_format.upper()
        if target_format in ["JPEG", "JPG"]:
            if image.mode in ("RGBA", "P"):
                return image.convert("RGB")
        return image

    @staticmethod
    def remove_background(image: Image.Image) -> Image.Image:
        """Removes the background from the image using rembg."""
        try:
            return rembg.remove(image)
        except Exception as e:
            raise RuntimeError(f"Failed to remove background: {e}")
