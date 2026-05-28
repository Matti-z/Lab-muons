
#include "ScintillatorSD.hh"
#include "G4TouchableHistory.hh"
#include "G4Step.hh"
#include "G4HCofThisEvent.hh"
#include "G4HCtable.hh"
#include "G4UnitsTable.hh"
#include "Analysis.hh"

ScintillatorSensitiveDetector::ScintillatorSensitiveDetector(G4String SDname)
  : G4VSensitiveDetector(SDname)
{
	G4cout<<"Creating SD with name: "<< SDname <<G4endl;
  // 'collectionName' is a protected data member of base class G4VSensitiveDetector.
  // Here we declare the name of the collection we will be using.
    collectionName.insert("ScintillatorHitCollection");
 
  // Note that we may add as many collection names we would wish: ie
  // a sensitive detector can have many collections.
}

ScintillatorSensitiveDetector::~ScintillatorSensitiveDetector()
{}



G4bool ScintillatorSensitiveDetector::ProcessHits(G4Step *step, G4TouchableHistory *)
{
	G4double edep = step->GetTotalEnergyDeposit();
	if (edep == 0.0) return false;
	
	G4double time = step->GetPreStepPoint()->GetGlobalTime();
	G4int particleID = step->GetTrack()->GetDefinition()->GetPDGEncoding();
	G4int trackID = step->GetTrack()->GetTrackID();
	
	// Store all hit info for muon decay analysis
	Analysis::GetInstance()->AddEDepScintillator(edep, time, particleID, trackID);
	
	return true;
}



void ScintillatorSensitiveDetector::Initialize(G4HCofThisEvent* /*HCE*/)
{
}

void ScintillatorSensitiveDetector::EndOfEvent(G4HCofThisEvent*)
{
}

