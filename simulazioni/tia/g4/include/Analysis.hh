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
};

/*!
 * \brief Analysis class for single scintillator detector
 * Tracks energy deposition and timing for muon decay detection.
 */
class Analysis {
public:
	//! Singleton pattern
	static Analysis* GetInstance() {
		if (Analysis::singleton == NULL) 
			Analysis::singleton = new Analysis();
		return Analysis::singleton;
	}
	
	//! Destructor
	virtual ~Analysis() {}
	
	//! Should be called at the beginning of an event
	void PrepareNewEvent(const G4Event* anEvent);
	
	//! Should be called at the end of an event
	void EndOfEvent(const G4Event* anEvent);
	
	//! Should be called at the beginning of a run
	void PrepareNewRun(const G4Run* aRun);
	
	//! Should be called at the end of a run
	void EndOfRun(const G4Run* aRun);
	
	//! Add energy and time deposit in scintillator
	void AddEDepScintillator(G4double edep, G4double time, 
	                         G4int particleID, G4int trackID) {
		thisEventData.totalEnergy += edep;
		thisEventData.hitEnergies.push_back(edep);
		thisEventData.hitTimes.push_back(time);
		thisEventData.particleIDs.push_back(particleID);
		thisEventData.trackIDs.push_back(trackID);
		thisEventData.numHits++;
		
		// Update first/last hit times
		if (thisEventData.firstHitTime < 0.0) {
			thisEventData.firstHitTime = time;
		}
		thisEventData.lastHitTime = time;
	}
	
	//! Get hit data for current event
	const ScintillatorEventData& GetEventData() const {
		return thisEventData;
	}
	
private:
	//! Private constructor: part of singleton pattern
	Analysis();
	
	//! Singleton static instance
	static Analysis* singleton;
	
	//! Hit data for current event
	ScintillatorEventData thisEventData;
	
	//! Accumulated data for run
	G4double thisRunTotalEnergy = 0.0;
	G4int thisRunNumHits = 0;
};

#endif /* ANALYSIS_HH_ */
