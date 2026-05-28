#include "Analysis.hh"
#include "G4UnitsTable.hh"

Analysis* Analysis::singleton = 0;

Analysis::Analysis()
{
}

void Analysis::PrepareNewEvent(const G4Event* /*anEvent*/)
{
	//Reset variables relative to this event
	thisEventData.totalEnergy = 0.0;
	thisEventData.firstHitTime = -1.0;
	thisEventData.lastHitTime = -1.0;
	thisEventData.numHits = 0;
	thisEventData.hitEnergies.clear();
	thisEventData.hitTimes.clear();
	thisEventData.particleIDs.clear();
	thisEventData.trackIDs.clear();
}

void Analysis::PrepareNewRun(const G4Run* /*aRun*/)
{
	//Reset variables relative to the run
	thisRunTotalEnergy = 0.0;
	thisRunNumHits = 0;
}
// void Analysis::AddEDepScintillator(G4double edep, G4double time, G4int particleID, G4int trackID)
// {
//     thisEventData.totalEnergy += edep;
//     thisEventData.hitEnergies.push_back(edep);
//     thisEventData.hitTimes.push_back(time);
//     thisEventData.particleIDs.push_back(particleID);
//     thisEventData.trackIDs.push_back(trackID);
//     thisEventData.numHits++;
    
//     if (thisEventData.firstHitTime < 0) {
//         thisEventData.firstHitTime = time;
//     }
//     thisEventData.lastHitTime = time;
// }
void Analysis::EndOfEvent(const G4Event* /*anEvent*/)
{
	//Accumulate over the run
	thisRunTotalEnergy += thisEventData.totalEnergy;
	thisRunNumHits += thisEventData.numHits;
}

void Analysis::EndOfRun(const G4Run* aRun)
{
	//Some print outs
	G4int numEvents = aRun->GetNumberOfEvent();

	G4cout << "=================" << G4endl;
	G4cout << "Summary for run: " << aRun->GetRunID() << G4endl;
	G4cout << "\t Events processed: " << numEvents << G4endl;
	G4cout << "\t Average energy in scintillator: " 
	       << G4BestUnit(thisRunTotalEnergy/numEvents,"Energy") << G4endl;
	G4cout << "\t Average number of hits: " 
	       << thisRunNumHits/numEvents << G4endl;
	G4cout << "=================" << G4endl;
}
