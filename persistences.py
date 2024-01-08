from ripser import Rips
import numpy as np
import persim
import matplotlib.pyplot as plt
from utils import read_xyz_file
from persim import PersistenceImager

class RipsComplex:
    def __init__(self, pt_cloud):
      self.diag = self._produce_diag(pt_cloud)

    def _produce_diag(self, data):
      rips = Rips(maxdim = 2, verbose = False).fit_transform(data)
      return rips
    
class PersistentLandscapes:
  def __init__(self, rips_complex, resolution:int = 100):
    self._resolution = resolution
    self._diags = rips_complex.diag
    self.landscapes = {hm: self._get_landscapes(hm) for hm in range(len(self._diags))}

  def _get_landscapes(self, hom_deg: int):
    temp_data = np.copy(self._diags[hom_deg])
    temp_data = temp_data[np.isfinite(temp_data).all(axis=1), :]
    start, stop = np.floor(np.min(temp_data[:, 0])), np.ceil(np.max(temp_data[:, 1]))
    landscape = persim.landscapes.PersistenceLandscaper(hom_deg = hom_deg, 
                                                        start = start, 
                                                        stop = stop, 
                                                        num_steps = self._resolution,
                                                        flatten = True)
    return landscape.fit_transform(self._diags)
  
  def featurize(self):
    # implement method from featurization paper
    pass

  def plot(self, hom_class: int = 0):
    plt.plot(self.landscapes[hom_class])
    plt.title("Landscape")
    plt.ylim([0, 1])
    plt.legend()
    plt.show()

class PersistentImage:
  def __init__(self, rips_complex, pixel_size:int = 0.1):
    self._pixel_size = pixel_size
    self._diags = rips_complex.diag
    self.images = {i: img for i, img in enumerate(self._get_images())}

  def _get_images(self):
    data = [rcd[np.isfinite(rcd).all(axis=1), :] for rcd in self._diags]
    self.pimgr = PersistenceImager(pixel_size=self._pixel_size)
    return self.pimgr.fit_transform(data)
  
  def featurize(self):
    # add featurization process from paper
    pass
    
  def plot(self):
    plt.figure(figsize=(15,7.5))
    for i, (key, img) in enumerate(self.images.items()):
      ax = plt.subplot(240+i+1)
      self.pimgr.plot_image(img, ax)
      ax.title.set_text(f"Hom Class {i}")

    plt.show()