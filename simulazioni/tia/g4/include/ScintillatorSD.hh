#ifndef ScintillatorSensitiveDetector_hh
#define ScintillatorSensitiveDetector_hh 1

#include "G4VSensitiveDetector.hh"
#include "G4VHit.hh"
#include "G4THitsCollection.hh"
#include "G4Allocator.hh"
#include "G4ThreeVector.hh"

class G4Step;
class G4TouchableHistory;
class G4HCofThisEvent;

// 1. Define the Hit Object
class ScintillatorHit : public G4VHit
{
public:
  ScintillatorHit() = default;
  ~ScintillatorHit() override = default;
  ScintillatorHit(const ScintillatorHit&) = default;
  ScintillatorHit& operator=(const ScintillatorHit&) = default;
  
  G4bool operator==(const ScintillatorHit& right) const { return (this == &right); }
  
  // Custom allocator for performance (fixes compilation error)
  inline void* operator new(size_t);
  inline void operator delete(void* aHit);

public:
  G4double edep = 0.0;           // Energy deposited
  G4ThreeVector pos;             // Position of hit
  G4double time = 0.0;           // Time of hit
  G4int particleID = 0;          // PDG encoding
  G4int trackID = 0;             // Track ID
  G4int copyNo = -1;             // <--- CRITICAL: Identifies which scintillator plane was hit
};

// 2. Define the Collection Type
using ScintillatorHitCollection = G4THitsCollection<ScintillatorHit>;

// Thread-local allocator instantiation
extern G4ThreadLocal G4Allocator<ScintillatorHit>* ScintillatorHitAllocator;

inline void* ScintillatorHit::operator new(size_t)
{
  if(!ScintillatorHitAllocator) ScintillatorHitAllocator = new G4Allocator<ScintillatorHit>;
  return (void*) ScintillatorHitAllocator->MallocSingle();
}

inline void ScintillatorHit::operator delete(void* aHit)
{
  ScintillatorHitAllocator->FreeSingle((ScintillatorHit*) aHit);
}

// 3. Define the Sensitive Detector
class ScintillatorSensitiveDetector : public G4VSensitiveDetector
{
public:
  ScintillatorSensitiveDetector(G4String SDname);
  ~ScintillatorSensitiveDetector() override;

  G4bool ProcessHits(G4Step *step, G4TouchableHistory *ROhist) override;
  void Initialize(G4HCofThisEvent* HCE) override;
  void EndOfEvent(G4HCofThisEvent* HCE) override;

private:
  ScintillatorHitCollection* fHitsCollection = nullptr;
};

#endif