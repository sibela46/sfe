#include <maya/MSimple.h>
#include <maya/MIOStream.h>
#include <maya/MStreamUtils.h>
#include <maya/MItDependencyNodes.h>
#include <maya/MLibrary.h>
#include <maya/MFileIO.h>
#include <maya/MFnTransform.h>
#include <maya/MVector.h>
#include <maya/MEulerRotation.h>
#include <maya/MFnMesh.h>
#include <maya/MItMeshVertex.h>

DeclareSimpleCommand(changeExpression, "Autodesk", "2017");
int indices[68] = { 241, 75, 189, 193, 205, 215, 212, 152, 1000, 999, 996, 983, 979, 974, 1042, 1114, 295, 293, 291, 290,
288, 1103, 1094, 1096, 1098, 1110, 287, 28, 40, 41, 111, 47, 45, 891, 940, 11, 5, 26, 247, 245, 243, 1055, 1035, 1038, 
1093, 854, 857, 60, 56, 51, 1639, 893, 865, 871, 873, 68, 66, 64, 94, 321, 319, 1125, 886, 887, 98, 97, 96};

float diff[136] = { 6.433780186921922, 30.420131571334082, 8.067229601146323, 25.946273585525603, 9.895769667728757, 22.078263664107, 14.286401651452138, 17.84478127672668, 15.630886016357067, 12.886243769630937, 16.78022486733107, 8.692977362690272, 16.918104454609193, 6.012717775207648, 15.603709953616544, 4.783918027407367, 12.703843442869015, 1.7440463871181464, 9.207791204960927, 0.228992969490605, 6.596022430039056, -1.283838191253949, 4.419137864426716, -1.3650976732374147, 2.5987453060099597, -0.650874886415238, 0.8824816575731802, -0.5542542975058495, -2.0062476747852998, 1.2872556216186126, -5.4944705077432445, 4.072319965535883, -9.93890887456132, 7.41297245598696, 3.9011494404718974, 38.01698797359688, 3.633458673204018, 41.93377426314612, 2.8862252986134536, 44.25916916594127, 1.4401425843113884, 43.21721324208585, 1.2253352472632741, 41.941175542738506, -7.054599127133201, 40.14838433892078, -10.380613269610649, 38.04753920939237, -12.758715910502133, 35.07602333147395, -14.07622917759329, 28.119073034956102, -10.308875188292859, 20.848251918472613, -2.0840601638270755, 40.1473737974041, -0.1980684887641928, 40.19933502437004, 1.8254015936688575, 40.865618061525765, 4.301595938480773, 40.57174997462204, 11.302754202304982, 46.19150983983286, 9.340522297114148, 44.265960783965966, 5.803068030844997, 40.606476746514716, 3.1139213915365644, 41.1015014354457, 0.9894965340807858, 40.79325809167773, 1.4434521195354364, 39.39920553504402, 0.868436932030022, 37.24460573674838, 2.748703002598859, 36.810116851307384, 2.573688844703838, 41.023721819341006, 2.8244769692699947, 44.24434860761136, 0.6693238814004872, 44.56286524947757, -3.806551718365995, 35.480614953624126, -6.27906326302616, 28.570994281575793, -4.831218669834243, 26.940896529419035, -4.712398251515424, 26.72779401994285, -1.7991054948234932, 33.44211024661439, -3.4148382592169355, 35.575028620074306, 23.751708044044108, 36.03475210685258, 23.676524841015976, 47.20318723107346, 16.298685620921106, 47.373771409742744, 10.791108401731321, 46.26840453245552, 4.658671977716267, 44.900592775593395, -0.6004483901108415, 40.814931584273324, -0.17649464533303671, 23.415400245262674, -0.39881842028876235, 8.945661147027067, 5.5895492646506, 4.227238458240436, 12.378686095778448, 4.890016148043173, 18.734421530324994, 7.636440066928344, 25.80647160971978, 17.06826563793379, 25.19127029380047, 36.264183854003875, 16.913289707148238, 50.40019791752519, 11.353431054898124, 49.362093275151324, 5.850736371457856, 47.91830587020496, -1.5089575859429942, 25.963272698864046, 4.976539588696937, 4.553103575717273, 11.312102264035161, 5.686334145063597, 18.225618059317412, 7.750339284367669 };

