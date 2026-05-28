
#include "RunAction.hh"
#include "Analysis.hh"

RunAction::RunAction() : G4UserRunAction()
{}

RunAction::~RunAction()
{}

void RunAction::BeginOfRunAction(const G4Run* run)
{
  Analysis::GetInstance()->PrepareNewRun(run);
}

void RunAction::EndOfRunAction(const G4Run* run)
{
  Analysis::GetInstance()->EndOfRun(run);
}