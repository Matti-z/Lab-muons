// 

#ifndef ANALYSIS_HH_
#define ANALYSIS_HH_

#include "G4Event.hh"
#include "G4Run.hh"
#include <vector>

/*!
 * \brief Structure to store scintillator hit data
 */
struct ScintillatorEventData {
  G4double totalEnergy = 0.0;
  G4double firstHitTime = -1.0;        // Time of first hit
  G4double lastHitTime = -1.0;         // Time of last hit
  G4int numHits = 0;
  std::vector<G4double> hitEnergies;   // Individual hit energies
  std::vector<G4double> hitTimes;      // Individual hit times
  std::vector<G4int> particleIDs;      // Type of each particle
  std::vector<G4int> trackIDs;         // Track ID of each hit
  std::vector<G4int> scintillatorIDs;  // Stores copyNo (0, 1, or 3) for each hit
};

/*!
 * \brief Analysis class for single scintillator detector
 */
class Analysis {
public:
	//! Singleton pattern
	static Analysis* GetInstance() {
		if (Analysis::singleton == nullptr) 
			Analysis::singleton = new Analysis();
		return Analysis::singleton;
	}
	
	virtual ~Analysis() {}
	
	void PrepareNewEvent(const G4Event* anEvent);
	void EndOfEvent(const G4Event* anEvent);
	void PrepareNewRun(const G4Run* aRun);
	void EndOfRun(const G4Run* aRun);
	
	//! Function declaration (implemented in Analysis.cc)
	void AddEDepScintillator(G4double edep, G4double time, 
	                         G4int particleID, G4int trackID, G4int copyNo);
	
	const ScintillatorEventData& GetEventData() const {
		return thisEventData;
	}
	
private:
	Analysis();
	static Analysis* singleton;
	
	ScintillatorEventData thisEventData;
	G4double thisRunTotalEnergy = 0.0;
	G4int thisRunNumHits = 0;
};

#endif /* ANALYSIS_HH_ */