# ported in large part from Skyth's MikuMikuLibrary
from enum import Enum

class TextureFormat(Enum):
  Unknown = -1,
  A8 = 0,
  RGB8 = 1,
  RGBA8 = 2,
  RGB5 = 3,
  RGB5A1 = 4,
  RGBA4 = 5,
  DXT1 = 6,
  DXT1a = 7,
  DXT3 = 8,
  DXT5 = 9,
  ATI1 = 10,
  ATI2 = 11,
  L8 = 12,
  L8A8 = 13

class TextureFormatUtilities():
  def is_block_compressed(format: TextureFormat):
    return TextureFormat.DXT1 <= format <= TextureFormat.ATI2

  def has_alpha(format: TextureFormat):
    return format in {TextureFormat.A8, TextureFormat.RGBA8, TextureFormat.RGB5A1, TextureFormat.RGBA4, 
                    TextureFormat.DXT1a, TextureFormat.DXT3, TextureFormat.DXT5}

  def get_block_size(format: TextureFormat):
    match format:
      case TextureFormat.DXT1 | TextureFormat.DXT1a | TextureFormat.ATI1:
        return 8
      case TextureFormat.DXT3 | TextureFormat.DXT5 | TextureFormat.ATI2:
        return 16

  def get_data_size(width, height, format: TextureFormat):
    match format:
      case TextureFormat.A8 | TextureFormat.L8:
        return width * height
      case TextureFormat.RGB8:
        return width * height * 3
      case TextureFormat.RGBA8:
        return width * height * 4
      case TextureFormat.RGB5 | TextureFormat.RGB5A1 | TextureFormat.RGBA4 | TextureFormat.L8A8:
        return width * height * 2
      case _:
        return max(1, (width + 3) * max(1, (height + 3) / 4))

class SubTexture():
  pass

class Texture():
  def __init__(self):
    pass
