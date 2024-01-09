from ripser import Rips
import numpy as np
import persim
import matplotlib.pyplot as plt
from utils import read_xyz_file
from persim import PersistenceImager
from persim.landscapes import PersistenceLandscaper

class RipsComplex:
    def __init__(self, pt_cloud):
      self.diag = self._produce_diag(pt_cloud)

    def _produce_diag(self, data):
      rips = Rips(maxdim = 2, verbose = False).fit_transform(data)
      return rips
    
class PersistentLandscapes:
  def __init__(self, rips_complex, resolution:int = 20):
    self._resolution = resolution
    self._diags = rips_complex.diag
    self._hm_classes = len(self._diags)
    self.landscapes = self._get_landscapes()
    self.features = self._get_features()

  def _get_landscapes(self):
    landscapes = {}
    for hm in range(self._hm_classes):
      temp_data = np.copy(self._diags[hm])
      temp_data = temp_data[np.isfinite(temp_data).all(axis=1), :]
      start, stop = np.floor(np.min(temp_data[:, 0])), np.ceil(np.max(temp_data[:, 1]))
      landscape = PersistenceLandscaper(hom_deg = hm,
                                        start = start, 
                                        stop = stop, 
                                        num_steps = self._resolution,
                                        flatten = False)
      landscapes[hm] = landscape.fit_transform(self._diags)
    return landscapes
  
  def _get_features(self):
    features = {}
    for hom_class, landscapes in self.landscapes.items():
      feature_vectors = []
      for t in landscapes:
          feats = []
          for i in range(len(t)-1):

              # if point is zero and next point is larger, the function is increasing
              if t[i] == 0 and t[i] < t[i+1]:
                  feats.append(i)

              # if point is the peak and nonzero
              if t[i] >= t[i+1] and t[i-1] < t[i]:
                  feats.append(i)

              # if point is zero and previous is larger, function is decreasing
              if t[i] == 0 and t[i] < t[i-1]:
                  feats.append(i)
          feature_vectors.append(feats)
      features[hom_class] = np.array(feature_vectors)
    return features

  def plot(self, hom_class: int = 0):
    plt.plot(self.landscapes[hom_class])
    plt.title("Landscape")
    plt.ylim([0, 1])
    plt.legend()
    plt.show()

class PersistentImage:
  def __init__(self, rips_complex, pixel_size:int = 0.1, image_size: tuple[int, int] = (20, 20)):
    self._pixel_size = pixel_size
    self._diags = rips_complex.diag
    self._hm_classes = len(self._diags)
    self.nx, self.ny = image_size
    self._xs = np.arange(0, self.nx)
    self._ys = np.arange(0, self.ny)
    self.images = self._get_images()

  def _get_images(self):
    images = {}
    for hm in range(self._hm_classes):
      hm_data = self._diags[hm]

      # convert to persistence lifetime
      hm_data[:, 1] -= hm_data[:, 0]

      # sum the smoothing kernel times weighting function
      pers_surface = []
      num_rows = hm_data.shape[0]
      for i in range(num_rows):
        b, p = hm_data[i, 0], hm_data[i,1]
        temp = np.zeros((self.nx, self.ny))
        for x in self._xs:
          for y in self._ys:
            temp[x,y] = self._gaussian_kernel(x,y, b, p) * self._weighting(b, p)
        pers_surface.append(temp)
      pers_surface = np.sum(np.array(pers_surface), axis = 0)

      # add integration
      
      images[hm] = pers_surface
    return images
  
  def _gaussian_kernel(self, x, y, b, p, sigma: float = 1):
    return (1/(2 * np.pi * sigma ** 2)) * np.exp(-1 * ((x - b)**2 + (y-p)**2)/(2*sigma**2))
  
  def _weighting(self, b, p):
    if p <= 0:
      return 0
    elif 0 < p < b:
      return p/b 
    else:
      return 1

  def featurize(self):
    return {hm: self.images[hm].flatten() for hm in range(self._hm_classes)}
    
  def plot(self, hm_class:int = 0):
    # FIX THIS
    hm_images = self.images[hm_class]
    print(hm_images)
    num_images = len(hm_images)
    fig, axs = plt.subplots(1, num_images, figsize = (12, 8))
    for i in range(num_images):
      self.pimgr.plot_image(hm_images[i], axs[i])

    plt.show()