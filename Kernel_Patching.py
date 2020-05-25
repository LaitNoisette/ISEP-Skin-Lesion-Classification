{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "Kernel_Patching.ipynb",
      "provenance": [],
      "collapsed_sections": [],
      "authorship_tag": "ABX9TyMLHGcA+SWVDg9k/JM4Zosx"
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    }
  },
  "cells": [
    {
      "cell_type": "code",
      "metadata": {
        "id": "6CTLwizEq-AJ",
        "colab_type": "code",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 51
        },
        "outputId": "cfea5858-3302-4c09-950e-c00f7c7668f2"
      },
      "source": [
        "!pip install opencv-python"
      ],
      "execution_count": 2,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "Requirement already satisfied: opencv-python in /usr/local/lib/python3.6/dist-packages (4.1.2.30)\n",
            "Requirement already satisfied: numpy>=1.11.3 in /usr/local/lib/python3.6/dist-packages (from opencv-python) (1.18.4)\n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "qE-oDiP-q_7_",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "import cv2"
      ],
      "execution_count": 0,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "JWvPD4dST88u",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "class KernelPatch():\n",
        "  patchKernelSize=None\n",
        "  imRoi=None\n",
        "  imRoiPadding=None\n",
        "  imPatchList=None\n",
        "\n",
        "  def __init__(self,kernelSize,imRoi):\n",
        "    self.patchKernelSize=kernelSize\n",
        "    self.imRoi=imRoi\n",
        "    self.imRoiPadding=self.generateRoiWithPadding()\n",
        "  \n",
        "  def extractOverlappingPatchListFromROI(self):\n",
        "    roiPadding=self.imRoiPadding\n",
        "    patchSize=self.patchKernelSize\n",
        "\n",
        "    maxXpos=roiPadding.shape[0]\n",
        "    maxYpos=roiPadding.shape[1]\n",
        "\n",
        "    baseX=0\n",
        "    baseY=0\n",
        "\n",
        "    listPatch=[]\n",
        "    while(baseX+patchSize<=maxXpos):\n",
        "      while(baseY+patchSize<=maxYpos):\n",
        "        listPatch.append(roiPadding[baseX:baseX+patchSize,baseY:baseY+patchSize])\n",
        "        baseY+=patchSize\n",
        "      baseX+=patchSize\n",
        "    \n",
        "    self.imPatchList=np.array(listPatch)\n",
        "    return self.imPatchList\n",
        "\n",
        "  def generateRoiWithPadding(self,borderType=cv2.BORDER_CONSTANT):\n",
        "    imCrop=np.copy(self.imRoi)\n",
        "    rX=np.mod(imCrop.shape[0],self.patchKernelSize)\n",
        "    rY=np.mod(imCrop.shape[1],self.patchKernelSize)\n",
        "\n",
        "    topBottomPadding=0\n",
        "    leftRightPadding=0\n",
        "\n",
        "    while(rX!=0):\n",
        "      topBottomPadding+=1\n",
        "      imCropPad=cv2.copyMakeBorder(imCrop,topBottomPadding,topBottomPadding,0,0,cv2.BORDER_CONSTANT)\n",
        "      rX=np.mod(imCropPad.shape[0],self.patchKernelSize)\n",
        "    \n",
        "    while(rY!=0):\n",
        "      leftRightPadding+=1\n",
        "      imCropPad=cv2.copyMakeBorder(imCrop,0,0,leftRightPadding,leftRightPadding,cv2.BORDER_CONSTANT)\n",
        "      rY=np.mod(imCropPad.shape[1],self.patchKernelSize)\n",
        "    \n",
        "    self.imRoiPadding=cv2.copyMakeBorder(imCrop,topBottomPadding,topBottomPadding,leftRightPadding,leftRightPadding,borderType)\n",
        "    return self.imRoiPadding"
      ],
      "execution_count": 0,
      "outputs": []
    }
  ]
}