#include "DetectorConstruction.hh"
#include "DetectorMessenger.hh"
#include "G4Material.hh"
#include "G4Box.hh"
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
#include "ScintillatorSD.hh"
#include "G4SubtractionSolid.hh"
#include "G4OpticalSurface.hh"
#include "G4LogicalSkinSurface.hh"

DetectorConstruction::DetectorConstruction()
   : scint1_YOffset(0.0),
     scint2_YOffset(0.0),
     scint3_YOffset(0.0),
     detectorMessenger(nullptr)
{
    DefineMaterials();
    ComputeParameters();
    detectorMessenger = new DetectorMessenger(this);
}

DetectorConstruction::~DetectorConstruction(){
    delete detectorMessenger;
}

void DetectorConstruction::DefineMaterials(){
    G4NistManager* man = G4NistManager::Instance();
    man->SetVerbose(1);

    pvt = man->FindOrBuildMaterial("G4_PLASTIC_SC_VINYLTOLUENE");
    air = man->FindOrBuildMaterial("G4_AIR");
    al = man->FindOrBuildMaterial("G4_Al");
}

void DetectorConstruction::ComputeParameters(){
    halfWrldLength = 2 * m;

    posFirstScintillator = G4ThreeVector(0., scint1_YOffset, 0.);
    posSecondScintillator = G4ThreeVector(0., scint2_YOffset, (8.4+(3/2))* cm); 
    posThirdScintillator = G4ThreeVector(0., scint3_YOffset, (12.8+(3/2))* cm);
}

G4VPhysicalVolume* DetectorConstruction::Construct(){
    ComputeParameters();
    // G4cout << "Computed tolerance = "
    //        << G4GeometryTolerance::GetInstance()->GetSurfaceTolerance()/cm
    //        << " cm" << G4endl;

    G4Box* solidWrld = new G4Box("World", halfWrldLength, halfWrldLength, halfWrldLength);
    logicWrld = new G4LogicalVolume(solidWrld, air, "World", 0, 0, 0);

    G4VPhysicalVolume* physiWrld = new G4PVPlacement(
        0,                  // no rotation
        G4ThreeVector(),    // at origin
        logicWrld,          // logical volume
        "World",            // name
        0,                  // no mother volume
        false,              // no boolean operations
        0);                 // copy number

    ConstructScintillator();

    // Visualization attributes
    G4VisAttributes* invisAttr = new G4VisAttributes();
    invisAttr->SetVisibility(false);
    logicWrld->SetVisAttributes(invisAttr);

    return physiWrld;
}

