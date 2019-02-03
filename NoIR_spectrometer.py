import numpy as np
import matplotlib.pyplot as plt

#read in and crop images captured using camera.py
#here we've looked at a fluorescent bulb, an incandescent bulb,
#an LED from a remote control, and a BIC lighter flame
FB = plt.imread('/home/pi/Desktop/FB.png')
sub_img_FB = FB[400:700, 510:1325]

flame = plt.imread('/home/pi/Desktop/flame2.png')
sub_img_flame = flame[400:700, 510:1325]

remote = plt.imread('/home/pi/Desktop/remote.png')
sub_img_remote = remote[400:700, 510:1325]

IB = plt.imread('/home/pi/Desktop/IB2.png')
sub_img_IB = IB[400:700, 510:1325]

#create figure with cropped spectra
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2, figsize = (12,12))

ax1.imshow(sub_img_flame)
ax2.imshow(sub_img_FB)
ax3.imshow(sub_img_remote)
ax4.imshow(sub_img_IB)

fig.tight_layout()
fig.savefig('/home/pi/Desktop/spectra_crop.png')

#function to convert RGB images to grayscale
def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

#cast images to grayscale
sub_img_FB_gray = rgb2gray(sub_img_FB)
sub_img_flame_gray = rgb2gray(sub_img_flame)
sub_img_remote_gray = rgb2gray(sub_img_remote)
sub_img_IB_gray = rgb2gray(sub_img_IB)

#project images to form 1-D spectra
spectrum_FB = [sum(x) for x in zip(*sub_img_FB_gray)]
spectrum_flame = [sum(x) for x in zip(*sub_img_flame_gray)]
spectrum_remote = [sum(x) for x in zip(*sub_img_remote_gray)]
spectrum_IB = [sum(x) for x in zip(*sub_img_IB_gray)]

#normalize spectra
spectrum_flame = [(x-min(spectrum_flame))/max(spectrum_flame) for x in spectrum_flame]
spectrum_FB = [(x-min(spectrum_FB))/max(spectrum_FB) for x in spectrum_FB]
spectrum_IB = [(x-min(spectrum_IB))/max(spectrum_IB) for x in spectrum_IB]
spectrum_remote = [(x-min(spectrum_remote))/max(spectrum_remote) for x in spectrum_remote]

#create figure with project spectra, pixel num vs intensity
fig1, ((ax01, ax02),(ax03, ax04)) = plt.subplots(2,2, figsize = (12,12))

ax02.plot(spectrum_FB)
ax02.set_xlabel('Pixel')
ax02.set_ylabel('Intensity (a.u.)')
ax02.set_title('Fluorescent Bulb')
ax01.plot(spectrum_flame)
ax01.set_xlabel('Pixel')
ax01.set_ylabel('Intensity (a.u.)')
ax01.set_title('Flame')
ax03.plot(spectrum_remote)
ax03.set_xlabel('Pixel')
ax03.set_ylabel('Intensity (a.u.)')
ax03.set_title('Remote')
ax04.plot(spectrum_IB)
ax04.set_xlabel('Pixel')
ax04.set_ylabel('Intensity (a.u.)')
ax04.set_title('Bulb')

#ax02.axvline(277)
#ax02.axvline(160)

fig1.tight_layout()
fig1.savefig('/home/pi/Desktop/spectra.png')

#create figure with spectra, wavelength vs intensity
#fluorescent bulb lines used to calibrate pixels per nm
fig2, ax11 = plt.subplots(1,1,figsize = (10,6))

#### pixels to nm ####
#160 = 436nm
#277 = 548nm

# 548 - 436 / 277 - 160 = 0.95726
# 436 = 0.95726*160 + b
# nm = 0.95726*pixel + 282.8376
######################

nm = [0.95726*x + 282.8376 for x in range(len(spectrum_flame))]

ax11.plot(nm, spectrum_flame, '-b', lw = 2, label = 'Flame')
ax11.plot(nm, spectrum_FB, '-g', lw = 2, label = 'Fluorescent Bulb')
ax11.plot(nm, spectrum_IB, '-r', lw = 2, label = 'Bulb')
ax11.plot(nm, spectrum_remote, '-k', lw = 2, label = 'Remote')

ax11.set_xlabel('Wavelength (nm)', fontsize = 14)
ax11.set_ylabel('Intensity (a.u.)', fontsize = 14)
ax11.set_title('Visible/IR Spectra', fontsize = 16)
ax11.tick_params(labelsize = 13)

ax11.legend(fontsize = 12)

fig2.tight_layout()
fig2.savefig('/home/pi/Desktop/spectra_wavelength.png')
