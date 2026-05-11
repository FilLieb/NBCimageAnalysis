//setup
run("Set Measurements...", "area mean standard modal min centroid center perimeter bounding fit shape feret's integrated median skewness kurtosis area_fraction display redirect=None decimal=3");
setOption("BlackBackground", true);

//Split and rename channels
title = getTitle();

selectWindow(title);
run("Split Channels");
selectWindow("C1-" + title);
rename("DAAO.tif");
selectWindow("C2-" + title);
rename("vGAT.tif");
selectWindow("C3-" + title);
rename("Cre.tif");
selectWindow("C4-" + title);
rename("Gphn.tif");

image = "DAAO";
image = "vGAT";
image = "Cre";
image = "Gphn";

//manual assignment of background and foreground

image = "DAAO";
n = 1;

selectWindow(image + ".tif");
save("C:/Users/liebs/VSCodeProjects/NBCimageAnalysis/training_4_channels/" + image + "/images/" + image + "-" + n + ".tif");
run("Duplicate...", "title=" + image + "-" + n + ".tif");
setOption("ScaleConversions", true);
run("8-bit");
changeValues(0,255,0);






//start drawing background areas (Freehand selection) and add them to ROI Magaer using Ctrl + T
image = "DAAO";
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
image = "DAAO";
n = 1;
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
save("C:/Users/liebs/VSCodeProjects/NBCimageAnalysis/training_4_channels/" + image + "/masks/" + image + "-" + n + ".tif");
roiManager("reset");