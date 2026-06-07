
// #include "Analysis.hh"
// #include "G4UnitsTable.hh"
// #include "G4Event.hh"
// #include "EventAction.hh"
// #include <algorithm> //std::sort

// Analysis* Analysis::singleton = nullptr;

// Analysis::Analysis()
// {
// }

// //creo un singolo evento
// void Analysis::PrepareNewEvent(const G4Event* ) // anEvent
// {
// 	//Reset variables relative to this event
// 	thisEventData.totalEnergy = 0.0;
// 	thisEventData.firstHitTime = -1.0; //non so perchè -1
// 	thisEventData.lastHitTime = -1.0; //non so perchè -1
// 	thisEventData.numHits = 0;
// 	thisEventData.hitEnergies.clear();
// 	thisEventData.hitTimes.clear();
// 	thisEventData.particleIDs.clear();
// 	thisEventData.trackIDs.clear();
// 	thisEventData.scintillatorIDs.clear(); 
// }
// //il seguente crea un file di output in teoria, però non lo salva, non so perchè (forse non ho mai avuto un decay?)
// //la sequenza non arriva fino a qui
// void Analysis::PrepareNewRun(const G4Run* aRun)
// {
//     thisRunTotalEnergy = 0.0;
//     thisRunNumHits = 0;
//  //specificare dove salvare i dati
//     G4String filename = "../results/mgp/run_" + std::to_string(aRun->GetRunID()) + ".csv";
//     csvFile.open(filename);
//     csvFileValid = csvFile.is_open();
//     if (!csvFileValid) {
//         G4cout << "WARNING: Could not open " << filename << G4endl;
// }

    
//     // Create clear columns for our logical signature
//     csvFile << "EventID,Coincidence,HitTop,HitMiddle,HitBottom,Decay,DecayTime_ns\n";
// }


// //il seguente *non* salva dati e non guarda solo il decay
// // void Analysis::PrepareNewRun(const G4Run* /*aRun*/)
// // {
// // 	//Reset variables relative to the run
// // 	thisRunTotalEnergy = 0.0;
// // 	thisRunNumHits = 0;
// // }

// void Analysis::AddEDepScintillator(G4double edep, G4double time, G4int particleID, G4int trackID, G4int copyNo)
// { 
//     G4cout << "HIT RECORDED: edep=" << edep << " time=" << time << " layer=" << copyNo << G4endl;
    
//     thisEventData.totalEnergy += edep;
//     thisEventData.hitEnergies.push_back(edep);//what does push_back do?
//     /*push_back() adds an element to the end of a vector. In your code, when you call thisEventData.hitEnergies.push_back(edep), 
//     you're storing the energy of that hit in a dynamic array. 
//     This lets you accumulate variable numbers of hits—you don't need to pre-allocate space; the vector grows as needed.
//     è come .append() di python*/
//     thisEventData.hitTimes.push_back(time);
//     thisEventData.particleIDs.push_back(particleID);
//     thisEventData.trackIDs.push_back(trackID);
//     thisEventData.scintillatorIDs.push_back(copyNo); 
//     thisEventData.numHits++;
    
//     if (thisEventData.firstHitTime < 0.0) {
//         thisEventData.firstHitTime = time;
//     }
//     thisEventData.lastHitTime = time;
// }



// //in un secondo momento vorrei anche salvare tutti i muoni che interagiscono con almeno uno dei tre piani 
// //per controllare le questioni di angolo solido in caso di scintillatori non allineati
// //ci provo

// void Analysis::EndOfEvent(const G4Event* event)
// {
//     thisRunTotalEnergy += thisEventData.totalEnergy;
//     thisRunNumHits += thisEventData.numHits;

//     if (thisEventData.numHits == 0) return;

//     int hitTop = 0;
//     int hitBottom = 0;
//     int hitMiddle = 0;
//     std::vector<G4double> middleTimes;

//     // 1. Sort through all the hits in this specific event
//     for (size_t i = 0; i < thisEventData.numHits; ++i) {
//         G4int layer = thisEventData.scintillatorIDs[i];
//         if (layer == 0) hitTop = 1;
//         if (layer == 2) hitBottom = 1;
//         if (layer == 1) {
//             hitMiddle = 1;
//             middleTimes.push_back(thisEventData.hitTimes[i]);
//         }
//     }

//     // 2. Determine coincidence type
//     int coincidenceCount = hitTop + hitMiddle + hitBottom;
//     G4String coincidenceType = "SINGLE";
//     if (coincidenceCount == 3) {
//         coincidenceType = "TRIPLE";
//     } else if (coincidenceCount == 2) {
//         coincidenceType = "DOUBLE";
//     }

//     // 3. Look for the delayed decay electron in the middle scintillator
//     G4double decayTime = -1.0; 
//     G4String decaySignature = "False";
    
//     if (middleTimes.size() >= 2) {
//         std::sort(middleTimes.begin(), middleTimes.end());
//         G4double firstTime = middleTimes.front();
//         G4double lastTime = middleTimes.back();
        
//         if ((lastTime - firstTime) > 50.0) {
//             decayTime = lastTime - firstTime;
//             decaySignature = "True";
//         }
//     }