G4VPhysicalVolume* DetectorConstruction::ConstructScintillator(){
    // Define dimensions
    sizex_scint = (80 - 0.0012) * cm;
    sizey_scint = (30 - 0.0012) * cm;
    sizez_scint = (3 - 0.0012) * cm;
    sizex_scint_m = (80 - 0.0012) * cm;
    sizey_scint_m = (30 - 0.0012) * cm;
    sizez_scint_m = (2 - 0.0012) * cm;
    
    G4double halfScintSizeX = sizex_scint / 2.;
    G4double halfScintSizeY = sizey_scint / 2.;
    G4double halfScintSizeZ = sizez_scint / 2.;
    G4double halfScintSizeX_m = sizex_scint_m / 2.;
    G4double halfScintSizeY_m = sizey_scint_m / 2.;
    G4double halfScintSizeZ_m = sizez_scint_m / 2.;
    
    // Define optical surface for aluminum foil
    G4OpticalSurface* alFoilSurface = new G4OpticalSurface("AlFoilSurface");
    alFoilSurface->SetType(dielectric_metal);
    alFoilSurface->SetFinish(polished);
    alFoilSurface->SetModel(glisur);

    // Add reflectivity properties
    G4MaterialPropertiesTable* foilMPT = new G4MaterialPropertiesTable();
    G4double photonEnergy[] = {10.0*eV, 0.5*MeV};
    G4double reflectivity[] = {0.95, 0.95}; 
    foilMPT->AddProperty("REFLECTIVITY", photonEnergy, reflectivity, 2);
    alFoilSurface->SetMaterialPropertiesTable(foilMPT);

    // --- PARTENOPE (First Scintillator) ---
    G4Box* solidScintPandG = new G4Box("Partenope", halfScintSizeX, halfScintSizeY, halfScintSizeZ);
    G4LogicalVolume* logicScintP = new G4LogicalVolume(
        solidScintPandG, pvt, "LogicPartenope");
        
    physiFirstScintillator = new G4PVPlacement(nullptr,
        posFirstScintillator,
        logicScintP,
        "Partenope",
        logicWrld,
        false,
        0,
        false);

    new G4LogicalSkinSurface("Partenope_Skin", logicScintP, alFoilSurface);

    // --- GIUNONE (Second Scintillator) ---
    G4LogicalVolume* logicScintG = new G4LogicalVolume(
        solidScintPandG, pvt, "LogicGiunone");
            
    physiSecondScintillator = new G4PVPlacement(
        nullptr,
        posSecondScintillator,
        logicScintG,
        "Giunone",
        logicWrld,
        false,
        1,
        false);

    new G4LogicalSkinSurface("Giunone_Skin", logicScintG, alFoilSurface);

    // --- MINERVA (Third Scintillator with Aluminum Wrap) ---
    // G4Box* outer_m = new G4Box("mwrap_outer", 40*cm, 15*cm, 1*cm);
    // G4Box* inner_m = new G4Box("mwrap_inner", 
    //     (40 - 0.0006)*cm, 
    //     (15 - 0.0006)*cm,
    //     (1 - 0.0006)*cm);
    
    // G4SubtractionSolid* hollow_m = new G4SubtractionSolid("hollow_m",
    //     outer_m,
    //     inner_m,
    //     0,
    //     G4ThreeVector(0, 0, 0));
    
    // G4LogicalVolume* logicmwrap = new G4LogicalVolume(
    //     hollow_m, al, "LogicMinervaWrap");

    // new G4LogicalSkinSurface("MinervaWrap_Skin", logicmwrap, alFoilSurface);
    
    // physimwrap = new G4PVPlacement(nullptr,
    //     posThirdScintillator,
    //     logicmwrap,
    //     "MinervaWrap",
    //     logicWrld,
    //     false,
    //     0,
    //     false);

    // G4Box* solidScintM = new G4Box("Minerva", halfScintSizeX_m, halfScintSizeY_m, halfScintSizeZ_m);
    // G4LogicalVolume* logicScintM = new G4LogicalVolume(
    //     solidScintM, pvt, "LogicMinerva");

    // physiThirdScintillator = new G4PVPlacement(
    //     nullptr,
    //     G4ThreeVector(0, 0, 0),
    //     logicScintM,
    //     "Minerva",
    //     logicmwrap,
    //     false,
    //     2,
    //     false);

    // new G4LogicalSkinSurface("Minerva_Skin", logicScintM, alFoilSurface);
    //=======================now minerva without wrap===================================
    // =========================================================================
    // CONFIGURATION 1: MINERVA WITHOUT METAL SKIN (BARE SCINTILLATOR)
    // =========================================================================

    // Create the bare Minerva scintillator solid and logical volume
    G4Box* solidScintM = new G4Box("Minerva", halfScintSizeX_m, halfScintSizeY_m, halfScintSizeZ_m);
    G4LogicalVolume* logicScintM = new G4LogicalVolume(solidScintM, pvt, "LogicMinerva");

    // Place Minerva DIRECTLY into the world volume (no aluminum box container)
    physiThirdScintillator = new G4PVPlacement(
        nullptr,
        posThirdScintillator,  // Uses its global position directly
        logicScintM,
        "Minerva",
        logicWrld,             // Mother volume is World
        false,
        2,                     // Copy number 2
        false);
    
    new G4LogicalSkinSurface("Minerva_Skin", logicScintM, alFoilSurface);

    // --- Visualization ---
    logicScintP->SetVisAttributes(new G4VisAttributes(G4Colour::Yellow()));
    logicScintG->SetVisAttributes(new G4VisAttributes(G4Colour::Blue()));
    logicScintM->SetVisAttributes(new G4VisAttributes(G4Colour::Red()));

    // --- Sensitive Detectors ---
    ScintillatorSensitiveDetector* scintSD0 = 
        new ScintillatorSensitiveDetector("Partenope");
    ScintillatorSensitiveDetector* scintSD1 = 
        new ScintillatorSensitiveDetector("Giunone");
    ScintillatorSensitiveDetector* scintSD2 = 
        new ScintillatorSensitiveDetector("Minerva");
    
    G4SDManager* sdManager = G4SDManager::GetSDMpointer();
    sdManager->AddNewDetector(scintSD0);
    sdManager->AddNewDetector(scintSD1);
    sdManager->AddNewDetector(scintSD2);
    
    logicScintP->SetSensitiveDetector(scintSD0);
    logicScintG->SetSensitiveDetector(scintSD1);
    logicScintM->SetSensitiveDetector(scintSD2);
    
    return physiFirstScintillator;
}
