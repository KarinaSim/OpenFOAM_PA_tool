import subprocess


class CaseSaver:
    def __init__(self, statusBar, case_dirname, bMD_tab, system_tab, sHMD_tab=None):

        self.statusBar = statusBar

        exist_flag = self.check_dir_existing(case_dirname)
        if exist_flag == "False":
            self.mkdir(case_dirname)

        str_blockMeshDict = self.get_blockMeshDict_str(bMD_tab)
        str_p, str_U = self.get_pU_str(bMD_tab)
        str_transportProperties = self.get_transportProps_str(system_tab)
        str_turbulenceProperties = self.get_turbulenceProps_str(system_tab)
        str_controlDict = self.get_controlDict_str(system_tab)
        str_fvSchemes = self.get_fvSchemes_str(system_tab)
        str_fvSolution = self.get_fvSolution_str(system_tab)

        try:
            self.write_blockMeshDict(str_blockMeshDict, case_dirname)
            self.write_p(str_p, case_dirname)
            self.write_U(str_U, case_dirname)
            self.write_transportProperties(str_transportProperties, case_dirname)
            self.write_turbulenceProperties(str_turbulenceProperties, case_dirname)
            self.write_controlDict(str_controlDict, case_dirname)
            self.write_fvSchemes(str_fvSchemes, case_dirname)
            self.write_fvSolution(str_fvSolution, case_dirname)
            if sHMD_tab is not None:
                str_snappyHexMeshDict = self.get_snappyHexMeshDict_str(sHMD_tab)
                if str_snappyHexMeshDict == "no stl":
                    self.statusBar.showMessage("snappyHexMeshDict is not saved: add stl", 2000)
                else:
                    self.write_snappyHexMeshDict(str_snappyHexMeshDict, case_dirname)
                    self.statusBar.showMessage("Case was saved successfully in directory", 5000)
            else:
                self.statusBar.showMessage("Case was saved successfully in directory", 5000)
        except:
            self.statusBar.showMessage("Case saving in directory error", 5000)


    def check_dir_existing(self, case_dirname):
        output = subprocess.run(["bash", "/home/karina/PycharmProjects/OpenFOAM_PA_tool/bin/check_direxist", case_dirname],
                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = output.stdout.decode("utf-8").rstrip()
        return out

    # def mkdir(self, case_dirname):
    #     output = None
    #     print("create")
    #     try:
    #         print("ok")
    #         dir = case_dirname +"0"
    #         output = subprocess.run(["mkdir", "-p", dir], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #         self.statusBar.showMessage("The directory " + dir + "was created successfully")
    #     except:
    #         print("er")
    #         err = output.stderr.decode("utf-8")
    #         self.statusBar.showMessage("Error creating the directory " + dir + ": " + err)
    #     # subprocess.run(["mkdir", case_dirname + "constant"])
    #     # subprocess.run(["mkdir", case_dirname + "system"])


    def mkdir(self, case_dirname):

        try:
            output = subprocess.run(["mkdir", "-p", case_dirname +"0"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out = output.stdout.decode('utf-8')
            err = output.stderr.decode('utf-8')
            subprocess.run(["mkdir", "-p", case_dirname +"constant/triSurface"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(["mkdir", case_dirname +"system"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.statusBar.showMessage("Case directory was successfully created", 5000)
        except:
            self.statusBar.showMessage("Creating directory error", 5000)



    def get_blockMeshDict_str(self, bMD_tab):
        blocks = bMD_tab.blocks_form.blocks
        convertToMeters = bMD_tab.blocks_form.scale.text()
        str_vertices = ""
        str_blocks = ""
        for item in range(0, blocks.count()):
            block = blocks.itemAt(item).widget()
            data = block.read_blockGUIdata()

            keys, values, cells, ratios = data
            str_blocks += "\thex {0} {1} simpleGrading {2}\n".format(keys, cells, ratios)
            for v in range(0, 8):
                str_vertices += "\t" + values[v] + "\n"
        str_vertices = "convertToMeters {0};\n\nvertices\n(\n{1});\n\n".format(convertToMeters, str_vertices)
        str_blocks = "blocks\n(\n" + str_blocks + ");\n\n"
        # print(str_vertices)
        # print(str_blocks)

        str_edges = ""
        edges = bMD_tab.edges_form.blocks_edges
        if edges.count() == 0:
            str_edges = "edges\n(\n" + ");\n\n"
        else:
            for item in range(0, edges.count()):
                block_edges = edges.itemAt(item).widget()
                data = block_edges.read_block_edgesGUIdata()
                for item in data.items():
                    str_edges += "\tarc {0} {1}\n".format(item[0], item[1])
            str_edges = "edges\n(\n" + str_edges + ");\n\n"
        # print(str_edges)


        patches = bMD_tab.patches_form.blocks_patches
        str_boundary = ""
        for item in range(0, patches.count()):
            block_patches = patches.itemAt(item).widget()
            data = block_patches.read_block_patchesGUIdata()
            # print(data)
            for item in data.items():
                name = item[0]
                type = item[1][0]
                face = item[1][1]
                str_boundary += "\t{0}\n\t{{\n\t\ttype {1};\n\t\tfaces\n\t\t(\n\t\t\t{2}\n\t\t);\n\t}}\n".format(name, type, face)
        str_boundary = "boundary\n(\n" + str_boundary + ");\n\n"
        # print(str_boundary)


        merged_patches = bMD_tab.mergedpatches_form.merged_patches
        str_mergePatchPairs = ""
        for item in range(0, merged_patches.count()):
            block_merged_patches = merged_patches.itemAt(item).widget()
            data = block_merged_patches.read_block_merged_patchesGUIdata()
            # print(data)
            for item in range(0, len(data)):
                str_mergePatchPairs += "\t{}\n".format(data[item])
        str_mergePatchPairs = "mergePatchPairs\n(\n" + str_mergePatchPairs + ");\n"
        # print(str_mergePatchPairs)


        str_blockMeshDict = str_vertices + str_blocks + str_edges + str_boundary + str_mergePatchPairs
        # print(str_blockMeshDict)
        return str_blockMeshDict



    def get_pU_str(self, bMD_tab):

        blocks_pU = bMD_tab.initialconds_form.blocks_pU
        str_boundaryField_p = ""
        str_boundaryField_U = ""
        if_p = bMD_tab.initialconds_form.if_p.text().replace(',', '.')
        if_U = [bMD_tab.initialconds_form.if_xU.text().replace(',', '.'), bMD_tab.initialconds_form.if_yU.text().replace(',', '.'),
                bMD_tab.initialconds_form.if_zU.text().replace(',', '.')]
        if_U = "(" + " ".join(if_U) + ")"


        for item in range(0,  bMD_tab.patches_form.blocks_patches.count()):
            block_pU = blocks_pU.itemAt(item).widget()
            data = block_pU.read_block_pUGUIdata()

            # print(data)
            for item in data[0].items():
                name = item[0]
                type = item[1]
                if isinstance(type, str):
                    str_boundaryField_p += "\t{0}\n\t{{\n\t\ttype {1};\n\t}}\n".format(name, type)
                else:
                    type = item[1][0]
                    value = item[1][1]
                    str_boundaryField_p += "\t{0}\n\t{{\n\t\ttype {1};\n\t\tvalue uniform {2};\n\t}}\n".format(name, type, value)
            for item in data[1].items():
                name = item[0]
                type = item[1]
                if isinstance(type, str):
                    str_boundaryField_U += "\t{0}\n\t{{\n\t\ttype {1};\n\t}}\n".format(name, type)
                else:
                    type = item[1][0]
                    value = item[1][1]
                    str_boundaryField_U += "\t{0}\n\t{{\n\t\ttype {1};\n\t\tvalue uniform {2};\n\t}}\n".format(name, type, value)

        str_surfaces_p = ""
        str_surfaces_U = ""
        surfaces_form = bMD_tab.initialconds_form.surfaces_form
        surfaces_p = surfaces_U = []
        if surfaces_form is not None:
            surfaces_p, surfaces_U = bMD_tab.initialconds_form.read_GUIdata_surface(surfaces_form)


        for item in surfaces_p:
            name = item[0]
            type = item[1]
            if isinstance(type, str):
                str_surfaces_p += "\t{0}\n\t{{\n\t\ttype {1};\n\t}}\n".format(name, type)
            else:
                type = item[1][0]
                value = item[1][1]
                str_surfaces_p += "\t{0}\n\t{{\n\t\ttype {1};\n\t\tvalue uniform {2};\n\t}}\n".format(name, type, value)
        for item in surfaces_U:
             name = item[0]
             type = item[1]
             if isinstance(type, str):
                 str_surfaces_U += "\t{0}\n\t{{\n\t\ttype {1};\n\t}}\n".format(name, type)
             else:
                 type = item[1][0]
                 value = item[1][1]
                 str_surfaces_U += "\t{0}\n\t{{\n\t\ttype {1};\n\t\tvalue uniform {2};\n\t}}\n".format(name, type, value)


        str_p = "dimensions\t\t[0 2 -2 0 0 0 0];\n\ninternalField\tuniform " + if_p + ";\n\nboundaryField\n{\n" + str_boundaryField_p + str_surfaces_p + "}\n"
        str_U = "dimensions\t\t[0 1 -1 0 0 0 0];\n\ninternalField\tuniform " + if_U + ";\n\nboundaryField\n{\n" + str_boundaryField_U + str_surfaces_U + "}\n"
        # print(str_p)
        # print(str_U)
        return [str_p, str_U]


    def get_transportProps_str(self, system_tab):
        prop_value = system_tab.transportprops_form.read_transportprops_GUIdata()
        # print(prop_value)
        str_transportProperties = "transportModel\t\tNewtonian;\n\nnu\t\t[0 2 -1 0 0 0 0] " + prop_value + ";\n"
        # print(str_transportProperties)
        return str_transportProperties


    def get_turbulenceProps_str(self, system_tab):
        props_values = system_tab.turbulenceprops_form.read_turbulenceprops_GUIdata()
        # print(props_values)
        str_tubulenceProperties = ""
        for item in range(0, len(props_values)):
            label = props_values[item][0]
            value = props_values[item][1]
            str_tubulenceProperties += "\t" + label + "\t\t" + value + ";\n\n"
        # print(str_RASProperties)
        return str_tubulenceProperties

    def get_controlDict_str(self, system_tab):
        runtime = system_tab.runtime_form.read_runtime_GUIdata()
        # print(runtime)
        str_controlDict = ""
        for item in range(0, len(runtime)):
            label = runtime[item][0]
            value = runtime[item][1]
            str_controlDict += "\t" + label + "\t\t\t" + value + ";\n\n"
        # print(str_controlDict)
        return str_controlDict


    def get_fvSchemes_str(self, system_tab):
        numschemes = system_tab.numschemes_form.read_numschemesGUIdata()
        # print(numschemes)
        str_fvSchemes = ""
        for item in numschemes.items():
            scheme = item[0]
            lv = item[1]
            str_lv = ""
            for i in range(0, len(lv)):
                label = lv[i][0]
                value = lv[i][1]
                str_lv += "\t" + label + "\t" + value + ";\n"
            str_fvSchemes += scheme + "\n{\n" + str_lv + "}\n\n"
        # print(str_fvSchemes)
        return str_fvSchemes


    def get_fvSolution_str(self, system_tab):
        solcontrol = system_tab.solcontrol_form.read_solcontrolGUI()
        # print(solcontrol)
        str_relaxationFactors = ""
        str_p = ""
        str_U = ""
        p = solcontrol["p"]
        for i in range(0, len(p)):
                label = p[i][0]
                value = p[i][1]
                str_p += "\t\t" + label + "\t" + value + ";\n"
        str_p = "\tp\n\t{\n" + str_p + "\t}\n"
        U = solcontrol["U"]
        for i in range(0, len(U)):
                label = U[i][0]
                value = U[i][1]
                str_U += "\t\t" + label + "\t" + value + ";\n"
        str_U = "\tU\n\t{\n" + str_U + "\t}\n"
        str_solvers = "solvers\n{\n" + str_p + str_U + "}\n\n"

        simple = solcontrol["SIMPLE"]
        str_simple = "SIMPLE\n{\n\t" + simple[0][0] + "\t" + simple[0][1] + ";\n\tresidualControl\n\t{\n\t\t" + \
                     simple[1][0] + "\t" + simple[1][1] + ";\n\t\t" + simple[2][0] + "\t" + simple[2][1] + ";\n\t}\n}\n"


        relaxationFactors = solcontrol["relaxationFactors"]
        str_relaxationFactors = "relaxationFactors\n{\n\tfields\n\t{\n\t\t" + relaxationFactors[0][0] + "\t" +\
                                relaxationFactors[0][1] + ";\n\t}\n\tequations\n\t{\n\t\t" + relaxationFactors[1][0] + \
                                "\t" + relaxationFactors[1][1] + ";\n\t}\n}\n"


        str_fvSolution = str_solvers + str_simple + str_relaxationFactors
        # print(str_fvSolution)
        return str_fvSolution


    def get_snappyHexMeshDict_str(self, sHMD_tab):
        surfaces = sHMD_tab.geometry_form.surfaces
        str_surfaces = ""
        stl_data_list = []
        counter_stl = 0
        for item in range(0, surfaces.count()):
            surface = surfaces.itemAt(item).widget()
            stl_data = surface.get_stl_data()
            if stl_data[0] is None:
                break
            stl_data_list.append(stl_data)
            data = surface.read_surfaceGUIdata()
            # print(data)
            name, type, file = data
            counter_stl += 1
            str_surfaces += "\t" + name + "\n\t{\n\t\ttype\t" + type + ";\n\t\tfile\t" + file + ";\n\t}\n"

        if counter_stl < surfaces.count() or counter_stl == 0:
            return "no stl"

        regions = sHMD_tab.geometry_form.regions
        str_regions = ""
        for item in range(0, regions.count()):
            region = regions.itemAt(item).widget()
            data = region.read_regionGUIdata()
            # print(data)
            name, type, val1, val2 = data
            if type == 'searchableSphere':
                str_regions += "\t" + name + "\n\t{\n\t\ttype\t" + type + ";\n\t\tcentre\t"\
                               + val1 + ";\n\t\tradius\t" + val2 + ";\n\t}\n"
            else:
                str_regions += "\t" + name + "\n\t{\n\t\ttype\t" + type + ";\n\t\tmin\t"\
                               + val1 + ";\n\t\tmax\t" + val2 + ";\n\t}\n"

        str_geometry = "geometry\n{\n" + str_surfaces + str_regions + "};\n\n"
        # print(str_geometry)


        castellatedMC_params = sHMD_tab.castellatedMC_form.read_castellatedGUI()
        # print(castellatedMC_params)
        str_castellatedMC_params = ""
        for item in range(0, len(castellatedMC_params)):
            label = castellatedMC_params[item][0]
            value = castellatedMC_params[item][1]
            str_castellatedMC_params += "\t" + label + "\t" + value + ";\n"

        csurfaces = sHMD_tab.castellatedMC_form.surfaces
        str_csurfaces = ""
        for item in range(0, csurfaces.count()):
            surface = csurfaces.itemAt(item).widget()
            data = surface.read_surfaceGUIdata()
            # print(data)
            name, level = data
            str_csurfaces += "\t\t" + name + "\n\t\t{\n\t\t\tlevel\t" + level + ";\n\t\t}\n"
        str_refinementSurfaces = "\trefinementSurfaces\n\t{\n" + str_csurfaces + "\t}\n\n"

        cregions = sHMD_tab.castellatedMC_form.regions
        str_cregions = ""
        for item in range(0, cregions.count()):
            region = cregions.itemAt(item).widget()
            data = region.read_regionGUIdata()
            name, mode, levels = data
            # print(data)
            str_cregions += "\t\t" + name + "\n\t\t{\n\t\t\tmode\t" + mode + ";\n\t\t\tlevels\t" + levels + ";\n\t\t}\n"
        str_refinementRegions = "\trefinementRegions\n\t{\n" + str_cregions + "\t}\n\n"

        str_castellatedMeshControls = "castellatedMeshControls\n{\n\tfeatures\n\t(\n\t);\n\n" + \
                                      str_refinementSurfaces + str_refinementRegions + \
                                      str_castellatedMC_params + "}\n\n"
        # print(str_castellatedMeshControls)

        snapC_params = sHMD_tab.snapC_form.read_snapC_GUIdata()
        # print(snapC_params)
        str_snapC_params = ""
        for item in range(0, len(snapC_params)):
            label = snapC_params[item][0]
            value = snapC_params[item][1]
            str_snapC_params += "\t" + label + "\t" + value + ";\n"
        str_snapControls = "snapControls\n{\n" + str_snapC_params + "}\n\n"
        # print(str_snapControls)


        addLayersC_params = sHMD_tab.addLayersC_form.read_addLayersC_GUIdata()
        # print(addLayersC_params)
        str_addLayersC_params = ""
        for item in range(0, len(addLayersC_params)):
            label = addLayersC_params[item][0]
            value = addLayersC_params[item][1]
            str_addLayersC_params += "\t" + label + "\t" + value + ";\n"
        str_addLayersControls = "addLayersControls\n{\n\tlayers\n\t{\n\t}\n" + str_addLayersC_params + "}\n\n"
        # print(str_addLayersControls)


        meshQC_params, relaxed = sHMD_tab.meshQC_form.read_meshQC_GUIdata()
        # print(meshQC_params)
        label = meshQC_params[0][0]
        value = meshQC_params[0][1]
        str_meshQC_params = "\t" + label + "\t" + value + "\n"
        for item in range(1, len(meshQC_params)):
            label = meshQC_params[item][0]
            value = meshQC_params[item][1]
            str_meshQC_params += "\t" + label + "\t" + value + ";\n"
        str_meshQualityControls = "meshQualityControls\n{\n" + str_meshQC_params + "\trelaxed\n\t{\n\t\t" + \
                                  relaxed[0] + "\t" + relaxed[1] + ";\n\t}\n}\n\n"
        # print(str_meshQualityControls)


        other_params, writeFlags = sHMD_tab.otherParams_form.read_otherParams_GUIdata()
        # print(other_params)
        str_other_params = ""
        str_writeFlags = ""
        for item in writeFlags:
            str_writeFlags += "\t" + item[0] + "\n"

        for item in range(0, len(other_params)):
            label = other_params[item][0]
            value = other_params[item][1]
            str_other_params += label + "\t" + value + ";\n"
        str_other_params = "writeFlags\n(\n" + str_writeFlags + ");\n\n" + str_other_params
        # print(str_other_params)

        str_snappyHexMeshDict = str_geometry + str_castellatedMeshControls + str_snapControls + \
                                str_addLayersControls + str_meshQualityControls + str_other_params
        # print(str_snappyHexMeshDict)

        str_meshQualityDict = '#includeEtc "caseDicts/mesh/generation/meshQualityDict"\n'

        return [str_snappyHexMeshDict, str_meshQualityDict, stl_data_list]



    def write_blockMeshDict(self, str, case_dirname):
        header = self.get_openfoam_header("dictionary", "blockMeshDict")
        file = header[0] + str + header[1]
        try:
            with open(case_dirname + "system/blockMeshDict", "w") as file_handler:
                file_handler.write(file)
            self.statusBar.showMessage("blockMeshDict was saved successfully", 2000)
        except IOError:
            self.statusBar.showMessage("blockMeshDict IOError has occurred!", 2000)

    def write_p(self, str, case_dirname):
        header = self.get_openfoam_header("volScalarField", "p")
        file = header[0] + str + header[1]
        try:
            with open(case_dirname + "0/p", "w") as file_handler:
                file_handler.write(file)
            self.statusBar.showMessage("p was saved successfully", 2000)
        except IOError:
            self.statusBar.showMessage("p IOError has occurred!", 2000)

    def write_U(self, str, case_dirname):
        header = self.get_openfoam_header("volVectorField", "U")
        file = header[0] + str + header[1]
        try:
            with open(case_dirname + "0/U", "w") as file_handler:
                file_handler.write(file)
            self.statusBar.showMessage("U was saved successfully", 2000)
        except IOError:
            self.statusBar.showMessage("U IOError has occurred!", 2000)

    def write_controlDict(self, str, case_dirname):
        header = self.get_openfoam_header("dictionary", "controlDict", "system")
        file = header[0] + str + header[1]
        try:
            with open(case_dirname + "system/controlDict", "w") as file_handler:
                file_handler.write(file)
            self.statusBar.showMessage("controlDict was saved successfully", 2000)
        except IOError:
            self.statusBar.showMessage("controlDict IOError has occurred!", 2000)

    def write_transportProperties(self, str, case_dirname):
        header = self.get_openfoam_header("dictionary", "transportProperties", "constant")
        file = header[0] + str + header[1]
        try:
            with open(case_dirname + "constant/transportProperties", "w") as file_handler:
                file_handler.write(file)
            self.statusBar.showMessage("transportProperties was saved successfully", 2000)
        except IOError:
            self.statusBar.showMessage("transportProperties IOError has occurred!", 2000)


    def write_turbulenceProperties(self, str, case_dirname):
        header = self.get_openfoam_header("dictionary", "turbulenceProperties", "constant")
        file = header[0] + str + header[1]
        try:
            with open(case_dirname + "constant/turbulenceProperties", "w") as file_handler:
                file_handler.write(file)
            self.statusBar.showMessage("turbulenceProperties was saved successfully", 2000)
        except IOError:
            self.statusBar.showMessage("turbulenceProperties IOError has occurred!", 2000)

    def write_fvSchemes(self, str, case_dirname):
        header = self.get_openfoam_header("dictionary", "fvSchemes", "system")
        file = header[0] + str + header[1]
        try:
            with open(case_dirname + "system/fvSchemes", "w") as file_handler:
                file_handler.write(file)
            self.statusBar.showMessage("fvSchemes was saved successfully", 2000)
        except IOError:
            self.statusBar.showMessage("fvSchemes IOError has occurred!", 2000)


    def write_fvSolution(self, str, case_dirname):
        header = self.get_openfoam_header("dictionary", "fvSolution", "system")
        file = header[0] + str + header[1]
        try:
            with open(case_dirname + "system/fvSolution", "w") as file_handler:
                file_handler.write(file)
            self.statusBar.showMessage("fvSolution was saved successfully", 2000)
        except IOError:
            self.statusBar.showMessage("fvSolution IOError has occurred!", 2000)


    def write_snappyHexMeshDict(self, list, case_dirname):
        header = self.get_openfoam_header("dictionary", "snappyHexMeshDict")
        file = header[0] + list[0] + header[1]
        try:
            with open(case_dirname + "system/snappyHexMeshDict", "w") as file_handler:
                file_handler.write(file)
            self.statusBar.showMessage("snappyHexMeshDict was saved successfully", 2000)
        except IOError:
            self.statusBar.showMessage("snappyHexMeshDict IOError has occurred!", 2000)

        header = self.get_openfoam_header("dictionary", "meshQualityDict")
        file = header[0] + list[1] + header[1]
        try:
            with open(case_dirname + "system/meshQualityDict", "w") as file_handler:
                file_handler.write(file)
            self.statusBar.showMessage("meshQualityDict was saved successfully", 1500)
        except IOError:
            self.statusBar.showMessage("meshQualityDict IOError has occurred!", 1500)

        stl_data_list = list[2]
        for item in stl_data_list:
            name, data = item
            try:
                with open(case_dirname +"constant/triSurface/" + name, "w") as filehandler:
                    filehandler.write(data)
                    self.statusBar.showMessage(name + " was successfully saved to the directory", 1500)
            except:
                    self.statusBar.showMessage(name + " IOError has occurred!", 1500)




    def get_openfoam_header(self, clas, object, location = None):
        str1 = "/*{0}*- C++ -*{1}*\\\n".format("-" * 32, "-" * 34)
        str2 = "  {0}{1}|{2}\n".format("=" * 9, " " * 17, " " * 49)
        str3 = "  \\\\{0}/  F ield{1}| OpenFOAM: The Open Source CFD Toolbox\n".format(" " * 6, " " * 9)
        str4 = "   \\\\{0}/{1}O peration{2}| Website:  https://openfoam.org\n".format(" " * 4, " " * 3, " " * 5)
        str5 = " {0}\\\\  /{1}A nd{2}| Version:  7\n".format(" " * 3, " " * 4, " " * 11)
        str6 = " {0}\\\\/{1}M anipulation  |{2}\n".format(" " * 4, " " * 5, " " * 49)
        str7 = "\\*{}*/\n".format("-" * 76)
        foam = ""
        if location is None:
            foam = "\tversion\t2.0;\n\tformat\tascii;\n\tclass\t" + clas + \
                       ";\n\tobject\t" + object + ";\n"
        else:
            foam = "\tversion\t2.0;\n\tformat\tascii;\n\tclass\t" + clas + \
                      ";\n\tlocation\t" + '"' + location + '"' + ";\n\tobject\t" + object + ";\n"
        str8_14 = "FoamFile\n{\n" + foam + "}\n"
        str15 = "\n//{} //\n\n".format(" *" * 37)
        end_str = "\n// {} //".format("*" * 73)
        openfoam_file_header = str1 + str2 + str3 + str4 + str5 + str6 + str7 + str8_14 + str15
        return [openfoam_file_header, end_str]
