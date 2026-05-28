// #include "Analysis.hh"
// #include "G4UnitsTable.hh"
// #include "G4SDManager.hh"
// #include "ScintillatorSD.hh"

// Analysis* Analysis::singleton = 0;

// Analysis::Analysis()
// {
// }

// void Analysis::PrepareNewEvent(const G4Event* /*anEvent*/)
// {
// 	//Reset variables relative to this event
// 	thisEventData.totalEnergy = 0.0;
// 	thisEventData.firstHitTime = -1.0;
// 	thisEventData.lastHitTime = -1.0;
// 	thisEventData.numHits = 0;
// 	thisEventData.hitEnergies.clear();
// 	thisEventData.hitTimes.clear();
// 	thisEventData.particleIDs.clear();
// 	thisEventData.trackIDs.clear();
// }

// void Analysis::PrepareNewRun(const G4Run* /*aRun*/)
// {
// 	//Reset variables relative to the run
// 	thisRunTotalEnergy = 0.0;
// 	thisRunNumHits = 0;
// }
// // void Analysis::AddEDepScintillator(G4double edep, G4double time, G4int particleID, G4int trackID)
// // {
// //     thisEventData.totalEnergy += edep;
// //     thisEventData.hitEnergies.push_back(edep);
// //     thisEventData.hitTimes.push_back(time);
// //     thisEventData.particleIDs.push_back(particleID);
// //     thisEventData.trackIDs.push_back(trackID);
// //     thisEventData.numHits++;
    
// //     if (thisEventData.firstHitTime < 0) {
// //         thisEventData.firstHitTime = time;
// //     }
// //     thisEventData.lastHitTime = time;
// // }
// void Analysis::AddEDepScintillator(G4double edep, G4double time, 
//                                    G4int particleID, G4int trackID, G4int copyNo) 
// {
//     thisEventData.totalEnergy += edep;
//     thisEventData.hitEnergies.push_back(edep);
//     thisEventData.hitTimes.push_back(time);
//     thisEventData.particleIDs.push_back(particleID);
//     thisEventData.trackIDs.push_back(trackID);
//     thisEventData.scintillatorIDs.push_back(copyNo); // Store the detector ID
//     thisEventData.numHits++;
    
//     if (thisEventData.firstHitTime < 0.0) {
//         thisEventData.firstHitTime = time;
//     }
//     thisEventData.lastHitTime = time;
// }

// void EventAction::EndOfEvent(const G4Event* event)
// {
//     G4SDManager* sdMngr = G4SDManager::GetSDMpointer();
//     G4HCofThisEvent* HCE = event->GetHCofThisEvent();
//     if(!HCE) return;

//     // Find collections by name
//     G4int id1 = sdMngr->GetCollectionID("ScintSD_PandG/ScintillatorHitCollection");
//     G4int id3 = sdMngr->GetCollectionID("ScintSD_Minerva/ScintillatorHitCollection");

//     auto analysis = Analysis::GetInstance();
//     analysis->PrepareNewEvent(event);

//     // Helper lambda function to parse a collection
//     auto parseCollection = [&](G4int hcID) {
//         if(hcID < 0) return;
//         auto hc = static_cast<ScintillatorHitCollection*>(HCE->GetHC(hcID));
//         if(!hc) return;

//         for(size_t i=0; i<hc->entries(); ++i) {
//             auto hit = (*hc)[i];
//             analysis->AddEDepScintillator(hit->edep, hit->time, hit->particleID, hit->trackID, hit->copyNo);
//         }
//     };

//     parseCollection(id1);
//     parseCollection(id3);

//     analysis->EndOfEvent(event);
// }

// void Analysis::EndOfRun(const G4Run* aRun)
// {
// 	//Some print outs
// 	G4int numEvents = aRun->GetNumberOfEvent();

// 	G4cout << "=================" << G4endl;
// 	G4cout << "Summary for run: " << aRun->GetRunID() << G4endl;
// 	G4cout << "\t Events processed: " << numEvents << G4endl;
// 	G4cout << "\t Average energy in scintillator: " 
// 	       << G4BestUnit(thisRunTotalEnergy/numEvents,"Energy") << G4endl;
// 	G4cout << "\t Average number of hits: " 
// 	       << thisRunNumHits/numEvents << G4endl;
// 	G4cout << "=================" << G4endl;
// }

#include "Analysis.hh"
#include "G4UnitsTable.hh"

Analysis* Analysis::singleton = nullptr;

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
	thisEventData.scintillatorIDs.clear(); 
}

void Analysis::PrepareNewRun(const G4Run* /*aRun*/)
{
	//Reset variables relative to the run
	thisRunTotalEnergy = 0.0;
	thisRunNumHits = 0;
}

void Analysis::AddEDepScintillator(G4double edep, G4double time, G4int particleID, G4int trackID, G4int copyNo) 
{
    thisEventData.totalEnergy += edep;
    thisEventData.hitEnergies.push_back(edep);
    thisEventData.hitTimes.push_back(time);
    thisEventData.particleIDs.push_back(particleID);
    thisEventData.trackIDs.push_back(trackID);
    thisEventData.scintillatorIDs.push_back(copyNo); 
    thisEventData.numHits++;
    
    if (thisEventData.firstHitTime < 0.0) {
        thisEventData.firstHitTime = time;
    }
    thisEventData.lastHitTime = time;
}

void Analysis::EndOfEvent(const G4Event* /*event*/)
{
    // Accumulate event metrics into run summary storage
    thisRunTotalEnergy += thisEventData.totalEnergy;
    thisRunNumHits += thisEventData.numHits;
}

void Analysis::EndOfRun(const G4Run* aRun)
{
	G4int numEvents = aRun->GetNumberOfEvent();
	if(numEvents == 0) return;

	G4cout << "=================" << G4endl;
	G4cout << "Summary for run: " << aRun->GetRunID() << G4endl;
	G4cout << "\t Events processed: " << numEvents << G4endl;
	G4cout << "\t Average energy in scintillator: " 
	       << G4BestUnit(thisRunTotalEnergy/numEvents,"Energy") << G4endl;
	G4cout << "\t Average number of hits: " 
	       << (G4double)thisRunNumHits/numEvents << G4endl;
	G4cout << "=================" << G4endl;
}