
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
    G4cout << ">>> BeginOfEventAction called!" << G4endl; //debugging printout
    // Automatically reset data lists for the new incoming event
    auto analysis = Analysis::GetInstance();
    analysis->PrepareNewEvent(event);
}

// void EventAction::EndOfEventAction(const G4Event* event)
// {//le prossime tre righe non ho idea di cosa siano
//     G4SDManager* sdMngr = G4SDManager::GetSDMpointer();
//     G4HCofThisEvent* HCE = event->GetHCofThisEvent();
//     if(!HCE) return;

//      // Debug: Print available collections
//     G4cout << "\n=== Available Collections ===" << G4endl;
//     for(int i = 0; i < HCE->GetNumberOfCollections(); ++i) {
//         auto coll = HCE->GetHC(i);
//         if(coll) {
//             G4cout << "Collection " << i << ": " << coll->GetName() << G4endl;
//         }
//     }
//     G4cout << "============================\n" << G4endl;

//     // Find collections by name from the SD manager
//     G4int id1 = G4SDManager::GetSDMpointer()->GetCollectionID("PandG/ScintillatorHitCollection");
//     G4int id3 = G4SDManager::GetSDMpointer()->GetCollectionID("Minerva/ScintillatorHitCollection");

//     auto analysis = Analysis::GetInstance();

//     auto hitCollection = static_cast<ScintillatorHitCollection*>(HCE->GetHC(id1));

//     if(hitCollection) {
//     G4cout << "Number of hits: " << hitCollection->entries() << G4endl;
//     }

//     // Lambda function to parse hit data out of the current event frame
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

//     // Finalize metrics calculation for this event
//     analysis->EndOfEvent(event);
// }

void EventAction::EndOfEventAction(const G4Event* event)
{
    // G4cout << "\n>>> EndOfEventAction called for event " << event->GetEventID() << G4endl;
    
    G4SDManager* sdMngr = G4SDManager::GetSDMpointer();
    G4HCofThisEvent* HCE = event->GetHCofThisEvent();
    
    if(!HCE) {
        G4cout << "ERROR: HCE is NULL!" << G4endl;
        return;
    }
    
    G4cout << "Number of hit collections: " << HCE->GetNumberOfCollections() << G4endl;

    G4int id1 = G4SDManager::GetSDMpointer()->GetCollectionID("PandG/ScintillatorHitCollection");
    G4int id3 = G4SDManager::GetSDMpointer()->GetCollectionID("Minerva/ScintillatorHitCollection");

    // G4cout << "Collection ID for PandG: " << id1 << G4endl;
    // G4cout << "Collection ID for Minerva: " << id3 << G4endl;

    auto analysis = Analysis::GetInstance();

    auto hitCollection = static_cast<ScintillatorHitCollection*>(HCE->GetHC(id1));

    if(hitCollection) {
        G4cout << "Number of hits in PandG: " << hitCollection->entries() << G4endl;
    } else {
        G4cout << "ERROR: hitCollection is NULL!" << G4endl;
    }

    // Lambda function to parse hit data
    auto parseCollection = [&](G4int hcID) {
        if(hcID < 0) {
            G4cout << "ERROR: Collection ID is invalid!" << G4endl;
            return;
        }
        auto hc = static_cast<ScintillatorHitCollection*>(HCE->GetHC(hcID));
        if(!hc) {
            G4cout << "ERROR: Hit collection pointer is NULL!" << G4endl;
            return;
        }

        G4cout << "Processing " << hc->entries() << " hits" << G4endl;
        for(size_t i=0; i<hc->entries(); ++i) {
            auto hit = (*hc)[i];
            analysis->AddEDepScintillator(hit->edep, hit->time, hit->particleID, hit->trackID, hit->copyNo);
        }
    };

    parseCollection(id1);
    parseCollection(id3);

    analysis->EndOfEvent(event);
}
