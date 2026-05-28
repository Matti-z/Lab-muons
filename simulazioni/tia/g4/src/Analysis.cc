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
#include <algorithm> //std::sort

Analysis* Analysis::singleton = nullptr;

Analysis::Analysis()
{
}

//creo un singolo evento
void Analysis::PrepareNewEvent(const G4Event* ) // anEvent
{
	//Reset variables relative to this event
	thisEventData.totalEnergy = 0.0;
	thisEventData.firstHitTime = -1.0; //non so perchè -1
	thisEventData.lastHitTime = -1.0; //non so perchè -1
	thisEventData.numHits = 0;
	thisEventData.hitEnergies.clear();
	thisEventData.hitTimes.clear();
	thisEventData.particleIDs.clear();
	thisEventData.trackIDs.clear();
	thisEventData.scintillatorIDs.clear(); 
}
//il seguente crea un file di output in teoria, però non lo salva, non so perchè (forse non ho mai avuto un decay?)
void Analysis::PrepareNewRun(const G4Run* aRun)
{
    thisRunTotalEnergy = 0.0;
    thisRunNumHits = 0;

    G4String filename = "run_" + std::to_string(aRun->GetRunID()) + ".csv";
    csvFile.open(filename);
    
    // Create clear columns for our logical signature
    csvFile << "EventID,HitTop,HitMiddle,HitBottom,DecayTime_ns\n";
}


//il seguente *non* salva dati e non guarda solo il decay
// void Analysis::PrepareNewRun(const G4Run* /*aRun*/)
// {
// 	//Reset variables relative to the run
// 	thisRunTotalEnergy = 0.0;
// 	thisRunNumHits = 0;
// }

void Analysis::AddEDepScintillator(G4double edep, G4double time, G4int particleID, G4int trackID, G4int copyNo) 
{ //i don't know what these functions do
    thisEventData.totalEnergy += edep;
    thisEventData.hitEnergies.push_back(edep);//what does push_back do?
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


//il seguente non discrimina il decay
// void Analysis::EndOfEvent(const G4Event* /*event*/)
// {
//     // Accumulate event metrics into run summary storage
//     thisRunTotalEnergy += thisEventData.totalEnergy;
//     thisRunNumHits += thisEventData.numHits;
// }



//il seguente discrimina il decay
void Analysis::EndOfEvent(const G4Event* event)
{
    thisRunTotalEnergy += thisEventData.totalEnergy;
    thisRunNumHits += thisEventData.numHits;

    if (thisEventData.numHits == 0) return;

    int hitTop = 0;
    int hitBottom = 0;
    int hitMiddle = 0;
    std::vector<G4double> middleTimes;

    // 1. Sort through all the hits in this specific event
    for (size_t i = 0; i < thisEventData.numHits; ++i) {
        G4int layer = thisEventData.scintillatorIDs[i];
        if (layer == 0) hitTop = 1;
        if (layer == 3) hitBottom = 1;
        if (layer == 1) {
            hitMiddle = 1;
            middleTimes.push_back(thisEventData.hitTimes[i]);
        }
    }

    // 2. Look for the delayed decay electron in the middle scintillator
    G4double decayTime = -1.0; 
    
    if (middleTimes.size() >= 2) {
        // Geant4 tracks time in nanoseconds by default.
        // We sort the hit times to find the first hit (muon) and last hit (electron)
        std::sort(middleTimes.begin(), middleTimes.end());
        G4double firstTime = middleTimes.front();
        G4double lastTime = middleTimes.back();
        
        // If the gap is greater than 50 ns, it's a decay, not just a single particle stepping
        if ((lastTime - firstTime) > 50.0) {
            decayTime = lastTime - firstTime;
        }
    }

    // 3. Write to CSV
    csvFile << event->GetEventID() << ","
            << hitTop << ","
            << hitMiddle << ","
            << hitBottom << ","
            << decayTime << "\n";
}

//in un secondo momento vorrei anche salvare tutti i muoni che interagiscono con almeno uno dei tre piani 
//per controllare le questioni di angolo solido in caso di scintillatori non allineati

void Analysis::EndOfRun(const G4Run* aRun)
{
	if (csvFile.is_open()) {
		csvFile.close(); // Close file stream safely
	}

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