//     // 4. Write to CSV
//     csvFile << event->GetEventID() << ","
//             << coincidenceType << ","
//             << hitTop << ","
//             << hitMiddle << ","
//             << hitBottom << ","
//             << decaySignature << ","
//             << decayTime << "\n";
//             // csvfile.flush();
// }




// void Analysis::EndOfRun(const G4Run* aRun)
// {
// 	if (csvFile.is_open()) {
// 		csvFile.close(); // Close file stream safely
// 	}

// 	G4int numEvents = aRun->GetNumberOfEvent();
// 	if(numEvents == 0) return;

// 	G4cout << "=================" << G4endl;
// 	G4cout << "Summary for run: " << aRun->GetRunID() << G4endl;
// 	G4cout << "\t Events processed: " << numEvents << G4endl;
// 	G4cout << "\t Average energy in scintillator: " 
// 	       << G4BestUnit(thisRunTotalEnergy/numEvents,"Energy") << G4endl;
// 	G4cout << "\t Average number of hits: " 
// 	       << (G4double)thisRunNumHits/numEvents << G4endl;
// 	G4cout << "=================" << G4endl;
// }
#include "Analysis.hh"
#include "G4UnitsTable.hh"
#include "G4Event.hh"
#include "G4Run.hh"
#include "EventAction.hh"
#include <algorithm> // std::sort

Analysis* Analysis::singleton = nullptr;

Analysis::Analysis()
{
}

// Prepare data containers for a brand new event frame
void Analysis::PrepareNewEvent(const G4Event* ) 
{
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

// Set up file handling at the start of a simulation run
void Analysis::PrepareNewRun(const G4Run* aRun)
{
    thisRunTotalEnergy = 0.0;
    thisRunNumHits = 0;

    // Open file streaming
    G4String filename = "../results/pmg/1/run_" + std::to_string(aRun->GetRunID()) + ".csv";
    csvFile.open(filename);
    csvFileValid = csvFile.is_open();
    
    if (!csvFileValid) {
        G4cout << "WARNING: Could not open " << filename << G4endl;
    }
    
    // Header tracking configuration based on spatial positioning:
    // Copy 0 = Top (Partenope), Copy 2 = Middle (Minerva), Copy 1 = Bottom (Giunone)
    if (csvFileValid) {
        csvFile << "EventID,Coincidence,Partenope,Minerva,Giunone,Decay,DecayTime_ns\n";
    }
}

void Analysis::AddEDepScintillator(G4double edep, G4double time, G4int particleID, G4int trackID, G4int copyNo)
{ 
    G4cout << "HIT RECORDED: edep=" << edep << " time=" << time << " layer=" << copyNo << G4endl;
    
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

void Analysis::EndOfEvent(const G4Event* event)
{
    thisRunTotalEnergy += thisEventData.totalEnergy;
    thisRunNumHits += thisEventData.numHits;

    if (!csvFileValid) return;
    if (thisEventData.numHits == 0) return;

    int hitTop = 0;
    int hitMiddle = 0;
    int hitBottom = 0;
    std::vector<G4double> middleTimes;

    // 1. Process hits based on actual physical layout
    // Copy 0 = Partenope (Z = 0) -> Top
    // Copy 2 = Minerva (Z = 9.9 cm) -> Middle
    // Copy 1 = Giunone (Z = 14.3 cm) -> Bottom
    for (size_t i = 0; i < thisEventData.numHits; ++i) {
        G4int layer = thisEventData.scintillatorIDs[i];
        if (layer == 0) {
            hitTop = 1;
        }
        else if (layer == 2) { 
            hitMiddle = 1;
            middleTimes.push_back(thisEventData.hitTimes[i]);
        }
        else if (layer == 1) {
            hitBottom = 1;
        }
    }

    // 2. Classify coincidence configuration
    int coincidenceCount = hitTop + hitMiddle + hitBottom;
    G4String coincidenceType = "SINGLE";
    if (coincidenceCount == 3) {
        coincidenceType = "TRIPLE";
    } else if (coincidenceCount == 2) {
        coincidenceType = "DOUBLE";
    }

    // 3. Track delayed decay signatures inside the true physical middle volume (Minerva)
    G4double decayTime = -1.0; 
    G4String decaySignature = "False";
    
    if (middleTimes.size() >= 2) {
        std::sort(middleTimes.begin(), middleTimes.end());
        G4double firstTime = middleTimes.front();
        G4double lastTime = middleTimes.back();
        
        // Decay signature filtering: checks if subsequent hits arrived late 
        if ((lastTime - firstTime) > 50.0) {
            decayTime = lastTime - firstTime;
            decaySignature = "True";
        }
    }

    // 4. Output dataset line writing and explicit buffer flushing
    csvFile << event->GetEventID() << ","
            << coincidenceType << ","
            << hitTop << ","
            << hitMiddle << ","
            << hitBottom << ","
            << decaySignature << ","
            << decayTime << "\n";
            
    csvFile.flush(); // Forces writing immediately to disk so you do not lose data if crashed
}

void Analysis::EndOfRun(const G4Run* aRun)
{
    if (csvFile.is_open()) {
        csvFile.close(); 
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