MStatus changeExpression::doIt(const MArgList&)
{
	for (int i = 0; i < 136; i++) {
		diff[i] = diff[i] * 2;
	}
	MStreamUtils::stdOutStream().rdbuf();

	// create an iterator to go through all nodes
	MItDependencyNodes it(MFn::kTransform);

	// get a handle to the first node
	MObject obj;

	while (!it.isDone()) {
		obj = it.item();
		MFnTransform transformMesh(obj);
		MString name = transformMesh.name();

		//MStreamUtils::stdOutStream() << name << "\n";
		// head
		/*if (name == "head_ctrl") {
			MEulerRotation rotateBy(0.0, 0.0, diff[24] / 150);
			MStatus out = transformMesh.setRotation(rotateBy);
			MStreamUtils::stdOutStream() << out << "\n";
		}
		if (name == "Ctl_Look") {
			MVector translateVector(-diff[24] / 50, -diff[92], 0);
			MStatus out = transformMesh.setTranslation(translateVector, MSpace::kTransform);
			MStreamUtils::stdOutStream() << out << "\n";
		}*/
		if (name == "Ctl_eyebrow_mid") { //27 mid eyebrow
			MVector translateVector(diff[54]/100, diff[55]/100, 0);
			MStatus out = transformMesh.setTranslation(translateVector, MSpace::kTransform);
			MStreamUtils::stdOutStream() << out << "\n";
		}
		if (name == "Ctl_eyebrow_in_L") {
			MVector translateVector(diff[42]/100, diff[43]/100, 0);
			MStatus out = transformMesh.setTranslation(translateVector, MSpace::kTransform);
			MStreamUtils::stdOutStream() << out << "\n";
		}
		if (name == "Ctl_eyebrow_mid_L") {
			MVector translateVector(diff[38] / 100, diff[39] / 100, 0);
			MStatus out = transformMesh.setTranslation(translateVector, MSpace::kTransform);
			MStreamUtils::stdOutStream() << out << "\n";
		}
		if (name == "Ctl_eyebrow_out_L") {
			MVector translateVector(diff[34] / 100, diff[35] / 100, 0);
			MStatus out = transformMesh.setTranslation(translateVector, MSpace::kTransform);
			MStreamUtils::stdOutStream() << out << "\n";
		}
		if (name == "Ctl_eyebrow_in_R") {
			MVector translateVector(diff[44] / 100, diff[45] / 100, 0);
			MStatus out = transformMesh.setTranslation(translateVector, MSpace::kTransform);
			MStreamUtils::stdOutStream() << out << "\n";
		}
		if (name == "Ctl_eyebrow_mid_R") {
			MVector translateVector(diff[48] / 100, diff[49] / 100, 0);
			MStatus out = transformMesh.setTranslation(translateVector, MSpace::kTransform);
			MStreamUtils::stdOutStream() << out << "\n";
		}
		if (name == "Ctl_eyebrow_out_R") {
			MVector translateVector(diff[52] / 100, diff[53] / 100, 0);
			MStatus out = transformMesh.setTranslation(translateVector, MSpace::kTransform);
			MStreamUtils::stdOutStream() << out << "\n";
		}
		// Left eye
		if (name == "Ctl_eyelid_corner_in_L") {
			MVector translateVector(diff[78] / 100, diff[79] / 100, 0);
			MStatus out = transformMesh.setTranslation(translateVector, MSpace::kTransform);
			MStreamUtils::stdOutStream() << out << "\n";
		}
		if (name == "Ctl_eyelid_corner_out_L") {
			MVector translateVector(diff[72] / 100, diff[73] / 100, 0);
			MStatus out = transformMesh.setTranslation(translateVector, MSpace::kTransform);
			MStreamUtils::stdOutStream() << out << "\n";
		}
		/*if (name == "Ctl_eyelid_up_in_L") {
			MVector translateVector(diff[76] / 100, diff[77] / 100, 0);
			MStatus out = transformMesh.setTranslation(translateVector, MSpace::kTransform);
			MStreamUtils::stdOutStream() << out << "\n";
		}
		if (name == "Ctl_eyelid_up_mid_L") {
			MVector translateVector(diff[76] / 100, diff[77] / 100, 0);
			MStatus out = transformMesh.setTranslation(translateVector, MSpace::kTransform);
			MStreamUtils::stdOutStream() << out << "\n";
		}
		if (name == "Ctl_eyelid_up_out_L") {
			MVector translateVector(diff[74] / 100, diff[75] / 100, 0);
			MStatus out = transformMesh.setTranslation(translateVector, MSpace::kTransform);
			MStreamUtils::stdOutStream() << out << "\n";
		}*/
		if (name == "Ctl_eyelid_dn_in_L") {
			MVector translateVector(diff[80] / 150, diff[81] / 150, 0.5);
			MStatus out = transformMesh.setTranslation(translateVector, MSpace::kTransform);
			MStreamUtils::stdOutStream() << out << "\n";
		}
		if (name == "Ctl_eyelid_dn_mid_L") {
			MVector translateVector(diff[80] / 150, diff[81] / 150, 0.5);
			MStatus out = transformMesh.setTranslation(translateVector, MSpace::kTransform);
			MStreamUtils::stdOutStream() << out << "\n";
		}
		if (name == "Ctl_eyelid_dn_out_L") {
			MVector translateVector(diff[82] / 150, diff[83] / 150, 0.5);
			MStatus out = transformMesh.setTranslation(translateVector, MSpace::kTransform);
			MStreamUtils::stdOutStream() << out << "\n";
		}
		// Right eye
		if (name == "Ctl_eyelid_corner_in_R") {
			MVector translateVector(diff[84] / 100, diff[85] / 100, 0);
			MStatus out = transformMesh.setTranslation(translateVector, MSpace::kTransform);
			MStreamUtils::stdOutStream() << out << "\n";
		}
		if (name == "Ctl_eyelid_corner_out_R") {
			MVector translateVector(diff[90] / 100, diff[91] / 100, 0);
			MStatus out = transformMesh.setTranslation(translateVector, MSpace::kTransform);
			MStreamUtils::stdOutStream() << out << "\n";
		}
		/*if (name == "Ctl_eyelid_up_in_R") {
			MVector translateVector(diff[86] / 100, diff[87] / 100, 0);
			MStatus out = transformMesh.setTranslation(translateVector, MSpace::kTransform);
			MStreamUtils::stdOutStream() << out << "\n";
		}
		if (name == "Ctl_eyelid_up_mid_R") {
			MVector translateVector(diff[86] / 100, diff[87] / 100, 0);
			MStatus out = transformMesh.setTranslation(translateVector, MSpace::kTransform);
			MStreamUtils::stdOutStream() << out << "\n";
		}
		if (name == "Ctl_eyelid_up_out_R") {
			MVector translateVector(diff[88] / 100, diff[89] / 100, 0);
			MStatus out = transformMesh.setTranslation(translateVector, MSpace::kTransform);
			MStreamUtils::stdOutStream() << out << "\n";
		}*/
		if (name == "Ctl_eyelid_dn_in_R") {
			MVector translateVector(diff[94] / 150, diff[95] / 150, 0);
			MStatus out = transformMesh.setTranslation(translateVector, MSpace::kTransform);
			MStreamUtils::stdOutStream() << out << "\n";
		}
		if (name == "Ctl_eyelid_dn_mid_R") {
			MVector translateVector(diff[94] / 150, diff[95] / 150, 0);
			MStatus out = transformMesh.setTranslation(translateVector, MSpace::kTransform);
			MStreamUtils::stdOutStream() << out << "\n";
		}
		if (name == "Ctl_eyelid_dn_out_R") {
			MVector translateVector(diff[92] / 150, diff[93] / 150, 0);
			MStatus out = transformMesh.setTranslation(translateVector, MSpace::kTransform);
			MStreamUtils::stdOutStream() << out << "\n";
		}
		// Mouth
		if (name == "Ctl_Corner_Lips_L") {
			MVector translateVector(diff[96] / 100, diff[97] / 100, 0);
			MStatus out = transformMesh.setTranslation(translateVector, MSpace::kTransform);
			MStreamUtils::stdOutStream() << out << "\n";
		}
		if (name == "Ctl_Corner_Lips_R") {
			MVector translateVector(diff[108] / 100, diff[109] / 100, 0);
			MStatus out = transformMesh.setTranslation(translateVector, MSpace::kTransform);
			MStreamUtils::stdOutStream() << out << "\n";
		}
		if (name == "Ctl_lip_up_L") {
			MVector translateVector(diff[98] / 100, diff[99] / 100, 0);
			MStatus out = transformMesh.setTranslation(translateVector, MSpace::kTransform);
			MStreamUtils::stdOutStream() << out << "\n";
		}
		if (name == "Ctl_lip_mid_up") {
			MVector translateVector(diff[102] / 100, diff[103] / 100, 0);
			MStatus out = transformMesh.setTranslation(translateVector, MSpace::kTransform);
			MStreamUtils::stdOutStream() << out << "\n";
		}
		if (name == "Ctl_lip_up_R") {
			MVector translateVector(diff[106] / 100, diff[107] / 100, 0);
			MStatus out = transformMesh.setTranslation(translateVector, MSpace::kTransform);
			MStreamUtils::stdOutStream() << out << "\n";
		}
		if (name == "Ctl_lip_dn_L") {
			MVector translateVector(diff[118] / 100, diff[119] / 100, 0);
			MStatus out = transformMesh.setTranslation(translateVector, MSpace::kTransform);
			MStreamUtils::stdOutStream() << out << "\n";
		}
		if (name == "Ctl_lip_mid_dn") {
			MVector translateVector(diff[114] / 100, diff[115] / 100, 0);
			MStatus out = transformMesh.setTranslation(translateVector, MSpace::kTransform);
			MStreamUtils::stdOutStream() << out << "\n";
		}
		if (name == "Ctl_lip_dn_R") {
			MVector translateVector(diff[110] / 100, diff[111] / 100, 0);
			MStatus out = transformMesh.setTranslation(translateVector, MSpace::kTransform);
			MStreamUtils::stdOutStream() << out << "\n";
		}
		// Cheeks
		if (name == "Ctl_cheek_up_out_L") {
			MVector translateVector(diff[0] / 100, diff[1] / 100, 0);
			MStatus out = transformMesh.setTranslation(translateVector, MSpace::kTransform);
			MStreamUtils::stdOutStream() << out << "\n";
		}
		if (name == "Ctl_cheek_up_out_R") {
			MVector translateVector(diff[32] / 100, diff[33] / 100, 0);
			MStatus out = transformMesh.setTranslation(translateVector, MSpace::kTransform);
			MStreamUtils::stdOutStream() << out << "\n";
		}
		it.next();
	}

	/*MObject face = it.item();
	MFnMesh fnMeshFace(face);

	for (int i = 0; i <= 68; i++) {
		MPoint currentPoint;
		fnMeshFace.getPoint(indices[i], currentPoint);
		float newX = diff[i*2]/300;
		float newY = diff[i * 2 + 1]/300;
		MPoint newPoint(newX, newY, 0.0, 1.0);
		MStatus out = fnMeshFace.setPoint(indices[i], currentPoint + newPoint, MSpace::kObject);
		MStreamUtils::stdOutStream() << out << "\n";
	}*/

	return MS::kSuccess;
}
