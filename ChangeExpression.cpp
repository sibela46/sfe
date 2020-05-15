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

float diff[136] = { 65.58597614003764, 32.97779547091761, 66.75121508765017, 35.16948155441071, 66.33368886753493, 36.87332349657436, 63.488194713708765, 37.96741669796933, 62.10254567784631, 38.955443048862605, 63.618178833521085, 40.70370094386004, 64.53767279577227, 42.44427569037089, 65.37869531177296, 45.789323906642494, 65.65227437894464, 46.21813342260748, 66.37752427922248, 47.720851276114445, 62.5335838430791, 41.22866653120218, 58.03302005869148, 36.213833581547306, 54.6113155703423, 32.77854359114167, 52.45043008988091, 33.7765236028813, 53.96822613790323, 35.46357232529749, 55.66556719717619, 38.030465271965, 57.52312087010398, 40.09476287080639, 72.28723285289976, 49.491539597005556, 78.40923956748429, 53.90670420939384, 80.50625597262797, 56.298324692231205, 82.16666484715427, 59.13045976258002, 83.12178852449244, 60.748670571890415, 75.50349563922987, 59.33661222510699, 74.93993415852731, 61.03849842442301, 73.268291066909, 62.89062833869312, 71.1992835799366, 65.76152939479323, 68.66061453544273, 65.95204016715164, 80.23770530172101, 60.21557806621297, 80.32136632667584, 66.1990750434054, 80.04031894408354, 71.6031744952225, 79.68595869735839, 76.52066562699412, 74.69414571706534, 65.53425062452601, 74.46690739667008, 69.58709700769401, 75.08577522924838, 72.66594291498967, 73.42090300030122, 71.74808002502726, 72.36748413895157, 70.93354009987621, 75.59236334760499, 46.53113252685341, 75.17980310211493, 49.5705956088965, 76.1392004286792, 51.50706059395907, 73.54826754671785, 52.467341071102, 74.44931467843224, 51.59813085187341, 73.3068788699851, 50.23798810908386, 73.99775051429424, 58.36002181951335, 73.74496131417925, 60.27463281881069, 74.09719703023302, 61.646757974083016, 72.28446547818669, 61.20264714245798, 74.13730525623487, 62.47312919211578, 73.73092115730185, 61.105230043905976, 83.0810640791974, 69.32306086005877, 81.03832192948323, 78.30003058220524, 77.05771111171725, 80.0153959871302, 71.13157846351942, 82.66600471390842, 66.22148465102384, 82.44768733138056, 56.16180255946426, 84.22426939745088, 45.15929832735526, 79.0057298341913, 54.27459921041054, 65.49721215182018, 64.01067298209068, 57.36765003584884, 69.08299206234426, 55.704460097752644, 74.61583949636861, 55.539783406849836, 79.92847420035736, 58.52670650418838, 83.9232606031112, 72.00325822412708, 75.2777659420077, 83.68263595305791, 70.30255180704432, 84.68397222921334, 66.0376616417019, 85.72637509606938, 43.36498152240142, 80.2417075392679, 65.64111245118409, 55.67200856736815, 70.06807194485009, 55.167708933336485, 75.88693829700355, 54.88539542933643 };

MStatus changeExpression::doIt(const MArgList&)
{
	
	MStreamUtils::stdOutStream().rdbuf();

	// create an iterator to go through all nodes
	MItDependencyNodes it(MFn::kTransform);

	// get a handle to the first node
	MObject obj;

	while (!it.isDone()) {
		obj = it.item();
		MFnTransform transformMesh(obj);
		MString name = transformMesh.name();

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
		if (name == "Ctl_eyelid_up_in_L") {
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
		}
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
		if (name == "Ctl_eyelid_up_in_R") {
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
		}
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
