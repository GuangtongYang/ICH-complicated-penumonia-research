import os
from uuid import getnode

'''
run this in 3DSlicer
Slicer.exe --python-script "D:\pythonScripts\nonRigidRegistration\skull_strip.py"
'''

file_path=r'D:\BaiduNetdiskDownload\DongyingData\CtImage_resize_norm_unbone'
file_names=os.listdir(file_path)
for name in file_names:
    volumePath=os.path.join(file_path,name)
    names_splite=name.split('.')
    name=names_splite[0]
    masterVolumeNode = slicer.util.loadVolume(volumePath)

    # Create segmentation
    segmentationNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentationNode")
    segmentationNode.CreateDefaultDisplayNodes() # only needed for display
    segmentationNode.SetReferenceImageGeometryParameterFromVolumeNode(masterVolumeNode)
    addedSegmentID = segmentationNode.GetSegmentation().AddEmptySegment("skull")

    # Create segment editor to get access to effects
    segmentEditorWidget = slicer.qMRMLSegmentEditorWidget()
    segmentEditorWidget.setMRMLScene(slicer.mrmlScene)
    segmentEditorNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentEditorNode")
    segmentEditorWidget.setMRMLSegmentEditorNode(segmentEditorNode)
    segmentEditorWidget.setSegmentationNode(segmentationNode)
    segmentEditorWidget.setMasterVolumeNode(masterVolumeNode)

        # Thresholding
    segmentEditorWidget.setActiveEffectByName("Threshold")
    effect = segmentEditorWidget.activeEffect()
    effect.setParameter("MinimumThreshold","106")
    effect.setParameter("MaximumThreshold","2000")
    effect.self().onApply()

    # Find largest cavity
    segmentEditorWidget.setActiveEffectByName("Islands")
    effect = segmentEditorWidget.activeEffect()
    effect.setParameterDefault("Operation", "KEEP_LARGEST_ISLAND")
    effect.self().onApply()

    # Solidify bone
    segmentEditorWidget.setActiveEffectByName("Wrap Solidify")
    effect = segmentEditorWidget.activeEffect()
    effect.setParameter("region", "largestCavity")
    effect.setParameter("splitCavities", True)
    effect.setParameter("splitCavitiesDiameter",30.0)
    effect.setParameter("outputType", "segment")
    effect.setParameter("remeshOversampling", 0.3)  # speed up solidification by lowering resolution
    effect.self().onApply()

    # Blank out the volume outside the object segment
    segmentEditorWidget.setActiveEffectByName('Mask volume')
    effect = segmentEditorWidget.activeEffect()
    effect.setParameter('FillValue', -30)
    effect.setParameter('Operation', 'FILL_OUTSIDE')
    effect.self().onApply()

    # Clean up
    segmentEditorWidget = None
    slicer.mrmlScene.RemoveNode(segmentEditorNode)
    slicer.mrmlScene.RemoveNode(segmentationNode)

    #output
    outputVolume=slicer.mrmlScene.GetFirstNodeByName(name+' masked')
    myStorageNode = outputVolume.CreateDefaultStorageNode()
    myStorageNode.SetFileName(os.path.join(r"D:\BaiduNetdiskDownload\DongyingData\SkullStripped",name+'.nii'))
    myStorageNode.WriteData(outputVolume)

    slicer.mrmlScene.RemoveNode(outputVolume)
    slicer.mrmlScene.RemoveNode(masterVolumeNode)



