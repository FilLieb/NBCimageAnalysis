//setup
run("Set Measurements...", "area mean standard modal min centroid center perimeter bounding fit shape feret's integrated median skewness kurtosis area_fraction display redirect=None decimal=3");
setOption("BlackBackground", true);

//Split and rename channels
title = getTitle();

selectWindow(title);
run("Split Channels");
selectWindow("C1-" + title);
rename("Cell.tif");
selectWindow("C2-" + title);
rename("vGAT.tif");
selectWindow("C3-" + title);
rename("Gphn.tif");
selectWindow("C4-" + title);
rename("gamma2.tif");

image = "Gphn";
image = "Cell";
image = "vGAT";
image = "gamma2";
image = "Soma";

//manual assignment of background and foreground

image = "Soma";
n = 1;

selectWindow(image + ".tif");
save("Z:/personal_data/Filip_Liebsch/SP8_Biocenter_small/2025-04-23_floxed/S325D_project/training/" + image +"/images/" + image + "-" + n + ".tif");
run("Duplicate...", "title=" + image + "-" + n + ".tif");
setOption("ScaleConversions", true);
run("8-bit");
changeValues(0,255,0);


//start drawing background areas (Freehand selection) and add them to ROI Magaer using Ctrl + T
image = "Soma";
n = 1;
//background
selectWindow(image + "-" + n + ".tif");
roiNumber = roiManager("count");
	run("Clear Results");	
	for (m = 0; m < roiNumber; m++) {
		roiManager("Select", m);
		changeValues(0,255,1);
		}

roiManager("reset");





//start drawing foreground  areas (Freehand selection) and add them to ROI Magaer using Ctrl + T
image = "Soma";
n = 5;
//foreground
selectWindow(image + "-" + n + ".tif");
roiNumber = roiManager("count");
	run("Clear Results");	
	for (m = 0; m < roiNumber; m++) {
		roiManager("Select", m);
		changeValues(0,255,2);
		}
selectWindow(image + "-" + n + ".tif");
run("Select None");
save("Z:/personal_data/Filip_Liebsch/SP8_Biocenter_small/2025-04-23_floxed/S325D_project/training/" + image +"/masks/" + image + "-" + n + ".tif");
roiManager("reset");