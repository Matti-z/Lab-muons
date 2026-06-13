#include "Analysis.hh"
#include "G4UnitsTable.hh"
#include "G4Event.hh"
#include "G4Run.hh"
#include "EventAction.hh"
#include <algorithm> // std::sort
#include "G4SystemOfUnits.hh"

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
    G4String filename = "../results/mgp/cos_2_3/run_" + std::to_string(aRun->GetRunID()) + ".csv";
    csvFile.open(filename);
    csvFileValid = csvFile.is_open();
    
    if (!csvFileValid) {
        G4cerr << "ERROR: Could not open file: " << filename << G4endl;
        return;  // Exit early if file fails to open
    }
    
    G4cout << "Successfully opened CSV file: " << filename << G4endl;
    
    csvFile << "EventID,Coincidence,HitTop,HitMiddle,HitBottom,Decay,DecayTime_ns\n";
    csvFile.flush();
}

void Analysis::AddEDepScintillator(G4double edep, G4double time, G4int particleID, 
                                    G4int trackID, G4int copyNo)
{ 
    // G4cout << "HIT RECORDED: edep=" << edep/MeV << " MeV, time=" 
    //        << time/ns << " ns, detector=" << copyNo << G4endl;
    
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

    // Skip if file not valid or no hits recorded
    if (!csvFileValid ) {
        return;
    }

    int hitTop = 0;
    int hitMiddle = 0;
    int hitBottom = 0;
    std::vector<G4double> middleTimes;

    // 1. Process hits based on actual physical layout
    // Copy 0 = Partenope  -> bottom
    // Copy 2 = Minerva  -> top
    // Copy 1 = Giunone  -> mid
    for (size_t i = 0; i < thisEventData.numHits; ++i) {
        G4int layer = thisEventData.scintillatorIDs[i];
        
        if (layer == 2) {
            hitTop = 1;
        }
        if (layer == 1) { 
            hitMiddle = 1;
            middleTimes.push_back(thisEventData.hitTimes[i]);
        }
        if (layer == 0) {  
            hitBottom = 1;
        }
    }

    // 2. Classify coincidence configuration
    int coincidenceCount = hitTop + hitMiddle + hitBottom;
    G4String coincidenceType = "NONE"; // Default to NONE instead of SINGLE
    
    if (coincidenceCount == 3) {
        coincidenceType = "TRIPLE";
    } else if (coincidenceCount == 2) {
        coincidenceType = "DOUBLE";
    } else if (coincidenceCount == 1) {
        coincidenceType = "SINGLE";
    }

    // 3. Track delayed decay signatures in the middle scintillator (Minerva only)
    G4double decayTime = -1.0; 
    G4String decaySignature = "False";
    
    // Requires at least 2 hits in middle layer to identify decay signature
    if (middleTimes.size() >= 2) {
        std::sort(middleTimes.begin(), middleTimes.end());
        G4double firstTime = middleTimes.front();
        G4double lastTime = middleTimes.back();
        
        // Decay signature: significant time gap between hits (> 50 ns)
        G4double timeDiff = lastTime - firstTime;
        if (timeDiff > 50.0 * ns) {  // Explicit unit specification for clarity
            decayTime = timeDiff / ns;  // Convert to nanoseconds for output
            decaySignature = "True";
        }
    }

    // 4. Write event data to CSV with explicit flushing
    csvFile << event->GetEventID() << ","
            << coincidenceType << ","
            << hitTop << ","
            << hitMiddle << ","
            << hitBottom << ","
            << decaySignature << ","
            << decayTime << "\n";
            
    csvFile.flush();  // Force immediate write to disk
}

void Analysis::EndOfRun(const G4Run* aRun)
{
    if (csvFile.is_open()) {
        csvFile.close(); 
    }

    G4int numEvents = aRun->GetNumberOfEvent();
    if(numEvents == 0) return;

    G4cout << "\n" << G4endl;
    G4cout << "================== RUN SUMMARY ==================" << G4endl;
    G4cout << "Run ID: " << aRun->GetRunID() << G4endl;
    G4cout << "Events processed: " << numEvents << G4endl;
    G4cout << "Average energy deposited: " 
           << G4BestUnit(thisRunTotalEnergy/numEvents,"Energy") << G4endl;
    G4cout << "Average hits per event: " 
           << (G4double)thisRunNumHits/numEvents << G4endl;
    G4cout << "=================================================" << G4endl << G4endl;
}
