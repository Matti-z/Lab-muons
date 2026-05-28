//lib per far diventare i detector sensitive
#ifndef ScintillatorSensitiveDetector_hh
#define ScintillatorSensitiveDetector_hh 1

#include "G4VSensitiveDetector.hh"


class G4Step;
class G4TouchableHistory;
class G4HCofThisEvent;           // <<- means "H(it) C(ollections) of This Event"


/*!
 * Defines sensitive part of scintillator detector geometry.
 *
 * Stores Hits with 
 *  * deposited energy
 *  * position
 * in <i>Hit Collections of This Event</i>
 *
 */

class ScintillatorSensitiveDetector : public G4VSensitiveDetector
{
public:
  /// Constructor
  ScintillatorSensitiveDetector(G4String SDname);
  /// Destructor
  ~ScintillatorSensitiveDetector();

public:
  /// @name methods from base class G4VSensitiveDetector
  //@{
  /// Mandatory base class method : it must to be overloaded:
   G4bool ProcessHits(G4Step *step, G4TouchableHistory *ROhist);

  /// (optional) method of base class G4VSensitiveDetector
  void Initialize(G4HCofThisEvent* HCE);
  /// (optional) method of base class G4VSensitiveDetector
  void EndOfEvent(G4HCofThisEvent* HCE);
  //@}

private:
};


class ScintillatorHit : public G4VHit
{
public:
  ScintillatorHit() = default;
  ~ScintillatorHit() override = default;
  
  ScintillatorHit(const ScintillatorHit&) = default;
  ScintillatorHit& operator=(const ScintillatorHit&) = default;
  
  G4bool operator==(const ScintillatorHit& right) const
  {
    return (this == &right);
  }
  
  inline void* operator new(size_t);
  inline void operator delete(void*);

public:
  G4double edep = 0.0;           // Energy deposited
  G4ThreeVector pos;              // Position of hit
  G4double time = 0.0;            // Time of hit
  G4int particleID = 0;           // Type of particle
  G4int trackID = 0;              // Track identifier
};


#endif
