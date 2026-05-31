
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
{//le prossime tre righe non ho idea di cosa siano
    G4SDManager* sdMngr = G4SDManager::GetSDMpointer();
    G4HCofThisEvent* HCE = event->GetHCofThisEvent();
    if(!HCE) return;

    // Find collections by name from the SD manager
    G4int id1 = G4SDManager::GetSDMpointer()->GetCollectionID("PandG/ScintillatorHitCollection");
    G4int id3 = G4SDManager::GetSDMpointer()->GetCollectionID("Minerva/ScintillatorHitCollection");

    auto analysis = Analysis::GetInstance();

    auto hitCollection = static_cast<ScintillatorHitCollection*>(HCE->GetHC(id1));

    if(hitCollection) {
    G4cout << "Number of hits: " << hitCollection->entries() << G4endl;
    }

    // Lambda function to parse hit data out of the current event frame
    auto parseCollection = [&](G4int hcID) {
        if(hcID < 0) return;
        auto hc = static_cast<ScintillatorHitCollection*>(HCE->GetHC(hcID));
        if(!hc) return;

        for(size_t i=0; i<hc->entries(); ++i) {
            auto hit = (*hc)[i];
            analysis->AddEDepScintillator(hit->edep, hit->time, hit->particleID, hit->trackID, hit->copyNo);
        }
    };


    parseCollection(id1);
    parseCollection(id3);

    // Finalize metrics calculation for this event
    analysis->EndOfEvent(event);
}

