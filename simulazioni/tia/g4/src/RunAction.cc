#include "RunAction.hh"
#include "EventAction.hh"
#include "Analysis.hh"
#include "G4Run.hh"

RunAction::RunAction(EventAction* theEventAction) 
  : eventAction(theEventAction)
{
}

RunAction::~RunAction()  // destructor
{
}

void RunAction::BeginOfRunAction(const G4Run* aRun)
{
    G4cout << "Starting Run: " << aRun->GetRunID() << G4endl;
    
    // Initialize Analysis for this run
    auto analysis = Analysis::GetInstance();
    analysis->PrepareNewRun(aRun);  // <-- THIS WAS MISSING!
}

void RunAction::EndOfRunAction(const G4Run* aRun)
{
    G4cout << "Ending Run: " << aRun->GetRunID() << G4endl;
    G4cout << "Number of events: " << aRun->GetNumberOfEvent() << G4endl;
    
    // Finalize Analysis for this run
    auto analysis = Analysis::GetInstance();
    analysis->EndOfRun(aRun);  // <-- THIS WAS MISSING!
}
