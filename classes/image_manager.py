import pygame


class ImageManager:
  _instance = None
  
  def __new__(cls):
    if cls._instance is None:
      cls._instance = super(ImageManager, cls).__new__(cls)
      cls._instance.images = {}
    return cls._instance
  
  def load_image(self, image_path):
    if image_path not in self.images:
      self.images[image_path] = pygame.image.load(image_path)
    return self.images[image_path]
