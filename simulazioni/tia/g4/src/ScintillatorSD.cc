#include "ScintillatorSD.hh"
#include "G4TouchableHistory.hh"
#include "G4Step.hh"
#include "G4HCofThisEvent.hh"
#include "G4SDManager.hh"
#include "G4UnitsTable.hh"

G4ThreadLocal G4Allocator<ScintillatorHit>* ScintillatorHitAllocator = nullptr;

ScintillatorSensitiveDetector::ScintillatorSensitiveDetector(G4String SDname)
  : G4VSensitiveDetector(SDname)
{
  collectionName.insert("ScintillatorHitCollection");
}

ScintillatorSensitiveDetector::~ScintillatorSensitiveDetector() {}

// Called automatically at the start of every event
void ScintillatorSensitiveDetector::Initialize(G4HCofThisEvent* HCE)
{
  G4cout << ">>> Initialize called for SD: " << GetName() << G4endl;
  fHitsCollection = new ScintillatorHitCollection(SensitiveDetectorName, collectionName[0]);
  
  // Let the SD manager handle the collection ID properly
  HCE->AddHitsCollection(
    G4SDManager::GetSDMpointer()->GetCollectionID(fHitsCollection),
    fHitsCollection
  );
  G4int collID = G4SDManager::GetSDMpointer()->GetCollectionID(fHitsCollection);
  G4cout << ">>> Collection created: " << SensitiveDetectorName << "/" << collectionName[0] 
         << " with ID: " << collID << G4endl;
}


// Called automatically every time a particle takes a step inside the volume
G4bool ScintillatorSensitiveDetector::ProcessHits(G4Step *step, G4TouchableHistory *)
{
  // G4cout << ">>> ProcessHits called in " << GetName() << G4endl; debug comme, works
  G4double edep = step->GetTotalEnergyDeposit();
  if (edep == 0.0) return false; // Ignore steps with no energy deposition
  
  // Create a hit object
  ScintillatorHit* newHit = new ScintillatorHit();
  
  // Fill hit attributes
  newHit->edep       = edep;
  newHit->time       = step->GetPreStepPoint()->GetGlobalTime();
  newHit->pos        = step->GetPreStepPoint()->GetPosition();
  newHit->particleID = step->GetTrack()->GetDefinition()->GetPDGEncoding();
  newHit->trackID    = step->GetTrack()->GetTrackID();
  
  // Get the copy number (0 = Partenope, 1 = Giunone, 3 = Minerva)
  newHit->copyNo     = step->GetPreStepPoint()->GetTouchable()->GetCopyNumber();
  
  // Push the hit into the collection
  fHitsCollection->insert(newHit);
  
  return true;
}

void ScintillatorSensitiveDetector::EndOfEvent(G4HCofThisEvent*) {}