//setup
run("Set Measurements...", "area mean standard modal min centroid center perimeter bounding fit shape feret's integrated median skewness kurtosis area_fraction display redirect=None decimal=3");
setOption("BlackBackground", true);

chosenDir = getDirectory("chose a directory");
processFiles(chosenDir);

function processFiles(directory) {

	fileList = getFileList(directory);

	outputDirName = directory + "Z-projection";

	folderCount = 1;
	while (File.exists(outputDirName)) {
		print(outputDirName + " exists");
		outputDirName = directory + "Z-projection_" + folderCount;
		folderCount++;
	}
	
	outputDirPath = outputDirName + File.separator;
	
	for (file = 0; file < fileList.length; file++) {
		if (endsWith(fileList[file], ".lif")) {
			File.makeDirectory(outputDirName);
			run("Bio-Formats Importer", "open=[" + directory + fileList[file] + "] autoscale color_mode=Composite rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT series_1 series_2");
			analyzeImage();	
		} else if (endsWith(fileList[file], "/") && !matches(fileList[file], ".*Z-projection.*")) {
			processFiles(directory + fileList[file]);
		}
	}
}

function analyzeImage() {
	originalImageTitle = getTitle();
	run("Z Project...", "projection=[Max Intensity]");
	rename("MaxZ_deconvolution.tif");
	save(outputDirPath + "MaxZ_deconvolution.tif");
	close("MaxZ_deconvolution.tif");
	
	selectWindow(originalImageTitle);
	run("Z Project...", "projection=[Average Intensity]");
	rename("AvZ_deconvolution.tif");
	save(outputDirPath + "AvZ_deconvolution.tif");
	close(originalImageTitle);
	close("AvZ_deconvolution.tif");
	
	
	originalImageTitle = getTitle();
	run("Z Project...", "projection=[Max Intensity]");
	rename("MaxZ_confocal.tif");
	save(outputDirPath + "MaxZ_confocal.tif");
	close("MaxZ_confocal.tif");
	
	selectWindow(originalImageTitle);
	run("Z Project...", "projection=[Average Intensity]");
	rename("AvZ_confocal.tif");
	save(outputDirPath + "AvZ_confocal.tif");
	close(originalImageTitle);
	close("AvZ_confocal.tif");
	
	
}

