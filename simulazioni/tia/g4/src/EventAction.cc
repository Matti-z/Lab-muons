#include "EventAction.hh"
#include "Analysis.hh"
#include "ScintillatorSD.hh"

#include "G4Event.hh"
#include "G4SDManager.hh"
#include "G4HCofThisEvent.hh"

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
    
    if(!HCE) return; // Guard rail against empty event collection pointers
    
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
            analysis->AddEDepScintillator(hit->edep, hit->time, hit->particleID, hit->trackID, hit->copyNo);
        }
    };

    // Parse all three layers into your analysis system
    parseCollection(id1); // Partenope (Copy 0 - Top)
    parseCollection(id2); // Giunone   (Copy 1 - Bottom)
    parseCollection(id3); // Minerva   (Copy 2 - Middle)

    // Finalize metrics calculation and write out to the CSV file
    analysis->EndOfEvent(event);
}