
from google.appengine.api import images

def HistoCompare(im1, im2, mode = "pct", alpha = .01):
    if im1.size == im2.size and im1.mode == im2.mode:
        h1 = im1.histogram()
        h2 = im2.histogram()
        SumIm1 = 0.0
        SumIm2 = 0.0
	diff = 0.0
	for i in range(len(h1)):
            SumIm1 += h1[i]
            SumIm2 += h2[i]
	    diff += abs(h1[i] - h2[i])
	maxSum = max(SumIm1, SumIm2)
	if mode == "pct":
            return diff/(2*maxSum)
	if diff > alpha*maxSum:
            return False
	return True
    return False


def PixelCompare(im1, im2, mode = "pct", alpha = .01):
    if im1.size == im2.size and im1.mode == im2.mode:
        randPix = im1.getpixel((0,0))
        maxSum = []
        diff = []
        for channel in range(len(randPix)):
            diff += [0.0]
            maxSum += [0.0]
        width = im1.size[0]
        height = im1.size[1]
        for i in range(width):
            for j in range(height):
                pixel1 = im1.getpixel((i,j))
                pixel2 = im2.getpixel((i,j))
                for channel in range(len(randPix)):
                    maxSum[channel] += 255
                    diff[channel] += abs(pixel1[channel] - pixel2[channel])
        if mode == "pct":
            ret = ()
            for channel in range(len(randPix)):
                ret += (diff[channel]/maxSum[channel],)
            return ret
        for channel in range(len(randPix)):
            if diff[channel] > alpha*maxSum[channel]:
                return False
        return True
    return False

def ImageCompare(im1, im2, mode = "pct", alpha = .01):
    if im1.size == im2.size and im1.mode == im2.mode:
        HistComp = HistoCompare(im1, im2, "pct")
        PixComp = PixelCompare(im1, im2, "pct")
        if mode == "pct":
            return (PixComp, XORComp)
        if mode == "alpha":
            if HistComp > alpha:
                return False
            for pct in PixComp:
                if pct > alpha:
                    return False
    return False

def FindDifferences(im1, im2):
    if im1.size == im2.size and im1.mode == im2.mode:
        width = im1.size[0]
        height = im2.size[1]
        ret = Image.new(im1.mode, im1.size)
        for i in range(width):
            for j in range(height):
                pixel1 = im1.getpixel((i,j))
                pixel2 = im2.getpixel((i,j))
                putPix = ()
                for channel in range(len(pixel1)):
                    putPix += (abs(pixel1[channel] - pixel2[channel]),)
                ret.putpixel((i,j), putPix)
        return ret
    return False

def GetKey(size, mode, seed = 0):
    import random
    key = Image.new(mode, size)
    random.seed(seed)
    for i in range(size[0]):
        for j in range(size[1]):
            if mode == "RGB":
                key.putpixel((i,j), (random.randint(0,255), random.randint(0,255), random.randint(0,255)))
            if mode == "CMYK":
                key.putpixel((i,j), (random.randint(0,255), random.randint(0,255), random.randint(-128,127)))
            if mode == "L":
                key.putpixel((i,j), random.randint(0,255))
    return key

def EncryptImage(file, seed=0):
    image = Image.open(file)
    key = GetKey(image.size, image.mode, seed)
    enc = ImageXOR(image, key)
    enc.save(file)