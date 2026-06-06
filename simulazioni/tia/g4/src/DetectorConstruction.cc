#include "DetectorConstruction.hh"
#include "DetectorMessenger.hh"
#include "G4Material.hh"
#include "G4Box.hh"
// #include "G4Tubs.hh"
#include "G4LogicalVolume.hh"
#include "G4PVPlacement.hh"
#include "G4PVReplica.hh"

#include "G4GeometryTolerance.hh"
#include "G4GeometryManager.hh"
#include "G4NistManager.hh"

#include "G4VisAttributes.hh"
#include "G4Colour.hh"


#include "G4SDManager.hh"
#include "G4SystemOfUnits.hh"
#include "G4PhysicalConstants.hh"

//ora voglio sensitive detector
#include "ScintillatorSD.hh"

DetectorConstruction::DetectorConstruction()
   : scint1_YOffset(0.0),
    scint2_YOffset(0.0),
    scint3_YOffset(0.0),
    detectorMessenger(nullptr)
{
    DefineMaterials(); //definition of mat
// -----------------------------------------
    ComputeParameters(); //compute par

    // Create the detector messenger
  detectorMessenger = new DetectorMessenger(this);

}

DetectorConstruction::~DetectorConstruction(){
    delete detectorMessenger;
}

void DetectorConstruction::DefineMaterials(){
    //get mat from Nist
    G4NistManager* man = G4NistManager::Instance();
    man->SetVerbose(1);

    // Retrieve the predefined plastic scintillator (Polyvinyltoluene)
    pvt = man->FindOrBuildMaterial("G4_PLASTIC_SC_VINYLTOLUENE");
    air = man->FindOrBuildMaterial("G4_AIR");
    al = man->FindOrBuildMaterial("G4_Al");

}

void DetectorConstruction::ComputeParameters(){
    //now i define the default geometry

    //wrld
    halfWrldLength = 2* m;

    //scintillators
    posFirstScintillator = G4ThreeVector(0., scint1_YOffset, 0.);
    posSecondScintillator = G4ThreeVector(0., scint2_YOffset, (12.8+(3/2))* cm); 
    posThirdScintillator = G4ThreeVector(0., scint3_YOffset, (8.4+(3/2))* cm);
}

G4VPhysicalVolume* DetectorConstruction::Construct(){
    //this function is called by G4 to construct detector


    //World
    // G4GeometryManager::GetInstance()->SetWorldMaximumExtent(2.*halfWrldLength);
    G4cout << "Computed tolerance = "
    << G4GeometryTolerance::GetInstance()->GetSurfaceTolerance()/cm
    << "cm" << G4endl;

    G4Box* solidWrld = new G4Box("World", halfWrldLength, halfWrldLength, halfWrldLength);
    logicWrld = new G4LogicalVolume(solidWrld, air, "World", 0, 0, 0);

    // ora ci piazzo il wrld physical volume non ruotato in 0, 0, 0

    G4VPhysicalVolume* physiWrld = new G4PVPlacement(
        0, //non ruotato
        G4ThreeVector(), //alle coordinate 000
        logicWrld, //il logic volume
        "World", //il suo nome
        0, //il suo volme madre, non ne ha
        false, //non ci sono operazioni booleane
        0 );//copynumber

    //ora costruisco il rivelatore davvero
    ConstructScintillator(); // necessario qui!!

    //per il momento non costruisco la lastra
    // ConstructLastra();


    //infine colori di visualizzazione
    G4Color
		green(0.0,1.0,0.0),
		blue(0.0,0.0,1.0),
		brown(0.4,0.4,0.1),
		white(1.0,1.0,1.0);
        
	logicWrld -> SetVisAttributes(new G4VisAttributes(white));
	// logicWorld -> SetVisAttributes(G4VisAttributes::Invisible);
    G4VisAttributes* invisAttr = new G4VisAttributes();
	invisAttr->SetVisibility(false);
	logicWrld -> SetVisAttributes(invisAttr);
	//always return the physical World
	//
	return physiWrld;

}

//ora devo costruire rivelatore

G4VPhysicalVolume* DetectorConstruction::ConstructScintillator(){
    sizex_scint = 80* cm;
    sizey_scint = 30* cm;
    sizez_scint = 3 * cm;
    sizex_scint_m = 80 * cm;
    sizey_scint_m = 30* cm;
    sizez_scint_m = 2 * cm;
    G4double halfScintSizeX = sizex_scint/2.;
	G4double halfScintSizeY = sizey_scint/2.;
	G4double halfScintSizeZ = sizez_scint/2.;
    G4double halfScintSizeX_m = sizex_scint_m/2.;
	G4double halfScintSizeY_m = sizey_scint_m/2.;
	G4double halfScintSizeZ_m = sizez_scint_m/2.;
    
    G4Box* solidScintPandG = new G4Box( "Partenope", halfScintSizeX, halfScintSizeY, halfScintSizeZ);

    G4LogicalVolume* logicScintPandG = new G4LogicalVolume(
        solidScintPandG, //its solid
        pvt, //itz material
        "PandG"); //name

        physiFirstScintillator = new G4PVPlacement(nullptr,                    // No rotation
              posFirstScintillator,                   // Position
              logicScintPandG,          // Logical volume to place
              "Partenope",                // Name
              logicWrld,                  // Mother volume
              false,                      // Not multiple copies
              0,
              false);                         // Copy number

    physiSecondScintillator = new G4PVPlacement(
        nullptr, 
        posSecondScintillator,
        logicScintPandG,
        "Giunone",
        logicWrld,
        false,
        1, 
        false);

    G4Box* solidScintM = new G4Box ("Minerva", halfScintSizeX_m, halfScintSizeY_m, halfScintSizeZ_m);
    G4LogicalVolume* logicScintM = new G4LogicalVolume(
        solidScintM, pvt, "Minerva");

    physiThirdScintillator = new G4PVPlacement(
        0, 
        posThirdScintillator,
        logicScintM,
        "Minerva", 
        logicWrld,
        false, 
        2,
        false);

    G4Color yellow(1, 1, 0);
    logicScintPandG->SetVisAttributes(new G4VisAttributes(yellow));
    G4Color red(1, 0, 0);
    logicScintM->SetVisAttributes(new G4VisAttributes(red));
        //----------------------------------------------------
    //faccio diventare "sensitive" il mio detector
    //===============================================================
    
    // Create SD instances
    ScintillatorSensitiveDetector* scintSD1 = 
        new ScintillatorSensitiveDetector("PandG");
    ScintillatorSensitiveDetector* scintSD2 = 
        new ScintillatorSensitiveDetector("Minerva");
    
    // Register with SDManager
    G4SDManager* sdManager = G4SDManager::GetSDMpointer();
    sdManager->AddNewDetector(scintSD1);
    sdManager->AddNewDetector(scintSD2);
    
    // Attach to logical volumes
    logicScintPandG->SetSensitiveDetector(scintSD1);
    logicScintM->SetSensitiveDetector(scintSD2);
    
    // ================================================
    
    return physiFirstScintillator;
}

// eventualmente devo inserire logic and physi contenenti 
// lastra alluminio/sale
// G4VPhysicalVolume* DetectorConstruction::ConstructionLastra(){

// }