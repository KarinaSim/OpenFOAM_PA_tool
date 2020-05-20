import datetime
import json

from pymongo import MongoClient

from data.windows.bMD_window import BMDWindow
from data.windows.sHMD_window import SHMDWindow
from data.windows.system_window import SystemWindow


class CaseDBLoader:
    def __init__(self, case_dirname, statusBar):

        self.statusBar = statusBar

        client = MongoClient()
        db = client.OpenFOAM_cases
        self.case = db[case_dirname]

    def set_tabs(self):
        tabs = []
        bMD_tab, surfaces_p, surfaces_U = self.set_bMDtab()

        system_tab = self.set_systemtab()

        sHMD_tab = self.set_sHMDtab(bMD_tab)

        if len(surfaces_p) != 0 and len(surfaces_U) != 0:
            self.bMD_tab.initialconds_form.set_surfaces(surfaces_p, surfaces_U)

        tabs.append(bMD_tab)
        tabs.append(system_tab)
        tabs.append(sHMD_tab)
        return tabs

    def set_bMDtab(self):
        self.bMD_tab = BMDWindow()
        scale, blocks, boundary, edges, mergePatchPairs = self.get_blockMeshDict()

        measure = [0, 0, 0]
        shift = [0, 0, 0]
        vertices, cells, ratios = blocks[0]
        block = [measure, shift]
        block.extend(blocks[0])

        self.bMD_tab.initialize("open", scale, block)
        self.bMD_tab.set_patchestypes(boundary[0])
        self.bMD_tab.set_edges(edges[0])

        p_internalField, p_boundaryField, surfaces_p = self.get_p()
        U_internalField, U_boundaryField, surfaces_U = self.get_U()

        internal = [p_internalField, U_internalField]
        self.bMD_tab.initialconds_form.if_p.setText(p_internalField)
        self.bMD_tab.initialconds_form.if_xU.setText(U_internalField[0])
        self.bMD_tab.initialconds_form.if_yU.setText(U_internalField[1])
        self.bMD_tab.initialconds_form.if_zU.setText(U_internalField[2])

        self.bMD_tab.set_initialconds(p_boundaryField[0], U_boundaryField[0])


        for i in range(1, len(blocks)):
            self.bMD_tab.blocks_form.set_block(blocks[i])
            self.bMD_tab.add_block(measure, shift, cells, ratios)
            self.bMD_tab.set_patchestypes(boundary[i])
            self.bMD_tab.set_edges(edges[i])
            self.bMD_tab.set_mergedPatches(mergePatchPairs[i - 1])
            self.bMD_tab.set_initialconds(p_boundaryField[i], U_boundaryField[i])

        return [self.bMD_tab, surfaces_p, surfaces_U]


    def set_sHMDtab(self, bMD_tab):

        snappyHexMeshDict = self.get_snappyHexkMeshDict()
        if snappyHexMeshDict is None:
            return None

        self.sHMD_tab = SHMDWindow(self.statusBar, bMD_tab)
        geometry, castellatedMC, snapC, addLayersC, meshQC, otherParams = snappyHexMeshDict

        self.sHMD_tab.initialize()
        self.sHMD_tab.set_surfaces(geometry[0], castellatedMC[1])
        self.sHMD_tab.set_regions(geometry[1], castellatedMC[2])
        self.sHMD_tab.castellatedMC_form.set_params(castellatedMC[0])
        self.sHMD_tab.snapC_form.set_params(snapC)
        self.sHMD_tab.addLayersC_form.set_params(addLayersC)
        self.sHMD_tab.meshQC_form.set_params(meshQC)
        self.sHMD_tab.otherParams_form.set_params(otherParams)


        return self.sHMD_tab



    def set_systemtab(self):

        self.system_tab = SystemWindow()
        self.system_tab.initialize()

        transportProperties = self.get_transportProperties()
        self.system_tab.transportprops_form.set_props(transportProperties)

        turbulenceProperties = self.get_turbulenceProperties()
        self.system_tab.turbulenceprops_form.set_props(turbulenceProperties)

        controlDict = self.get_controlDict()
        self.system_tab.runtime_form.set_params(controlDict)

        fvSolution = self.get_fvSolution()
        self.system_tab.solcontrol_form.set_params(fvSolution)

        fvSchemes = self.get_fvSchemes()
        self.system_tab.numschemes_form.set_params(fvSchemes)


        return self.system_tab



    def get_blockMeshDict(self):
        blockMeshDict = self.case.find_one({"_id": "blockMeshDict"})
        blocks_count = len(blockMeshDict["vertices"])
        blocks = []
        for i in range(0, blocks_count):
            verts = blockMeshDict["vertices"][i]
            vertices = []
            for item in verts:
                vertex = item.strip("()").split(" ")
                vertex = [float(item) for item in vertex]
                vertices.append(vertex)
            cells = blockMeshDict["blocks"][i][1]
            cells = cells.strip("()").split(" ")
            ratios = blockMeshDict["blocks"][i][2]
            ratios = ratios.strip("()").split(" ")
            block = [vertices, cells, ratios]
            blocks.append(block)
            # print(blocks)
            scale = blockMeshDict["convertToMeters"]

        boundary = blockMeshDict["boundary"]
        # print(boundary)

        edges = blockMeshDict["edges"]
        edges = [{key:value.strip("()").split(" ") for key,value in item.items()} for item in edges]
        # print(edges)
        mergePatchPairs = blockMeshDict["mergePatchPairs"]
        mergePatchPairs = [item.strip("()").split(" ") for item in mergePatchPairs]

        return [scale, blocks, boundary, edges, mergePatchPairs]


    def get_p(self):
        p = self.case.find_one({"_id": "p"})
        p_internalField = p["internalField"]
        p_boundaryField = p["boundaryField"]
        surfaces_p = p["surfaces_p"]
        return [p_internalField, p_boundaryField, surfaces_p]


    def get_U(self):
        U = self.case.find_one({"_id": "U"})
        U_internalField = U["internalField"]
        U_internalField = U_internalField.strip("()").split(" ")
        U_boundaryField = U["boundaryField"]
        surfaces_U = U["surfaces_U"]
        return [U_internalField, U_boundaryField, surfaces_U]



    def get_snappyHexkMeshDict(self):
        snappyHexkMeshDict = self.case.find_one({"_id": "snappyHexMeshDict"})
        if snappyHexkMeshDict is None:
            return None
        geometry = snappyHexkMeshDict["geometry"]
        surfaces = geometry[0]["surfaces"]
        regions = geometry[1]["regions"]
        for item in regions:
            item[2] = item[2].strip("()").split(" ")
            if item[1] == "searchableBox":
                item[3] = item[3].strip("()").split(" ")
        geometry = [surfaces, regions]

        castellatedMC = snappyHexkMeshDict["castellatedMeshControls"]
        params = castellatedMC[0]["params"]
        csurfaces = castellatedMC[1]["csurfaces"]
        cregions = castellatedMC[2]["cregions"]

        for item in params:
            if item[0] == "locationInMesh":
                item[1] = item[1].strip("()").split(" ")
        for item in csurfaces:
            item[1] = item[1].strip("()").split(" ")
        for item in cregions:
             if item[1] == "distance":
                 item[2] = item[2].strip("()").split(") (")
                 item[2] = [l.split(" ") for l in item[2]]
             else:
                 item[2] = item[2].strip("()").split(" ")
        castellatedMC = [params, csurfaces, cregions]

        snapC = snappyHexkMeshDict["snapControls"]
        addLayersC = snappyHexkMeshDict["addLayersControls"]

        meshQC = snappyHexkMeshDict["meshQualityControls"]
        params = meshQC["params"]
        relaxed = meshQC["relaxed"][1]
        meshQC = [params, relaxed]

        otherParams = snappyHexkMeshDict["otherParams"]
        params = otherParams["params"]
        writeFlags = otherParams["writeFlags"]
        otherParams = [params, writeFlags]

        return [geometry, castellatedMC, snapC, addLayersC, meshQC, otherParams]


    def get_transportProperties(self):
        transportProperties = self.case.find_one({"_id": "transportProperties"})
        nu = transportProperties["nu"]
        return nu

    def get_turbulenceProperties(self):
        turbulenceProperties = self.case.find_one({"_id": "turbulenceProperties"})
        turbulenceProperties = turbulenceProperties["props"]
        return turbulenceProperties


    def get_controlDict(self):
        controlDict = self.case.find_one({"_id": "controlDict"})
        controlDict = controlDict["params"]
        return controlDict


    def get_fvSolution(self):
        fvSolution = self.case.find_one({"_id": "fvSolution"})
        p = fvSolution["p"]
        U = fvSolution["U"]
        SIMPLE = fvSolution["SIMPLE"]
        relaxationFactors = fvSolution["relaxationFactors"]


        fvSolution = [p, U, SIMPLE, relaxationFactors]
        return fvSolution


    def get_fvSchemes(self):
        fvSchemes = self.case.find_one({"_id": "fvSchemes"})

        ddtSchemes = fvSchemes["ddtSchemes"]
        gradSchemes = fvSchemes["gradSchemes"]
        divSchemes = fvSchemes["divSchemes"]
        laplacianSchemes = fvSchemes["laplacianSchemes"]
        interpolationSchemes = fvSchemes["interpolationSchemes"]
        snGradSchemes = fvSchemes["snGradSchemes"]
        fluxRequired = fvSchemes["fluxRequired"]

        fvSchemes = [ddtSchemes, gradSchemes, divSchemes, laplacianSchemes,
                     interpolationSchemes, snGradSchemes, fluxRequired]
        return fvSchemes
