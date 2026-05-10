//setup
run("Set Measurements...", "area mean min integrated");
setOption("BlackBackground", true);



//functions
renaming();
maskSoma();
maskCell();	


function renaming() { 
	
	//Split and rename channels
	selectWindow("MaxZ_deconvolution.tif");
	run("Split Channels");
	selectWindow("C1-MaxZ_deconvolution.tif");
	rename("CellMaxZ.tif");
	selectWindow("C2-MaxZ_deconvolution.tif");
	rename("vGATMaxZ.tif");
	selectWindow("C3-MaxZ_deconvolution.tif");
	rename("mScarletGphnMaxZ.tif");
	selectWindow("C4-MaxZ_deconvolution.tif");
	rename("gamma2MaxZ.tif");

	close("gamma2MaxZ.tif");
	close("vGATMaxZ.tif");
	close("mScarletGphnMaxZ.tif");
	
}

//maskSoma function filters, segments, and creates a Mask of the Soma. The mask will be saved as Soma.tif
function maskSoma() { 
	//Soma mask
	selectWindow("CellMaxZ.tif");
	run("Median...", "radius=15");//10
	run("Duplicate...", "title=SomaMask.tif");
	run("Enhance Contrast...", "saturated=0.1 normalize");	//0.1
	run("Auto Threshold", "method=Otsu white");
	run("Options...", "iterations=4 count=1 black do=Dilate");
	run("Analyze Particles...", "size=25-Infinity show=Masks");
	rename("Soma.tif");
	save(outputDirPath + "Soma.tif");
	close("SomaMask.tif");
}



//maskCell function filters, segments, and creates a Mask of the Cell. The mask will be saved as Cell.tif
function maskCell() { 
	//Soma mask
	selectWindow("CellMaxZ.tif");
	
	run("Enhance Contrast...", "saturated=0.1 normalize");	//0.1
	run("Auto Threshold", "method=Mean white");
	run("Options...", "iterations=4 count=1 black do=Dilate");
	run("Analyze Particles...", "size=350-Infinity show=Masks");
	rename("Cell.tif");
	save(outputDirPath + "Cell.tif");
	close("Cell.tif");
	close("CellMask.tif");

}

