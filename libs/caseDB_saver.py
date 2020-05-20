import datetime
import json

from pymongo import MongoClient

class CaseDBSaver:
    def __init__(self, statusBar, case_dirname, bMD_tab, system_tab, sHMD_tab=None):


        self.statusBar = statusBar

        json_blockMeshDict = self.get_json_blockMeshDict(bMD_tab)
        json_p, json_U = self.get_json_pU(bMD_tab)
        json_transportProperties = self.get_json_transportProperties(system_tab)
        json_turbulenceProperties = self.get_json_turbulenceProperties(system_tab)
        json_controlDict = self.get_json_controlDict(system_tab)
        json_fvSchemes = self.get_json_fvSchemes(system_tab)
        json_fvSolution = self.get_json_fvSolution(system_tab)


        client = MongoClient()
        db = client.OpenFOAM_cases
        case = db[case_dirname]

        try:
            case.save(json_blockMeshDict)
            case.save(json_p)
            case.save(json_U)
            case.save(json_transportProperties)
            case.save(json_turbulenceProperties)
            case.save(json_controlDict)
            case.save(json_fvSchemes)
            case.save(json_fvSolution)
            if sHMD_tab is not None:
                json_snappyHexMeshDict = self.get_json_snappyHexMeshDict(sHMD_tab)
                if json_snappyHexMeshDict == "no stl":
                    self.statusBar.showMessage("Case is not saved: add stl", 2000)
                else:
                    case.save(json_snappyHexMeshDict)
                    self.statusBar.showMessage("Case was saved successfully in DB", 5000)
            else:
                snappyHexMeshDict = case.find_one({"_id": "snappyHexMeshDict"})
                if snappyHexMeshDict is not None:
                    case.delete_one(snappyHexMeshDict)
                self.statusBar.showMessage("Case was saved successfully in DB", 5000)
        except:
            self.statusBar.showMessage("Case saving in DB error", 5000)



    def get_json_blockMeshDict(self, bMD_tab):

        blocks = bMD_tab.blocks_form.blocks
        convertToMeters = bMD_tab.blocks_form.scale.text()

        json_blocks = []
        json_vertices = []
        for item in range(0, blocks.count()):
            block = blocks.itemAt(item).widget()
            data = block.read_blockGUIdata()

            keys, values, cells, ratios = data
            # print(data)
            block = [keys, cells, ratios]
            json_blocks.append(block)
            json_vertices.append(values)


        edges = bMD_tab.edges_form.blocks_edges
        json_edges = []
        if edges.count() == 0:
            json_edges = []
        else:
            for item in range(0, edges.count()):
                block_edges = edges.itemAt(item).widget()
                data = block_edges.read_block_edgesGUIdata()
                # print(data)
                json_edges.append(data)


        patches = bMD_tab.patches_form.blocks_patches
        json_boundary = []
        for item in range(0, patches.count()):
            block_patches = patches.itemAt(item).widget()
            data = block_patches.read_block_patchesGUIdata()
            # print(data)
            json_boundary.append(data)


        merged_patches = bMD_tab.mergedpatches_form.merged_patches
        json_mergePatchPairs = []
        for item in range(0, merged_patches.count()):
            block_merged_patches = merged_patches.itemAt(item).widget()
            data = block_merged_patches.read_block_merged_patchesGUIdata()
            # print(data)
            json_mergePatchPairs.extend(data)


        json_blockMeshDict = {"_id":"blockMeshDict", "date": datetime.datetime.utcnow(),
                              "convertToMeters": convertToMeters, "vertices":json_vertices,
                              "blocks":json_blocks, "edges":json_edges, "boundary":json_boundary,
                              "mergePatchPairs":json_mergePatchPairs}
        # with open("/home/karina/PycharmProjects/patool/testfiles/json_files", "w") as file:
        #     file.write(json.dumps(json_blockMeshDict, skipkeys=True, ensure_ascii=False, indent='\t', separators=(', ', ': ')))
        return json_blockMeshDict


    def get_json_pU(self, bMD_tab):

        blocks_pU = bMD_tab.initialconds_form.blocks_pU
        json_p = ""
        json_U = ""
        json_internalField_p = bMD_tab.initialconds_form.if_p.text()
        json_internalField_U = [bMD_tab.initialconds_form.if_xU.text(),
                                bMD_tab.initialconds_form.if_yU.text(), bMD_tab.initialconds_form.if_zU.text()]
        json_internalField_U = "(" + " ".join(json_internalField_U) + ")"
        json_boundaryField_p = []
        json_boundaryField_U = []

        for item in range(0, bMD_tab.patches_form.blocks_patches.count()):
            block_pU = blocks_pU.itemAt(item).widget()
            data = block_pU.read_block_pUGUIdata()
            # print(data)
            json_boundaryField_p.append(data[0])
            json_boundaryField_U.append(data[1])


        surfaces_form = bMD_tab.initialconds_form.surfaces_form
        print(surfaces_form)
        surfaces_p = surfaces_U = []
        if surfaces_form is not None:
            surfaces_p, surfaces_U = bMD_tab.initialconds_form.read_GUIdata_surface(surfaces_form)
        else:
            surfaces_p = surfaces_U = []


        json_p = {"_id":"p", "date": datetime.datetime.utcnow(), "dimensions": "[0 2 -2 0 0 0 0]",
                  "internalField": json_internalField_p, "boundaryField":json_boundaryField_p, "surfaces_p": surfaces_p}
        json_U = {"_id":"U", "date": datetime.datetime.utcnow(), "dimensions": "[0 1 -1 0 0 0 0]",
                  "internalField": json_internalField_U, "boundaryField":json_boundaryField_U, "surfaces_U": surfaces_U}
        # with open("/home/karina/PycharmProjects/patool/testfiles/json_files", "w") as file:
        #     file.write(json.dumps(json_p, skipkeys=True, ensure_ascii=False, indent='\t', separators=(', ', ': ')))
        return [json_p, json_U]


    def get_json_transportProperties(self, system_tab):

        transport_prop_value = system_tab.transportprops_form.read_transportprops_GUIdata()
        # print(transport_prop_value)
        json_transportProperties = {"_id":"transportProperties", "date": datetime.datetime.utcnow(),
                                    "nu":transport_prop_value}
        # with open("/home/karina/PycharmProjects/patool/testfiles/json_files", "w") as file:
        #     file.write(json.dumps(json_transportProperties, skipkeys=True, ensure_ascii=False, indent='\t', separators=(', ', ': ')))
        return json_transportProperties

    def get_json_turbulenceProperties(self, system_tab):

        turbulence_props = system_tab.turbulenceprops_form.read_turbulenceprops_GUIdata()
        # print(turbulence_props)
        json_turbulenceProperties = {"_id":"turbulenceProperties",  "date": datetime.datetime.utcnow(), "props":turbulence_props}
        # with open("/home/karina/PycharmProjects/patool/testfiles/json_files", "w") as file:
        #     file.write(json.dumps(json_turbulenceProperties, skipkeys=True, ensure_ascii=False, indent='\t', separators=(', ', ': ')))
        return json_turbulenceProperties


    def get_json_controlDict(self, system_tab):

        runtime = system_tab.runtime_form.read_runtime_GUIdata()
        # print(runtime)
        json_controlDict = {"_id":"controlDict", "date": datetime.datetime.utcnow(),
                            "params":runtime}
        # with open("/home/karina/PycharmProjects/patool/testfiles/json_files", "w") as file:
        #     file.write(json.dumps(json_controlDict, skipkeys=True, ensure_ascii=False, indent='\t', separators=(', ', ': ')))
        return json_controlDict


    def get_json_fvSchemes(self, system_tab):

        numschemes = system_tab.numschemes_form.read_numschemesGUIdata()
        # print(numschemes)
        numschemes.update({"_id":"fvSchemes", "date": datetime.datetime.utcnow()})
        json_fvSchemes = numschemes
        # with open("/home/karina/PycharmProjects/patool/testfiles/json_files", "w") as file:
        #     file.write(json.dumps(json_fvSchemes, skipkeys=True, ensure_ascii=False, indent='\t', separators=(', ', ': ')))
        return json_fvSchemes


    def get_json_fvSolution(self, system_tab):

        solcontrol = system_tab.solcontrol_form.read_solcontrolGUI()
        # print(solcontrol)
        solcontrol.update({"_id":"fvSolution", "date": datetime.datetime.utcnow()})
        json_fvSolution = solcontrol
        # with open("/home/karina/PycharmProjects/patool/testfiles/json_files", "w") as file:
        #     file.write(json.dumps(json_fvSolution, skipkeys=True, ensure_ascii=False, indent='\t', separators=(', ', ': ')))
        return json_fvSolution


    def get_json_snappyHexMeshDict(self, sHMD_tab):
        surfaces = sHMD_tab.geometry_form.surfaces
        json_surfaces = []
        counter_stl = 0
        for item in range(0, surfaces.count()):
            surface = surfaces.itemAt(item).widget()
            stl_data = surface.get_stl_data()[1]
            if stl_data is None:
                break
            # stl_dir_list.append(stl_dir)
            surface_data = surface.read_surfaceGUIdata()
            surface_data.append(stl_data)
            # print(surface_data)
            counter_stl += 1
            json_surfaces.append(surface_data)
        json_surfaces = {"surfaces":json_surfaces}

        if counter_stl < surfaces.count() or counter_stl == 0:
            return "no stl"


        regions = sHMD_tab.geometry_form.regions
        json_regions = []
        for item in range(0, regions.count()):
            region = regions.itemAt(item).widget()
            region_data = region.read_regionGUIdata()
            # print(region_data)
            json_regions.append(region_data)
        json_regions = {"regions":json_regions}


        castellatedMC_params = sHMD_tab.castellatedMC_form.read_castellatedGUI()
        json_castellatedMC_params = {"params": castellatedMC_params}


        csurfaces = sHMD_tab.castellatedMC_form.surfaces
        json_csurfaces = []

        for item in range(0, csurfaces.count()):
            csurface = csurfaces.itemAt(item).widget()
            csurface_data = csurface.read_surfaceGUIdata()
            # print(surface_data)
            json_csurfaces.append(csurface_data)
        json_csurfaces = {"csurfaces":json_csurfaces}


        cregions = sHMD_tab.castellatedMC_form.regions
        json_cregions = []
        for item in range(0, cregions.count()):
            cregion = cregions.itemAt(item).widget()
            cregion_data = cregion.read_regionGUIdata()
            # print(region_data)
            json_cregions.append(cregion_data)
        json_cregions = {"cregions":json_cregions}


        snapC_params = sHMD_tab.snapC_form.read_snapC_GUIdata()
        addLayersC_params = sHMD_tab.addLayersC_form.read_addLayersC_GUIdata()

        meshQC_params, relaxed = sHMD_tab.meshQC_form.read_meshQC_GUIdata()
        json_meshQualityControls = {"params":meshQC_params, "relaxed":relaxed}

        other_params, writeFlags = sHMD_tab.otherParams_form.read_otherParams_GUIdata()
        json_other_params = {"params":other_params, "writeFlags":writeFlags}



        json_snappyHexMeshDict = {"_id":"snappyHexMeshDict", "date": datetime.datetime.utcnow(),
                              "geometry":[json_surfaces, json_regions], "castellatedMeshControls":
                                      [json_castellatedMC_params, json_csurfaces, json_cregions],
                                  "snapControls":snapC_params, "addLayersControls":addLayersC_params,
                                  "meshQualityControls":json_meshQualityControls, "otherParams":json_other_params}
        # with open("/home/karina/PycharmProjects/patool/testfiles/json_files", "w") as file:
        #     file.write(json.dumps(json_snappyHexMeshDict, skipkeys=True, ensure_ascii=False, indent='\t', separators=(', ', ': ')))

        return json_snappyHexMeshDict
