import numpy as np
import cv2
from skimage import img_as_float
from skimage.restoration import denoise_nl_means,inpaint,denoise_tv_chambolle, denoise_bilateral,denoise_tv_bregman


def filtroMorfologico(path,iterations=1):
    # Cargar la imagen
    imagen = cv2.imread(path, 0)

    # Crear un kernel de '1' de 3x3
    kernel = np.ones((3, 3), np.uint8)

    # Se aplica la transformacion: Morphological Gradient
    transformacion = cv2.dilate(imagen, kernel, iterations) - cv2.erode(imagen, kernel, iterations)

    return transformacion

def denoiseNonLocalMeans(path):
    """
    Reemplaza la intensidad de cada pixel con la media de los pixels a su alrededor
    """
    imagen = cv2.imread(path, 0)
    noisy = img_as_float(imagen)

    denoise = denoise_nl_means(noisy, 7, 9, 0.08)

    return denoise

def denoiseBilateral(path,multichannel):
    """
    -Reemplaza el valor de cada pixel en funcion de la proximidad espacial y radiometrica
     medida por la funcion Gaussiana de la distancia euclidiana entre dos pixels y con
     cierta desviacion estandar.
    -False si la imagen es una escala de grises, sino True
    """
    imagen = cv2.imread(path, 0)
    noisy = img_as_float(imagen)

    denoise = denoise_bilateral(noisy, 7, 9, 0.08,multichannel)

    return denoise


def denoiseTV_Chambolle(path,multichannel):
    """
    -Tiende a producir imagenes como las de los dibujos animados.
    -Reduce al minimo la variacion total de la imagen
    """
    imagen = cv2.imread(path, 0)
    noisy = img_as_float(imagen)

    denoise = denoise_tv_chambolle(noisy, 7, 9, 0.08,multichannel)

    return denoise

def denoiseTV_Bregman(path,isotropic):
    """
    -isotropic es el atributo para cambiar entre filtrado isotropico y anisotropico
    """
    imagen = cv2.imread(path, 0)
    noisy = img_as_float(imagen)

    denoise = denoise_tv_bregman(noisy, 7, 9, 0.08, isotropic)

    return denoise

def denoiseInpaint(pathImagen,pathMask,multichannel):
    imagen = cv2.imread(pathImagen, 0)
    noisy = img_as_float(imagen)
    image_orig = noisy
    mask = np.asarray(cv2.imread(pathMask,0))

    # Afecta a la imagen original en las regiones marcadas por la mascara
    # Se puede cambiar de acuerdo a lo que se necesite
    # En este caso produce defectos en la zona
    image_defect = image_orig.copy()
    for layer in range(image_defect.shape[-1]):
        image_defect[np.where(mask)] = 1

    image_result = inpaint.inpaint_biharmonic(image_defect, mask, multichannel)

    return image_result
