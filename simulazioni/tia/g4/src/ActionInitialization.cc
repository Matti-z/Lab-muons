#include "ActionInitialization.hh"
#include "PrimaryGeneratorAction.hh"
#include "EventAction.hh"
#include "RunAction.hh"

ActionInitialization::ActionInitialization() : G4VUserActionInitialization()
{}

ActionInitialization::~ActionInitialization()
{}

void ActionInitialization::BuildForMaster() const
{
  SetUserAction(new RunAction(nullptr));  // Master doesn't need EventAction
}

void ActionInitialization::Build() const
{
  auto eventAction = new EventAction();
  SetUserAction(new PrimaryGeneratorAction());
  SetUserAction(eventAction);
  SetUserAction(new RunAction(eventAction));  // <-- PASS EventAction to RunAction
}
