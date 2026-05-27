#ifndef DetectorConstruction_h
#define DetectorConstruction_h

#include "G4VUserDetectorConstruction.hh"
#include "G4ThreeVector.hh"

#include "globals.hh"
#include "G4VUserDetectorConstruction.hh"

class G4LogicalVolume;
class G4VPhysicalVolume;
class G4Material;

//-------------------------------------------

class DetectorConstruction : public G4VUserDetectorConstruction{
    public: 
    DetectorConstruction(); //costruttore
    ~DetectorConstruction(); //distruttore

    public: 
    G4VPhysicalVolume* Construct(); //construct geometry
    G4ThreeVector FirstScintillatorPosition() const  { return posFirstScintillator; }
    G4ThreeVector SecondScintillatorPosition() const { return posSecondScintillator; }
    G4ThreeVector ThirdScintillatorPosition() const { return posThirdScintillator; }

    G4ThreeVector SetFirstScintillatorPosition(const G4ThreeVector & pos) { return posFirstScintillator=pos; }
    G4ThreeVector SetSecondScintillatorPosition(const G4ThreeVector & pos) { return posSecondScintillator=pos; }
    G4ThreeVector SetThirdScintillatorPosition(const G4ThreeVector & pos) { return posThirdScintillator=pos; }
    

    private:
    void DefineMaterials(); //the needed materials
    void ComputeParameters();//initialize geom parameters
    G4VPhysicalVolume* ConstructScintillator();
    G4VPhysicalVolume* ConstrucLastra();

    private:
    G4Material* air;
    // G4Material* devo vedere di cosa sono fatti scintillatori
    G4Material* pvt;
    G4Material* al;
    G4Material* Na;
    G4Material* I;


    //mother volume
    G4LogicalVolume* logicWrld;
    G4double halfWrldLength;


    //other volumes
     G4VPhysicalVolume* physiFirstScintillator;
  //! 2nd scint plane
    G4VPhysicalVolume* physiSecondScintillator;
  //! 3rd scint plane
    G4VPhysicalVolume* physiThirdScintillator;
    //eventualmente lastra
    G4VPhysicalVolume* physilastra;


    G4ThreeVector posFirstScintillator;
    G4ThreeVector posSecondScintillator;
    G4ThreeVector posThirdScintillator;
    G4double sizez_scint;
    G4double sizey_scint;
    G4double sizex_scint;
    G4double sizez_scint_m;
    G4double sizey_scint_m;
    G4double sizex_scint_m;
    G4ThreeVector posLastra;
};
#endif