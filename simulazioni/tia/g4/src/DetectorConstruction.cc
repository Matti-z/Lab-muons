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

// #include "G4ThreeVector.hh"

#include "G4SDManager.hh"
#include "G4SystemOfUnits.hh"
#include "G4PhysicalConstants.hh"

//ora voglio sensitive detector
#include "ScintillatorSD.hh"

//per fare operazioni logiche con solidi
#include "G4SubtractionSolid.hh"

//a quanto pare alluminio di per sè non ha tutte le proprietà ottiche reali...
#include "G4OpticalSurface.hh"
#include "G4LogicalSkinSurface.hh"

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
    sizex_scint = (80 - 0.4)* cm;
    sizey_scint = (30 - 0.4)* cm;
    sizez_scint = (3 - 0.4) * cm;
    sizex_scint_m = (80 - 0.4) * cm;
    sizey_scint_m = (30 - 0.4)* cm;
    sizez_scint_m = (2 - 0.4) * cm;
    sizex_al_foil = 80* cm;
    sizey_al_foil = 30* cm;
    sizez_al_foil = 3 * cm;
    sizex_al_foil_m = 80* cm;
    sizey_al_foil_m = 30 * cm;
    sizez_al_foil_m = 2 * cm;
    G4double halfScintSizeX = sizex_scint/2.;
	G4double halfScintSizeY = sizey_scint/2.;
	G4double halfScintSizeZ = sizez_scint/2.;
    G4double halfScintSizeX_m = sizex_scint_m/2.;
	G4double halfScintSizeY_m = sizey_scint_m/2.;
	G4double halfScintSizeZ_m = sizez_scint_m/2.;
    
    //creo una box cava di alluminio in cui successivamente inserire scint
    //il wrap è di 1,5 mm di alluminio per lato, rimane dello spazio vuoto tra pvt e alluminio, idealmente si può ridurre
    //ho fatto così poichè non abbiamo vere specifiche tecniche
    //ci sarebbe da aggiungere un altro wrap di vinile, evito
    G4Box* outer_pg = new G4Box("Pwrap", sizex_al_foil/2, sizey_al_foil/2, sizez_al_foil/2);
    G4Box* inner_pg = new G4Box("inner_box",( sizex_al_foil/2 - 0.15*cm),  (sizey_al_foil/2 - 0.15 *cm),
     (sizez_al_foil/2 - 0.15*cm));  
    G4SubtractionSolid* hollow_pg = new G4SubtractionSolid("hollow_pg",
                                                        outer_pg,
                                                        inner_pg,
                                                        0,  // no rotation
                                                        G4ThreeVector(0, 0, 0));  // centered
    G4LogicalVolume* logicpwrap = new G4LogicalVolume(
        hollow_pg, al, "Pwrap"
    );
    // Define a reflective optical surface properties for the foil wrapper
    G4OpticalSurface* alFoilSurface = new G4OpticalSurface("AlFoilSurface");
    alFoilSurface->SetType(dielectric_metal);
    alFoilSurface->SetFinish(polished);
    alFoilSurface->SetModel(glisur);

    // Add reflectivity properties (e.g., reflecting 90% of optical photons)
    G4MaterialPropertiesTable* foilMPT = new G4MaterialPropertiesTable();
    G4double photonEnergy[] = {1.0*eV, 0.5*MeV};
    G4double reflectivity[] = {0.95, 0.95}; 
    foilMPT->AddProperty("REFLECTIVITY", photonEnergy, reflectivity, 2);
    alFoilSurface->SetMaterialPropertiesTable(foilMPT);

    // Apply this surface to your Aluminum Wrap Logical Volumes
    new G4LogicalSkinSurface("PandG_Wrap_Skin", logicpwrap, alFoilSurface);
    physipwrap = new G4PVPlacement(nullptr,                    // No rotation
        posFirstScintillator,                   // Position
        logicpwrap,          // Logical volume to place
        "P_wrap",                // Name
        logicWrld,                  // Mother volume
        false,                      // Not multiple copies
        0,
        false);    
        
    G4Box* solidScintPandG = new G4Box( "Partenope", halfScintSizeX, halfScintSizeY, halfScintSizeZ);
    
    G4LogicalVolume* logicScintP = new G4LogicalVolume(
        solidScintPandG, //its solid
        pvt, //itz material
        "P"); //name
        
    physiFirstScintillator = new G4PVPlacement(nullptr,                    // No rotation
        G4ThreeVector(0*cm, 0*cm, 0*cm),                   // Position
        logicScintP,          // Logical volume to place
        "Partenope",                // Name
        logicpwrap,                  // Mother volume
        false,                      // Not multiple copies
        0,
        false);                         // Copy number


     G4LogicalVolume* logicgwrap = new G4LogicalVolume(
        hollow_pg, al, "Gwrap"
    );
        
    physigwrap = new G4PVPlacement(nullptr,                    // No rotation
        posSecondScintillator,                   // Position
        logicgwrap,          // Logical volume to place
        "G_wrap",                // Name
        logicWrld,                  // Mother volume
        false,                      // Not multiple copies
        0,
        false);


    G4LogicalVolume* logicScintG = new G4LogicalVolume(
        solidScintPandG, //its solid
        pvt, //itz material
        "P"); //name
            
        
    physiSecondScintillator = new G4PVPlacement(
        nullptr, 
        G4ThreeVector(0*cm, 0*cm, 0*cm),
        logicScintG,
        "Giunone",
        logicgwrap,
        false,
        1, 
        false);
        
        //creo wrap per minerva
        G4Box* outer_m = new G4Box("mwrap", sizex_al_foil_m/2, sizey_al_foil_m/2, sizez_al_foil_m/2);
        G4Box* inner_m = new G4Box("inner_box_m",( sizex_al_foil_m/2 - 0.15*cm),  (sizey_al_foil_m/2 - 0.15 *cm),
        (sizez_al_foil_m/2 - 0.15*cm));
        G4SubtractionSolid* hollow_m = new G4SubtractionSolid("hollow_m",
            outer_m,
            inner_m,
            0,  // no rotation
            G4ThreeVector(0, 0, 0));  // centered
            G4LogicalVolume* logicmwrap = new G4LogicalVolume(
                hollow_m, al, "m_wrap"
            );
    
    new G4LogicalSkinSurface("M_Wrap_Skin", logicmwrap, alFoilSurface);
    
    physimwrap = new G4PVPlacement(nullptr,                    // No rotation
            posThirdScintillator,                   // Position
            logicmwrap,          // Logical volume to place
            "M_wrap",                // Name
            logicWrld,                  // Mother volume
            false,                      // Not multiple copies
            0,
            false);    



    G4Box* solidScintM = new G4Box ("Minerva", halfScintSizeX_m, halfScintSizeY_m, halfScintSizeZ_m);
    G4LogicalVolume* logicScintM = new G4LogicalVolume(
        solidScintM, pvt, "Minerva");

    physiThirdScintillator = new G4PVPlacement(
        0, 
        G4ThreeVector(0*cm, 0*cm, 0*cm),
        logicScintM,
        "Minerva", 
        logicmwrap,
        false, 
        2,
        false);

    G4Color yellow(1, 1, 0);
    logicScintP->SetVisAttributes(new G4VisAttributes(yellow));
    G4Color blue(0, 0, 1);
    logicScintG->SetVisAttributes(new G4VisAttributes(blue));
    G4Color red(1, 0, 0);
    logicScintM->SetVisAttributes(new G4VisAttributes(red));
    G4Color white = G4Color::White();
    logicmwrap->SetVisAttributes(new G4VisAttributes(white));
    logicpwrap->SetVisAttributes(new G4VisAttributes(white));
    logicgwrap->SetVisAttributes(new G4VisAttributes(white));
        //----------------------------------------------------
    //faccio diventare "sensitive" il mio detector
    //===============================================================
    
    // Create SD instances
    ScintillatorSensitiveDetector* scintSD0 = 
        new ScintillatorSensitiveDetector("Partenope");
    ScintillatorSensitiveDetector* scintSD1 = 
        new ScintillatorSensitiveDetector("Giunone");
    ScintillatorSensitiveDetector* scintSD2 = 
        new ScintillatorSensitiveDetector("Minerva");
    
    // Register with SDManager
    G4SDManager* sdManager = G4SDManager::GetSDMpointer();
    sdManager->AddNewDetector(scintSD0);
    sdManager->AddNewDetector(scintSD1);
    sdManager->AddNewDetector(scintSD2);
    
    // Attach to logical volumes
    logicScintP->SetSensitiveDetector(scintSD0);
    logicScintG->SetSensitiveDetector(scintSD1);
    logicScintM->SetSensitiveDetector(scintSD2);
    
    // ================================================
    
    return physiFirstScintillator;
}

// eventualmente devo inserire logic and physi contenenti 
// lastra alluminio/sale
// G4VPhysicalVolume* DetectorConstruction::ConstructionLastra(){

// }