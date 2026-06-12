#include "EventAction.hh"
#include "Analysis.hh"
#include "ScintillatorSD.hh"

#include "G4Event.hh"
#include "G4SDManager.hh"
#include "G4HCofThisEvent.hh"
#include "G4RunManager.hh"
#include "G4Run.hh"
#include <iostream>

EventAction::EventAction() : G4UserEventAction()
{
}

EventAction::~EventAction()
{
}

void EventAction::BeginOfEventAction(const G4Event* event)
{   
    // Automatically reset data lists for the new incoming event
    auto analysis = Analysis::GetInstance();
    analysis->PrepareNewEvent(event);
}

void EventAction::EndOfEventAction(const G4Event* event)
{
    G4SDManager* sdMngr = G4SDManager::GetSDMpointer();
    G4HCofThisEvent* HCE = event->GetHCofThisEvent();
    
    if(!HCE) {
        G4cout << ">>> EndOfEventAction: HCE null" << G4endl;
        return;
    }

    // Dynamically retrieve the collection IDs for all 3 layers
    G4int id1 = sdMngr->GetCollectionID("Partenope/ScintillatorHitCollection");
    G4int id2 = sdMngr->GetCollectionID("Giunone/ScintillatorHitCollection");
    G4int id3 = sdMngr->GetCollectionID("Minerva/ScintillatorHitCollection");

    auto analysis = Analysis::GetInstance();

    // Lambda function to parse hit data safely
    auto parseCollection = [&](G4int hcID) {
        if(hcID < 0) return; // Invalid ID fallback
        
        auto hc = static_cast<ScintillatorHitCollection*>(HCE->GetHC(hcID));
        if(!hc) return; // Legitimate case: no hits occurred in this layer for this event

       for(size_t i = 0; i < hc->entries(); ++i) {
        auto hit = (*hc)[i];
        // 🛑 NEW REFINED FILTER:
            // Accept the primary muon (TrackID == 1) OR any muon/electron variant (PDG 11, -11, 13, -13)
            G4int absPDG = std::abs(hit->particleID);
            
            if (hit->trackID == 1 || absPDG == 13 || absPDG == 11){
            analysis->AddEDepScintillator(hit->edep, hit->time, hit->particleID, hit->trackID, hit->copyNo);
        }
    }
    };

    // Parse all three layers into your analysis system
    parseCollection(id1); // Partenope (Copy 0 - bottom)
    parseCollection(id2); // Giunone   (Copy 1 - middle)
    parseCollection(id3); // Minerva   (Copy 2 - top)

    // Finalize metrics calculation and write out to the CSV file
    analysis->EndOfEvent(event);

    // =========================================================================
    // TERMINAL PROGRESS BAR IMPLEMENTATION
    // =========================================================================
    G4int eventId = event->GetEventID();
    const G4Run* currentRun = G4RunManager::GetRunManager()->GetCurrentRun();
    
    if (currentRun) {
        G4int totalEvents = currentRun->GetNumberOfEventToBeProcessed();
        
        // Update the bar at 1% increments (or every event if run size is tiny)
        G4int printInterval = totalEvents / 100;
        if (printInterval < 1) printInterval = 1;

        if (eventId % printInterval == 0 || eventId == totalEvents - 1) {
            G4double progress = (G4double)(eventId + 1) / totalEvents;
            G4int barWidth = 40; // Total character width of the loading bar

            std::cout << "\r[";
            G4int pos = barWidth * progress;
            for (G4int i = 0; i < barWidth; ++i) {
                if (i < pos) std::cout << "=";
                else if (i == pos) std::cout << ">";
                else std::cout << " ";
            }
            std::cout << "] " << G4int(progress * 100.0) << " % (" 
                      << (eventId + 1) << "/" << totalEvents << ")" << std::flush;
        }

        // Drop a fresh line at the end of the batch to preserve standard Geant4 EndOfRun printouts
        if (eventId == totalEvents - 1) {
            std::cout << std::endl;
        }
    }
}