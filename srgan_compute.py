import matplotlib.pyplot as plt
from srgan import generator
from utils import load_image, resolve_single

model = generator()
model.load_weights('./srgan/gan_generator.h5')

def srgan_compute(img_path):
    lr = load_image(img_path)
    sr = resolve_single(model, lr).numpy()
    return sr

